import json
from typing import TYPE_CHECKING
from bclib.context.context import Context
from bclib.utility.dict_ex import DictEx

if TYPE_CHECKING:
    from bclib.dispatcher.idispatcher import IDispatcher


class RabbitContext(Context):
    """Context for rabbit-mq request"""

    def __init__(self, rabbit_message: 'DictEx',  dispatcher: 'IDispatcher'):
        super().__init__(dispatcher)
        self.__rabbit_message: DictEx = rabbit_message
        self.__message = DictEx(json.loads(
            rabbit_message.message)) if rabbit_message.message else None
        self.url = self.__rabbit_message.host

    @property
    def host(self) -> 'str':
        return self.__rabbit_message.host

    @property
    def queue(self) -> 'str':
        return self.__rabbit_message.queue

    @property
    def raw_message(self) -> 'str':
        return self.__rabbit_message.message

    @property
    def message(self) -> 'DictEx':
        return self.__message
