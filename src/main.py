import sys
from pprint import pprint
from dotenv import load_dotenv

from helpers.Project import Project
from utils.arguments import get_arguments
from logger.logger import logger


def init() -> dict:
    load_dotenv()

    arguments = get_arguments()

    logger.info(f"Starting with args: {arguments}")
    pprint(f"Starting with args: {arguments}")

    return arguments


if __name__ == "__main__":
    args = init()

    project = Project(args)
    project.start()
    sys.exit()
