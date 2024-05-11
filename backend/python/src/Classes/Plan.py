import dataclasses
from src.utils import get_value
import datetime

@dataclasses.dataclass
class Plan:
    id: str
    price: float
    base_credits: int
    created_at: datetime.datetime
    name: str
    popularity_score: int
    price_rep: str

    def to_dict(self):
        return dataclasses.asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return Plan(**data)

    @staticmethod
    def from_id(id: str):
        value = get_value(table='plans', line=id.lower())
        return Plan.from_dict(value)
