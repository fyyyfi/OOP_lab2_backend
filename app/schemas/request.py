from datetime import datetime

from pydantic import BaseModel, Field


class RequestBase(BaseModel):
    tenant_name: str = Field(..., min_length=2, max_length=128)
    address: str = Field(..., min_length=2, max_length=255)
    work_type: str = Field(..., min_length=2, max_length=32)
    description: str = ""
    volume_hours: int = Field(1, ge=1, le=1000)
    desired_time: datetime | None = None


class RequestCreate(RequestBase):
    pass


class RequestUpdate(BaseModel):
    tenant_name: str | None = None
    address: str | None = None
    work_type: str | None = None
    description: str | None = None
    volume_hours: int | None = Field(None, ge=1, le=1000)
    desired_time: datetime | None = None
    status: str | None = None


class RequestResponse(RequestBase):
    id: int
    status: str

    model_config = {"from_attributes": True}
