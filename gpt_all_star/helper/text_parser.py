class TextParser:
    @staticmethod
    def cut_last_n_lines(text: str, n: int) -> str:
        lines = text.split("\n")
        return "\n".join(lines[:-n])


def format_file_to_input(file_name: str, file_content: str) -> str:
    file_str = f"""
    {file_name}
    ```
    {file_content}
    ```
    """
    return file_str
