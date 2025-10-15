"""Nursery stage: grafting cultivars onto propagated rootstock."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import NurseryBatch


@dataclass
class GraftingConfig:
    """Parameters for grafting success and costs."""

    cultivar_name: str
    labour_cost_per_tree: float
    pruning_cost_per_tree: float
    success_rate: float


def graft(batch: NurseryBatch, config: GraftingConfig) -> NurseryBatch:
    """Apply cultivar grafting and update tree count based on success."""

    successful = int(batch.trees * config.success_rate)
    batch.cost.add("grafting_labour", batch.trees * config.labour_cost_per_tree)
    batch.cost.add("pruning", successful * config.pruning_cost_per_tree)
    batch.notes.append(
        f"Grafted cultivar {config.cultivar_name} with {successful} successful unions."
    )
    batch.trees = successful
    return batch

