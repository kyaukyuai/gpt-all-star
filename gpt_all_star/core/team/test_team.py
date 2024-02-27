import unittest

from gpt_all_star.core.team import AgentRole, Team


class TestTeam(unittest.TestCase):
    def test_add_instructions_to_profile_copilot(self):
        # Create a Team instance with a COPILOT agent
        copilot = Team(AgentRole.COPILOT, "Copilot Profile")
        
        # Call the _add_instructions_to_profile method
        copilot._add_instructions_to_profile()
        
        # Assert that the profile contains the expected instructions for COPILOT
        expected_profile = "Copilot Profile\nAny instruction you get that is labeled as **IMPORTANT**, you follow strictly."
        self.assertEqual(copilot.profile, expected_profile)
    
    def test_add_instructions_to_profile_other_role(self):
        # Create a Team instance with an agent of a different role
        other_agent = Team(AgentRole.OTHER, "Other Agent Profile")
        
        # Call the _add_instructions_to_profile method
        other_agent._add_instructions_to_profile()
        
        # Assert that the profile does not contain the COPILOT instructions
        expected_profile = "Other Agent Profile"
        self.assertEqual(other_agent.profile, expected_profile)

if __name__ == "__main__":
    unittest.main()
