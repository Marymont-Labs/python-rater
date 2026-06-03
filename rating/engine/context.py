# engine/context.py

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class RatingContext:
    quote_version: Any
    vehicles: list
    drivers: list

    # intermediate outputs
    vehicle_rate_parts: Dict[int, Dict[str, float]] = field(default_factory=dict)
    policy_rate_parts: Dict[str, float] = field(default_factory=dict)

    # tracing
    trace: List[dict] = field(default_factory=list)