import warnings
from dotenv import load_dotenv
import typer

from gpt_all_star.cli.console_terminal import MAIN_COLOR, ConsoleTerminal
from gpt_all_star.core.project import Project
from gpt_all_star.core.steps.steps import StepType


app = typer.Typer()
warnings.simplefilter("ignore")


@app.command()
def main(
    step: StepType = typer.Option(
        StepType.DEFAULT,
        "--step",
        "-s",
        help="Step to be performed",
        case_sensitive=False,
        show_choices=True,
    ),
    project_name: str = typer.Option(
        None,
        "--project_name",
        "-p",
        help="Project name",
        case_sensitive=True,
        show_choices=True,
    ),
    japanese_mode: bool = typer.Option(
        False,
        "--japanese_mode",
        "-j",
        help="Japanese mode",
    ),
    auto_mode: bool = typer.Option(
        False,
        "--auto_mode",
        "-a",
        help="Auto mode",
    ),
) -> None:
    load_dotenv()
    console = ConsoleTerminal()
    console.title("gpt-all-star")

    project = Project(step, project_name, japanese_mode, auto_mode)
    project.start()
    project.finish()

    console.print(
        "Thank you for using gpt-all-star! See you next time!:bye:",
        style=f"{MAIN_COLOR} bold",
    )


if __name__ == "__main__":
    main()
