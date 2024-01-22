from typing import Optional, Union

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
import pyfiglet
from rich.console import Console
from rich.style import Style as RichStyle
from rich.text import Text

MAIN_COLOR = "#44EE77"
SUB_COLOR = "#FB475E"


class ConsoleTerminal:
    def __init__(self):
        self._console = Console()

    def title(self, title: str) -> None:
        ascii_art = pyfiglet.figlet_format(title)
        self._console.print(ascii_art, style=f"{MAIN_COLOR} bold")
        self.new_lines(1)

    def section(self, title: str) -> None:
        self._console.rule(title, style=f"{MAIN_COLOR} bold")

    def new_lines(self, count: int = 1) -> None:
        self._console.print("\n" * (count - 1))

    def print(self, text: str, style: Optional[Union[str, RichStyle]] = None) -> None:
        self._console.print(text, style=style)

    def _choice(
        self,
        question: str,
        choices: list[str],
        default: int,
        style: Union[str, RichStyle] | None = None,
    ) -> str:
        text = Text(f"{question}:\n", style=style)
        for i, option in enumerate(choices, 1):
            separator = "" if i == len(choices) else "\n"
            text.append(f"  {i}. {option}{separator}", style=style)
        self._console.print(text)

        choice = self._input("project.history").strip() or default
        return choices[int(choice) - 1]

    def _input(self, history_file, file_names=None):
        if file_names is None:
            file_names = set()

        user_input = ""
        multiline_input = False

        style = Style.from_dict({"": f"{SUB_COLOR}"})
        completer_instance = FileContentCompleter(file_names)

        while True:
            if multiline_input:
                show = ". "
            else:
                show = "You: "

            try:
                line = prompt(
                    show,
                    completer=completer_instance,
                    history=FileHistory(history_file),
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


class FileContentCompleter(Completer):
    def __init__(self, fine_names):
        self.words = []
        for file_name in fine_names:
            with open(file_name, "r") as f:
                content = f.read()
            self.words.extend(content.split())

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words:
            return

        last_word = words[-1]
        for word in self.words:
            if word.startswith(last_word):
                yield Completion(word, start_position=-len(last_word))
