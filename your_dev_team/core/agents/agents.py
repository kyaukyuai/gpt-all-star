from dataclasses import dataclass

from your_dev_team.core.agents.architect import Architect
from your_dev_team.core.agents.copilot import Copilot
from your_dev_team.core.agents.designer import Designer
from your_dev_team.core.agents.engineer import Engineer
from your_dev_team.core.agents.product_owner import ProductOwner


@dataclass
class Agents:
    copilot: Copilot
    product_owner: ProductOwner
    engineer: Engineer
    architect: Architect
    designer: Designer
