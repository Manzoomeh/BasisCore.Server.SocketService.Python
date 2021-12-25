import json
from typing import Any
from context import Context
from utility import DictEx


class RabbitContext(Context):
    """Context for rabbit-mq request"""

    def __init__(self, rabbit_message: DictEx, options: DictEx):
        super().__init__(options)
        self.__rabbit_message: DictEx = rabbit_message
        self.__message = DictEx(json.loads(
            rabbit_message.message)) if rabbit_message.message else None

    @property
    def host(self) -> str:
        return self.__rabbit_message.host

    @property
    def queue(self) -> str:
        return self.__rabbit_message.queue

    @property
    def raw_message(self) -> str:
        return self.__rabbit_message.message

    @property
    def message(self) -> Any:
        return self.__message

    @property
    def url(self) -> str:
        return self.host