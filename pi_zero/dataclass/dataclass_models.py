from dataclasses import dataclass, asdict

@dataclass
class SensorData:
    """Dataclass for sensor data."""
    client: str
    brightness: float

    def to_json(self) -> str:
        import json
        return json.dumps(asdict(self))