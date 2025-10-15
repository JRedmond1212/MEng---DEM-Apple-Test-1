"""Nursery stage: propagation of rootstocks."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import NurseryBatch, WeatherSnapshot


@dataclass
class PropagationConfig:
    """Parameters that influence propagation success."""

    irrigation_cost_per_tree: float
    mulch_cost_per_tree: float
    survival_rate: float


def propagate(batch: NurseryBatch, config: PropagationConfig, weather: WeatherSnapshot) -> NurseryBatch:
    """Propagate the selected rootstock and update survival numbers."""

    survived = int(batch.trees * config.survival_rate * (1 - weather.risk_factor * 0.2))
    batch.cost.add("irrigation", survived * config.irrigation_cost_per_tree)
    batch.cost.add("mulch", survived * config.mulch_cost_per_tree)
    batch.notes.append(
        "Propagation complete with survival rate "
        f"{config.survival_rate:.0%}; weather modifier {weather.risk_factor:.2f}."
    )
    batch.trees = survived
    return batch

