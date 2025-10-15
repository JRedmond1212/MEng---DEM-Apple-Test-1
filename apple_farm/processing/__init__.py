"""Processing workflows for apple products."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..entities import HarvestLot, ProcessedProduct
from .cider import CiderProcessingConfig, process_cider
from .fresh import FreshProcessingConfig, process_fresh
from .juice import JuiceProcessingConfig, process_juice


@dataclass
class ProcessingConfig:
    """Aggregate configuration for all processing branches."""

    fresh: FreshProcessingConfig
    cider: CiderProcessingConfig
    juice: JuiceProcessingConfig


def run_processing(lot: HarvestLot, config: ProcessingConfig) -> List[ProcessedProduct]:
    """Process harvest grades into final products."""

    products: List[ProcessedProduct] = []
    products.append(process_fresh(lot, config.fresh))
    products.append(process_cider(lot, config.cider))
    products.append(process_juice(lot, config.juice))
    return products

__all__ = [
    "ProcessingConfig",
    "run_processing",
    "FreshProcessingConfig",
    "CiderProcessingConfig",
    "JuiceProcessingConfig",
]

