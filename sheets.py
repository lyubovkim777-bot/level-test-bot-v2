"""
Запись заявок учеников в Google Таблицу через Google Apps Script Web App
(файл apps_script.gs — вставляется прямо в таблицу через
Extensions -> Apps Script, без Cloud Console и сервисных аккаунтов).

Если GOOGLE_SCRIPT_URL не задан — запись в таблицу просто пропускается
(например, если используются только уведомления в Telegram через ADMIN_CHAT_ID).
"""
import logging
from datetime import datetime

import aiohttp

import config

logger = logging.getLogger(__name__)


async def append_lead(
    name: str, phone: str, username: str, score: int, level_ru: str, idk_count: int = 0
) -> bool:
    """Отправляет заявку ученика в Google Таблицу. Возвращает True при успехе."""
    if not config.GOOGLE_SCRIPT_URL:
        return False

    payload = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": name,
        "phone": phone,
        "username": f"@{username}" if username else "",
        "score": score,
        "level": level_ru,
        "idk_count": idk_count,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config.GOOGLE_SCRIPT_URL, json=payload, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    logger.warning("Google Apps Script вернул статус %s", resp.status)
                    return False
                return True
    except Exception:
        logger.exception("Не удалось отправить заявку в Google Таблицу")
        return False
