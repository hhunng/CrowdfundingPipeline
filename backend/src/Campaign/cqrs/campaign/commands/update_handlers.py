from cqrs.handlers import ICommandHandler
from repository.campaign_repo import CampaignRepository
from cqrs.campaign.command import CampaignCommand

class UpdateCampaignCommandHandler(ICommandHandler): 
    
    def __init__(self): 
        self.repo:CampaignRepository = CampaignRepository()
        
    async def handle(self, command:CampaignCommand) -> bool:
        campaign_id = command.details['campaign_id']
        details = {key: value for key, value in command.details.items() if key != 'campaign_id'}
        result = await self.repo.update_campaign(campaign_id, details)
        return result
    
    async def handle_raised_amount(self, command:CampaignCommand) -> bool:
        campaign_id = command.details['campaign_id']
        amount = command.details['raised_amount']
        result = await self.repo.update_campaign_raised_amount(campaign_id, amount)
        return result