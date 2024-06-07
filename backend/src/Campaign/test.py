from model.data.gino_model import Campaign

async def update_campaign_raised_amount(self, campaign_id: int, amount: int) -> bool:
        try:
            campaign = await Campaign.query.where(Campaign.campaign_id == campaign_id).gino.first()
            if campaign is not None:
                print(f"Current raised_amount: {campaign.raised_amount}, Adding amount: {amount}")
                new_raised_amount = campaign.raised_amount + amount
                return new_raised_amount
            else:
                print(f"No campaign with id '{campaign_id}' found")
                return False
        except Exception as e:
            print(f"Error updating campaign: {e}")
            return False
        
print(update_campaign_raised_amount(4, 1000))