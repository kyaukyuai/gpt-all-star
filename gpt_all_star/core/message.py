from __future__ import annotations
import json

import re
from typing import Any
import warnings

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

warnings.simplefilter("ignore")


class Message:
    @staticmethod
    def create_system_message(message: str) -> SystemMessage:
        return SystemMessage(content=message)

    @staticmethod
    def create_human_message(message: str) -> HumanMessage:
        return HumanMessage(content=message)

    @staticmethod
    def create_ai_message(message: str) -> AIMessage:
        return AIMessage(content=message)

    @staticmethod
    def parse_message(message: str) -> list[tuple[str, str]]:
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, message, re.DOTALL)

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
    def parse_to_json(message: str) -> dict[str, Any]:
        try:
            return json.loads(message)
        except:
            matches = re.finditer(r"```\S*\n(.+?)\n```", message, re.DOTALL)
            json_str = "\n".join(match.group(1) for match in matches)
            return json.loads(json_str)
