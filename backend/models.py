from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, \
    Float, UniqueConstraint


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    phone_number = Column(String)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    seller_id = Column(Integer, ForeignKey("users.id"))


class ProductData(Base):
    __tablename__ = "products_data"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True, index=True)
    month = Column(Date, nullable=False)
    sells = Column(Integer)
    price = Column(Float)

    __table_args__ = (UniqueConstraint('id', 'month',
                                       name='_product_month_uc'), )
