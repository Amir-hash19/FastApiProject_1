# app/core/i18n.py
import gettext
import os
from fastapi import Request

# مسیر فایل‌های ترجمه
LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "locales")

# زبان پیش‌فرض
DEFAULT_LANG = "en"

# زبان‌های پشتیبانی‌شده
SUPPORTED_LANGS = ["en", "fa"]

def get_language_from_request(request: Request) -> str:
    """
    تشخیص زبان از QueryParam یا Header
    """
    lang = request.query_params.get("lang")
    if not lang:
        lang = request.headers.get("Accept-Language", DEFAULT_LANG)
    lang = lang.split(",")[0].lower().strip()
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    return lang

def get_translator(lang: str):
    """
    برگرداندن شیء gettext برای زبان انتخاب‌شده
    """
    try:
        translator = gettext.translation(
            "messages", localedir=LOCALES_DIR, languages=[lang]
        )
        translator.install()
        _ = translator.gettext
    except FileNotFoundError:
        gettext.install("messages", localedir=LOCALES_DIR)
        _ = gettext.gettext
    return _

async def get_text_function(request: Request):
    """
    Dependency برای FastAPI جهت فراهم کردن تابع ترجمه
    """
    lang = get_language_from_request(request)
    _ = get_translator(lang)
    return _
