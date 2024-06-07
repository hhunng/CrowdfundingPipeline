from model.data.gino_model import Donation
from typing import Dict, Any, List
from db_config.gino_connect import db
from sqlalchemy import func, Sequence

class DonationRepository:

    async def create_donation(self, details: Dict[str, Any]) -> bool:
        try:
            async with db.acquire() as conn:
                seq = Sequence('donation_donation_id_seq')
                id = await conn.scalar(func.next_value(seq))
                details['donation_id'] = id
            await Donation.create(**details)
            return True
        except Exception as e:
            print(f"Error creating donation: {e}")
            return False
        
    async def get_donation_by_donator_id(self, donator_id: int):
        try:
            query = await Donation.query.where(Donation.donator_id == donator_id).gino.all()
            if query is not None:
                return [donation.to_dict() for donation in query]
            else:
                print(f"No donation with donator_id '{donator_id}' found")
                return None
        except Exception as e:
            print(f"Error retrieving donation: {e}")
            return None