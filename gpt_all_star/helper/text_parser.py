import json
import re
from typing import Any


class TextParser:
    @staticmethod
    def cut_last_n_lines(text: str, n: int) -> str:
        lines = text.split("\n")
        return "\n".join(lines[:-n])

    @staticmethod
    def parse_code_from_text(text: str) -> list[tuple[str, str]]:
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, text, re.DOTALL)

        files = []
        for match in matches:
            # Strip the filename of any non-allowed characters and convert / to \
            path = re.sub(r'[:<>"|?*]', "", match.group(1))

            # Remove leading and trailing brackets
            path = re.sub(r"^\[(.*)]$", r"\1", path)

            # Remove leading and trailing backticks
            path = re.sub(r"^`(.*)`$", r"\1", path)

            # Remove trailing ]
            path = re.sub(r"[]:]$", "", path)

            # Get the code
            specification = match.group(2)

            # Add the file to the list
            files.append((path, specification))

        return files

    @staticmethod
    def to_json(text: str) -> dict[str, Any]:
        try:
            return json.loads(text)
        except BaseException:
            matches = re.finditer(r"```\S*\n(.+?)\n```", text, re.DOTALL)
            json_str = "\n".join(match.group(1) for match in matches)
            return json.loads(json_str)


def format_file_to_input(file_name: str, file_content: str) -> str:
    file_str = f"""
    {file_name}
    ```
    {file_content}
    ```
    """
    return file_str
