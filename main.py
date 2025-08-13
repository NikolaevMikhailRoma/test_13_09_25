from src.parser import create_knowledge_base
from src.postprocess import postprocess_knowledge_base
import config


def main():
    # Parse websites
    create_knowledge_base(
        urls_file=config.LINK_LIST_PATH,
        output_file=config.PARSED_DATA_PATH,
        limit=config.PARSING_LIMIT
    )
    
    # Clean up the data
    postprocess_knowledge_base(
        input_file=config.PARSED_DATA_PATH,
        output_file=config.PARSED_DATA_PATH
    )


if __name__ == "__main__":
    main()