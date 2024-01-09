from dataclasses import dataclass

from your_dev_team.core.agents.Architect import Architect
from your_dev_team.core.agents.Engineer import Engineer
from your_dev_team.core.agents.ProductOwner import ProductOwner


@dataclass
class Agents:
    product_owner: ProductOwner
    engineer: Engineer
    architect: Architect
