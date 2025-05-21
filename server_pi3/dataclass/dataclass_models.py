from datetime import datetime

from pydantic import BaseModel


class MeasuredData(BaseModel):
    time: datetime
    temperature: float
    humidity: float
    pressure: float
    light_level: float = None


