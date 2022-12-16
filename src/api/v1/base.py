import logging
from typing import Union

from fastapi import APIRouter, Depends, Header, Query, responses
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from core.config import app_settings
from db.db import get_session
from schemas.responses import (DelUrl, RespCheckDb, RespMakeShort,
                               RespRedirect, RespStats)
from schemas.url import UrlDataBase
from services.base import url_data_crud

router = APIRouter()
log = logging.getLogger(__name__)


@router.delete("/{url_id}", response_model=DelUrl,
               description="Mark url as deleted.")
async def get_long_url(url_id: str, db: AsyncSession = Depends(get_session)):
    log.info("Start get_long_url")
    url_obj = await url_data_crud.delete_url_info(db=db, url_id=url_id)
    return DelUrl(deleted=url_obj.deleted)


@router.get("/ping", response_model=RespCheckDb,
            description="Check status database.")
async def ping_to_database(db: AsyncSession = Depends(get_session)):
    log.info("Start ping to database")
    status = await url_data_crud.check_db(db=db)
    return RespCheckDb(status=status)


@router.get("/{url_id}/stats", response_model=RespStats,
            description="Get statistics about url.")
async def get_stats_url(
    url_id: str,
    db: AsyncSession = Depends(get_session),
    offset: Union[int, None] = Query(default=0, ge=0),
    max_result: Union[int, None] = Query(default=10, ge=1, lt=50),
    full_info: bool = False
):
    log.info("Get stats start")
    stats = await url_data_crud.get_stats(
        db=db, url_id=url_id, full_info=full_info, offset=offset,
        max_result=max_result
    )
    return RespStats(stats=stats)


@router.get("/{url_id}", response_model=RespRedirect,
            description="Redirect to long url on short url.")
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


@router.post("/", response_model=RespMakeShort,
             status_code=status.HTTP_201_CREATED,
             description="Create object in service.")
async def make_short_url(url_obj: UrlDataBase,
                         db: AsyncSession = Depends(get_session)):
    log.info("Start make_short_url")
    db_obj = await url_data_crud.get(db=db, url_obj=url_obj)
    if db_obj is None:
        log.info("Not exist obj in database")
        db_obj = await url_data_crud.create(db=db, url_obj=url_obj)
    log.info("Created url obj")
    return RespMakeShort(short_url=f"127.0.0.1:{app_settings.project_port}"
                                   f"/api/v1/{db_obj.url_id}")
