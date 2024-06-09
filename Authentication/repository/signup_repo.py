from model.data.gino_model import User
from typing import Dict, Any, List
from sqlalchemy import func, Sequence
from db_config.gino_connect import db
class SignupRepository:

    async def create_signup_user(self, details: Dict[str, Any]) -> bool:
        try:
            async with db.acquire() as conn:
                seq = Sequence('user_user_id_seq')
                id = await conn.scalar(func.next_value(seq))
                details['user_id'] = id
            await User.create(**details)
            return True
        except Exception as e:
            print(f"Error in signing up user: {e}")
            return False