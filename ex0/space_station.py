from typing import Optional
from datetime import datetime

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except Exception as e:
    print(e)


try:
    class SpaceStation(BaseModel):
        station_id: str = Field(..., min_length=3, max_length=10)
        name: str = Field(..., min_length=1, max_length=50)
        crew_size: int = Field(..., ge=1, le=20)
        power_level: float = Field(..., ge=0.0, lt=100.0)
        oxygen_level: float = Field(..., ge=0.0, lt=100.0)
        last_maintenance: datetime = Field(...)
        is_operational: bool = Field(default=True)
        notes: Optional[str] = Field(max_length=200)

        @model_validator(mode='after')
        def validate_information(self) -> 'SpaceStation':
            if self.last_maintenance > datetime.now():
                raise ValueError("Last maintenance can't be in the future")
            if self.crew_size > 20 or self.crew_size < 0:
                raise ValueError("Input should be less than or equal to 20")
            if self.power_level > 100 or self.power_level < 0:
                raise ValueError("Power level should be in range of 0 and 100")
            return self
except Exception as e:
    print(e)


def main() -> None:
    print("Space Station Data Validation")
    print("#" * 50)
    try:
        valid = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=20,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2025, 6, 6, 12, 12, 5),
            is_operational=False,
            notes="test")
        operational = 'Operational' if valid.is_operational else 'Malfunction'
        print("Valid sation created:")
        print(f"ID: {valid.station_id}")
        print(f"Name: {valid.name}")
        print(f"Crew: {valid.crew_size} people")
        print(f"Power: {valid.power_level}%")
        print(f"Oxygen: {valid.oxygen_level}%")
        print(f"Status: {operational}")
    except ValidationError as e:
        print("=" * 30)
        custom_err = e.errors()[0]['msg']
        print(custom_err)
    except Exception as e:
        print(e)
        return None
    except NameError as e:
        print(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
