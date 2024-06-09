from pydantic import BaseModel
from datetime import date

class DonationReq(BaseModel):
    donation_amount: int
    donation_date: date
    message_leaving: str

    class Config:
        orm_mode = True