import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand, Message

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Змінні середовища вже присутні в контейнері!
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")

# Ініціалізуємо бота та диспетчер
bot_glob = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обробник для команди /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привіт! Я SpeculatorBot. Напиши щось, і я повторю!")
    logger.info(f"Виконано команду /start від користувача {message.from_user.id}")

# Обробник для команди /hello
@dp.message(Command(commands=["hello"]))
async def say_hello(message: Message):
    await message.answer("Hello = текст для команди Hello.")
    logger.info(f"Виконано команду /hello від користувача {message.from_user.id}")

# Обробник для команди /ololo
@dp.message(Command(commands=["ololo"]))
async def say_ololo(message: Message):
    await message.answer("ololo = текст для команди ololo")
    logger.info(f"Виконано команду /ololo від користувача {message.from_user.id}")

# Обробник для будь-якого тексту
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"{message.text}", parse_mode="Markdown")
    logger.info(f"Відповідь на повідомлення від {message.from_user.id}: {message.text}")

# Функція для налаштування команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/hello", description="Привітання"),
        BotCommand(command="/ololo", description="Сказати ololo"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Команди бота налаштовано")

async def main():
    # Налаштування команд бота
    await set_commands(bot_glob)
    logger.info("Запуск бота")
    # Запуск бота
    await dp.start_polling(bot_glob)

if __name__ == "__main__":
    asyncio.run(main())
