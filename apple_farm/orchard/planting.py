"""Orchard establishment: planting stage."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import NurseryBatch, OrchardBlock


@dataclass
class PlantingConfig:
    """Parameters for planting and land preparation."""

    land_prep_cost_per_tree: float
    scaffolding_cost_per_tree: float
    density_factor: float


def plant(batch: NurseryBatch, config: PlantingConfig) -> OrchardBlock:
    """Plant nursery trees into the orchard block."""

    planted = int(batch.trees * config.density_factor)
    block = OrchardBlock(
        planted_trees=planted,
        managed_trees=planted,
        years_since_planting=0,
        fruiting=False,
        expected_yield_kg=0.0,
    )
    block.costs.add("land_prep", planted * config.land_prep_cost_per_tree)
    block.costs.add("scaffolding", planted * config.scaffolding_cost_per_tree)
    block.notes.extend(batch.notes)
    block.notes.append("Trees planted into orchard block.")
    return block

