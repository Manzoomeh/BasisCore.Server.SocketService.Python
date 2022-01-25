from abc import ABC
from struct import error
from typing import TYPE_CHECKING, Any
from xml.dom import NotSupportedErr

if TYPE_CHECKING:
    from .. import dispatcher

from bclib.db_manager import SqlDb, SQLiteDb, MongoDb, RabbitConnection, RESTfulConnection
from bclib.utility import DictEx, HttpStatusCodes


class Context(ABC):
    """Base class for dispatching"""

    def __init__(self, dispatcher: 'dispatcher.IDispatcher') -> None:
        super().__init__()
        self.dispatcher = dispatcher
        self.url_segments: DictEx = None
        self.url: str = None
        self.is_adhoc = True

    def open_sql_connection(self, key: str) -> SqlDb:
        return self.dispatcher.db_manager.open_sql_connection(key)

    def open_sqllite_connection(self, key: str) -> SQLiteDb:
        return self.dispatcher.db_manager.open_sqllite_connection(key)

    def open_mongo_connection(self, key: str) -> MongoDb:
        return self.dispatcher.db_manager.open_mongo_connection(key)

    def open_restful_connection(self, key: str) -> RESTfulConnection:
        return self.dispatcher.db_manager.open_restful_connection(key)

    def open_rabbit_connection(self, key: str) -> RabbitConnection:
        return self.dispatcher.db_manager.open_rabbit_connection(key)

    def generate_error_responce(self,  error: error) -> dict:
        """Generate error responce from process result"""
        raise NotSupportedErr(
            'Generating error responce not supported in this type of context')