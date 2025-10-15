"""Processing cider from graded apples."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot, ProcessedProduct


@dataclass
class CiderProcessingConfig:
    """Parameters for cider production."""

    pressing_yield: float
    fermentation_loss_fraction: float
    bottling_efficiency: float


def process_cider(lot: HarvestLot, config: CiderProcessingConfig) -> ProcessedProduct:
    """Convert cider-grade apples into finished cider."""

    feedstock = lot.by_grade.get("cider", 0.0)
    pressed = feedstock * config.pressing_yield
    fermentation_loss = pressed * config.fermentation_loss_fraction
    fermented = pressed - fermentation_loss
    bottled = fermented * config.bottling_efficiency
    waste = feedstock - bottled

    product = ProcessedProduct(
        name="Cider",
        quantity=bottled,
        unit="litres",
        waste_kg=waste,
        by_products={
            "pomace_to_animal_feed": fermentation_loss,
        },
        notes=[
            "Pressed, fermented, pasteurised, and bottled cider ready for distribution.",
        ],
    )
    return product

