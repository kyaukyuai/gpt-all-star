from prompt_toolkit.history import FileHistory

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.styles import Style
from rich.console import Console

from logger.logger import logger


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


def get_input(history_file, file_names=None):
    if file_names is None:
        file_names = set()

    user_input = ""
    multiline_input = False

    style = Style.from_dict({"": "green"})
    completer_instance = FileContentCompleter(file_names)

    while True:
        if multiline_input:
            show = ". "
        else:
            show = "> "

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


def ask_user(question: str, require_some_input=True):
    console = Console()

    while True:
        console.print(question, style="yellow bold")
        answer = get_input('project.history').strip()
        console.print()

        logger.info('Question: %s', question)
        logger.info('Answer: %s', answer)

        if not answer:
            if require_some_input:
                print("No input provided! Please try again.")
            else:
                print("Exiting application.")
                exit(0)
        else:
            return answer
