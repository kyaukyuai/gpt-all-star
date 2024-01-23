from dataclasses import dataclass

from gpt_all_star.core.agents.architect.architect import Architect
from gpt_all_star.core.agents.copilot.copilot import Copilot
from gpt_all_star.core.agents.designer.designer import Designer
from gpt_all_star.core.agents.engineer.engineer import Engineer
from gpt_all_star.core.agents.product_owner.product_owner import ProductOwner
from gpt_all_star.core.agents.qa_engineer.qa_engineer import QAEngineer


@dataclass
class Agents:
    copilot: Copilot
    product_owner: ProductOwner
    engineer: Engineer
    architect: Architect
    designer: Designer
    qa_engineer: QAEngineer
