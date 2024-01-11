import warnings
from dotenv import load_dotenv
import typer
from your_dev_team.cli.ConsoleTerminal import ConsoleTerminal

from your_dev_team.core.Project import Project
from your_dev_team.cli.arguments import get_arguments
from your_dev_team.logger.logger import logger


app = typer.Typer()
warnings.simplefilter("ignore")


def hello_world() -> None:
    ConsoleTerminal().panel("your-dev-team")


def init() -> dict:
    load_dotenv()

    arguments = get_arguments()

    logger.info(f"Starting with args: {arguments}")

    return arguments


@app.command()
def main() -> None:
    hello_world()
    args = init()

    project = Project(args)
    project.start()
    project.finish()


if __name__ == "__main__":
    main()
