from dataclasses import dataclass

from your_dev_team.core.agents.Architect import Architect
from your_dev_team.core.agents.Copilot import Copilot
from your_dev_team.core.agents.Designer import Designer
from your_dev_team.core.agents.Engineer import Engineer
from your_dev_team.core.agents.ProductOwner import ProductOwner


@dataclass
class Agents:
    copilot: Copilot
    product_owner: ProductOwner
    engineer: Engineer
    architect: Architect
    designer: Designer
