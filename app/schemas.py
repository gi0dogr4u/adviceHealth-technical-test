from pydantic import BaseModel, constr, Field


class OwnerCreate(BaseModel):
    name: constr(min_length=1)


class CarCreate(BaseModel):
    color: constr(min_length=1) = Field(..., pattern='^(yellow|blue|gray)$')
    model: constr(min_length=1) = Field(..., pattern='^(hatch|sedan|convertible)$')
    owner_id: int


class OwnerResponse(BaseModel):
    id: int
    name: str


class CarResponse(BaseModel):
    id: int
    color: str
    model: str
    owner_id: int
    owner_name: str
