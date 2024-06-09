from cqrs.handlers import IQueryHandler
from repository.newsfeed_repo import NewsfeedRepository
from cqrs.newsfeed.queries import NewsfeedListQuery, NewsfeedRecordQuery

class ListNewsfeedQueryHandler(IQueryHandler): 
    def __init__(self): 
        self.repo:NewsfeedRepository = NewsfeedRepository()
        self.query:NewsfeedListQuery = NewsfeedListQuery()
        
    async def handle(self) -> NewsfeedListQuery:
        data = await self.repo.get_all_newsfeed()
        self.query.records = data
        return self.query
    

class RecordNewsfeedQueryHandler(IQueryHandler): 
    def __init__(self): 
        self.repo:NewsfeedRepository = NewsfeedRepository()
        self.query:NewsfeedRecordQuery = NewsfeedRecordQuery()
    
    async def handle_by_author_id(self, author_id) -> NewsfeedListQuery:
        data = await self.repo.get_newsfeed_by_author_id(author_id)
        self.query.record = data
        return self.query