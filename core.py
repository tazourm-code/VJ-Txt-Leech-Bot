# Don't Remove Credit Tg - @VJ_Bots
import os
import time
import datetime
import aiohttp
import aiofiles
import asyncio
import logging
import requests
import tgcrypto
import subprocess
import concurrent.futures
import re

from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message

# ভিডিওর ডিউরেশন বের করার ফাংশন
def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# আপনার অরিজিনাল ফাংশনগুলো (সেম রাখা হয়েছে)
def exec(cmd):
    process = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = process.stdout.decode()
    print(output)
    return output

def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        print("Waiting for tasks to complete")
        fut = executor.map(exec,cmds)

async def aio(url,name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k

# আপনার স্ক্রিনশটের মতো প্রোগ্রেস বার জেনারেটর
def get_prog_bar(percent):
    done = int(percent / 5)
    return f"[{'█' * done}{'▒' * (20 - done)}]"

# ডাউনলোড ফাংশন (লাইভ প্রোগ্রেস বার আপডেট সহ)
async def download_video(url, cmd, name, m: Message):
    # 'subprocess.run' এর বদলে 'asyncio subprocess' ব্যবহার করা হয়েছে যা আটকে থাকবে না
    process = await asyncio.create_subprocess_shell(
        f"{cmd} --newline",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    last_edit = 0
    while True:
        line = await process.stdout.readline()
        if not line: break
        
        output = line.decode().strip()
        # আপনার স্ক্রিনশটের মতো ডাটা পার্স করা হচ্ছে
        match = re.search(r"(\d+\.\d+)% of\s+([\d\.]+\w+) at\s+([\d\.]+\w+/s) ETA\s+([\d:]+)", output)
        
        if match and (time.time() - last_edit) > 4:
            percent = float(match.group(1))
            bar = get_prog_bar(percent)
            status = (f"**Status: DOWNLOADING...**\n\n"
                      f"{bar} {percent}%\n"
                      f"**⚙️ Process:** {match.group(2)}\n"
                      f"**⚡️ Speed:** {match.group(3)}\n"
                      f"**⌛️ ETA:** {match.group(4)}")
            try:
                await m.edit_text(status)
                last_edit = time.time()
            except: pass

    await process.wait()
    
    # ফাইল খোঁজার লজিক (আপনার আগের কোড অনুযায়ী)
    for ext in ['mp4', 'mkv', 'webm']:
        if os.path.isfile(f"{name}.{ext}"):
            return f"{name}.{ext}"
    return name if os.path.isfile(name) else None

# ভিডিও পাঠানোর ফাংশন (আপলোড প্রোগ্রেস সহ)
async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    # থাম্বনেইল তৈরি
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    
    thumbnail = f"{filename}.jpg" if thumb == "no" else thumb
    dur = int(duration(filename))
    start_time = time.time()

    try:
        # আপলোডের সময় 'utils.progress_bar' কাজ করবে
        await m.reply_video(filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply, start_time))
    except Exception:
        await m.reply_document(filename, caption=cc, progress=progress_bar, progress_args=(reply, start_time))
    
    # ক্লিনআপ
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(f"{filename}.jpg"): os.remove(f"{filename}.jpg")
    await reply.delete(True)
    
