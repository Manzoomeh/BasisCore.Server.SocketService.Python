from typing import Callable
from .no_signaler import NoSignaler
from .signaler import Signaler
from .rabbit_signaler import RabbitSignaller


def create_signaler(options: dict, callback: Callable[[list[str]], None]) -> Signaler:
    ret_val: None
    signaler_type = options["type"] if options and "type" in options else "none"
    if signaler_type == "rabbit":
        ret_val = RabbitSignaller(options, callback)
    elif signaler_type == "none":
        ret_val = NoSignaler()
    else:
        raise Exception(
            f"unknown type for cache signaller('${signaler_type}')")

    return ret_val
