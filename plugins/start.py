#(©)Codeflix_Bots

import logging
import base64
import random
import re
import string
import time
import asyncio

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
)
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_user, del_user, full_userbase, present_user
from shortzy import Shortzy
from config import TIME

SECONDSOP = TIME


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_id = ADMINS  # Fetch the owner's ID from config

    # Check if the user is the owner
    if id == owner_id:
        # Owner-specific actions
        # You can add any additional actions specific to the owner here
        await message.reply("You are the owner! Additional actions can be added here.")

    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except:
                pass

        verify_status = await get_verify_status(id)
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply(f"<b>❗Aapke bot ka verify token expire ho gaya hai.\n\n/start pe click karke new token lo aur apne aap ko verify karo unlimited use ke liye bina kisi error ke.\n\nAgar koi problem ho toh contact karo - @HACKHEISTBOT ❤</b>")
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            if verify_status["link"] == "":
                reply_markup = None
            await message.reply(f"<b>Welcome in our unlimited plan 🥰 !!</b>\n\n<b><blockquote>Ab aap bot ko bina kisi problem ke 30 ghante ke liye unlimited use kar sakte hain.\n\n30 ghante baad, bot ko unlimited use karne ke liye aapko fir se token link open karke verify karna hoga, next 30 ghante ke liye.\n\nDhanyawad 🙏🙏</blockquote><b>\n\n<b>Agar koi samasya ho toh contact kare @HACKHEISTBOT pe</b>", reply_markup=reply_markup, protect_content=False, quote=True)

        elif len(message.text) > 7 and verify_status['is_verified']:
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()
            
            snt_msgs = []
            
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦", url='https://t.me/HIDDEN_OFFICIALS_3/3')]])
                else:
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦", url='https://t.me/HIDDEN_OFFICIALS_3/3')]])

                try:
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                    snt_msgs.append(snt_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    snt_msgs.append(snt_msg)
                except:
                    pass

            if SECONDSOP != 0:
                notification_msg = await message.reply(f"<b>‼️ Watch Fast Lectures and Notes before Deleted after 5 hour.\n\nIf Your Lecture Pdf Deleted Don't worry you again able to access 🥰\n\n Go back from where you got link and again click on link and get Again\n\n𝐒𝐨𝐫𝐫𝐲,𝐅𝐨𝐫 𝐭𝐡𝐢𝐬 𝐍𝐨𝐭 𝐅𝐨𝐫𝐰𝐚𝐫𝐝𝐢𝐧𝐠 𝐨𝐧 𝐚𝐧𝐝 𝐧𝐨𝐭 𝐟𝐨𝐫 𝐚 𝐟𝐮𝐥𝐥 𝐭𝐢𝐦𝐞 𝐛𝐜𝐳 𝐰𝐞 𝐠𝐨𝐭 𝐜𝐨𝐩𝐲𝐫𝐢𝐠𝐡𝐭𝐬 😖😖 🙏</b>")
                await asyncio.sleep(SECONDSOP)
                for snt_msg in snt_msgs:
                    try:
                        await snt_msg.delete()
                    except:
                        pass
                await notification_msg.delete()
                return

        elif verify_status['is_verified']:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton('⚡️ 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠', url='https://t.me/Hidden_officials_3'),
                  InlineKeyboardButton('🍁 𝗬𝗢𝗨𝗧𝗨𝗕𝗘', url='https://youtube.com/@TEAM_OPMASTER')]]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )

        else:
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                short_url = f"api.shareus.io"
                TUT_VID = f"https://t.me/ultroid_official/18"
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("𝗢𝗣𝗘𝗡 𝗩𝗘𝗥𝗜𝗙𝗜𝗬 𝗧𝗢𝗞𝗘𝗡", url=link)],
                    [InlineKeyboardButton('𝐇𝐎𝐖 𝐓𝐎 𝐎𝐏𝐄𝐍 ?', url=TUT_VID)]
                ]
                await message.reply(f"<b>Your Verify Token is Expired 😖,\nOpen new token for again use bot unlimited.\n\n☆NOTE - After {get_exp_time(VERIFY_EXPIRE)} again you have to verify yourself using token\n\n<b><blockquote>What is the Verify token ? 🤔\nIf you pass 1 token url then you are able to use bot unlimited and get any file/video unlimited times in this {get_exp_time(VERIFY_EXPIRE)} time interval</blockquote><b>\n\nSo open Link and use bot 😍\nIf any problem to open link then watch below HOW TO OPEN?? And still you have problem contact @HACKHEISTBOT ❤</b>", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)


WAIT_MSG = "<b>ᴡᴏʀᴋɪɴɢ....</b>"

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟏", url=client.invitelink),
            InlineKeyboardButton(text="𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟐", url=client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '• 𝐍𝐨𝐰 𝐂𝐥𝐢𝐜𝐤 𝐌𝐞',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} ᴜꜱᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪʟʟ ᴡᴀɪᴛ ʙʀᴏᴏ... </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except Exception as e:
                unsuccessful += 1
                logging.error(f"Broadcast Error: {e}")
            total += 1
        
        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴍʏ sᴇɴᴘᴀɪ!!</u>

ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total}</code>
ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ: <code>{blocked}</code>
ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
ᴜɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code></b></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
