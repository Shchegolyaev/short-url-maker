import logging
from typing import Union

from fastapi import APIRouter, Depends, Header, responses
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from core.config import PROJECT_PORT
from core.db_availability import check_db_connect
from db.db import get_session
from schemas.url import UrlDataBase
from services.base import url_data_crud

router = APIRouter()
log = logging.getLogger(__name__)


@router.delete("/{url_id}")
async def get_long_url(url_id: str, db: AsyncSession = Depends(get_session)):
    log.info("Start get_long_url")
    url_obj = await url_data_crud.delete_url_info(db=db, url_id=url_id)
    return {"Deleted": f"{url_obj.deleted}"}


@router.get("/ping")
async def ping_to_database():
    log.info("Start ping to database")
    return {"Availability": check_db_connect()}


@router.get("/{url_id}/stats")
async def get_stats_url(
    url_id: str,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    max_result: int = 10,
    full_info: bool = False,
):
    log.info("Get stats start")
    count_red = await url_data_crud.get_stats(
        db=db, url_id=url_id, full_info=full_info, offset=offset,
        max_result=max_result
    )
    return {"res": count_red}


@router.get("/{url_id}")
async def get_long_url(
    url_id: str,
    db: AsyncSession = Depends(get_session),
    user_agent: Union[str, None] = Header(default=None),
):
    log.info("Start get long url")
    url_obj = await url_data_crud.get_by_url_id(url_id=url_id, db=db)
    if not url_obj:
        log.info("Not object in db")
        return responses.Response(
            content="Item not found", status_code=status.HTTP_404_NOT_FOUND
        )
    if url_obj.deleted:
        log.info("Object already deleted")
        return Response(content="Gone", status_code=status.HTTP_410_GONE)
    log.info("Go to redirect url")
    await url_data_crud.add_redirect(url_obj=url_obj, db=db, info=user_agent)
    log.info("End get long url")
    return responses.RedirectResponse(
        url_obj.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def make_short_url(url_obj: UrlDataBase,
                         db: AsyncSession = Depends(get_session)):
    log.info("Start make_short_url")
    db_obj = await url_data_crud.get(db=db, url_obj=url_obj)
    if db_obj is None:
        log.info("Not exist obj in database")
        db_obj = await url_data_crud.create(db=db, url_obj=url_obj)
    log.info("Created url obj")
    return {"short_url": f"127.0.0.1:{PROJECT_PORT}/api/v1/{db_obj.url_id}"}
