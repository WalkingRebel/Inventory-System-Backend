from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    purchase_officer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    vendor = relationship("User", foreign_keys=[vendor_id])
    purchase_officer = relationship("User", foreign_keys=[purchase_officer_id])
    product = relationship("Product")
