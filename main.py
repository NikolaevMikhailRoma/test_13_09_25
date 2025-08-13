from src.parser import create_knowledge_base
import config


def main():
    create_knowledge_base(
        urls_file=config.LINK_LIST_PATH,
        output_file=config.PARSED_DATA_PATH,
        limit=config.PARSING_LIMIT
    )


if __name__ == "__main__":
    main()