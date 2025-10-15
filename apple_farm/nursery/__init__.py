"""Nursery workflow orchestrating rootstock selection through quality control."""
from __future__ import annotations

from dataclasses import dataclass

from .grafting import GraftingConfig, graft
from .propagation import PropagationConfig, propagate
from .quality_control import QualityControlConfig, inspect
from .rootstock import RootstockSelectionConfig, select_rootstock
from ..entities import NurseryBatch, WeatherSnapshot


@dataclass
class NurseryConfig:
    """Aggregate configuration for the full nursery pipeline."""

    rootstock: RootstockSelectionConfig
    propagation: PropagationConfig
    grafting: GraftingConfig
    quality: QualityControlConfig


def run_nursery(config: NurseryConfig, weather: WeatherSnapshot) -> NurseryBatch:
    """Execute the nursery pipeline and return the resulting batch."""

    batch = select_rootstock(config.rootstock, weather)
    batch = propagate(batch, config.propagation, weather)
    batch = graft(batch, config.grafting)
    batch = inspect(batch, config.quality)
    return batch

__all__ = [
    "NurseryConfig",
    "run_nursery",
    "RootstockSelectionConfig",
    "PropagationConfig",
    "GraftingConfig",
    "QualityControlConfig",
]

