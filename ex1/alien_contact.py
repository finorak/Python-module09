from datetime import datetime
from enum import Enum
from typing import Optional

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except Exception as e:
    print(e)


class Contact(Enum):
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


try:
    class AlienContact(BaseModel):
        contact_id: str = Field(..., min_length=5, max_length=15)
        timestamp: datetime = Field(...)
        location: str = Field(..., min_length=3, max_length=100)
        contact_type: Contact = Field(...)
        signale_strength: float = Field(..., ge=0.0, le=10.0)
        duration_minutes: int = Field(..., ge=1, le=1440)
        witness_count: int = Field(..., ge=1, le=100)
        message_recieved: Optional[str] = Field(default="", max_length=500)
        is_verified: bool = Field(default=True)

        @model_validator(mode='after')
        def validate_form(self) -> 'AlienContact':
            if not self.contact_id.startswith('AC'):
                raise ValueError("Contact ID must start with 'AC'")
            if self.signale_strength > 7.0:
                if not self.message_recieved:
                    raise ValueError("Didn't recieve a message")
            if self.contact_type.value == 4:
                if self.witness_count < 3:
                    raise ValueError("Telepathic contact requires "
                                     "at least 3 witnesses")
            return self

except Exception as e:
    print(e)


def main() -> None:
    try:
        alien_contact = AlienContact(
                contact_id="AC-2024_001",
                timestamp=datetime(2025, 5, 5, 12, 45, 30),
                contact_type=Contact.radio,
                location="Area 51, Nevada",
                signale_strength=8.5,
                duration_minutes=45,
                witness_count=5,
                message_recieved="Greetings from Zeta Retucili"
                )
        print("=" * 20)
        print("Valid contact report:")
        print(f"ID: {alien_contact.contact_id}")
        print(f"Type: {alien_contact.contact_type.name}")
        print(f"Location: {alien_contact.location}")
        print(f"Signal: {alien_contact.signale_strength}/10")
        print(f"Duration: {alien_contact.duration_minutes} minutes")
        print(f"Witnesses: {alien_contact.witness_count}")
        print(f"Message: '{alien_contact.message_recieved}'\n")
    except ValidationError as e:
        custom_err = e.errors()[0]['msg']
        print("=" * 20)
        print(custom_err)
        return None
    except Exception as e:
        print("=" * 20)
        print(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
