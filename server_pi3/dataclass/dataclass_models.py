from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeasuredData(BaseModel):
    client: str
    time: datetime
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    brightness: Optional[float] = None


