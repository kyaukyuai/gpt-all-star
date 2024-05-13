import tiktoken
from langchain_core.messages import BaseMessage


class Tokenizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self._tiktoken_tokenizer = (
            tiktoken.encoding_for_model(model_name)
            if "gpt-4" in model_name
            or "gpt-3.5" in model_name
            or "gpt-4o" in model_name
            else tiktoken.get_encoding("cl100k_base")
        )

    def num_tokens(self, txt: str) -> int:
        return len(self._tiktoken_tokenizer.encode(txt))

    def num_tokens_from_messages(self, messages: list[BaseMessage]) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += self.num_tokens(message.content)
        return num_tokens
