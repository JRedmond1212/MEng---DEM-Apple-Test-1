"""Distribution stage covering storage, transport, and consumers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..entities import DistributionBatch, ProcessedProduct


@dataclass
class DistributionConfig:
    """Parameters influencing distribution losses and demand."""

    storage_decay_fraction: float
    energy_cost_per_kg: float
    transport_loss_fraction: float
    consumer_demand_kg: float


def distribute(products: List[ProcessedProduct], config: DistributionConfig) -> DistributionBatch:
    """Simulate distribution chain to consumers."""

    total_quantity = sum(p.quantity for p in products)
    storage_losses = total_quantity * config.storage_decay_fraction
    transported = total_quantity - storage_losses
    delivered = transported * (1 - config.transport_loss_fraction)
    unsold = max(delivered - config.consumer_demand_kg, 0.0)

    notes = [
        f"Stored products with decay fraction {config.storage_decay_fraction:.0%}.",
        "Transported goods to retailers and consumers.",
    ]

    distribution = DistributionBatch(
        products=products,
        storage_losses_kg=storage_losses,
        customer_demand=config.consumer_demand_kg,
        unsold_kg=unsold,
        notes=notes,
    )

    if unsold > 0:
        distribution.notes.append("Unsold product directed to waste stream.")

    return distribution

