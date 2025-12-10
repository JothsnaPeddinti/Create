from sqlalchemy import Column, Integer, String, Text ,DateTime, Enum, func
from database import Base
from datetime import datetime
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from schemas import Priority
from database import Base

class PriorityEnum(PyEnum):
    low="low"
    medium="medium"
    high="high"




class Email(Base):
    __tablename__ = "emails"

    id=Column(Integer,primary_key=True,index=True)
    from_address=Column(String,nullable=False)
    to_address=Column(String,nullable=False)
    subject=Column(String,nullable=False)
    body=Column(Text,nullable=False)
    attachment_path=Column(String,nullable=True)
    appname=Column(String,nullable=True)
    feature=Column(String,nullable=True)
    priority = Column(Enum(Priority),default=Priority.low)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=True)

    
    
