from pydantic import BaseModel
from typing import Optional

class AllEmployee(BaseModel):
    emp_name :str
    email : str
    phone_no :str
    position :str
    u_name :str
    password :str
    
    
class emppass(BaseModel):
    password :str
    
class update(BaseModel):
    phone_no :str
    position :str
    
class PartialEmployee(BaseModel):
    
    emp_name: Optional[str] = None
    position: Optional[str] = None
   