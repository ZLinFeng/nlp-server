# coding=utf-8
"""
@file    wrapper
@date    2022/7/22 7:03 PM
@author  zlf
"""
import time
from functools import wraps
from fastapi import Request

from loguru import logger


def used_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]
        if request is None:
            logger.warning("Missing Request parameter.")
        start_time = int(round(time.time() * 1000))
        res = await func(*args, **kwargs)
        end_time = int(round(time.time() * 1000))
        logger.info("From host: {}, Used time: {}ms, Method: {}, Url: {}",
                    request.client.host if request is not None else "Missing",
                    end_time - start_time,
                    request.method if request is not None else "Missing",
                    request.url if request is not None else "Missing")
        return res

    import inspect
    sig = inspect.signature(wrapper)
    sig.replace(parameters=[
        *filter(
            lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
            inspect.signature(wrapper).parameters.values()
        )
    ], return_annotation=inspect.signature(func).return_annotation)
    return wrapper
