from pydantic import BaseModel, ConfigDict, Field


class SalesCreate(BaseModel):
    customer_id: int
    product_id: int
    unit_price: float = Field(gt=0)
    quantity: int = Field(default=1, ge=1)
    status: str | None = None
    sales_officer_id: int | None = None


class SalesUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str | None = None


class SalesOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    sales_officer_id: int | None = None
