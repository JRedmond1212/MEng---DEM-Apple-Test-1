"""Processing apple juice from graded apples."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot, ProcessedProduct


@dataclass
class JuiceProcessingConfig:
    """Parameters for juice processing."""

    pressing_yield: float
    filtration_loss_fraction: float
    pasteurisation_efficiency: float
    concentration_rate: float
    packaging_efficiency: float


def process_juice(lot: HarvestLot, config: JuiceProcessingConfig) -> ProcessedProduct:
    """Convert juice-grade apples into consumer juice products."""

    feedstock = lot.by_grade.get("juice", 0.0)
    pressed = feedstock * config.pressing_yield
    filtered = pressed * (1 - config.filtration_loss_fraction)
    pasteurised = filtered * config.pasteurisation_efficiency
    concentrated = pasteurised * config.concentration_rate
    packaged = concentrated * config.packaging_efficiency
    waste = feedstock - packaged

    product = ProcessedProduct(
        name="Apple Juice",
        quantity=packaged,
        unit="litres",
        waste_kg=waste,
        by_products={
            "pomace_to_animal_feed": pressed * config.filtration_loss_fraction,
        },
        notes=[
            "Pressed, filtered, pasteurised, concentrated, and packaged juice ready for distribution.",
        ],
    )
    return product

