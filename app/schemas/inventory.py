from pydantic import BaseModel, ConfigDict, Field


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=0, default=0)


class InventoryAdjust(BaseModel):
    delta: int


class InventoryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: int
    quantity: int


class InventoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
