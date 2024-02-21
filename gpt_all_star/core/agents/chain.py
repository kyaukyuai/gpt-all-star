from __future__ import annotations

import os

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from gpt_all_star.core.agents.agent import Agent, _create_llm


def create_assign_supervisor_chain(members: list[Agent] = []):
    members = [member.name for member in members]
    system_prompt = f"""You are a supervisor tasked with managing a conversation between the following workers: {str(members)}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
"""
    function_def = {
        "name": "assign",
        "description": "Assign the task.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "assign": {
                    "title": "Assign",
                    "anyOf": [
                        {"enum": members},
                    ],
                }
            },
            "required": ["assign"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Select one of: {members}",
            ),
        ]
    ).partial(members=str(members))

    return (
        prompt
        | _create_llm(os.getenv("OPENAI_API_MODEL_NAME"), 0.1).bind_functions(
            functions=[function_def], function_call="assign"
        )
        | JsonOutputFunctionsParser()
    )
