"""
Donat shop bot: /start menyusi (banner + 3 ta tugma + Mini App tugmasi)

O'rnatish:   pip install aiogram
Ishga tushirish:
    export BOT_TOKEN="123456:ABC..."
    python bot.py
"""
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

# ====== SOZLAMALAR (o'zingiznikiga almashtiring) ======
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = "Osonnpay"                        # botingiz nomi (@Osonnpay_bot)
WEBAPP_URL = "https://your-domain.uz"        # Mini App manzili (faqat https!)
SUPPORT_URL = "https://t.me/your_support"    # qo'llab-quvvatlash
CHANNEL_URL = "https://t.me/your_channel"    # yangiliklar kanali
BANNER_PATH = "banner.jpg"                   # o'zingizning banner rasmingiz
# ======================================================

WELCOME_TEXT = (
    "Assalomu alaykum! 👋\n"
    f"{BOT_NAME} botiga xush kelibsiz 🎮\n\n"
    "Sevimli o'yinlaringiz va Telegram xizmatlariga tez, xavfsiz va "
    "ishonchli tarzda donat qiling!\n\n"
    "Davom etish uchun quyidagi menyudan foydalaning 👇"
)

dp = Dispatcher()


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # web_app tugmasi: Mini App'ni chat ichida ochadi
            [
                InlineKeyboardButton(
                    text="🛒 Xarid qilish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            # url tugmalari: havola ochadi (↗ belgisi bilan ko'rinadi)
            [
                InlineKeyboardButton(text="💬 Qo'llab-quvvatlash", url=SUPPORT_URL),
                InlineKeyboardButton(text="📢 Yangiliklar kanali", url=CHANNEL_URL),
            ],
        ]
    )


@dp.message(CommandStart())
async def start(message: Message):
    if os.path.exists(BANNER_PATH):
        await message.answer_photo(
            FSInputFile(BANNER_PATH),
            caption=WELCOME_TEXT,
            reply_markup=main_keyboard(),
        )
    else:  # banner bo'lmasa ham ishlayveradi
        await message.answer(WELCOME_TEXT, reply_markup=main_keyboard())


async def main():
    bot = Bot(BOT_TOKEN)
    # Xabar yozish maydonining chap tomonidagi "Mini App" tugmasi
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Mini App",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
