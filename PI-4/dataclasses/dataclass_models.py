from pydantic import BaseModel


class SensorData(BaseModel):
    """Dataclass for sensor data."""
    temperature: float
    humidity: float
    pressure: float