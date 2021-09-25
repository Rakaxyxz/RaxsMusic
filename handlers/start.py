from time import time

from datetime import datetime

from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT

from helpers.filters import command

from pyrogram import Client, filters

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from helpers.decorators import sudo_users_only

START_TIME = datetime.utcnow()

START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()

TIME_DURATION_UNITS = (

    ('week', 60 * 60 * 24 * 7),

    ('day', 60 * 60 * 24),

    ('hour', 60 * 60),

    ('min', 60),

    ('sec', 1)

)

async def _human_time_duration(seconds):

    if seconds == 0:

        return 'inf'

    parts = []

    for unit, div in TIME_DURATION_UNITS:

        amount, seconds = divmod(int(seconds), div)

        if amount > 0:

            parts.append('{} {}{}'

                         .format(amount, unit, "" if amount == 1 else "s"))

    return ', '.join(parts)

@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)

async def start_(client: Client, message: Message):

    await message.reply_text(

        f"""<b>✨ **HAI Welcome ANAK YATIM {message.from_user.first_name}** \n

💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) BOT INI BERFUNGSI ZEBAGAI SARANA MUSIK DI VOICE CHAT GRUP ANDA!**

💡 **Silahkan Lihat untuk Mengikuti Perintah Perintah Untuk menjalankan Bot musik Kami» 📚 Tombol Perintah!**

❔ **Untuk Mengetahui Cara menggunakan bot ini Silahkan Klik» ❓ Perintah dasar button!**

</b>""",

        reply_markup=InlineKeyboardMarkup(

            [ 

                [

                    InlineKeyboardButton(

                        "➕ Tambahkan kami ke Grup Anda➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")

                ],[

                    InlineKeyboardButton(

                        "❓ perintah dasar", callback_data="cbhowtouse")

                ],[

                    InlineKeyboardButton(

                         "📚 perintah", callback_data="cbcmds"

                    ),

                    InlineKeyboardButton(

                        "💝 Donasi", url=f"https://t.me/{OWNER_NAME}")

                ],[

                    InlineKeyboardButton(

                        "👥 Grup Resmi", url=f"https://t.me/{GROUP_SUPPORT}"

                    ),

                    InlineKeyboardButton(

                        "📣 Channel Resmi", url=f"https://t.me/{UPDATES_CHANNEL}")

                ],[

                    InlineKeyboardButton(

                        "🌐 Source Code", url="https://github.com/RakaXyxz/Raxsmusic"

                    )

                ]

            ]

        ),

     disable_web_page_preview=True

    )

@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)

async def start(client: Client, message: Message):

    current_time = datetime.utcnow()

    uptime_sec = (current_time - START_TIME).total_seconds()

    uptime = await _human_time_duration(int(uptime_sec))

    await message.reply_text(

        f"""✅ **bot Menjalankan**\n<b>💠 **uptime:**</b> `{uptime}`""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "✨ Grup", url=f"https://t.me/{GROUP_SUPPORT}"

                    ),

                    InlineKeyboardButton(

                        "📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}"

                    )

                ]

            ]

        )

    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)

async def help(client: Client, message: Message):

    await message.reply_text(

        f"""<b>👋🏻 **Hello Anak Anjing** {message.from_user.mention()}</b>

**Mohon Sebelum Menggunakan Bot Musik Lebih Baik Utamakan baca perintah Perintah Yang ada disini!**

⚡ __Powered by {BOT_NAME} A.I__""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        text="❔ BAGAIMANA MENGGUNAKAN BOT GANTENG INI", callback_data="cbguide"

                    )

                ]

            ]

        ),

    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)

async def help_(client: Client, message: Message):

    await message.reply_text(

        f"""<b>💡 Hallo Anak Anjing {message.from_user.mention} Selamat Datang Di Menu Bantuan babu!</b>

**Hy apakah Menu ini bisa membuka beberapa menu perintah yang tersedia,disetiap menu perintah juga ada penjelasan singkat masing masing perintah**

⚡ __Powered by {BOT_NAME} A.I__""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "📚 Dasar perintah", callback_data="cbbasic"

                    ),

                    InlineKeyboardButton(

                        "📕 Advanced Cmd", callback_data="cbadvanced"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📘 Admin Cmd", callback_data="cbadmin"

                    ),

                    InlineKeyboardButton(

                        "📗 Sudo Cmd", callback_data="cbsudo"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📙 Pemilik Cmd", callback_data="cbowner"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📔 Senang senang Cmd", callback_data="cbfun"

                    )

                ]

            ]

        )

    )

@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)

async def ping_pong(client: Client, message: Message):

    start = time()

    m_reply = await message.reply_text("pinging...")

    delta_ping = time() - start

    await m_reply.edit_text(

        "🤖 `PONG!!`\n"

        f"⚡ `{delta_ping * 1000:.3f} ms`"

    )

@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)

@sudo_users_only

async def get_uptime(client: Client, message: Message):

    current_time = datetime.utcnow()

    uptime_sec = (current_time - START_TIME).total_seconds()

    uptime = await _human_time_duration(int(uptime_sec))

    await message.reply_text(

        "🤖 bot status:\n"

        f"• **uptime:** `{uptime}`\n"

        f"• **start time:** `{START_TIME_ISO}`"

    )
