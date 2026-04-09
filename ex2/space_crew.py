from datetime import datetime
from enum import Enum
from typing import List

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except Exception as e:
    print(e)


class Rank(Enum):
    cadet = 1
    officer = 2
    lieutenant = 3
    captain = 4
    commander = 5


try:
    class CrewMember(BaseModel):
        member_id: str = Field(..., min_length=3, max_length=10)
        name: str = Field(..., min_length=2, max_length=50)
        rank: Rank = Field(...)
        age: int = Field(..., ge=18, le=80)
        specialization: str = Field(..., min_length=3, max_length=30)
        years_experience: int = Field(..., ge=0, le=50)
        is_active: bool = Field(default=True)

    class SpaceMission(BaseModel):
        mission_id: str = Field(..., min_length=5, max_length=15)
        mission_name: str = Field(..., min_length=3, max_length=100)
        destination: str = Field(..., min_length=3, max_length=50)
        lunch_date: datetime = Field(...)
        duration_days: int = Field(..., ge=1, le=3650)
        crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
        mission_status: str = Field(default="planned")
        budget_millions: float = Field(..., ge=1.0, le=10000.0)

        @model_validator(mode='after')
        def validate_form(self) -> "SpaceMission":
            commander_captain = False
            if not self.mission_id.startswith("M"):
                raise ValueError("Mission ID must start with 'M'")
            for crew in self.crew:
                if not crew.is_active:
                    raise ValueError("All crew must be active")
                if crew.rank.value in (4, 5):
                    commander_captain = True
                    break
            if self.duration_days > 365:
                if not self.get_experience():
                    raise ValueError("Long missions (> 365 days) need "
                                     "50% experienced crew (5+ years)")
            if not commander_captain:
                raise ValueError("Mission must have at lest "
                                 "one Commander or Captain")
            return self

        def get_experience(self) -> bool:
            exp = 0
            for crew in self.crew:
                if crew.years_experience >= 5:
                    exp += 1
            return exp * 2 >= len(self.crew)

        def get_crew(self) -> None:
            if not self.crew:
                return None
            print("Crew members:")
            for crew in self.crew:
                print(f"- {crew.name} ({crew.rank.name})"
                      " - {crew.specialization}")

except Exception as e:
    print(e)


def main() -> None:
    try:
        crews = [
            CrewMember(
                member_id="M_01", name="Sarah Connor",
                rank=Rank.commander, specialization="Mission Command",
                age=25, years_experience=5
                ),
            CrewMember(
                member_id="M_02", name="Jhon Smith",
                rank=Rank.lieutenant, specialization="Navigation",
                age=25, years_experience=5
                ),
            CrewMember(
                member_id="M_03", name="Alice Johnson",
                rank=Rank.officer, specialization="Engineering",
                age=25, years_experience=5
                )
            ]
        space_mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishement",
                crew=crews, destination="Mars", duration_days=900,
                budget_millions=2500.0, lunch_date=datetime(
                    2024, 5, 6, 12, 30, 15
                    )
                )
        print("=" * 20)
        print("Valid mission created:")
        print(f"Mission: {space_mission.mission_name}")
        print(f"ID: {space_mission.mission_id}")
        print(f"Destination: {space_mission.destination}")
        print(f"Duration: {space_mission.duration_days} days")
        print(f"Budget: ${space_mission.budget_millions}M")
        print(f"Crew size: {len(space_mission.crew)}")
        space_mission.get_crew()
    except ValidationError as e:
        custom_err = e.errors()[0]['msg']
        print(custom_err)
    except Exception as e:
        print("=" * 30)
        print(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
