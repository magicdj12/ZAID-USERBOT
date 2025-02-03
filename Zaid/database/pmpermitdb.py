from Zaid.database import cli
import asyncio

# ایجاد کالکشن در دیتابیس برای مدیریت پیام‌های خصوصی
collection = cli["Zaid"]["pmpermit"]

# پیام‌های پیش‌فرض
PMPERMIT_MESSAGE = (
    "**هشدار!⚠️ لطفاً این پیام را با دقت بخوانید..\n\n**"
    "**من ربات کاربری زید هستم و اینجا هستم تا از صاحبم در برابر اسپمرها محافظت کنم.**"
    "**اگر اسپمر نیستید، لطفاً صبر کنید!.\n\n**"
    "**تا آن موقع، اسپم نکنید، وگرنه توسط من بلاک و گزارش خواهید شد، پس در ارسال پیام دقت کنید!**"
)

BLOCKED = "**بیپ بوپ! یک اسپمر پیدا شد! با موفقیت بلاک شد!**"

LIMIT = 5  # محدودیت تعداد پیام‌ها

# توابع مدیریت تنظیمات
async def set_pm(value: bool):
    """فعال/غیرفعال کردن سیستم محافظت پیام خصوصی"""
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": 1})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)

async def set_permit_message(text):
    """تنظیم پیام هشدار"""
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})

async def set_block_message(text):
    """تنظیم پیام بلاک"""
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})

async def set_limit(limit):
    """تنظیم محدودیت تعداد پیام‌ها"""
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})

async def get_pm_settings():
    """دریافت تنظیمات فعلی"""
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message

async def allow_user(chat):
    """اضافه کردن کاربر به لیست مجاز"""
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)

async def get_approved_users():
    """دریافت لیست کاربران مجاز"""
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []

async def deny_user(chat):
    """حذف کاربر از لیست مجاز"""
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})

async def pm_guard():
    """بررسی وضعیت فعال بودن محافظت پیام خصوصی"""
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
