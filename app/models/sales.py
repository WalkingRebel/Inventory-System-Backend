from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class SalesOrder(Base):
    __tablename__ = "sales_order"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    sales_officer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    customer = relationship("User", foreign_keys=[customer_id])
    sales_officer = relationship("User", foreign_keys=[sales_officer_id])
    product = relationship("Product")
