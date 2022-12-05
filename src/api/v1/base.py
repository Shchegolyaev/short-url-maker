import sys
from typing import Optional, Union

from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.entity import UrlDataCreate
from services.entity import url_data_crud

router = APIRouter()


@router.post('/')
async def make_short_url(
        url_obj: UrlDataCreate,
        db: AsyncSession = Depends(get_session)):
    short_url = await url_data_crud.get(db=db, url_obj=url_obj)
    if short_url is None:
        short_url = await url_data_crud.create(db=db, url_obj=url_obj)
    return {"short_url": short_url}



