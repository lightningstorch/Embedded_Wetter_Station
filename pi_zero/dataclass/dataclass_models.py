from pydantic import BaseModel


class SensorData(BaseModel):
    """Dataclass for sensor data."""
    client: str
    temperature: float
    pressure: float
    light_level: float