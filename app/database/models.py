from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# SQLAlchemy ORM Table Declaration for User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# SQLAlchemy ORM Table Declaration for Alerts
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False)
    crypto_name = Column(String, nullable=False)
    price_to_alert = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
