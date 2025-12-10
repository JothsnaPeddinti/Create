from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from typing import Optional,Literal
from enum import Enum 



class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class EmailCreate(BaseModel):
    from_address: str
    to_address: str
    subject: Optional[str]=None
    body:str
    attachment_path: Optional[str] = None
    appname: Optional[str] = None
    feature: Optional[str] = None
    priority: Optional[Priority] = Priority.low

class BulkEmailCreate(BaseModel):
    emails:List[EmailCreate]


class EmailResponse(BaseModel):
    id: int
    from_address:str
    to_address:str
    subject: Optional[str] = None
    body:str
    attachment_path: Optional[str] = None
    appname: Optional[str] = None
    feature: Optional[str] = None
    priority: Priority = Priority.low
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None


    class Config:
        orm_mode=True    