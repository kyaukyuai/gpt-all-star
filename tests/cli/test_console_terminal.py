from unittest.mock import MagicMock, patch

import pyfiglet
import pytest

from gpt_all_star.cli.console_terminal import ConsoleTerminal


@pytest.fixture
def console_terminal():
    return ConsoleTerminal()


def test_title(console_terminal):
    """
    Test the title method of ConsoleTerminal.
    Verifies that it prints the title using pyfiglet and the correct style.
    """
    console_terminal.console = MagicMock()
    title = "Test Title"
    console_terminal.title(title)
    console_terminal.console.print.assert_called_once_with(
        pyfiglet.figlet_format(title), style=f"{console_terminal.main_color} bold"
    )


def test_section(console_terminal):
    """
    Test the section method of ConsoleTerminal.
    Checks that it prints a section title with the correct style.
    """
    console_terminal.console = MagicMock()
    console_terminal.section("Test Section")
    console_terminal.console.rule.assert_called_once_with(
        "Test Section", style=f"{console_terminal.main_color} bold"
    )


def test_print(console_terminal):
    """
    Test the print method of ConsoleTerminal.
    Verifies that it prints the provided text with the specified style.
    """
    console_terminal.console = MagicMock()
    console_terminal.print("Test Text", style="red")
    console_terminal.console.print.assert_called_once_with("Test Text", style="red")


def test_new_lines(console_terminal):
    """
    Test the new_lines method of ConsoleTerminal.
    Checks that it prints the correct number of newline characters.
    """
    console_terminal.console = MagicMock()
    console_terminal.new_lines(3)
    console_terminal.console.print.assert_called_once_with("\n\n")


def test_choice(console_terminal, monkeypatch):
    """
    Test the choice method of ConsoleTerminal.
    Verifies that it displays the question and choices correctly,
    and returns the selected choice based on user input.
    The monkeypatch fixture is used to simulate user input.
    """
    console_terminal.console = MagicMock()
    monkeypatch.setattr('builtins.input', lambda _: "2")
    choices = ["Option 1", "Option 2", "Option 3"]
    selected_choice = console_terminal.choice("Select an option", choices, default=1)
    assert selected_choice == "Option 2"


def test_input_single_line(console_terminal, monkeypatch):
    """
    Test the input method of ConsoleTerminal for single line input.
    Checks that it prompts for input and returns the user's input.
    The monkeypatch fixture is used to simulate user input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "Single line input")
    user_input = console_terminal.input()
    assert user_input == "Single line input"


def test_input_multiline(console_terminal, monkeypatch):
    """
    Test the input method of ConsoleTerminal for multiline input.
    Verifies that it correctly handles input enclosed in curly braces,
    and returns the multiline input.
    The monkeypatch fixture is used to simulate user input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "{")
    monkeypatch.setattr('builtins.input', lambda _: "Line 1", raising=False)
    monkeypatch.setattr('builtins.input', lambda _: "Line 2", raising=False)
    monkeypatch.setattr('builtins.input', lambda _: "}", raising=False)
    user_input = console_terminal.input()
    assert user_input == "Line 1\nLine 2\n"


def test_input_eof(console_terminal, monkeypatch):
    """
    Test the input method of ConsoleTerminal when EOF is encountered.
    Checks that it returns None when EOFError is raised.
    The monkeypatch fixture is used to simulate the EOFError.
    """
    monkeypatch.setattr('builtins.input', lambda _: (_ for _ in ()).throw(EOFError))
    user_input = console_terminal.input()
    assert user_input is None
