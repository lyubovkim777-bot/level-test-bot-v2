"""
Конфигурация бота. Все значения берутся из переменных окружения
(на Render задаются в разделе Environment, локально — из файла .env).
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Токен бота, выданный @BotFather.
# ВАЖНО: это должен быть токен ЭТОГО бота (второго, нового), а не токен
# старого бота "Test_by_Englishizer_bot" — при копировании из BotFather
# внимательно проверяйте, какой именно бот открыт (см. README).
BOT_TOKEN = os.environ["BOT_TOKEN"]

# URL веб-приложения Google Apps Script, привязанного к таблице
# (см. apps_script.gs и README.md — Cloud Console и сервисный аккаунт не нужны)
GOOGLE_SCRIPT_URL = os.environ.get("GOOGLE_SCRIPT_URL", "")

# Ссылка или контакт для кнопки "Записаться на пробное занятие"
# Может быть ссылкой на форму записи, Calendly, WhatsApp и т.п.
BOOKING_URL = os.environ.get("BOOKING_URL", "https://t.me/your_manager")

# ID чата/группы, куда бот дублирует уведомления о новых заявках (необязательно)
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")

# --- Настройки хостинга (вебхук для Render) ---
# Если WEBHOOK_URL не задан — бот работает через polling (для локального теста)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # напр. https://your-app.onrender.com
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 8080))
