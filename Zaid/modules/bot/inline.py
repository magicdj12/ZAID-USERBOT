import time
import traceback
from sys import version as pyver
import os
import shlex
import textwrap
from typing import Tuple
import asyncio 

from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)

from Zaid import CMD_HELP, StartTime, app
from Zaid.helper.data import Data
from Zaid.helper.inline import inline_wrapper, paginate_help

async def get_readable_time(seconds: int) -> str:
    """تبدیل ثانیه به فرمت قابل خواندن زمان"""
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["ثانیه", "دقیقه", "ساعت", "روز"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


async def alive_function(message: Message, answers):
    """تابع نمایش وضعیت ربات"""
    uptime = await get_readable_time((time.time() - StartTime))
    msg = f"""
<b> — سلام، من فعال هستم.</b>

<b> • کاربر :</b> {message.from_user.mention}
<b> • پلاگین‌ها :</b> <code>{len(CMD_HELP)} ماژول</code>
<b> • نسخه پایتون :</b> <code>{pyver.split()[0]}</code>
<b> • نسخه پایروگرام :</b> <code>{pyrover}</code>
<b> • زمان فعالیت ربات :</b> <code>{uptime}</code>

<b> — نسخه ربات: 2.0</b>
"""
    answers.append(
        InlineQueryResultArticle(
            title="وضعیت",
            description="بررسی وضعیت ربات",
            thumb_url="https://telegra.ph/file/cc0890d0876bc18c19e05.jpg",
            input_message_content=InputTextMessageContent(
                msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("──「 راهنما 」──", callback_data="helper")]]
            ),
        )
    )
    return answers


async def help_function(answers):
    """تابع نمایش راهنمای دستورات"""
    bttn = paginate_help(0, CMD_HELP, "helpme")
    answers.append(
        InlineQueryResultArticle(
            title="راهنما!",
            description="مشاهده لیست دستورات و راهنما",
            thumb_url="https://telegra.ph/file/cc0890d0876bc18c19e05.jpg",
            input_message_content=InputTextMessageContent(
                Data.text_help_menu.format(len(CMD_HELP))
            ),
            reply_markup=InlineKeyboardMarkup(bttn),
        )
    )
    return answers


@app.on_inline_query()
@inline_wrapper
async def inline_query_handler(client: Client, query):
    """مدیریت کننده کوئری‌های inline"""
    try:
        text = query.query.strip().lower()
        string_given = query.query.lower()
        answers = []
        if text.strip() == "":
            return
        elif text.split()[0] == "alive":
            # نمایش وضعیت ربات
            answerss = await alive_function(query, answers)
            await client.answer_inline_query(query.id, results=answerss, cache_time=10)
        elif string_given.startswith("helper"):
            # نمایش منوی راهنما
            answers = await help_function(answers)
            await client.answer_inline_query(query.id, results=answers, cache_time=0)
    except Exception as e:
        e = traceback.format_exc()
        print(e, "InLine")
