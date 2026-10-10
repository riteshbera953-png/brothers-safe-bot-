"""
BROTHERS SAFE TELEGRAM BOT
Admin / Super Admin and Force Join configuration only.
This file intentionally does not include SMS-sending or bombing functionality.

Install:
    pip install aiogram

Before running:
1. Revoke the token previously shared in chat using @BotFather.
2. Paste the NEW token into BOT_TOKEN below.
3. Replace the two FORCE_JOIN_LINKS values with the real invite/public links.
4. Make the bot an administrator in both channels so membership checks work.

Run:
    python safe_bot.py
"""

import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

# Hard-coded admin configuration
ADMIN_CHAT_ID = 5999496406
SUPER_ADMIN_ID = 5999496406

# IMPORTANT: use a newly generated token; do not reuse the token exposed in chat.
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

FORCE_JOIN_ENABLED = True
FORCE_JOIN_CHANNEL_IDS = [
    -1004309254414,
    -1004466128264,
]

# Replace these with each channel's actual public URL or invite link.
FORCE_JOIN_LINKS = [
    "https://t.me/PANELEMPIRE2",
    "https://t.me/brotherpanell",
]

dp = Dispatcher()


def force_join_keyboard():
    rows = []
    for index, link in enumerate(FORCE_JOIN_LINKS, start=1):
        if link.startswith("https://") and "PASTE_" not in link:
            rows.append([
                InlineKeyboardButton(text=f"Join Channel {index}", url=link)
            ])
    rows.append([
        InlineKeyboardButton(text="I Joined — Check Again", callback_data="check_join")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def missing_channels(bot: Bot, user_id: int):
    missing = []
    for channel_id in FORCE_JOIN_CHANNEL_IDS:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status not in ("member", "administrator", "creator"):
                missing.append(channel_id)
        except TelegramBadRequest:
            # Common causes: bot is not an admin in the channel, or channel ID is wrong.
            missing.append(channel_id)
    return missing


async def show_home(message: Message, bot: Bot):
    user_id = message.from_user.id
    if FORCE_JOIN_ENABLED:
        missing = await missing_channels(bot, user_id)
        if missing:
            await message.answer(
                "Please join both required channels, then tap “I Joined — Check Again”.",
                reply_markup=force_join_keyboard(),
            )
            return

    if user_id == SUPER_ADMIN_ID:
        await message.answer(
            f"Welcome, Super Admin.\nAdmin ID: {ADMIN_CHAT_ID}\n"
            f"Super Admin ID: {SUPER_ADMIN_ID}\nForce Join: {'ON' if FORCE_JOIN_ENABLED else 'OFF'}"
        )
    else:
        await message.answer("Welcome! Channel membership verified.")


@dp.message(CommandStart())
async def start(message: Message, bot: Bot):
    await show_home(message, bot)


@dp.callback_query(lambda query: query.data == "check_join")
async def check_join(callback, bot: Bot):
    if FORCE_JOIN_ENABLED:
        missing = await missing_channels(bot, callback.from_user.id)
        if missing:
            await callback.answer("You still need to join both channels.", show_alert=True)
            return

    await callback.answer("Membership verified!")
    if callback.message:
        if callback.from_user.id == SUPER_ADMIN_ID:
            await callback.message.answer(
                f"Welcome, Super Admin.\nAdmin ID: {ADMIN_CHAT_ID}\n"
                f"Super Admin ID: {SUPER_ADMIN_ID}\nForce Join: ON"
            )
        else:
            await callback.message.answer("Welcome! Channel membership verified.")


async def main():
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_NEW_BOT_TOKEN_HERE":
        raise RuntimeError("BOT_TOKEN is missing. Set it in Render Environment Variables.")
    bot = Bot(token=BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
