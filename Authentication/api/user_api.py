from fastapi import APIRouter, Depends
from db_config.gino_connect import sess_db
from cqrs.user.query.query_handlers import RecordUserQueryHandler
from cqrs.user.queries import UserRecordQuery

router = APIRouter(dependencies=[Depends(sess_db)])

@router.get("/get_fullname_by_username", tags=['User'])
async def get_fullname_by_username(username: str):
    handler = RecordUserQueryHandler()
    query:UserRecordQuery = await handler.handle_fullname_by_username(username)
    return query.record