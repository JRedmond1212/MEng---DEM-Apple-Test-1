"""Orchestrator for the apple farm production chain."""
from __future__ import annotations

from dataclasses import dataclass

from .distribution import DistributionConfig, distribute
from .entities import BatchStatus, FarmReport, WeatherSnapshot
from .harvesting import HarvestConfig, run_harvest
from .nursery import NurseryConfig, run_nursery
from .orchard import OrchardConfig, run_orchard
from .processing import ProcessingConfig, run_processing


@dataclass
class AppleFarmConfig:
    """Collect configuration objects for all chain stages."""

    nursery: NurseryConfig
    orchard: OrchardConfig
    harvesting: HarvestConfig
    processing: ProcessingConfig
    distribution: DistributionConfig
    weather: WeatherSnapshot


class AppleFarm:
    """High-level façade to run the configured farm pipeline."""

    def __init__(self, config: AppleFarmConfig):
        self.config = config

    def run(self) -> FarmReport:
        """Execute the production chain from nursery to distribution."""

        nursery_batch = run_nursery(self.config.nursery, self.config.weather)

        if nursery_batch.status is not BatchStatus.ACCEPTED:
            # If the nursery batch is rejected we short-circuit and capture empty downstream states.
            empty_orchard = run_orchard(
                nursery_batch,
                self.config.orchard,
            )
            empty_harvest = run_harvest(empty_orchard, self.config.harvesting)
            processed_products = run_processing(empty_harvest, self.config.processing)
            distribution_batch = distribute(processed_products, self.config.distribution)
            return FarmReport(
                nursery=nursery_batch,
                orchard=empty_orchard,
                harvest=empty_harvest,
                processed_goods=processed_products,
                distribution=distribution_batch,
            )

        orchard_block = run_orchard(nursery_batch, self.config.orchard)
        harvest_lot = run_harvest(orchard_block, self.config.harvesting)
        processed_products = run_processing(harvest_lot, self.config.processing)
        distribution_batch = distribute(processed_products, self.config.distribution)

        return FarmReport(
            nursery=nursery_batch,
            orchard=orchard_block,
            harvest=harvest_lot,
            processed_goods=processed_products,
            distribution=distribution_batch,
        )

