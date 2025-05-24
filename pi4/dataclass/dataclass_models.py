from pydantic import BaseModel


class SensorData(BaseModel):
    """Dataclass for sensor my_data."""
    client: str
    temperature: float
    humidity: float
    pressure: float