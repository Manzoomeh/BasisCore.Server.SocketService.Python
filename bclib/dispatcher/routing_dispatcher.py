import asyncio
import inspect

from typing import Callable, Any, Coroutine
from dependency_injector import containers

from bclib.logger.ilogger import ILogger
from bclib.db_manager.db_manager import DbManager
from cache.cache_manager import CacheManager
from bclib.utility import DictEx
from bclib.context.context_factory import ContextFactory
from bclib.listener.message import Message, MessageType
from bclib.dispatcher.dispatcher_helper import DispatcherHelper
from bclib.dispatcher.dispatcher import Dispatcher


class RoutingDispatcher(Dispatcher, DispatcherHelper):

    def __init__(self, container: 'containers.Container', context_factory: 'ContextFactory', options: 'DictEx', cache_manager: 'CacheManager', db_manager: 'DbManager', logger: 'ILogger', loop: 'asyncio.AbstractEventLoop' = None):
        super().__init__(container=container, options=options,
                         cache_manager=cache_manager, db_manager=db_manager, logger=logger, loop=loop)
        self._context_factory = context_factory

    async def _on_message_receive_async(self, message: Message) -> Coroutine:
        """Process received message"""

        try:
            context = await self._context_factory.create_context_async(message, self)
            response = await self.dispatch_async(context)
            await message.set_result_async(response)
        except Exception as ex:
            print(f"Error in process received message {ex}")
            raise ex

    def run_in_background(self, callback: 'Callable|Coroutine', *args: Any) -> asyncio.Future:
        """helper for run function in background thread"""

        if inspect.iscoroutinefunction(callback):
            return self.event_loop.create_task(callback(*args))
        else:
            return self.event_loop.run_in_executor(None, callback, *args)

    async def send_message_async(self, message: MessageType) -> bool:
        """Send message to endpoint"""
        raise NotImplementedError(
            "Send ad-hoc message not support in this type of dispatcher")

    def cache(self, life_time: "int" = 0, key: "str" = None):
        """Cache result of function for seconds of time or until signal by key for clear"""

        return self.cache_manager.cache_decorator(key, life_time)
