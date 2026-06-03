from dataclasses import dataclass, field
from typing import List, Optional
from rating.models.rate_part import RatePart


@dataclass
class VehicleRatingResult:
    vehicle_id: str
    vehicle_index: int

    rate_parts: List[RatePart] = field(default_factory=list)

    liability_premium: Optional[float] = None
    medpay_premium: Optional[float] = None
    pip_premium: Optional[float] = None
    umbi_premium: Optional[float] = None
    uimbi_premium: Optional[float] = None
    comprehensive_premium: Optional[float] = None
    collision_premium: Optional[float] = None