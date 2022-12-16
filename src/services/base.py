import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.keygen import create_unique_random_key
from models.url_info import Redirect, UrlInfo
from schemas.url import UrlDataBase

log = logging.getLogger(__name__)


class RepositoryDB:

    async def check_db(self, db: AsyncSession):
        status = "Available"
        try:
            statement = select(UrlInfo)
            await db.execute(statement=statement)
            log.info("Database is available")
        except Exception:
            log.info("Database not available")
            status = "Not available"
        return status

    async def delete_url_info(self, db: AsyncSession, url_id: str):
        log.info("Delete url info CRUD start")
        db_obj = await self.get_by_url_id(url_id=url_id, db=db)
        db_obj.deleted = True
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_stats(
        self,
        db: AsyncSession,
        url_id: str,
        full_info: bool,
        offset: int,
        max_result: int,
    ):
        log.info("Get stats CRUD start")
        db_obj = await self.get_by_url_id(db=db, url_id=url_id)
        statement = select(func.count(Redirect.created_at)).where(
            Redirect.url_info_id == db_obj.id
        )
        count_redirects = (await db.execute(statement=statement)).all()
        stats = {"count redirects": count_redirects[0]["count"]}
        if full_info:
            statement = select(Redirect.created_at,
                               Redirect.person_info).where(
                Redirect.url_info_id == db_obj.id
            )
            information = (await db.execute(statement=statement)).all()
            stats["full-info"] = information[offset: offset + max_result]
        return stats

    async def add_redirect(self, db: AsyncSession, url_obj: UrlInfo,
                           info: str):
        log.info("Add redirect CRUD start")
        db_obj = Redirect(person_info=info, url_info_id=url_obj.id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_url_id(self, db: AsyncSession, url_id: str):
        log.info("Get_by_url_id CRUD start")
        statement = select(UrlInfo).where(UrlInfo.url_id == url_id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get(self, db: AsyncSession, url_obj: UrlDataBase):
        log.info("Get CRUD start")
        obj_in_data = jsonable_encoder(url_obj)
        db_obj = UrlInfo(**obj_in_data)
        statement = select(UrlInfo).where(UrlInfo.long_url == db_obj.long_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def create(self, db: AsyncSession, url_obj: UrlDataBase):
        log.info("Create CRUD start")
        db_obj = UrlInfo(url_id=create_unique_random_key(),
                         long_url=url_obj.long_url)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


url_data_crud = RepositoryDB()
