"""Orchard establishment: ongoing management operations."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import OrchardBlock


@dataclass
class ManagementConfig:
    """Management inputs and their costs."""

    annual_pruning_cost_per_tree: float
    fertiliser_cost_per_tree: float
    spray_cost_per_tree: float
    weather_modifier: float


def manage(block: OrchardBlock, config: ManagementConfig) -> OrchardBlock:
    """Apply management operations to the orchard block."""

    per_tree_cost = (
        config.annual_pruning_cost_per_tree
        + config.fertiliser_cost_per_tree
        + config.spray_cost_per_tree
    )
    block.costs.add("management", block.managed_trees * per_tree_cost)
    block.notes.append(
        "Applied pruning, fertiliser, and spray schedule with "
        f"weather modifier {config.weather_modifier:.2f}."
    )
    block.years_since_planting += 1
    return block

