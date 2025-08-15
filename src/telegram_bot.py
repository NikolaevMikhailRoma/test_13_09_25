import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from src.llm_client import send_message_to_llm
from src.postprocess import format_text_for_telegram
import config


bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Handle /start command."""
    await message.answer("Hello! I'm EORA bot. Ask me questions!", parse_mode="HTML")


@dp.message()
async def message_handler(message: types.Message):
    """Handle all text messages."""
    # Input validation
    if not message.text or len(message.text.strip()) == 0:
        await message.answer("Please send a non-empty message.", parse_mode="HTML")
        return
    
    # Rate limiting - basic protection
    if len(message.text) > 4000:
        await message.answer("Message too long. Please limit to 4000 characters.", parse_mode="HTML")
        return
    
    user_message = message.text
    
    # Send typing action
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Get response from LLM
    response = send_message_to_llm(user_message)
    
    if response:
        # Format response for Telegram
        formatted_response = format_text_for_telegram(response)
        try:
            await message.answer(formatted_response, parse_mode="HTML")
        except Exception as e:
            # Fallback to plain text if HTML parsing fails
            await message.answer(response)
    else:
        await message.answer("Sorry, an error occurred while processing the request.", parse_mode="HTML")


async def run_bot():
    """Run the Telegram bot."""
    print("Starting Telegram bot...")
    await dp.start_polling(bot)