import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand, Message
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Ініціалізуємо бота та диспетчер
bot_glob = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обробник для команди /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привіт! Я SpeculatorBot. Напиши щось, і я повторю!")

# Обробник для кнопки hello
@dp.message(Command(commands=["hello"]))
async def say_hello(message: Message):
    await message.answer("Hello = текст для команди Hello.")

# Обробник для кнопки ololo
@dp.message(Command(commands=["ololo"]))
async def say_ololo(message: Message):
    await message.answer("ololo = текст для команди ololo")

# Обробник для будь-якого тексту
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"{message.text}", parse_mode="Markdown")

# Функція для налаштування команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/hello", description="Привітання"),
        BotCommand(command="/ololo", description="Сказати ololo"),
    ]
    await bot.set_my_commands(commands)

async def main():
    # Налаштування команд бота
    await set_commands(bot_glob)
    # Запуск бота
    await dp.start_polling(bot_glob)

if __name__ == "__main__":
    asyncio.run(main())
