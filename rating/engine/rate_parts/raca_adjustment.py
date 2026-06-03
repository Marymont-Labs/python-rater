# rating/engine/rate_parts/raca_adjustment.py
#
# RACA Adjustment Factor rate parts — one function per coverage.
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "RACA Adjustment Factor" dataset from ctx.datasets
#   2. Find the row where state + zip_code + rating_classification match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
#   {
#    "state": "OH",
#    "rate_type": "ISO RACA Environmental Loss Costs",
#    "source_file": "oh_raca_env_factors.csv",
#    "zip_code": "43001",
#    "rating_classification": "Private Passenger Types",
#    "liability_env_loss_cost": "251.93873",
#    "collision_env_loss_cost": "263.91794",
#    "comprehensive_env_loss_cost": "94.65687",
#    "liability_ocp_adj": "1.008",
#    "collision_ocp_adj": "1.137",
#    "comprehensive_ocp_adj": "1.187",
#    "processed_date_time": "Thu Sep 07 2023 13:24:33 GMT-0400 (Eastern Daylight Time)"
#  },
#
# All three coverage factors are columns on the SAME row -- no coverage_type field to match on
# We find the row by rating_classification, then read the right column

from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "RACA Adjustment Factor"
DATASET_NAME = "RACA Adjustment Factor"


def _find_raca_row(
    dataset: list,
    rating_classification: str
) -> Optional[dict]:
    """
    Find the single row matching this vehicle's rating_classification. 
    The dataset is already filtered to state + zip_code by dataset loader
    """
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("rating_classification") == rating_classification
        ):
            return row
    return None


def _make_rate_part(
    ctx: VehicleRatingContext,
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


def fetch_raca_ocp_liability_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_raca_row(dataset, ctx.rating_classification)
    value = row.get("liability_ocp_adj") if row else None
    return _make_rate_part(ctx, "racaLiabilityOCPFactor", "Liability", value)

def fetch_raca_ocp_collision_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_raca_row(dataset, ctx.rating_classification)
    value = row.get("collision_ocp_adj") if row else None
    return _make_rate_part(ctx, "racaCollisionOCPFactor", "Collision", value)

def fetch_raca_ocp_comprehensive_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_raca_row(dataset, ctx.rating_classification)
    value = row.get("comprehensive_ocp_adj") if row else None
    return _make_rate_part(ctx, "racaComprehensiveOCPFactor", "Comprehensive", value)
