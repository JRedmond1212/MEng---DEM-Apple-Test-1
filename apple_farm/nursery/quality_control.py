"""Nursery stage: quality control decision before orchard delivery."""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import BatchStatus, NurseryBatch


@dataclass
class QualityControlConfig:
    """Quality control thresholds."""

    min_trees: int
    rejection_rate: float


def inspect(batch: NurseryBatch, config: QualityControlConfig) -> NurseryBatch:
    """Inspect the batch and flag it as accepted or rejected."""

    rejected_trees = int(batch.trees * config.rejection_rate)
    accepted_trees = batch.trees - rejected_trees
    batch.notes.append(
        f"Quality control removed {rejected_trees} trees; {accepted_trees} ready for orchard."
    )
    batch.trees = accepted_trees

    if accepted_trees >= config.min_trees:
        batch.status = BatchStatus.ACCEPTED
        batch.notes.append("Batch accepted for delivery to orchard.")
    else:
        batch.status = BatchStatus.REJECTED
        batch.notes.append("Batch rejected – sent to mulch/waste stream.")

    return batch

