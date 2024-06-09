from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from db_config.gino_connect import sess_db
from model.request.campaign import CampaignReq
from cqrs.campaign.commands.update_handlers import UpdateCampaignCommandHandler
from cqrs.campaign.commands.create_handlers import AddCampaignCommandHandler
from cqrs.campaign.commands.delete_handlers import DeleteCampaignCommandHandler
from cqrs.campaign.query.query_handlers import ListCampaignQueryHandler, RecordCampaignQueryHandler
from cqrs.campaign.command import CampaignCommand
from cqrs.campaign.queries import CampaignListQuery, CampaignRecordQuery
from secure.jwt import get_current_user, get_user_id
router = APIRouter(dependencies=[Depends(sess_db)])


@router.post("/campaign/add", tags = ['Campaign'])
async def add_campaign(req: CampaignReq, current_user: dict = Depends(get_current_user)): 
    handler = AddCampaignCommandHandler()
    campaign_profile = dict()
    campaign_profile["title"] = req.title
    campaign_profile["description"] = req.description
    campaign_profile["goal_amount"] = req.goal_amount
    campaign_profile["raised_amount"] = req.raised_amount
    campaign_profile["start_date"] = req.start_date
    campaign_profile["end_date"] = req.end_date
    campaign_profile["category"] = req.category
    campaign_profile["media"] = req.media
    campaign_profile["status"] = req.status
    campaign_profile["user_id"] = get_user_id(current_user["username"])
    command = CampaignCommand()
    command.details = campaign_profile
    result = await handler.handle(command)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'Create campaign profile problem encountered'}, status_code=500) 

@router.patch("/campaign/update", tags = ['Campaign'])
async def update_campaign(campaign_id: int, req: CampaignReq, current_user: dict = Depends(get_current_user)):
    campaign_dict = req.dict(exclude_unset=True)
    command = CampaignCommand()
    command.details = {'campaign_id': campaign_id, **campaign_dict}
    handler = UpdateCampaignCommandHandler()
    result = await handler.handle(command)
    if result:
        return req
    else:
        return JSONResponse(status_code=500, content="Update campaign profile problem encountered")
    
@router.patch("/campaign/update_raised_amount", tags = ['Campaign'])
async def update_campaign_raised_amount(campaign_id: int, amount: int):
    command = CampaignCommand()
    command.details = {'campaign_id': campaign_id, 'raised_amount': amount}
    handler = UpdateCampaignCommandHandler()
    result = await handler.handle_raised_amount(command)
    if result:
        return {"message": "Raised amount updated successfully"}
    else:
        return JSONResponse(status_code=500, content="Update raised amount error")
    
@router.delete("/campaign/delete", tags = ['Campaign'])
async def delete_campaign(campaign_id: int, current_user: dict = Depends(get_current_user)):
    command = CampaignCommand()
    handler = DeleteCampaignCommandHandler()
    command.details = {'campaign_id' : campaign_id}
    result = await handler.handle(command)
    if result:
        return {"message": "Campaign deleted successfully"}
    else:
        return JSONResponse(status_code=500, content="Delete campaign error")

@router.get("/campaign/list", tags = ['Campaign'])
async def list_campaigns(current_user: dict = Depends(get_current_user)): 
    handler = ListCampaignQueryHandler()
    query:CampaignListQuery = await handler.handle() 
    return query.records

@router.get("/campaign/get_by_user_id", tags = ['Campaign'])
async def get_campaign_by_user_id(current_user: dict = Depends(get_current_user)):
    user_id = get_user_id(current_user["username"])
    handler = RecordCampaignQueryHandler()
    query:CampaignRecordQuery = await handler.handle_by_user_id(user_id) 
    return query.record

# @router.get("/campaign/get_by_title", tags = ['Campaign'])
# async def get_campaign_by_title(title: str, current_user: dict = Depends(get_current_user)):
#     handler = RecordCampaignQueryHandler()
#     query:CampaignRecordQuery = await handler.handle_by_campaign_title(title) 
#     return query.record

@router.get("/campaign/get_by_title", tags = ['Campaign'])
async def get_campaign_by_title(title: str):
    handler = RecordCampaignQueryHandler()
    query:CampaignRecordQuery = await handler.handle_by_campaign_title(title) 
    return query.record

@router.get("/campaign/get_campaign_id_by_title", tags = ['Campaign'])
async def get_campaign_id_by_title(title: str):
    handler = RecordCampaignQueryHandler()
    query:CampaignRecordQuery = await handler.handle_campaign_id_by_title(title) 
    return query.record