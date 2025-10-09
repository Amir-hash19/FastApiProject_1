# app/core/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from core.utils.i18n import get_translator, DEFAULT_LANG, SUPPORTED_LANGS

class LocalizationMiddleware(BaseHTTPMiddleware):
    """
    Middleware برای تشخیص زبان کاربر از Header یا Query
    """

    async def dispatch(self, request: Request, call_next):
        # ۱. بررسی query parameter
        lang = request.query_params.get("lang")

        # ۲. بررسی header (Accept-Language)
        if not lang:
            lang = request.headers.get("Accept-Language", DEFAULT_LANG)

        # تمیزسازی
        lang = lang.split(",")[0].lower().strip()
        if lang not in SUPPORTED_LANGS:
            lang = DEFAULT_LANG

        # ۳. ایجاد translator و اضافه کردن به request.state
        request.state.lang = lang
        request.state._ = get_translator(lang)

        # ادامه روند
        response = await call_next(request)
        response.headers["Content-Language"] = lang
        return response