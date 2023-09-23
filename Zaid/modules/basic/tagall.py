from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message


from Zaid.modules.help import add_command_help

spam_chats = []

TAGMES = [ " **चलो एक पार्टी करते हैं 🥳🥳** ",
                     " **आप ग्रुप में बात क्यों नहीं करते 😒😒** ",
                     " **खुश रहो✌️🙂** ",
                     " **माँ ने मुझे डाँटा 🥲** ",
                     " **आप कल कहाँ गए थे? 🤔** ",
                     " **क्या चल रहा है इन दिनों 😌❤️🥀** ",
                     " **नमस्ते 👀** ",
                     " **हम मित्र हो सकते हैं ?** ",
                     " **आप कॉलेज या स्कूल में हैं** ",
                     " **गलत मत कहो 🙊** ",
                     " **मुझे देखो 😒❤️👀** ",
                     " **आज क्यों खफा हो...? 😒** ",
                     " **नमस्ते 😈** ",
                     " **मुझे अपने ग्रुप में शामिल करें मैं सभी को टैग कर दूंगी ❤️** ",
                     " **क्या आप मेरे दोस्त हैं 😒😒** ",
                    " **कल मज़ा आया 🥳🥳** ",
                    " **आपने भोजन कर लिया 😚** ",
                    " **बहुत तेज़ जा रहे हो 😏😏** ",
                    " **मैं कल खरीदारी के लिए जाना चाहती हूँ 💞** ",
                    " **क्या आप रिश्ते में हैं? 👀** ",
                    " **और कैदी कैसा है 👀** ",
                    " **क्या आप मुझे कभी याद करते हो 🥺🥺** ",
                    " **मुझे भूल गए 🥺🥀** ",
                    " **आज मैंने बंदर देखा 😌👉🐒** ",
                    " **बात करो यार ❤️👀** ",
                    " **वॉयस चैट पर आइए** ",
                    " **वॉयस चैट पर लडाई हो रही 🤯🤯** ",
                    " **मुझे कभी याद नहीं करते 💔💔** ",
                    " **हाँ 👀** ",
                    " **दोस्त आप कहां हैं ❤️💫** ",
                    " **मुझे अपने ग्रुप में जोड़ें 🥺** ",
                    " **यहाँ आओ @TKS_JOIN 👀** ",
                    " **आप सो गए क्या 🤔🤔** ",
                    " **नमस्ते जी 💞** ",
                    " **अगर आपके जैसा दोस्त है तो इसमें चिंता की क्या बात है?❣️** ",
                    " **कितने खामोश हो यार 😒** ",
                    " **आप गाना जानते हैं 👀** ",
                    " **शांत हो जाओ हर कोई** ",
                    " **हाय 👀** ",
                    " **आप के घर में सब कैसे हैं 😌❤️🥀** ",
                    " **उठो भी 😶** ",
                    " **आप कब से हैं 🧐** ",
                    " **मैंने #𝗔𝗽𝗻𝗲 ख्वाहिशो😇 को दिवार 𝗠𝗮𝗶𝗻 चुनवा दिया, खामखाँ #𝗭𝗶𝗻𝗱𝗲𝗴𝗶 में अनारकली💃बनके नाच रही थी** ",
                    " **नींदे उडा रख्खी है #𝗠𝗘𝗥𝗜 किसी ने.... ये कहकर की... 𝗧𝗨𝗠👉 मुझे अच्छे लगते 𝗛𝗢..😘😘** ",
                    " **𝗦𝗨𝗡𝗢👂👂👂… तुम👧 ही रख लो अपना बना कर औरों ने तो छोड़ दिया #_𝗧𝗨𝗠𝗛𝗔𝗥𝗔👉 समझकर..!!😔** ",
                    " **नींदे उडा रख्खी है #𝗠𝗘𝗥𝗜 किसी ने.... ये कहकर की... 𝗧𝗨𝗠👉 मुझे अच्छे लगते 𝗛𝗢..😘😘 ** ",
                    " **#_𝗗𝗜𝗟💖 तो हर किसी के पास होता हैँ, लेकिन सब #𝗗𝗜𝗪𝗔𝗟𝗘💑 नहीँ❌ होते…** ",
                    " **#𝗦𝘂𝗻𝗼👂बस #𝗜𝘁𝗻𝗮 है तुमसे👉 कहना हमेशा #𝗠𝗲𝗿𝗲😍 ही होक रहना...** ",
                    " **पहली #𝗠𝗼𝗵𝗮𝗯𝗮𝘁💝 का एहसास है तू, मिट के मिट न पाए वो #_𝗣𝘆𝗮𝗿😍 है तू..** ",
                    " ** मैंने #𝗔𝗽𝗻𝗲 ख्वाहिशो😇 को दिवार 𝗠𝗮𝗶𝗻 चुनवा दिया, खामखाँ #𝗭𝗶𝗻𝗱𝗲𝗴𝗶 में अनारकली💃 बनके नाच रही थी** ",
                    " **आह चाहिए #𝗘𝗸☝ उम्र असर होते तक 𝗞𝗼𝗻 जीता है 𝗧𝗲𝗿𝗶 ज़ुल्फ़👧 के सर होते तक** ",
                    " **𝗔𝗴𝗮𝗿 आप 𝗞𝗵𝘂𝘀😊 होना चाहते हो तो 𝗟𝗶𝗳𝗲 _𝗺𝗮𝗶𝗻 अकेले रहना ज्यादा सही है** ",
                    " **झगड़ा तभी होता है जब #𝗗𝗮𝗿𝗱 होता है,𝗔𝘂𝗿 #दर्द वही होता है जहाँ #𝗣𝘆𝗮𝗿💝 होता है** ",
                    " **#𝗖𝗼𝗺𝗽𝘂𝘁𝗲𝗿 के जैसा  दिमाग था 𝗠𝗲𝗿𝗮….#𝗣𝗮𝗴𝗟𝗶👧 ने  ‎𝗟𝘂𝘃_𝘂_𝗟𝘂𝘃_𝘂 कर के  ‎हैंग कर दिया** ",
                    " **#𝗣𝗮𝗴𝗟𝗶👧  तू #_फ़ेसबुक  की बात करती है,𝗛𝗮𝗺 तो #_𝗢𝗟𝗫  पे भी #𝗟𝗮𝗱𝗸𝗶 सेट  कर लेते है** ",
                    " **#𝗘𝗻𝗴𝗹𝗶𝘀𝗵 की 𝗕𝗼𝗼𝗸 बन गई हो 𝗧𝘂𝗺👉 |पसंद तो आती हो पर #समझ् मे 𝗡𝗮𝗵𝗶✖ 🙂** ",
                    " **#𝗣𝘆𝗮𝗿💏 𝗘𝗸☝ खूबसूरत एहसास है….ये #_𝗹𝗶𝗻𝗲 बिलकुल #𝗕𝗮𝗸𝘄𝗮𝘀😝** "
                    " **𝗔𝗽𝗻𝗶 #इंडिया में सरकार हो या #𝗦𝗵𝗮𝗱𝗶👫,सबको 𝗘𝗸☝ साल में #𝗞𝗵𝘂𝘀 खबरी चाहिए..** ",
                    " **𝗠𝘂𝗷𝗵𝗲 लगता है 🤔बहुत जल्दी घरवाले 𝗠𝘂𝗷𝗵𝗲 🙄#𝗠𝗼𝗯𝗶𝗹𝗲 📲 𝗔𝘂𝗿 𝗰𝗵𝗮𝗿𝗴𝗲𝗿🔌पकड़ा कर, घर से निकाल देंगे** ",
                    " **𝗛𝗮𝗺 तो ऐसी #𝗟𝗮𝗱𝗸𝗶👸 पटायेंगे जो हो सबसे हटके …..जिसे देखते ही #𝗗𝗶𝗟💝 को लगे 𝟰𝟰𝟬 𝘃𝗼𝗹𝘁 के झटके.😂** ",
                    " **𝗝𝗮𝗯 समय ही 𝗪𝗮𝘀𝘁𝗲 करना है तो 😏😂😂😀 #𝗙𝗮𝗰𝗲𝗯𝗼𝗼𝗸 चला के सबसे साथ करू,अकेले के साथ 𝗸𝗶𝘆𝗮 करूँ 😏** ",
                    " **𝗗𝗶𝗻 भर 𝗞𝗶𝘁𝗻𝗮 भी क्यूँ ना घूम लो, सबसे #_हॉट_#𝗟𝗮𝗱𝗸𝗶 तब ही दिखेगी 𝗝𝗮𝗯 घरवाले साथ हो** ",
                    " **#𝗦𝗵𝗮𝘆𝗮𝗿𝗶 लिखने से लड़कियाँ 𝗜𝗺𝗽𝗿𝗲𝘀𝘀 होती है ऐसा सुना है….. चलो इस साल ये भी 𝗧𝗿𝘆 कर के देख लेते है😂😂** ",
         ]

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@Client.on_message(filters.command("tagall", ".") & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**Send me a message or reply to a message!**")
    await message.delete()
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif direp:
                await direp.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command("cancel", ".") & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**It seems there is no tagall here.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Cancelled.**")


add_command_help(
    "tagall",
    [
        [
            "tagall [text/reply ke chat]",
            "Tag all the members one by one",
        ],
        [
            "cancel",
            f"to stop .tagall",
        ],
    ],
)
