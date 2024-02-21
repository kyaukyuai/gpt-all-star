from gpt_all_star.core.execution.execution import execute_project
from gpt_all_star.core.execution.planning_prompt import get_planning_prompt


def run_project():
    # Get the planning prompt
    planning_prompt = get_planning_prompt()

    # Execute the project
    execute_project(planning_prompt)
