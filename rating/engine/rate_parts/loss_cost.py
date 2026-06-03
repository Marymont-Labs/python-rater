# rating/engine/rate_parts/loss_cost.py
#
# Base Loss Cost rate parts — one function per coverage.
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Territory Base Loss Cost" dataset from ctx.datasets
#   2. Find the row where coverage_type + rating_classification + vehicle_category match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
#   {
#     "state": "OH",
#     "territory_no": "102",
#     "coverage_type": "Liability",
#     "rating_classification": "Public Auto",
#     "vehicle_category": "Taxicabs And Limousines",
#     "loss_cost_rate": "2263",
#     ...
#   }
#
# fetchLossCostFactors() already filters by state + territory before storing
# in datasets, so here we only need to match coverage_type + classification + category.

from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Base Loss Cost"
DATASET_NAME = "Territory Base Loss Cost"


def _find_loss_cost(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    vehicle_category: str,
) -> Optional[str]:
    """
    Mirror of the JS inner loop:
        if lossCostObj.coverage_type == 'Liability'
        && lossCostObj.rating_classification == thisRatingClassification
        && lossCostObj.vehicle_category == thisVehicleCategory
    """
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type
            and row.get("rating_classification") == rating_classification
            and row.get("vehicle_category") == vehicle_category
        ):
            return row.get("loss_cost_rate")
    return None


def _make_rate_part(
    ctx: VehicleRatingContext,
    coverage_type: str,
    rate_name: str,
    rate_category: str,
    value: Optional[str],
) -> dict:
    """Build the rate part dict. Returns {} if no matching row found."""
    if value is None:
        return {}
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": RATE_PART_CATEGORY,
        "rateName": rate_name,
        "rateCategory": rate_category,
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": value,
    }


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_loss_cost_liability_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    value = _find_loss_cost(
        dataset,
        coverage_type="Liability",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "Liability", "liabilityLossCostRate", "Liability", value)


def fetch_loss_cost_pip_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    value = _find_loss_cost(
        dataset,
        coverage_type="PIP",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "PIP", "pipLossCostRate", "PIP", value)


def fetch_loss_cost_medpay_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    value = _find_loss_cost(
        dataset,
        coverage_type="MedPay",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "MedPay", "medPayLossCostRate", "MedPay", value)


def fetch_loss_cost_collision_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    value = _find_loss_cost(
        dataset,
        coverage_type="Collision",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "Collision", "collisionLossCostRate", "Collision", value)


def fetch_loss_cost_comprehensive_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    value = _find_loss_cost(
        dataset,
        coverage_type="Comprehensive",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "Comprehensive", "comprehensiveLossCostRate", "Comprehensive", value)


def fetch_loss_cost_umbi_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset("Territory Base Loss Cost UMBI")
    value = _find_loss_cost(
        dataset,
        coverage_type="UMBI",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "UMBI", "umbiLossCostRate", "UMBI", value)


def fetch_loss_cost_uimbi_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset("Territory Base Loss Cost UIMBI")
    value = _find_loss_cost(
        dataset,
        coverage_type="UIMBI",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
    )
    return _make_rate_part(ctx, "UIMBI", "uimbiLossCostRate", "UIMBI", value)