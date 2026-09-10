"""
Telegram-бот: тест на определение уровня английского языка (v2, с опцией "Я не знаю").

Сценарий:
1. /start -> приветствие, кнопка "Начать тест".
2. Бот последовательно задаёт 50 вопросов (грамматика + лексика),
   ученик отвечает кнопками a/b/c/d ИЛИ нажимает "🤷 Я не знаю",
   если не уверен — так ученик не гадает наугад.
3. По завершении бот сразу показывает уровень (Beginner..Advanced)
   и сколько раз ученик честно признался, что не знает ответ.
4. Бот запрашивает имя и телефон ученика.
5. Заявка (имя, телефон, уровень, кол-во "не знаю") сохраняется в Google Таблицу.
6. Ученику показывается кнопка "Записаться на пробное занятие".

ВАЖНО (см. README.md, раздел "Частые ошибки"):
- Никогда не запускайте этот файл локально (`python bot.py`) с тем же
  BOT_TOKEN, что используется в проде на Render. Режим polling ниже
  удаляет вебхук при старте (bot.delete_webhook) — это оборвёт продовую
  версию бота для всех учеников. Для локальных тестов заведите отдельного
  тестового бота через BotFather.

Запуск локально:  python bot.py   (работает через polling, см. предупреждение выше)
Запуск на Render: см. README.md — используется вебхук.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import config
import sheets
from questions import QUESTIONS, get_level

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

TOTAL_QUESTIONS = len(QUESTIONS)
IDK = "idk"  # значение letter для кнопки "Я не знаю"


class TestStates(StatesGroup):
    answering = State()
    waiting_name = State()
    waiting_phone = State()


def question_keyboard(idx: int) -> InlineKeyboardMarkup:
    q = QUESTIONS[idx]
    buttons = [
        [InlineKeyboardButton(text=f"{letter.upper()}) {text}", callback_data=f"ans:{idx}:{letter}")]
        for letter, text in q["options"].items()
    ]
    buttons.append(
        [InlineKeyboardButton(text="🤷 Я не знаю", callback_data=f"ans:{idx}:{IDK}")]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def question_text(idx: int) -> str:
    q = QUESTIONS[idx]
    return f"Вопрос {idx + 1} из {TOTAL_QUESTIONS}\n\n{q['question']}"


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def booking_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Записаться на пробное занятие", url=config.BOOKING_URL)]
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(score=0, idk_count=0)
    text = (
        "Привет! 👋\n\n"
        f"Это короткий тест на определение уровня английского ({TOTAL_QUESTIONS} вопросов, "
        "~15-30 минут). Если не уверены в ответе — не гадайте, а нажимайте «🤷 Я не знаю»: "
        "так тест точнее покажет ваш реальный уровень.\n\n"
        "В конце вы сразу узнаете свой уровень и сможете записаться "
        "на пробное занятие.\n\n"
        "Готовы начать?"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Начать тест ✏️", callback_data="start_test")]]
    )
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(TestStates.answering)
    await state.update_data(score=0, idk_count=0, current_idx=0)
    await callback.message.edit_text(question_text(0), reply_markup=question_keyboard(0))
    await callback.answer()


@router.callback_query(TestStates.answering, F.data.startswith("ans:"))
async def handle_answer(callback: CallbackQuery, state: FSMContext) -> None:
    _, idx_str, letter = callback.data.split(":")
    idx = int(idx_str)

    data = await state.get_data()
    # защита от повторного нажатия на уже отвеченный вопрос
    if data.get("current_idx", 0) != idx:
        await callback.answer()
        return

    score = data.get("score", 0)
    idk_count = data.get("idk_count", 0)

    if letter == IDK:
        idk_count += 1
    elif QUESTIONS[idx]["answer"] == letter:
        score += 1

    next_idx = idx + 1
    if next_idx < TOTAL_QUESTIONS:
        await state.update_data(score=score, idk_count=idk_count, current_idx=next_idx)
        await callback.message.edit_text(question_text(next_idx), reply_markup=question_keyboard(next_idx))
        await callback.answer()
        return

    # тест завершён
    en_level, ru_level = get_level(score)
    await state.update_data(score=score, idk_count=idk_count, current_idx=next_idx)
    await state.set_state(TestStates.waiting_name)

    idk_line = (
        f"Отметили «не знаю» на {idk_count} из {TOTAL_QUESTIONS} вопросов — "
        "это тоже честная и полезная информация.\n\n"
        if idk_count
        else ""
    )
    result_text = (
        "🎉 Тест завершён!\n\n"
        f"Ваш результат: {score} из {TOTAL_QUESTIONS}\n"
        f"Ваш уровень: {ru_level} ({en_level})\n\n"
        f"{idk_line}"
        "Чтобы записаться на пробное занятие, напишите, пожалуйста, "
        "ваше имя."
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(result_text)
    await callback.answer()


@router.message(TestStates.waiting_name)
async def handle_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name:
        await message.answer("Пожалуйста, введите имя текстом.")
        return

    await state.update_data(name=name)
    await state.set_state(TestStates.waiting_phone)
    await message.answer(
        f"Приятно познакомиться, {name}! Теперь отправьте, пожалуйста, номер телефона "
        "— нажмите кнопку ниже или введите его вручную.",
        reply_markup=phone_keyboard(),
    )


@router.message(TestStates.waiting_phone, F.contact)
async def handle_phone_contact(message: Message, state: FSMContext) -> None:
    await finish_registration(message, state, message.contact.phone_number)


@router.message(TestStates.waiting_phone, F.text)
async def handle_phone_text(message: Message, state: FSMContext) -> None:
    phone = (message.text or "").strip()
    if len(phone) < 5:
        await message.answer("Похоже, это не номер телефона. Попробуйте ещё раз.")
        return
    await finish_registration(message, state, phone)


async def finish_registration(message: Message, state: FSMContext, phone: str) -> None:
    data = await state.get_data()
    name = data.get("name", "")
    score = data.get("score", 0)
    idk_count = data.get("idk_count", 0)
    _, ru_level = get_level(score)
    username = message.from_user.username or ""

    saved = await sheets.append_lead(
        name=name, phone=phone, username=username, score=score, level_ru=ru_level, idk_count=idk_count
    )

    await message.answer(
        "Спасибо! Заявка принята ✅\n\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Уровень: {ru_level}\n\n"
        "Нажмите кнопку ниже, чтобы записаться на пробное занятие.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer("👇", reply_markup=booking_keyboard())

    if config.ADMIN_CHAT_ID:
        try:
            await message.bot.send_message(
                config.ADMIN_CHAT_ID,
                f"🆕 Новая заявка\nИмя: {name}\nТелефон: {phone}\n"
                f"Username: @{username}\nБаллы: {score}/{TOTAL_QUESTIONS}\n"
                f"«Не знаю»: {idk_count}\nУровень: {ru_level}",
            )
        except Exception:
            logger.exception("Не удалось отправить уведомление админу")

    if not saved:
        logger.warning("Google Sheets не настроен — заявка не сохранена в таблицу: %s / %s", name, phone)

    await state.clear()


async def _run_polling() -> None:
    if not config.WEBHOOK_URL:
        logger.warning(
            "⚠️  Запуск в режиме polling (локально). НЕ делайте этого с тем же BOT_TOKEN, "
            "что используется в проде на Render — это сорвёт вебхук и продовый бот перестанет "
            "отвечать ученикам. Для локальных тестов используйте отдельного тестового бота "
            "(см. README.md, раздел 'Частые ошибки')."
        )
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def _run_webhook() -> None:
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    async def on_startup(app: web.Application) -> None:
        await bot.set_webhook(f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}", drop_pending_updates=True)

    app = web.Application()
    app.on_startup.append(on_startup)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=config.PORT)


if __name__ == "__main__":
    if config.WEBHOOK_URL:
        _run_webhook()
    else:
        asyncio.run(_run_polling())
