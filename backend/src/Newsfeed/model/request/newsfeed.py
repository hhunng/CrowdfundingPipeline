from pydantic import BaseModel
from datetime import date

class NewsfeedReq(BaseModel): 
    headline: str
    summary: str
    media: bytes 
    publish_date: date 
    category: str
    class Config:
        orm_mode = True

