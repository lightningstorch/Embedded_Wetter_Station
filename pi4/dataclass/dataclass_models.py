from pydantic import BaseModel


class SensorData(BaseModel):
    """Dataclass for sensor data."""
    client: str
    temperature: float
    humidity: float
    pressure: float