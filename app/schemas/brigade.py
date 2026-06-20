from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.specialist import SpecialistResponse


class BrigadeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    request_id: int
    specialist_ids: list[int] = Field(default_factory=list)
    scheduled_at: datetime | None = None


class BrigadeResponse(BaseModel):
    id: int
    name: str
    request_id: int
    scheduled_at: datetime | None
    status: str
    specialists: list[SpecialistResponse]

    model_config = {"from_attributes": True}
