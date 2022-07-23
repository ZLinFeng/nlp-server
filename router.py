# coding=utf-8
"""
@file    router
@date    2022/7/21 8:32 PM
@author  zlf
"""
from fastapi import APIRouter
from web.nlp_controller import nlp_router

app_router = APIRouter()

app_router.include_router(nlp_router,
                          prefix="/nlp",
                          tags=["nlp"])
