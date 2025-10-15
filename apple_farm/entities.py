"""Core dataclasses shared across the apple farm production chain."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class BatchStatus(str, Enum):
    """High level status flags for batches travelling through the chain."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class CostRecord:
    """Break down cumulative costs and investments for a batch."""

    items: Dict[str, float] = field(default_factory=dict)

    @property
    def total(self) -> float:
        return sum(self.items.values())

    def add(self, name: str, value: float) -> None:
        self.items[name] = self.items.get(name, 0.0) + value


@dataclass
class WeatherSnapshot:
    """Simple descriptor for weather related notes in each step."""

    description: str
    risk_factor: float


@dataclass
class NurseryBatch:
    """Represents rootstock material that will eventually become orchard trees."""

    trees: int
    status: BatchStatus = BatchStatus.PENDING
    cost: CostRecord = field(default_factory=CostRecord)
    notes: List[str] = field(default_factory=list)


@dataclass
class OrchardBlock:
    """Represents the orchard during the establishment and production stage."""

    planted_trees: int
    managed_trees: int
    years_since_planting: int
    fruiting: bool
    expected_yield_kg: float
    costs: CostRecord = field(default_factory=CostRecord)
    notes: List[str] = field(default_factory=list)


@dataclass
class HarvestLot:
    """Represents harvested apples grouped by grades."""

    total_kg: float
    by_grade: Dict[str, float]
    notes: List[str] = field(default_factory=list)


@dataclass
class ProcessedProduct:
    """Represents processed goods leaving the processing stage."""

    name: str
    quantity: float
    unit: str
    waste_kg: float = 0.0
    by_products: Dict[str, float] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


@dataclass
class DistributionBatch:
    """Represents goods ready for dispatch to retailers/consumers."""

    products: List[ProcessedProduct]
    storage_losses_kg: float
    customer_demand: float
    unsold_kg: float
    notes: List[str] = field(default_factory=list)


@dataclass
class FarmReport:
    """Final compiled report summarising the entire run."""

    nursery: NurseryBatch
    orchard: OrchardBlock
    harvest: HarvestLot
    processed_goods: List[ProcessedProduct]
    distribution: DistributionBatch

