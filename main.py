import asyncio
# from src.parser import create_knowledge_base
from src.parser import create_knowledge_base_async
from src.postprocess import postprocess_knowledge_base


from src.telegram_bot import run_bot
import config


async def main():
    # Parse websites and create knowledge base
    # print("Creating knowledge base...")
    # await create_knowledge_base_async(
    #     urls_file=config.LINK_LIST_PATH,
    #     output_file=config.PARSED_DATA_PATH,
    #     limit=config.PARSING_LIMIT
    # )
    
    # Clean up the data
    postprocess_knowledge_base(
        input_file=config.PARSED_DATA_PATH,
        output_file=config.PARSED_DATA_PATH
    )
    
    # Run Telegram bot
    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())