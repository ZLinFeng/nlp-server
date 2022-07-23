# coding=utf-8
"""
@file    nlp_controller
@date    2022/7/22 5:24 PM
@author  zlf
"""
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Request

from web.wrapper import used_time

nlp_router = APIRouter()


class LangReqeust(BaseModel):
    content: str


@nlp_router.post("/lang")
@used_time
async def detect_lang(lang: LangReqeust, request: Request):
    pass
