"""Nursery stage: rootstock selection and procurement."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import NurseryBatch, WeatherSnapshot


@dataclass
class RootstockSelectionConfig:
    """Configuration values controlling rootstock selection logic."""

    target_trees: int
    cost_per_tree: float
    weather_risk_threshold: float = 0.3


def select_rootstock(config: RootstockSelectionConfig, weather: WeatherSnapshot) -> NurseryBatch:
    """Select rootstock material based on weather risk tolerance."""

    batch = NurseryBatch(trees=config.target_trees)
    batch.cost.add("rootstock", config.target_trees * config.cost_per_tree)
    batch.notes.append(f"Weather outlook: {weather.description}")

    if weather.risk_factor > config.weather_risk_threshold:
        batch.notes.append("Procurement scaled back due to weather risk.")
        reduced_trees = int(config.target_trees * (1 - weather.risk_factor))
        batch.trees = max(reduced_trees, int(config.target_trees * 0.5))
    else:
        batch.notes.append("Weather suitable for full procurement.")

    return batch

