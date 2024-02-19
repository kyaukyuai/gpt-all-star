import threading
import time

import typer
from dotenv import load_dotenv
from rich import box
from rich.live import Live
from rich.panel import Panel

from gpt_all_star.cli.console_terminal import MAIN_COLOR, ConsoleTerminal
from gpt_all_star.core.project import Project
from gpt_all_star.core.steps.steps import StepType

COMMAND_NAME = "GPT ALL STAR"
app = typer.Typer()


def run_project(project):
    project.start()
    project.finish()


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
) -> None:
    load_dotenv()
    console = ConsoleTerminal()
    console.title(COMMAND_NAME)

    project = Project(step, project_name, japanese_mode, review_mode, debug_mode)

    project_thread = threading.Thread(target=run_project, args=(project,))
    project_thread.start()

    start_time = time.time()
    with Live(console=console.console, refresh_per_second=10) as live:
        while project_thread.is_alive():
            elapsed_time = time.time() - start_time
            panel = Panel(
                f"[bold green]Execution Time: {elapsed_time:.2f} seconds",
                box=box.SIMPLE,
                title="",
            )
            live.update(panel)
            time.sleep(0.1)

    console.print(
        f"Thank you for using {COMMAND_NAME}! See you next time! :bye:",
        style=f"{MAIN_COLOR} bold",
    )


if __name__ == "__main__":
    main()
