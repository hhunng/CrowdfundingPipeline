from model.data.gino_model import User
from typing import Dict, Any

class SigninRepository:

    async def create_login_user(self, details: Dict[str, Any]) -> bool:
        try:
            await User.create(**details)
            return True
        except Exception as e:
            print(f"Error in logging in: {e}")
            return False