from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeasuredData(BaseModel):
    client: str
    time: datetime
    temperature: float
    pressure: float
    humidity: Optional[float] = None
    light_level: Optional[float] = None


