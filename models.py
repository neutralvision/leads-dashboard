from sqlalchemy import Column, Integer, String, Enum
import enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# DB MODELS
class LeadState(enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"


class Lead(Base):
    __tablename__ = "leads"
    LEAD_ID = Column(Integer, primary_key=True, index=True)
    FIRST_NAME = Column(String, index=True)
    LAST_NAME = Column(String, index=True)
    EMAIL = Column(String, index=True)
    RESUME = Column(String)
    STATE = Column(Enum(LeadState), default=LeadState.PENDING)

# REQUEST MODELS:
