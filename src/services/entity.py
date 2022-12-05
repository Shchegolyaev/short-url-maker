from models.url import UrlData as UrlDataModel
from schemas.entity import UrlDataCreate
from .base import RepositoryDB


class RepositoryUrlData(RepositoryDB[UrlDataModel, UrlDataCreate]):
    pass


url_data_crud = RepositoryUrlData(UrlDataModel)
