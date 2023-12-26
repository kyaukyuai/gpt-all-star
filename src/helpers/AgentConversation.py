class AgentConversation:
    def __init__(self, agent):
        # [{'role': 'system'|'user'|'assistant', 'content': ''}, ...]
        self.messages: list[dict] = []
        self.agent = agent
        self.high_level_step = self.agent.project.current_step
