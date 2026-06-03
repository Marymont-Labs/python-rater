from dataclasses import dataclass, field
from typing import List

from rating.models.quote_version import QuoteVersion


@dataclass
class Quote:
    quote_id: str
    quote_name: str

    quote_versions: List[QuoteVersion] = field(default_factory=list)