from model.data.gino_model import Campaign
from typing import Dict, Any, List
from db_config.gino_connect import db
from sqlalchemy import func, Sequence

class CampaignRepository:

    async def create_campaign(self, details: Dict[str, Any]) -> bool:
        try:
            async with db.acquire() as conn:
                seq = Sequence('campaign_campaign_id_seq')
                id = await conn.scalar(func.next_value(seq))
                details['campaign_id'] = id
            await Campaign.create(**details)
            return True
        except Exception as e:
            print(f"Error creating campaign: {e}")
            return False
        

    async def update_campaign(self, campaign_id: int, details: Dict[str, Any]) -> bool:
        try:
            campaign = await Campaign.query.where(Campaign.campaign_id == campaign_id).gino.first()
            if campaign is not None:
                await campaign.update(**details).apply()
                return True
            else:
                print(f"No campaign with id '{campaign_id}' found")
                return False
        except Exception as e:
            print(f"Error updating campaign: {e}")
            return False
        
    async def delete_campaign(self, campaign_id: int) -> bool:
        try:
            campaign = await Campaign.query.where(Campaign.campaign_id == campaign_id).gino.first()
            if campaign is not None:
                await campaign.delete()
                return True
            else:
                print(f"No campaign with id '{id}' found")
                return False
        except Exception as e:
            print(f"Error deleting campaign: {e}")
            return False

    async def get_all_campaign(self) -> List[Dict[str, Any]]:
        try:
            query = await Campaign.query.gino.all()
            if query is not None:
                return [camapaign.to_dict() for camapaign in query]
            else:
                print(f"No campaign found")
                return []
        except Exception as e:
            print(f"Error retrieving all campaign: {e}")
            return []
        
    async def get_campaign_by_user_id(self, user_id: int):
        try:
            query = await Campaign.query.where(Campaign.user_id == user_id).gino.all()
            if query is not None:
                return [campaign.to_dict() for campaign in query]
            else:
                print(f"No campaign with user_id '{user_id}' found")
                return None
        except Exception as e:
            print(f"Error retrieving campaign: {e}")
            return None
        
    async def get_campaign_by_title(self, title: str):
        try:
            query = await Campaign.query.where(Campaign.title == title).gino.all()
            if query is not None:
                return [campaign.to_dict() for campaign in query]
            else:
                print(f"No campaign with title '{title}' found")
                return None
        except Exception as e:
            print(f"Error retrieving campaign: {e}")
            return None