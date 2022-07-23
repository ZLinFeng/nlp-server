# coding=utf-8
"""
@file    nlp_controller
@date    2022/7/22 5:24 PM
@author  zlf
"""
from fastapi import APIRouter
from pydantic import BaseModel

from service.lang.index import lang_service

nlp_router = APIRouter()


class LangReqeust(BaseModel):
    content: str


class LangResponse(BaseModel):
    lang: str


@nlp_router.post("/lang")
async def detect_lang(body: LangReqeust):
    # res = LangResponse()
    return lang_service.invoke(content=body.content)
