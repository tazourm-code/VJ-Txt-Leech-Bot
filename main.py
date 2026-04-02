# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, re, sys, json, time, asyncio, requests, subprocess
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nআমি আপনার অটো-ডাউনলোডার বট।\n\n✅ সরাসরি লিঙ্ক দিলে ৩৬০পি-তে ডাউনলোড হবে।\n✅ অথবা /upload কমান্ড দিয়ে .TXT ফাইল পাঠান।</b>")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# সরাসরি লিঙ্ক দিলে অটো ৩৬০পি ডাউনলোড লজিক
@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    msg = await m.reply_text("⚡ **লিঙ্ক প্রসেস করছি...**")
    name = f"video_{int(time.time())}"
    
    # Bunny Net বা Vimeo এর জন্য রেফারার সেটআপ
    ref = ""
    if "b-cdn.net" in url: ref = '--referer "https://iframe.mediadelivery.net/"'
    elif "vimeo" in url: ref = '--referer "https://vimeo.com/"'

    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {ref} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
        await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:100]}`")

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    input_msg: Message = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
       with open(x, "r") as f:
           content = f.read().split("\n")
       links = [i.split("://", 1) for i in content if "://" in i]
       os.remove(x)
    except:
           await m.reply_text("**Invalid file!**")
           return
    
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤:** **{len(links)}**\n\nসবগুলো অটোমেটিক ৩৬০পি-তে ডাউনলোড হচ্ছে...")

    for i in range(len(links)):
        try:
            name1 = links[i][0].strip()
            url = "https://" + links[i][1].strip()
            name = f'{str(i+1).zfill(3)}) {name1}'[:50]

            # অটো ৩৬০পি ফরম্যাট সেটআপ
            ytf = "bestvideo[height<=360]+bestaudio/best[height<=360]/best"
            ref = '--referer "https://iframe.mediadelivery.net/"' if "b-cdn.net" in url else ""
            cmd = f'yt-dlp -f "{ytf}" {ref} "{url}" -o "{name}.mp4"'

            prog = await m.reply_text(f"📥 **ডাউনলোড হচ্ছে:** `{name1}`")
            res_file = await helper.download_video(url, cmd, name)
            await helper.send_vid(bot, m, f"🎬 **Name:** {name1}\n👤 **Owner:** @TG_Classes", res_file, "no", name, prog)
            time.sleep(1)
        except: continue

    await m.reply_text("**𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎**")

bot.run()
    
