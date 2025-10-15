"""Orchard establishment and growth workflow."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import NurseryBatch, OrchardBlock
from .management import ManagementConfig, manage
from .planting import PlantingConfig, plant
from .production import ProductionConfig, evaluate_production


@dataclass
class OrchardConfig:
    """Aggregate configuration for orchard establishment and production."""

    planting: PlantingConfig
    management: ManagementConfig
    production: ProductionConfig


def run_orchard(batch: NurseryBatch, config: OrchardConfig) -> OrchardBlock:
    """Execute the orchard workflow from planting to production decision."""

    block = plant(batch, config.planting)
    block = manage(block, config.management)
    block = evaluate_production(block, config.production)
    return block

__all__ = [
    "OrchardConfig",
    "run_orchard",
    "PlantingConfig",
    "ManagementConfig",
    "ProductionConfig",
]

