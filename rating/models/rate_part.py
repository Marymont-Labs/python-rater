from dataclasses import dataclass
# from uuid import uuid4

@dataclass
class RatePart:
    rate_part_id: str
    rate_part_category: str
    rate_name: str
    rate_category: str
    rating_classification: str
    vehicle_index: int
    value: float