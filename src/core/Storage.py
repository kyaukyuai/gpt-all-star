from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


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
        with self.get_path(item).open('r', encoding='utf-8') as f:
            return f.read()

    def __setitem__(self, key: str, value: str):
        if key.startswith('../'):
            raise ValueError(f"File name '{key}' attempted to access parent path.")

        full_path = self.path / key
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(value, encoding='utf-8')

    def __delitem__(self, item: str):
        item_path = self.get_path(item)

        if item_path.is_file():
            item_path.unlink()
        elif item_path.is_dir():
            shutil.rmtree(item_path)


@dataclass
class Storages:
    origin: Storage
    result: Storage
    src: Storage
