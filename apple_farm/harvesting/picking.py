"""Harvesting stage: picking operations."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot, OrchardBlock


@dataclass
class PickingConfig:
    """Parameters for picking logistics."""

    field_grading_efficiency: float
    time_to_harvest_days: int


def pick(block: OrchardBlock, config: PickingConfig) -> HarvestLot:
    """Harvest fruit from the orchard block and create an initial lot."""

    if not block.fruiting:
        return HarvestLot(total_kg=0.0, by_grade={}, notes=["No fruit available for harvest."])

    effective_yield = block.expected_yield_kg * config.field_grading_efficiency
    lot = HarvestLot(
        total_kg=effective_yield,
        by_grade={"field_run": effective_yield},
    )
    lot.notes.append(
        f"Harvested over {config.time_to_harvest_days} days with efficiency "
        f"{config.field_grading_efficiency:.0%}."
    )
    return lot

