import json
import re
from typing import Any


class TextParser:
    @staticmethod
    def cut_last_n_lines(text: str, n: int) -> str:
        lines = text.split("\n")
        return "\n".join(lines[:-n])

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
