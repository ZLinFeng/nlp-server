# coding=utf-8
"""
@file    main
@date    2022/7/21 8:19 PM
@author  zlf
"""
import inspect
import sys

import uvicorn
from fastapi import FastAPI

from config.settings import global_settings
from router import app_router
import filters
from context import scan_modules

app = FastAPI(title=global_settings.APP_NAME)
app.include_router(app_router)


@app.on_event("startup")
async def init_hook():
    scan_modules(["filters"])  # scan and import
    filter_modules = inspect.getmembers(filters, inspect.ismodule)
    for (_, _module) in filter_modules:
        for (_, _class) in inspect.getmembers(_module, inspect.isclass):
            app.add_middleware(_class)


@app.on_event("shutdown")
async def shutdown_hook():
    pass


if __name__ == '__main__':
    uvicorn.run("main:app",
                port=global_settings.APP_PORT,
                host="0.0.0.0",
                workers=global_settings.APP_WORKERS)
