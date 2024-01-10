from typing import Optional, Union

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.style import Style as RichStyle

from your_dev_team.logger.logger import logger


class ConsoleTerminal:
    def __init__(self):
        self._console = Console()

    def section(self, title: str) -> None:
        self._console.rule(title, style="#63CD91 bold")

    def new_lines(self, count: int = 1) -> None:
        self._console.print("\n" * (count - 1))

    def print(self, text: str, style: Optional[Union[str, RichStyle]] = None) -> None:
        self._console.print(text, style=style)

    def panel(self, title: str) -> None:
        ascii_art = pyfiglet.figlet_format(title)
        self._console.print(ascii_art, style="#63CD91 bold")
        self.new_lines(1)

    def next(self, text: str) -> None:
        self.print(text, style="#FFFFFF bold")
        self.new_lines(1)

    def input(self, history_file, file_names=None):
        if file_names is None:
            file_names = set()

        user_input = ""
        multiline_input = False

        style = Style.from_dict({"": "#FF910A"})
        completer_instance = FileContentCompleter(file_names)

        while True:
            if multiline_input:
                show = ". "
            else:
                show = "you: "

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

    def ask_user(
        self, question: str, questioner: str | None = None, require_some_input=True
    ):
        while True:
            self.print(
                f"[#FFFF00 bold]{questioner if questioner is not None else ''}:[/#FFFF00 bold] {question}",
                style="#FFFFFF bold",
            )
            answer = self.input("project.history").strip()
            self.new_lines(1)

            logger.info("Question: %s", question)
            logger.info("Answer: %s", answer)

            if not answer:
                if require_some_input:
                    print("No input provided! Please try again.")
                else:
                    print("Exiting application.")
                    exit(0)
            else:
                return answer


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
