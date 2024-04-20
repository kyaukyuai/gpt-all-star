import warnings

import typer
from dotenv import load_dotenv

from gpt_all_star.cli.console_terminal import MAIN_COLOR, ConsoleTerminal
from gpt_all_star.core.project import Project
from gpt_all_star.core.steps.steps import StepType

COMMAND_NAME = "GPT ALL STAR"
app = typer.Typer()


warnings.filterwarnings("ignore")


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
    review_mode: bool = typer.Option(
        False,
        "--review_mode",
        "-r",
        help="Review mode",
    ),
    debug_mode: bool = typer.Option(
        False,
        "--debug_mode",
        "-d",
        help="Debug mode",
    ),
    plan_and_solve: bool = typer.Option(
        False,
        "--plan_and_solve",
        help="Plan-and-Solve Prompting",
    ),
) -> None:
    load_dotenv()
    console = ConsoleTerminal()
    console.title(COMMAND_NAME)

    project = Project(
        step, project_name, japanese_mode, review_mode, debug_mode, plan_and_solve
    )
    project.start()
    project.finish()

    console.print(
        f"Thank you for using {COMMAND_NAME}! See you next time! :bye:",
        style=f"{MAIN_COLOR} bold",
    )


if __name__ == "__main__":
    main()
