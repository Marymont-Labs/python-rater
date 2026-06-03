# rating/engine/rate_parts/policy_tier.py
#
# Policy Tier rate parts — one function per coverage. Coverages are Liability, MedPay, PIP, Collision
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Driver Score Policy Tier" dataset from ctx.datasets
#   2. Find the row where coverage_type + average_attract_score is between score_range_low and score_range_high
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
#    {
#    "state": "OH",
#    "rate_type": "Policy Tier",
#    "source_file": "oh_policy_tier.csv",
#    "coverage_type": "PIP",
#    "score_range_low": "725",
#    "score_range_high": "772",
#    "driver_score_tier": "Tier 9",
#    "policy_tier_factor": "0",
#    "processed_date_time": "Thu Sep 07 2023 13:24:14 GMT-0400 (Eastern Daylight Time)"
#  },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Driver Score Policy Tier"
DATASET_NAME = "Driver Score Policy Tier"


def _find_policy_tier(
    dataset: list,
    coverage_type: str,
    average_attract_score: int,
) -> Optional[str]:
    
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type
            and float(row.get("score_range_high",0)) >= average_attract_score
            and float(row.get("score_range_low",0)) <= average_attract_score
        ):
            return row.get("policy_tier_factor")
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

def _find(ctx: VehicleRatingContext, coverage_type: str) -> Optional[str]:
    dataset = ctx.get_dataset(DATASET_NAME)
    return _find_policy_tier(dataset, coverage_type, ctx.average_attract_score)

# ── One function per coverage ─────────────────────────────────────────────────

def fetch_policy_tier_liability_rate(ctx: VehicleRatingContext) -> dict:      
    return _make_rate_part(ctx, "policyTierLiabilityFactor", "Liability", _find(ctx,"Liability"))

def fetch_policy_tier_medpay_rate(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "policyTierMedpayFactor", "MedPay", _find(ctx,"MedPay"))

def fetch_policy_tier_pip_rate(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "policyTierPipFactor", "PIP", _find(ctx,"PIP"))


def fetch_policy_tier_collision_rate(ctx: VehicleRatingContext) -> dict:  
    return _make_rate_part(ctx, "policyTierCollisionFactor", "Collision", _find(ctx,"Collision"))
