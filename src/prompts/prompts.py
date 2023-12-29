import os

from jinja2 import Environment, FileSystemLoader

from logger.logger import logger


def get_prompt(prompt_name):
    logger.info(f"Getting prompt for {prompt_name}")

    prompts_path = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    file_loader = FileSystemLoader(prompts_path)
    env = Environment(loader=file_loader)

    template = env.get_template(prompt_name)
    return template.render()
