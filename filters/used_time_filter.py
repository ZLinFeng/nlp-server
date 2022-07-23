# coding=utf-8
"""
@file    used_time_filter
@date    2022/7/23 4:47 PM
@author  zlf
"""
import inspect
import time

from starlette.types import Scope, Send, Receive, ASGIApp
from loguru import logger

from utils import app_filter


@app_filter(order=0)
class UsedTimeFilter:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            start_time = int(round(time.time() * 1000))
            await self.app(scope, receive, send)
            end_time = int(round(time.time() * 1000))
            logger.info("From host: {}, Used time: {}ms, Method: {}, Url: {}",
                        scope["client"][0],
                        end_time - start_time,
                        scope["method"],
                        scope["path"])
