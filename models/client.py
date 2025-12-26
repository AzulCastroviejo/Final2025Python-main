from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from models.base_model import BaseModel
from models.enums import UserRole

class ClientModel(BaseModel):
    __tablename__ = "clients"

    name = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    
    addresses = relationship("AddressModel", back_populates="client", cascade="all, delete-orphan", lazy="select")
    orders = relationship("OrderModel", back_populates="client", lazy="select")
    bills = relationship("BillModel", back_populates="client", lazy="select")  # ✅ Added
