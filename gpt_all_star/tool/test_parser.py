class TextParser:
    @staticmethod
    def cut_last_n_lines(text: str, n: int) -> str:
        lines = text.split("\n")
        return "\n".join(lines[:-n])
