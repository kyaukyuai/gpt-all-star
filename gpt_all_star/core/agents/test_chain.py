from gpt_all_star.core.agents.chain import Chain
from gpt_all_star.core.message import Message

def test_create_git_commit_message_chain():
    chain = Chain()
    result = chain.create_git_commit_message_chain().invoke(
        {"messages": [Message.create_human_message("Test diff")]}
    )
    assert "branch" in result
    assert "message" in result

def test_create_command_to_execute_application_chain():
    chain = Chain() 
    result = chain.create_command_to_execute_application_chain().invoke(
        {"messages": [Message.create_human_message("Test source code")]}
    )
    assert "command" in result