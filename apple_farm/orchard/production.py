"""Orchard production decision and yield calculation."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import OrchardBlock


@dataclass
class ProductionConfig:
    """Parameters to determine fruit production and yield."""

    juvenile_period_years: int
    mature_yield_per_tree: float
    weather_yield_modifier: float


def evaluate_production(block: OrchardBlock, config: ProductionConfig) -> OrchardBlock:
    """Decide whether the block is fruiting and estimate yield."""

    if block.years_since_planting < config.juvenile_period_years:
        block.fruiting = False
        block.expected_yield_kg = 0.0
        block.notes.append("Block too young for fruit production; prepare for next season.")
        return block

    block.fruiting = True
    base_yield = block.managed_trees * config.mature_yield_per_tree
    block.expected_yield_kg = base_yield * config.weather_yield_modifier
    block.notes.append(
        "Fruit production achieved with expected yield "
        f"{block.expected_yield_kg:.1f} kg."
    )
    return block

