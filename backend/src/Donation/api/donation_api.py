from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from db_config.gino_connect import sess_db
from model.request.donation import DonationReq
from cqrs.donation.commands.create_handlers import AddDonationCommandHandler
from cqrs.donation.query.query_handlers import ListDonationQueryHandler, RecordDonationQueryHandler
from cqrs.donation.command import DonationCommand
from cqrs.donation.queries import DonationListQuery, DonationRecordQuery
from secure.jwt import get_current_user, get_user_id, get_campaign_id, update_raised_amount

router = APIRouter(dependencies=[Depends(sess_db)])

@router.post("/donation/add", tags=['Donation'])
async def add_donation(title: str, req: DonationReq, current_user: dict = Depends(get_current_user)): 
    handler = AddDonationCommandHandler()
    donation_profile = dict()
    donation_profile["campaign_id"] = get_campaign_id(title)
    donation_profile["donator_id"] = get_user_id(current_user["username"])
    donation_profile["donation_amount"] = req.donation_amount
    donation_profile["donation_date"] = req.donation_date
    donation_profile["message_leaving"] = req.message_leaving
    command = DonationCommand()
    command.details = donation_profile
    result = await handler.handle(command)
    if result == True:
        update_raised_amount(get_campaign_id(title), donation_profile["donation_amount"]) 
        return req 
    else: 
        return JSONResponse(content={'message':'create donation profile problem encountered'}, status_code=500) 
    
@router.get("/donation/list", tags=['Donation'])
async def list_donations(current_user: dict = Depends(get_current_user)): 
    donator_id = get_user_id(current_user["username"])
    handler = RecordDonationQueryHandler()
    query: DonationRecordQuery = await handler.handle(donator_id)
    return query.record

