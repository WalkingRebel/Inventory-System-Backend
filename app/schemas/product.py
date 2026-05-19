from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    price: float = Field(gt=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1)
    sku: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
