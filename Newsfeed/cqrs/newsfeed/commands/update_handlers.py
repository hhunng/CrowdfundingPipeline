from cqrs.handlers import ICommandHandler
from repository.newsfeed_repo import NewsfeedRepository
from cqrs.newsfeed.command import NewsfeedCommand

class UpdateNewsfeedCommandHandler(ICommandHandler): 
    
    def __init__(self): 
        self.repo:NewsfeedRepository = NewsfeedRepository()
        
    async def handle(self, command:NewsfeedCommand) -> bool:
        newsfeed_id = command.details['newsfeed_id']
        details = {key: value for key, value in command.details.items() if key != 'newsfeed_id'}
        result = await self.repo.update_newsfeed(newsfeed_id, details)
        return result