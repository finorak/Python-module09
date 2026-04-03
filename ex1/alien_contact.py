from datetime import datetime
from pydantic import BaseModel, Field, model_validator


try:
    from pydantic import BaseModel
except Exception as e:
    print(e)


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: int
    signale_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    is_verified: bool = Field(default=True)

    @model_validator(mode='after')
    def validate_form(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError("Contact ID must start with 'AC'")
        return self


def main() -> None:
    pass


if __name__ == "__main__":
    main()
