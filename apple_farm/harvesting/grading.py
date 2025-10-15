"""Harvesting stage: grading into product streams."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot


@dataclass
class GradingConfig:
    """Grade percentages for different product streams."""

    dessert_fraction: float
    cooking_fraction: float
    cider_fraction: float
    juice_fraction: float
    processing_loss_fraction: float


def grade(lot: HarvestLot, config: GradingConfig) -> HarvestLot:
    """Split the harvest lot into grades according to configured fractions."""

    if lot.total_kg <= 0:
        lot.notes.append("No fruit to grade.")
        return lot

    remainder = 1 - config.processing_loss_fraction
    dessert = lot.total_kg * config.dessert_fraction * remainder
    cooking = lot.total_kg * config.cooking_fraction * remainder
    cider = lot.total_kg * config.cider_fraction * remainder
    juice = lot.total_kg * config.juice_fraction * remainder
    loss = lot.total_kg * config.processing_loss_fraction

    lot.by_grade = {
        "dessert": dessert,
        "cooking": cooking,
        "cider": cider,
        "juice": juice,
        "loss": loss,
    }
    lot.notes.append("Harvest graded into product streams.")
    return lot

