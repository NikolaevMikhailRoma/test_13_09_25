import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from src.llm_client import send_message_to_llm
import config


bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Handle /start command."""
    await message.answer("Привет! Я бот EORA. Задавайте вопросы!")


@dp.message()
async def message_handler(message: types.Message):
    """Handle all text messages."""
    user_message = message.text
    
    # Send typing action
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Get response from LLM
    response = send_message_to_llm(user_message)
    
    if response:
        await message.answer(response)
    else:
        await message.answer("Извините, произошла ошибка при обработке запроса.")


async def run_bot():
    """Run the Telegram bot."""
    print("Starting Telegram bot...")
    await dp.start_polling(bot)