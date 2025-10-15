"""Harvesting workflow."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot, OrchardBlock
from .grading import GradingConfig, grade
from .picking import PickingConfig, pick
from .storage import StorageConfig, store


@dataclass
class HarvestConfig:
    """Aggregate configuration for the harvesting workflow."""

    picking: PickingConfig
    storage: StorageConfig
    grading: GradingConfig


def run_harvest(block: OrchardBlock, config: HarvestConfig) -> HarvestLot:
    """Execute picking, storage, and grading."""

    lot = pick(block, config.picking)
    lot = store(lot, config.storage)
    lot = grade(lot, config.grading)
    return lot

__all__ = [
    "HarvestConfig",
    "run_harvest",
    "PickingConfig",
    "StorageConfig",
    "GradingConfig",
]

