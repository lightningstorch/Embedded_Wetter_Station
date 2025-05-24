from typing import Optional

from pydantic import BaseModel


class SensorData(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    brightness: Optional[float] = None


class ToggleLight(BaseModel):
    client: str
    toggle: bool = True

