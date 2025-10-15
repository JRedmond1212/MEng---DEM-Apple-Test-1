"""Processing of dessert table apples and cooking apples."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot, ProcessedProduct


@dataclass
class FreshProcessingConfig:
    """Parameters for fresh market preparation."""

    washing_loss_fraction: float
    waxing_cost_per_kg: float
    packing_cost_per_kg: float


def process_fresh(lot: HarvestLot, config: FreshProcessingConfig) -> ProcessedProduct:
    """Process the dessert/cooking apples for distribution."""

    feedstock = lot.by_grade.get("dessert", 0.0) + lot.by_grade.get("cooking", 0.0)
    retained = feedstock * (1 - config.washing_loss_fraction)
    waste = feedstock - retained

    product = ProcessedProduct(
        name="Fresh Apples",
        quantity=retained,
        unit="kg",
        waste_kg=waste,
        notes=[
            f"Washed apples with loss fraction {config.washing_loss_fraction:.0%}",
            "Applied waxing and packed into retail bags/trays.",
        ],
    )
    product.by_products["packing_cost"] = retained * config.packing_cost_per_kg
    product.by_products["waxing_cost"] = retained * config.waxing_cost_per_kg
    return product

