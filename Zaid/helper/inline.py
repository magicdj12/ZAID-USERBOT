# وارد کردن توابع مورد نیاز
from math import ceil  # برای گرد کردن اعداد به بالا
from traceback import format_exc  # برای فرمت کردن خطاها

# وارد کردن کلاس‌های خطا و انواع دکمه‌های درون خطی از پایروگرام 
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle, 
    InputTextMessageContent,
)

from Zaid import ids as list_users  # لیست کاربران مجاز

looters = None  # متغیر سراسری برای شماره صفحه

def paginate_help(page_number, loaded_modules, prefix):
    """
    تابعی برای صفحه‌بندی راهنمای ماژول‌ها
    
    پارامترها:
    page_number: شماره صفحه فعلی
    loaded_modules: لیست ماژول‌های بارگذاری شده
    prefix: پیشوند برای callback_data
    """
    number_of_rows = 5  # تعداد ردیف‌ها در هر صفحه
    number_of_cols = 3  # تعداد ستون‌ها در هر صفحه
    global looters
    looters = page_number
    
    # فیلتر کردن ماژول‌های قابل نمایش و مرتب‌سازی آنها
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    
    # ساخت دکمه‌ها برای هر ماژول
    modules = [
        InlineKeyboardButton(
            text="{}".format(x),
            callback_data=f"ub_modul_{x}",
        )
        for x in helpable_modules
    ]
    
    # گروه‌بندی دکمه‌ها در ردیف‌ها
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    
    # اضافه کردن دکمه تکی در صورت نیاز
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
        
    # محاسبه تعداد کل صفحات و صفحه فعلی
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    
    # اضافه کردن دکمه‌های ناوبری
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                InlineKeyboardButton(text="✘", callback_data=f"{prefix}_prev({modulo_page})"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close_help"),
                InlineKeyboardButton(text="✘", callback_data=f"{prefix}_next({modulo_page})"),
            )
        ]
    return pairs

def cb_wrapper(func):
    """
    دکوراتور برای مدیریت callback queries
    فقط کاربران مجاز می‌توانند از دکمه‌ها استفاده کنند
    """
    async def wrapper(client, cb):
        users = list_users
        if cb.from_user.id not in users:
            await cb.answer(
                "شما اجازه استفاده ندارید!",
                cache_time=0,
                show_alert=True,
            )
        else:
            try:
                await func(client, cb)
            except MessageNotModified:
                await cb.answer("🤔🧐")
            except Exception:
                print(format_exc())
                await cb.answer(
                    "خطایی رخ داده است. لطفا لاگ‌ها را بررسی کنید!",
                    cache_time=0,
                    show_alert=True,
                )
    return wrapper

def inline_wrapper(func):
    """
    دکوراتور برای مدیریت inline queries
    فقط کاربران مجاز می‌توانند از قابلیت inline استفاده کنند
    """
    async def wrapper(client, inline_query):
        users = list_users
        if inline_query.from_user.id not in users:
            await client.answer_inline_query(
                inline_query.id,
                cache_time=1,
                results=[
                    InlineQueryResultArticle(
                        title="متاسفم، شما نمی‌توانید از این ربات استفاده کنید!",
                        input_message_content=InputTextMessageContent(
                            "شما اجازه دسترسی به این ربات را ندارید"
                        ),
                    )
                ],
            )
        else:
            await func(client, inline_query)
    return wrapper
