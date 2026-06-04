# rating/engine/dataset_loader.py
#
# Phase 1 — Dataset Loader.
# Fetches all policy-level S3 lookup tables once per QuoteVersion,
# filtering each dataset down before storing — exactly as the JS does.
#
# JS pattern:
#   fetchLossCostFactors(state, territory, key)
#     → fetch S3 JSON → filter by state + territory → store as dataset
#
# Each fetch_ function here:
#   1. Fetches the raw S3 JSON file by key
#   2. Applies the same filter the JS applies (state, territory, zip, etc.)
#   3. Returns (dataset_name, filtered_data)
#
# All fetches run concurrently via asyncio.gather (mirrors JS Promise.all).

import asyncio
import json
import logging
from typing import Any, Optional, Tuple
import os

from rating.models.quote_version import QuoteVersion
from rating.services.s3_client import s3, BUCKET_NAME

logger = logging.getLogger(__name__)
# Load variables from the .env file


# ── S3 fetch primitive ────────────────────────────────────────────────────────

def _read_s3_json(key: str) -> Any:
    """Blocking S3 fetch. Run via run_in_executor to stay async-safe."""
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return json.loads(response["Body"].read().decode("utf-8"))


async def _fetch(key: Optional[str]) -> Any:
    """Async wrapper around the blocking S3 read."""
    if not key:
        return None
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, _read_s3_json, key)
    except Exception as exc:
        logger.warning("dataset_loader: failed to fetch key=%s — %s", key, exc)
        return None


# ── Per-dataset fetch + filter functions ─────────────────────────────────────
# Each mirrors one JS fetchXxxFactors() function exactly.
# Returns (dataset_name, filtered_data).

async def _fetch_loss_cost(qv: QuoteVersion) -> Tuple[str, Any]:
    """
    JS: fetchLossCostFactors(state, territory, key)
    Filter: state == thisState AND territory_no == thisTerritory
    Sorted by coverage_type (mirrors JS _.sortBy)
    """
    data = await _fetch(qv.loss_cost_key)
    if data:
        data = [
            row for row in data
            if row.get("state") == qv.state_abbreviation
            and row.get("territory_no") == qv.iso_territory_id
        ]
        data = sorted(data, key=lambda r: r.get("coverage_type", ""))
    return "Territory Base Loss Cost", data


async def _fetch_loss_cost_umbi(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchLossCostUMBIFactors(state, key) — filter by state only."""
    data = await _fetch(qv.loss_cost_umbi_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Territory Base Loss Cost UMBI", data


async def _fetch_loss_cost_uimbi(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchLossCostUIMBIFactors(state, key) — filter by state only."""
    data = await _fetch(qv.loss_cost_uimbi_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Territory Base Loss Cost UIMBI", data


async def _fetch_policy_tier(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchPolicyTierFactors(state, key)"""
    data = await _fetch(qv.policy_tier_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Driver Score Policy Tier", data


async def _fetch_named_insured(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchNamedInsuredFactors(state, key)"""
    data = await _fetch(qv.named_insured_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Named Insured", data


async def _fetch_raca(qv: QuoteVersion) -> Tuple[str, Any]:
    """
    JS: fetchRaca_OCP_ENV_Factors(state, zipCode, key)
    Filter: state + zip_code
    """
    data = await _fetch(qv.raca_adjustment_key)
    if data:
        data = [
            r for r in data
            if r.get("state") == qv.state_abbreviation
            and r.get("zip_code") == qv.zip_code 
            # and r.get("rating_classification") = qv.rating_classification
        ]
    return "RACA Adjustment Factor", data


async def _fetch_increased_limits(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchIncreasedLimitsFactor(state, key)"""
    data = await _fetch(qv.increased_limit_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Increased Limit Factor", data


async def _fetch_primary_class(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchPrimaryClassFactors(state, key)"""
    data = await _fetch(qv.primary_class_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Primary Class Factor", data


async def _fetch_naics(qv: QuoteVersion) -> Tuple[str, Any]:
    """
    JS: fetchSecondaryClassNaicsFactors(state, naicsCode, key)
    Filter: state + naics_code
    """
    data = await _fetch(qv.naics_business_class_key)
    if data:
        data = [
            r for r in data
            if r.get("state") == qv.state_abbreviation
            and r.get("naics_code") == qv.naics_code
        ]
    return "Secondary Class and NAICS Factors", data


async def _fetch_fleet(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchFleetFactors(state, key)"""
    data = await _fetch(qv.fleet_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Fleet Factor", data


async def _fetch_age_group(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchAgeGroupFactors(state, key)"""
    data = await _fetch(qv.age_group_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Age Group (Model Year) Factor", data


async def _fetch_ocn(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchOriginalCostNewFactors(state, key)"""
    data = await _fetch(qv.ocn_stated_value_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Original Cost New / Stated Value Factor", data


async def _fetch_liability_deductible(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchLiabilityDeductibleFactors(state, key)"""
    data = await _fetch(qv.liability_deductible_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Liability Deductible Factor", data


async def _fetch_pd_deductible(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchPDDeductibleFactors(state, key)"""
    data = await _fetch(qv.pd_deductible_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "PD Deductible Factor", data


async def _fetch_driver_history(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchDriverHistoryFactors(state, key)"""
    data = await _fetch(qv.driver_history_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Driver History Factor", data


async def _fetch_heavy_dumping(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchTruckloadFactors(state, key)"""
    data = await _fetch(qv.heavy_dumping_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Heavy Dumping Factor", data


async def _fetch_private_passenger(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchPrivatePassengerFactors(state, key)"""
    data = await _fetch(qv.private_passenger_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Private Passenger Factor", data


async def _fetch_discretionary_credit(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchDiscretionaryCreditFactors(state, key)"""
    data = await _fetch(qv.discretionary_credit_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Discretionary Credit Factor", data


async def _fetch_rate_category(qv: QuoteVersion) -> Tuple[str, Any]:
    """JS: fetchRateCategoryFactors(state, key)"""
    data = await _fetch(qv.rate_category_key)
    if data:
        data = [r for r in data if r.get("state") == qv.state_abbreviation]
    return "Rate Category Factor", data


# ── Phase 1 entry point ───────────────────────────────────────────────────────

async def load_datasets(qv: QuoteVersion) -> dict:
    """
    Fetch and filter all lookup datasets for one QuoteVersion.
    Returns dict keyed by dataset name — stored in ctx.datasets.

    All 19 fetches run concurrently (mirrors JS Promise.all).
    """
    tasks = [
        _fetch_loss_cost(qv),
        _fetch_loss_cost_umbi(qv),
        _fetch_loss_cost_uimbi(qv),
        _fetch_policy_tier(qv),
        _fetch_named_insured(qv),
        _fetch_raca(qv),
        _fetch_increased_limits(qv),
        _fetch_primary_class(qv),
        _fetch_naics(qv),
        _fetch_fleet(qv),
        _fetch_age_group(qv),
        _fetch_ocn(qv),
        _fetch_liability_deductible(qv),
        _fetch_pd_deductible(qv),
        _fetch_driver_history(qv),
        _fetch_heavy_dumping(qv),
        _fetch_private_passenger(qv),
        _fetch_discretionary_credit(qv),
        _fetch_rate_category(qv),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    datasets = {}
    for result in results:
        if isinstance(result, Exception):
            logger.warning("dataset_loader: a dataset fetch raised — %s", result)
        else:
            name, data = result
            datasets[name] = data
            logger.debug("dataset_loader: loaded '%s' (%s rows)",
                         name, len(data) if data else 0)

    return datasets