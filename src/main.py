import sys
from dotenv import load_dotenv

from core.Project import Project
from cli.arguments import get_arguments
from logger.logger import logger


def init() -> dict:
    load_dotenv()

    arguments = get_arguments()

    logger.info(f"Starting with args: {arguments}")

    return arguments


if __name__ == "__main__":
    args = init()

    project = Project(args)
    project.start()
    sys.exit()
