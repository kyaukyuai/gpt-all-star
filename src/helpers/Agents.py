from dataclasses import dataclass

from helpers.agents.ProductOwner import ProductOwner


@dataclass
class Agents:
    product_owner: ProductOwner
