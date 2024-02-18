import logging
import platform
import subprocess
import warnings
from typing import Optional, Type, Union

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


class ShellInput(BaseModel):
    """Commands for the Bash Shell tool."""

    commands: Union[str, list[str]] = Field(
        ...,
        description="List of shell commands to run. Deserialized using json.loads",
    )
    """List of shell commands to run."""

    @root_validator
    def _validate_commands(cls, values: dict) -> dict:
        """Validate commands."""
        # TODO: Add real validators
        commands = values.get("commands")
        if not isinstance(commands, list):
            values["commands"] = [commands]
        # Warn that the bash tool is not safe
        # warnings.warn(
        #     "The shell tool has no safeguards by default. Use at your own risk."
        # )
        return values


def _get_platform() -> str:
    """Get platform."""
    system = platform.system()
    if system == "Darwin":
        return "MacOS"
    return system


class ShellTool(BaseTool):
    name: str = "terminal"
    """Name of tool."""

    description: str = f"Run shell commands on this {_get_platform()} machine."
    """Description of tool."""

    args_schema: Type[BaseModel] = ShellInput
    """Schema for input arguments."""
    ask_human_input: bool = False
    """
    If True, prompts the user for confirmation (y/n) before executing
    a command generated by the language model in the bash shell.
    """

    root_dir: str = "./"
    """If specified, all file operations are made relative to root_dir."""

    verbose: bool = False
    """If True, print the stdout."""

    def _run(
        self,
        commands: Union[str, list[str]],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run commands and return final output."""

        not_allowed_commands = ["npm start", "yarn start"]

        if self._is_command_not_allowed(commands, not_allowed_commands):
            if self.verbose:
                warnings.warn(
                    "The command 'npm start' or 'yarn start' is not allowed to be executed."
                )
            return None

        if self.verbose:
            print(f"Executing command:\n {commands}")

        timeout = 300  # Timeout in seconds

        try:
            if self.ask_human_input:
                if not self._get_user_confirmation():
                    logger.info("Invalid input. User aborted command execution.")
                    return None

            return self._execute_commands(commands, timeout)

        except Exception as e:
            logger.error(f"Error during command execution: {e}")
            return None

    def _is_command_not_allowed(
        self, commands: Union[str, list[str]], not_allowed_commands: list[str]
    ) -> bool:
        """Check if the command is not allowed."""
        import re

        return isinstance(commands, (str, list)) and any(
            re.search(
                cmd, " ".join(commands if isinstance(commands, list) else [commands])
            )
            for cmd in not_allowed_commands
        )

    def _get_user_confirmation(self) -> bool:
        """Get user confirmation to proceed with command execution.
        Returns:
            bool: True if the user confirms (input is 'y'), False otherwise."""
        """Get user confirmation to proceed with command execution."""
        user_input = input("Proceed with command execution? (y/n): ").lower()
        return user_input == "y"

    def _execute_commands(\n        self, commands: Union[str, list[str]], timeout: int\n    ) -> Optional[str]:\n        """Execute commands and return the output.\n\n        Args:\n            commands (Union[str, list[str]]): The command(s) to execute.\n            timeout (int): The timeout in seconds.\n        Returns:\n            Optional[str]: The output of the executed commands, or None if there was an error."""
        self, commands: Union[str, list[str]], timeout: int
    ) -> Optional[str]:
        """Execute commands and return the output."""
        import time

        process = subprocess.Popen(
            commands,
            shell=True,
            cwd=self.root_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        start_time = time.time()
        while True:
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    if self.verbose:
                        logger.error(f"Error during command execution: {stdout}")
                    return None
                if self.verbose:
                    print(stdout)
                time_count = time.time() - start_time
                print(f"Time count: {time_count}")
                return stdout
            if time.time() - start_time > timeout:
                process.terminate()
                logger.info("Command execution timed out.")
                return None
