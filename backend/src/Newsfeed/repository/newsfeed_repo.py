from model.data.gino_model import Newsfeed
from typing import Dict, Any, List
from db_config.gino_connect import db
from sqlalchemy import func, Sequence

class NewsfeedRepository:

    async def create_newsfeed(self, details: Dict[str, Any]) -> bool:
        try:
            async with db.acquire() as conn:
                seq = Sequence('newsfeed_newsfeed_id_seq')
                id = await conn.scalar(func.next_value(seq))
                details['newsfeed_id'] = id
            await Newsfeed.create(**details)
            return True
        except Exception as e:
            print(f"Error creating newsfeed: {e}")
            return False
        
    async def update_newsfeed(self, newsfeed_id: int, details: Dict[str, Any]) -> bool:
        try:
            newsfeed = await Newsfeed.query.where(Newsfeed.newsfeed_id == newsfeed_id).gino.first()
            if newsfeed is not None:
                await newsfeed.update(**details).apply()
                return True
            else:
                print(f"No newsfeed with id '{newsfeed_id}' found")
                return False
        except Exception as e:
            print(f"Error updating newsfeed: {e}")
            return False
        

    async def delete_newsfeed(self, newsfeed_id: int) -> bool:
        try:
            newsfeed = await Newsfeed.query.where(Newsfeed.newsfeed_id == newsfeed_id).gino.first()
            if newsfeed is not None:
                await newsfeed.delete()
                return True
            else:
                print(f"No newsfeed with id '{newsfeed_id}' found")
                return False
        except Exception as e:
            print(f"Error deleting newsfeed: {e}")
            return False
        
    async def get_newsfeed_by_author_id(self, author_id: int):
        try:
            query = await Newsfeed.query.where(Newsfeed.author_id == author_id).gino.all()
            if query is not None:
                return [newsfeed.to_dict() for newsfeed in query]
            else:
                print(f"No newsfeed with author_id '{author_id}' found")
                return None
        except Exception as e:
            print(f"Error retrieving newsfeed: {e}")
            return None
        
        
    async def get_newsfeed_by_category(self, category: str) -> List[Dict[str, Any]]:
        try:
            newsfeeds = await Newsfeed.query.where(Newsfeed.category == category).gino.all()
            return [newsfeed.to_dict() for newsfeed in newsfeeds]
        except Exception as e:
            print(f"Error retrieving newsfeed: {e}")
            return []

    async def get_all_newsfeed(self) -> List[Dict[str, Any]]:
        try:
            query = await Newsfeed.query.gino.all()
            if query is not None:
                return [newsfeed.to_dict() for newsfeed in query]
            else:
                print(f"No newsfeed found")
                return []
        except Exception as e:
            print(f"Error retrieving all newsfeed: {e}")
            return []