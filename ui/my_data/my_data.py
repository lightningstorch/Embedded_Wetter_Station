from typing import Optional

from pydantic import BaseModel


class SensorData(BaseModel):
    temp: Optional[float] = None
    hum: Optional[float] = None
    brightness: Optional[float] = None
    # camera_frame: Optional[float] = None

