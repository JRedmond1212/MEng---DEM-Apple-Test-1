"""Command line entry point to run a sample apple farm scenario."""
from __future__ import annotations

from pprint import pprint

from . import AppleFarm, AppleFarmConfig, WeatherSnapshot
from .distribution import DistributionConfig
from .harvesting import HarvestConfig, GradingConfig, PickingConfig, StorageConfig
from .nursery import (
    GraftingConfig,
    NurseryConfig,
    PropagationConfig,
    QualityControlConfig,
    RootstockSelectionConfig,
)
from .orchard import ManagementConfig, OrchardConfig, PlantingConfig, ProductionConfig
from .processing import (
    CiderProcessingConfig,
    FreshProcessingConfig,
    JuiceProcessingConfig,
    ProcessingConfig,
)


def build_default_config() -> AppleFarmConfig:
    """Assemble a complete farm configuration with illustrative numbers."""

    nursery_config = NurseryConfig(
        rootstock=RootstockSelectionConfig(target_trees=1200, cost_per_tree=1.2),
        propagation=PropagationConfig(
            irrigation_cost_per_tree=0.3,
            mulch_cost_per_tree=0.25,
            survival_rate=0.85,
        ),
        grafting=GraftingConfig(
            cultivar_name="Honeycrisp",
            labour_cost_per_tree=0.5,
            pruning_cost_per_tree=0.2,
            success_rate=0.9,
        ),
        quality=QualityControlConfig(min_trees=700, rejection_rate=0.05),
    )

    orchard_config = OrchardConfig(
        planting=PlantingConfig(
            land_prep_cost_per_tree=1.0,
            scaffolding_cost_per_tree=0.4,
            density_factor=0.95,
        ),
        management=ManagementConfig(
            annual_pruning_cost_per_tree=0.6,
            fertiliser_cost_per_tree=0.4,
            spray_cost_per_tree=0.3,
            weather_modifier=0.9,
        ),
        production=ProductionConfig(
            juvenile_period_years=4,
            mature_yield_per_tree=25.0,
            weather_yield_modifier=0.85,
        ),
    )

    harvesting_config = HarvestConfig(
        picking=PickingConfig(field_grading_efficiency=0.95, time_to_harvest_days=10),
        storage=StorageConfig(storage_capacity_kg=15000, daily_decay_rate=0.01, storage_days=7),
        grading=GradingConfig(
            dessert_fraction=0.35,
            cooking_fraction=0.25,
            cider_fraction=0.2,
            juice_fraction=0.15,
            processing_loss_fraction=0.05,
        ),
    )

    processing_config = ProcessingConfig(
        fresh=FreshProcessingConfig(
            washing_loss_fraction=0.02,
            waxing_cost_per_kg=0.1,
            packing_cost_per_kg=0.15,
        ),
        cider=CiderProcessingConfig(
            pressing_yield=0.7,
            fermentation_loss_fraction=0.05,
            bottling_efficiency=0.9,
        ),
        juice=JuiceProcessingConfig(
            pressing_yield=0.65,
            filtration_loss_fraction=0.08,
            pasteurisation_efficiency=0.95,
            concentration_rate=0.6,
            packaging_efficiency=0.9,
        ),
    )

    distribution_config = DistributionConfig(
        storage_decay_fraction=0.03,
        energy_cost_per_kg=0.05,
        transport_loss_fraction=0.02,
        consumer_demand_kg=8000,
    )

    weather = WeatherSnapshot(description="Mild spring with occasional showers", risk_factor=0.2)

    return AppleFarmConfig(
        nursery=nursery_config,
        orchard=orchard_config,
        harvesting=harvesting_config,
        processing=processing_config,
        distribution=distribution_config,
        weather=weather,
    )


def main() -> None:
    config = build_default_config()
    farm = AppleFarm(config)
    report = farm.run()
    pprint(report)


if __name__ == "__main__":
    main()

