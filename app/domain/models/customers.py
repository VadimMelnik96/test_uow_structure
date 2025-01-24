from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.base import Base


class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    last_name: Mapped[str] = mapped_column(String(500), default="")
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="customer")