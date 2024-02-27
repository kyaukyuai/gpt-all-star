import unittest

from gpt_all_star.core.steps.system_design.additional_tasks import \
    additional_tasks


class TestAdditionalTasks(unittest.TestCase):
    def test_additional_tasks(self):
        expected_output = [
            {
                "action": "Add a new file",
                "working_directory": ".",
                "filename": "technologies.md",
                "command": "",
                "context": """This task requires compiling a precise list of technologies for building an application, focusing on source code implementation.
The list should adhere to project specifications and be guided by Technologies Guidelines emphasizing relevance, compatibility, and preference.
These guidelines mandate including only essential, actively used technologies, ensuring their compatibility, and excluding any that cannot be integrated.
Additionally, when multiple options are available for a specific project component, the guidelines prioritize React, JavaScript, chakra-ui and HTML.
""",
                "objective": """To produce a document clearly outlining the necessary and compatible technologies for the project's development, prioritizing preferred technologies.
This aims to ensure an efficient and coherent development process using a streamlined, compatible technology stack, thereby facilitating easier integration and implementation.
""",
                "reason": """Creating a focused and guided list of technologies is essential for the project's success.
It enables the development team to make informed decisions about the technology stack, ensuring that each technology chosen is not only relevant and compatible but also preferred within the project's context.
This approach minimizes integration issues, optimizes development efforts, and ensures the project is built on a solid and efficient foundation of technologies well-suited to its requirements.
""",
            },
        ]

        result = additional_tasks()
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
