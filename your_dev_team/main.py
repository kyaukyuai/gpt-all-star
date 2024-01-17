import warnings
from dotenv import load_dotenv
import typer

from your_dev_team.cli.console_terminal import ConsoleTerminal
from your_dev_team.core.project import Project
from your_dev_team.core.steps.steps import StepType


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
) -> None:
    load_dotenv()
    console = ConsoleTerminal()
    console.panel("your-dev-team")

    project = Project(step, project_name, japanese_mode)
    project.start()
    project.finish()

    console.print(
        "Thank you for using your-dev-team! See you next time!", style="#44EE77 bold"
    )


if __name__ == "__main__":
    main()
