from sqlalchemy import Column,String,Boolean,DateTime
from database.database import Base
import uuid
from datetime import datetime

class Employee(Base):
    __tablename__ = "EmpDetails"
    
    id = Column(String(50),primary_key=True,default=str(uuid.uuid4()))
    emp_name = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    phone_no = Column(String(50),nullable=False)
    position = Column(String(50),nullable=False)
    u_name = Column(String(50),nullable=False)
    password  = Column(String(70),nullable= False)
    is_active = Column(Boolean,default=True)
    is_delete = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    