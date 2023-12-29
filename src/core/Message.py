from __future__ import annotations

import json
import re

from langchain_core.messages import (BaseMessage, AIMessage, HumanMessage, SystemMessage, messages_to_dict,
                                     messages_from_dict)


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
    def serialize_messages(messages: list[BaseMessage]) -> str:
        return json.dumps(messages_to_dict(messages))

    @staticmethod
    def deserialize_messages(json_dict_str: str) -> list[BaseMessage]:
        data = json.loads(json_dict_str)
        pre_validated_data = [{
            **item, "data": {
                **item["data"], "is_chunk": False
            }
        } for item in data]
        return list(messages_from_dict(pre_validated_data))

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
