import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Ініціалізуємо бота та диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Створення клавіатури
keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="hello")],
    [KeyboardButton(text="ololo")]
], resize_keyboard=True)

# Обробник для команди /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привіт! Я SpeculatorBot. Ось моє меню:", reply_markup=keyboard)

# Обробник для кнопки hello
@dp.message(lambda message: message.text == "hello")
async def say_hello(message: Message):
    await message.answer("Привітання! Як справи?")

# Обробник для кнопки ololo
@dp.message(lambda message: message.text == "ololo")
async def say_ololo(message: Message):
    await message.answer("ololo")

# Обробник для будь-якого тексту
@dp.message()
async def echo_message(message: Message):
    # message уже містить у собі форматований текст, тепер його треба правильно надрукувати.
    await message.answer(f"{message.text}", parse_mode="Markdown")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
