"""Harvesting stage: short-term storage operations."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import HarvestLot


@dataclass
class StorageConfig:
    """Storage capacity and decay parameters."""

    storage_capacity_kg: float
    daily_decay_rate: float
    storage_days: int


def store(lot: HarvestLot, config: StorageConfig) -> HarvestLot:
    """Apply storage constraints and quality decay."""

    if lot.total_kg <= 0:
        return lot

    stored = min(lot.total_kg, config.storage_capacity_kg)
    decay_factor = (1 - config.daily_decay_rate) ** config.storage_days
    retained = stored * decay_factor
    loss = stored - retained

    lot.notes.append(
        f"Stored {stored:.1f} kg for {config.storage_days} days; "
        f"losses {loss:.1f} kg."
    )
    lot.total_kg = retained
    lot.by_grade["stored"] = retained
    return lot

