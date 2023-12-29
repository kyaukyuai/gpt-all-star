from dataclasses import dataclass

from core.agents.Engineer import Engineer
from core.agents.ProductOwner import ProductOwner


@dataclass
class Agents:
    product_owner: ProductOwner
    engineer: Engineer
