from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from db_config.gino_connect import sess_db
from model.request.newsfeed import NewsfeedReq
from cqrs.newsfeed.commands.update_handlers import UpdateNewsfeedCommandHandler
from cqrs.newsfeed.commands.create_handlers import AddNewsfeedCommandHandler
from cqrs.newsfeed.commands.delete_handlers import DeleteNewsfeedCommandHandler
from cqrs.newsfeed.query.query_handlers import ListNewsfeedQueryHandler, RecordNewsfeedQueryHandler
from cqrs.newsfeed.command import NewsfeedCommand
from cqrs.newsfeed.queries import NewsfeedListQuery, NewsfeedRecordQuery
from secure.jwt import get_current_user, get_user_id, get_fullname

router = APIRouter(dependencies=[Depends(sess_db)])


@router.post("/newsfeed/add", tags=['Newsfeed'])
async def add_newsfeed(req: NewsfeedReq, current_user: dict = Depends(get_current_user)): 
    handler = AddNewsfeedCommandHandler()
    newsfeed_profile = dict()
    newsfeed_profile["author"] = get_fullname(current_user["username"])
    newsfeed_profile["headline"] = req.headline
    newsfeed_profile["summary"] = req.summary
    newsfeed_profile["media"] = req.media
    newsfeed_profile["publish_date"] = req.publish_date
    newsfeed_profile["category"] = req.category
    newsfeed_profile["author_id"] = get_user_id(current_user["username"])
    command = NewsfeedCommand()
    command.details = newsfeed_profile
    result = await handler.handle(command)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'create newsfeed problem encountered'}, status_code=500) 

@router.patch("/newsfeed/update", tags=['Newsfeed'])
async def update_newsfeed(newsfeed_id: int, req: NewsfeedReq, current_user: dict = Depends(get_current_user)):
    newsfeed_dict = req.dict(exclude_unset=True)
    command = NewsfeedCommand()
    command.details = {'newsfeed_id': newsfeed_id, **newsfeed_dict}
    handler = UpdateNewsfeedCommandHandler()
    result = await handler.handle(command)
    if result:
        return req
    else:
        return JSONResponse(status_code=500, content="Update newsfeed problem encountered")

@router.delete("/newsfeed/delete", tags=['Newsfeed'])
async def delete_newsfeed(newsfeed_id: int, current_user: dict = Depends(get_current_user)):
    command = NewsfeedCommand()
    handler = DeleteNewsfeedCommandHandler()
    command.details = {'newsfeed_id' : newsfeed_id}
    result = await handler.handle(command)
    if result:
        return {"message": "Newsfeed deleted successfully"}
    else:
        return JSONResponse(status_code=500, content="Delete newsfeed error")

@router.get("/newsfeed/list", tags=['Newsfeed'])
async def list_newsfeeds(current_user: dict = Depends(get_current_user)): 
    handler = ListNewsfeedQueryHandler()
    query:NewsfeedListQuery = await handler.handle() 
    return query.records

@router.get("/newsfeed/list_by_author_id", tags=['Newsfeed'])
async def list_newsfeeds_by_author_id(current_user: dict = Depends(get_current_user)):
    author_id = get_user_id(current_user["username"]) 
    handler = RecordNewsfeedQueryHandler()
    query:NewsfeedRecordQuery = await handler.handle_by_author_id(author_id) 
    return query.record