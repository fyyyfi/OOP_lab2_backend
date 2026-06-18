"""Specialist schemas."""
from pydantic import BaseModel, Field


class SpecialistBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=128)
    specialty: str = Field(..., min_length=2, max_length=32)
    is_available: bool = True


class SpecialistCreate(SpecialistBase):
    pass


class SpecialistUpdate(BaseModel):
    full_name: str | None = None
    specialty: str | None = None
    is_available: bool | None = None


class SpecialistResponse(SpecialistBase):
    id: int

    model_config = {"from_attributes": True}
