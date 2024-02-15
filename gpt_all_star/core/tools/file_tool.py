import warnings
from typing import Optional, Type

from langchain_community.tools.file_management.utils import (
    INVALID_PATH_TEMPLATE,
    BaseFileToolMixin,
    FileValidationError,
)
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool


class UpdateFileInput(BaseModel):
    """Input for UpdateFileTool."""

    file_path: str = Field(..., description="name of file")
    inserts: Optional[dict[int, str]] = Field(
        ...,
        description="Dictionary where key is the line number (1-indexed) and value is the text to be inserted at that line.",
    )
    """List of UpdateFileTool to run."""


class UpdateFileTool(BaseFileToolMixin, BaseTool):
    name: str = "update_file"
    """Name of tool."""

    args_schema: Type[BaseModel] = UpdateFileInput
    """Schema for input arguments."""

    description: str = "Update a file by inserting text at specific line numbers."
    """Description of tool."""

    def _run(
        self,
        file_path: str,
        inserts: Optional[dict[int, str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Tool that updates a file to disk."""
        if inserts is None:
            warnings.warn(
                "inserts is None. This tool will not make any changes to the file."
            )
            return None
        try:
            update_path = self.get_relative_path(file_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="file_path", value=file_path)
        try:
            update_path.parent.mkdir(exist_ok=True, parents=False)
            with update_path.open("r", encoding="utf8") as file:
                lines = file.readlines()

            sorted_inserts = sorted(inserts.items())

            for line_number, text in sorted_inserts:
                if 1 <= line_number <= len(lines) + 1:
                    lines.insert(line_number - 1, text + "\n")
                else:
                    return f"Error: Line number {line_number} is out of range."

            with update_path.open("w") as file:
                file.writelines(lines)

            return f"Document edited and saved to {file_path}"
        except Exception as e:
            return "Error: " + str(e)
