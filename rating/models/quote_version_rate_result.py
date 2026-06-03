from dataclasses import dataclass, field
from typing import List
from rating.models.vehicle_rate_result import VehicleRatingResult

@dataclass
class QuoteVersionRatingResult:
    quote_version_id: str
    quote_version_name: str

    vehicle_results: List[VehicleRatingResult] = field(default_factory=list)

    total_liability: float = 0
    total_medpay: float = 0
    total_pip: float = 0
    total_umbi: float = 0
    total_uimbi: float = 0
    total_comprehensive: float = 0
    total_collision: float = 0
    total_premium: float = 0