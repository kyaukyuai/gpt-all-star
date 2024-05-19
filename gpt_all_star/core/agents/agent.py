from __future__ import annotations

import os
import re
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import BaseMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.prompt import PromptTemplate
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.llm import LLM_TYPE, create_llm
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.tools.shell_tool import ShellTool
from gpt_all_star.helper.translator import create_translator
from langchain_community.agent_toolkits import FileManagementToolkit

# from gpt_all_star.core.tools.llama_index_tool import llama_index_tool


class Agent(ABC):
    def __init__(
        self,
        role: AgentRole,
        storages: Storages | None,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
        color: str | None = None,
        tools: list = [],
        language: str | None = None,
    ) -> None:
        self.console = ConsoleTerminal()
        self._llm = create_llm(LLM_TYPE[os.getenv("ENDPOINT", default="OPENAI")])

        self.role: AgentRole = role
        self.name: str = name or self._get_default_profile().name
        self.profile: str = profile or self._get_default_profile().prompt.format()
        self.color: str = color or self._get_default_profile().color

        self.messages: list[BaseMessage] = [Message.create_system_message(self.profile)]
        self.storages = storages
        self.debug_mode = debug_mode
        self.additional_tools = tools
        self.set_executor(
            working_directory=(
                self.storages.root.path.absolute() if self.storages else os.getcwd()
            )
        )

        self._set_language(language)
        self._ = create_translator(self.language)

    def _set_language(self, language: str | None) -> None:
        self.language = language if language is not None else "en"

    def set_executor(self, working_directory: str) -> None:
        file_tools = FileManagementToolkit(
            root_dir=str(working_directory),
            selected_tools=["read_file", "write_file", "list_directory", "file_delete"],
        ).get_tools()
        self.tools = (
            self.additional_tools
            + file_tools
            + [ShellTool(verbose=self.debug_mode, root_dir=str(working_directory))]
        )
        self.executor = self._create_executor(self.tools)

    def state(self, text: str) -> None:
        self.console.print(f"{self.name}: {text}", style=f"bold {self.color}")

    def output_md(self, md: str) -> None:
        self.console.print(Panel(Markdown(md, style="bold")))

    def output_html(self, html: str) -> None:
        self.console.print(Panel(html))

    def output_files(self, exclude_dirs=[]) -> None:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", width=40)
        table.add_column("Size(Bytes)", style="dim", justify="right")
        table.add_column("Date Modified", style="dim", justify="right")

        for root, dirs, files in os.walk(self.storages.app.path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    relative_path = os.path.relpath(
                        filepath, start=self.storages.app.path
                    )
                    stat = os.stat(filepath)
                    filesize = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    table.add_row(
                        relative_path,
                        str(filesize),
                        mtime,
                    )
        self.console.print(table)

    def ask(self, question: str, is_required: bool = True, default: str = None) -> str:
        while True:
            if default and default.endswith("\n"):
                default = re.sub(r"\n$", "", default)
            default_value = f"\n(default: {default})" if default else ""
            self.console.print(
                f"[{self.color} bold]{self.name}: {question}[/{self.color} bold][white]{default_value}[/white]"
            )
            answer = self.console.input("project.history").strip() or default
            self.console.new_lines(1)

            if answer or not is_required:
                return answer
            print("No input provided! Please try again.")

    def present_choices(
        self,
        question: str,
        choices: list[str],
        default: str,
    ) -> str:
        return self.console.choice(
            f"{self.name}: {question} (default: {default})",
            choices=choices,
            default=default,
            style=f"bold {self.color}",
        )

    def latest_message_content(self) -> str:
        return self.messages[-1].content.strip()

    def _get_default_profile(self) -> AgentProfile:
        return AGENT_PROFILES[self.role]

    def _create_executor(self, tools: list) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.profile,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_tool_calling_agent(self._llm, tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=self.debug_mode,
            handle_parsing_errors=True,
        )


class AgentRole(str, Enum):
    COPILOT = "copilot"
    PRODUCT_OWNER = "product_owner"
    ENGINEER = "engineer"
    ARCHITECT = "architect"
    DESIGNER = "designer"
    QA_ENGINEER = "qa_engineer"
    PROJECT_MANAGER = "project_manager"


@dataclass
class AgentProfile:
    name: str
    color: str
    prompt: PromptTemplate


AGENT_PROFILES = {
    AgentRole.COPILOT: AgentProfile(
        name="Copilot",
        color="#C4C4C4",
        prompt=PromptTemplate.from_template(""),
    ),
    AgentRole.PRODUCT_OWNER: AgentProfile(
        name="Steve Jobs",
        color="#FBE7C6",
        prompt=PromptTemplate.from_template(
            """You are an experienced product owner who defines specification of a software application.
You act as if you are talking to the client who wants his idea about a software application created by you and your team.
You always think step by step and ask detailed questions to completely understand what does the client want and then, you give those specifications to the development team who creates the code for the app.
"""
        ),
    ),
    AgentRole.ENGINEER: AgentProfile(
        name="DHH",
        color="#B4F8C8",
        prompt=PromptTemplate.from_template(
            """You are a super engineer with excellent command of React, JavaScript, and chakra-ui.
Your job is to implement **fully working** applications.
Always follow the best practices for the requested languages and frameworks for folder/file structure and how to package the project.
"""
        ),
    ),
    AgentRole.ARCHITECT: AgentProfile(
        name="Jeff Dean",
        color="#A0E7E5",
        prompt=PromptTemplate.from_template(
            """You are a seasoned software architect, specializing in designing architectures for minimum viable products (MVPs) for web applications.
On the front-end side, you excel in React.js best practice.
"""
        ),
    ),
    AgentRole.DESIGNER: AgentProfile(
        name="Jonathan Ive",
        color="#FFAEBC",
        prompt=PromptTemplate.from_template(
            """You are an experienced designer at Apple, specializing in creating user-friendly interfaces and experiences that follow the Human Interface Guidelines.
Also skilled in understanding and using `chakra-ui` specifications.
Proactively use `react-icons`, and if you do, don't forget to include them in dependencies in package.json.
"""
        ),
    ),
    AgentRole.QA_ENGINEER: AgentProfile(
        name="Sam Altman",
        color="#65463E",
        prompt=PromptTemplate.from_template(
            """You are a super engineer who specializes in testing that an application is fully functional according to specifications.
You have an eye for detail and a knack for finding hidden bugs.
You check for import omissions, variable declarations, parenthesis mismatches, syntax errors, and more.
You also check for security vulnerabilities and logic errors.
"""
        ),
    ),
    AgentRole.PROJECT_MANAGER: AgentProfile(
        name="Elon Musk",
        color="#DCBAA9",
        prompt=PromptTemplate.from_template(
            """You are a world-class project manager with extensive knowledge of everything from coding to design and testing, managing projects with enthusiasm to bring applications to full completion.
"""
        ),
    ),
}
