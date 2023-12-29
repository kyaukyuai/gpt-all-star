from dataclasses import dataclass

from core.agents.ProductOwner import ProductOwner


@dataclass
class Agents:
    product_owner: ProductOwner
