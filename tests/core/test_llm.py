from unittest.mock import patch

import pytest

from gpt_all_star.core.llm import _create_chat_openai


@pytest.fixture
def mock_openai():
    with patch("gpt_all_star.core.llm.openai") as mock:
        yield mock


@pytest.fixture
def mock_chat_openai():
    with patch("gpt_all_star.core.llm.ChatOpenAI") as mock:
        yield mock


def test_create_chat_openai_with_base_url(mock_openai, mock_chat_openai):
    base_url = "https://custom-openai-api.com/v1"
    _create_chat_openai(model_name="gpt-4", temperature=0.1, base_url=base_url)

    mock_chat_openai.assert_called_once_with(
        model_name="gpt-4",
        temperature=0.1,
        streaming=True,
        client=mock_openai.chat.completions,
        openai_api_base=base_url,
    )


def test_create_chat_openai_without_base_url(mock_openai, mock_chat_openai):
    _create_chat_openai(model_name="gpt-4", temperature=0.1, base_url=None)

    mock_chat_openai.assert_called_once_with(
        model_name="gpt-4",
        temperature=0.1,
        streaming=True,
        client=mock_openai.chat.completions,
        openai_api_base=None,
    )
