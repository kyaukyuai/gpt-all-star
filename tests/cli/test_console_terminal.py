from unittest.mock import MagicMock, patch

import pyfiglet
import pytest

from gpt_all_star.cli.console_terminal import ConsoleTerminal


@pytest.fixture
def console_terminal():
    return ConsoleTerminal()


def test_title(console_terminal):
    console_terminal.console = MagicMock()
    title = "Test Title"
    console_terminal.title(title)
    console_terminal.console.print.assert_called_once_with(
        pyfiglet.figlet_format(title), style=f"{console_terminal.main_color} bold"
    )


def test_section(console_terminal):
    console_terminal.console = MagicMock()
    console_terminal.section("Test Section")
    console_terminal.console.rule.assert_called_once_with(
        "Test Section", style=f"{console_terminal.main_color} bold"
    )


def test_print(console_terminal):
    console_terminal.console = MagicMock()
    console_terminal.print("Test Text", style="red")
    console_terminal.console.print.assert_called_once_with("Test Text", style="red")


def test_new_lines(console_terminal):
    console_terminal.console = MagicMock()
    console_terminal.new_lines(3)
    console_terminal.console.print.assert_called_once_with("\n\n")


def test_choice(console_terminal):
    console_terminal.console = MagicMock()
    console_terminal.prompt = MagicMock()
    console_terminal.prompt.ask.return_value = "2"
    choices = ["Option 1", "Option 2", "Option 3"]
    selected_choice = console_terminal.choice("Select an option", choices, default=1)
    assert selected_choice == "Option 2"


@patch("gpt_all_star.cli.console_terminal.prompt")
def test_input_single_line(mock_prompt, console_terminal):
    mock_prompt.return_value = "Single line input"
    user_input = console_terminal.input()
    assert user_input == "Single line input"


@patch("gpt_all_star.cli.console_terminal.prompt")
def test_input_multiline(mock_prompt, console_terminal):
    mock_prompt.side_effect = ["{", "Line 1", "Line 2", "}"]
    user_input = console_terminal.input()
    assert user_input == "Line 1\nLine 2\n"


@patch("gpt_all_star.cli.console_terminal.prompt")
def test_input_eof(mock_prompt, console_terminal):
    mock_prompt.side_effect = EOFError
    user_input = console_terminal.input()
    assert user_input is None
