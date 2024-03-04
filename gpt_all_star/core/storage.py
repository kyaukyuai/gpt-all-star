from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from gpt_all_star.helper.text_parser import format_file_to_input


class Storage:
    def __init__(self, path: str | Path):
        self.path = Path(path).absolute()
        self.path.mkdir(parents=True, exist_ok=True)

    def __contains__(self, item: str):
        return (self.path / item).is_file()

    def get_path(self, item: str):
        item_path = self.path / item
        if not item_path.is_file():
            raise KeyError(f"File '{item}' could not be found in '{self.path}'")
        return item_path

    def __getitem__(self, item: str):
        with self.get_path(item).open("r", encoding="utf-8") as f:
            return f.read()

    def __setitem__(self, key: str, value: str):
        if key.startswith("../"):
            raise ValueError(f"File name '{key}' attempted to access parent path.")

        full_path = self.path / key
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(value, encoding="utf-8")

    def __delitem__(self, item: str):
        item_path = self.get_path(item)

        if item_path.is_file():
            item_path.unlink()
        elif item_path.is_dir():
            shutil.rmtree(item_path)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def recursive_file_search(
        self, path: Path | None = None, files_dict=None
    ) -> dict[str, str]:
        if files_dict is None:
            files_dict = {}
        excluded_files = ["package-lock.json", "yarn.lock"]
        excluded_dirs = ["node_modules", ".git", ".archive", ".idea", "build"]

        for item in (path or self.path).iterdir():
            if item.is_file() and item.name not in excluded_files:
                try:
                    file_content = item.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                files_dict[str(item)] = file_content
            elif item.is_dir() and item.name not in excluded_dirs:
                self.recursive_file_search(item, files_dict)
        return files_dict


@dataclass
class Storages:
    root: Storage
    docs: Storage
    app: Storage
    archive: Storage

    def archive_storage(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = os.path.join(self.archive.path, timestamp)

        if not os.path.exists(destination):
            os.makedirs(destination)

        for item in os.listdir(self.root.path):
            if item != ".archive":
                shutil.move(os.path.join(self.root.path, item), destination)
        self.docs.path.mkdir(parents=True, exist_ok=True)
        self.app.path.mkdir(parents=True, exist_ok=True)

    def current_source_code(self, debug_mode: bool = False) -> str:
        source_code_contents = []
        for (
            filename,
            file_content,
        ) in self.app.recursive_file_search().items():
            if debug_mode:
                print(f"Adding file {filename} to the prompt...")
            formatted_code = format_file_to_input(
                f"./{os.path.relpath(filename, self.app.path)}", file_content
            )
            source_code_contents.append(formatted_code)
        return "\n".join(source_code_contents) if source_code_contents else "N/A"
