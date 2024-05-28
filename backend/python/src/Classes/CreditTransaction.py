import dataclasses
import datetime
from src.utils import insert_value

@dataclasses.dataclass
class CreditTransaction:
    id: str
    date: datetime.datetime
    credits: int
    type_: str
    metadata: dict[str, str]
    user_id: str

    def add(self):
        """Adds an initialized transaction to the database"""
        table = "transactions"
        insert_value(table=table, values=dataclasses.asdict(self))