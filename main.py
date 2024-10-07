import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Ініціалізуємо бота та диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обробник для команди /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привіт! Я SpeculatorBot. Як я можу допомогти?")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
