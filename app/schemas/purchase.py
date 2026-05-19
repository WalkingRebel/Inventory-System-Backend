from pydantic import BaseModel, ConfigDict, Field


class PurchaseCreate(BaseModel):
    vendor_id: int
    product_id: int
    unit_price: float = Field(gt=0)
    quantity: int = Field(default=1, ge=1)
    status: str | None = None
    purchase_officer_id: int | None = None


class PurchaseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str | None = None


class PurchaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vendor_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    purchase_officer_id: int | None = None
