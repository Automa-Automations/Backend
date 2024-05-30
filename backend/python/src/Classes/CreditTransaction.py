import dataclasses
import datetime
from src.utils import insert_value
import datetime

@dataclasses.dataclass
class CreditTransaction:
    id: str
    created_at: datetime.datetime
    credits: int
    head: str
    metadata: dict[str, str] # This can be for any unstructured data
    user_id: str

    def add(self):
        """Adds an initialized transaction to the database"""
        table = "transactions"
        val = dataclasses.asdict(self)
        val['created_at'] = val['created_at'].isoformat()
        insert_value(table=table, values=val)



