from pydantic import BaseModel
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str
    name: str
    crew_size: int
    power_level: float
    oxygen_level: float
    last_maintenance: datetime
    is_operational: bool = True
    notes: str


def main() -> None:
    valid = SpaceStation(
            station_id="test",
            name="finoana",
            crew_size=5,
            power_level=5.4,
            oxygen_level=6.2,
            last_maintenance="21-06-2024 12:20:20",
            is_operational=False,
            notes="test")
    print(valid.crew_size)


if __name__ == "__main__":
    main()
