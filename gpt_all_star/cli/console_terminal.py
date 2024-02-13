from dataclasses import dataclass
from typing import Optional, Union

import pyfiglet
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style as RichStyle
from rich.text import Text

MAIN_COLOR = "#392AE2"
SUB_COLOR = "#262626"


@dataclass
class ConsoleTerminal:
    console: Console = Console()
    prompt: Prompt = Prompt()
    main_color: str = MAIN_COLOR
    sub_color: str = SUB_COLOR

    def title(self, title: str) -> None:
        self.console.print(
            pyfiglet.figlet_format(title), style=f"{self.main_color} bold"
        )

    def section(self, title: str) -> None:
        self.console.rule(title, style=f"{self.main_color} bold")

    def print(self, text: str, style: Optional[Union[str, RichStyle]] = None) -> None:
        self.console.print(text, style=style)

    def new_lines(self, count: int = 1) -> None:
        self.console.print("\n" * (count - 1))

    def choice(
        self,
        question: str,
        choices: list[str],
        default: int,
        style: Optional[Union[str, RichStyle]] = None,
    ) -> str:
        text = Text(f"{question}:\n", style=style)
        for i, option in enumerate(choices, 1):
            separator = "" if i == len(choices) else "\n"
            text.append(f"  {i}. {option}{separator}", style=style)

        self.console.print(text)

        choice = self.prompt.ask(
            f"[bold {self.main_color}]You[/bold {self.main_color}]: ",
            choices=[str(x) for x in range(1, len(choices) + 1)],
            default=str(int(default)),
        )
        return choices[int(choice) - 1]

    def input(self, file_names=None):
        if file_names is None:
            file_names = set()

        user_input = ""
        multiline_input = False

        style = Style.from_dict({"": f"{self.main_color}"})

        while True:
            if multiline_input:
                show = ". "
            else:
                show = "You: "

            try:
                line = prompt(
                    show,
                    completer=None,
                    history=None,
                    style=style,
                )
            except EOFError:
                return
            if line.strip() == "{" and not multiline_input:
                multiline_input = True
                continue
            elif line.strip() == "}" and multiline_input:
                break
            elif multiline_input:
                user_input += line + "\n"
            else:
                user_input = line
                break

        return user_input
