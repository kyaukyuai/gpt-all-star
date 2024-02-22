import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.agents.agent import Agent


class AgentTest(unittest.TestCase):
    def test_invoke(self):
        # Create a mock Agent instance
        agent = Agent()

        # Test the invoke method with a valid message
        message = "Hello, world!"
        result = agent.invoke(message)
        self.assertEqual(result, "Response")

        # Test the invoke method with an empty message
        empty_message = ""
        result = agent.invoke(empty_message)
        self.assertEqual(result, "")

        # Test the invoke method with an invalid input
        invalid_message = None
        with self.assertRaises(TypeError):
            agent.invoke(invalid_message)

    def test_execute(self):
        # Create a mock Agent instance
        agent = Agent()

        # Test executing a single command
        command = "print('Hello, world!')"
        result = agent.execute(command)
        self.assertEqual(result, "Hello, world!")

        # Test executing multiple commands
        commands = ["x = 1", "y = 2", "z = x + y"]
        result = agent.execute(commands)
        self.assertEqual(result, 3)

        # Test executing an invalid command
        invalid_command = "invalid_command"
        with self.assertRaises(SyntaxError):
            agent.execute(invalid_command)


if __name__ == "__main__":
    unittest.main()
