# Don't Remove Credit Tg - @VJ_Bots
import os
import time
import datetime
import aiohttp
import asyncio
import logging
import subprocess
import re
from utils import progress_bar
from pyrogram import Client
from pyrogram.types import Message

# ভিডিওর ডিউরেশন বের করার ফাংশন
def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# ইউটিউব-ডিএলপি প্রোগ্রেস পার্স করার ফাংশন
def parse_progress(line):
    # yt-dlp এর আউটপুট থেকে পার্সেন্টেজ, সাইজ, স্পিড এবং ইটিএ বের করা
    pattern = r'(\d+\.\d+)% of\s+([\d\.]+\w+) at\s+([\d\.]+\w+/s) ETA\s+([\d:]+)'
    match = re.search(pattern, line)
    if match:
        return {
            "percent": match.group(1),
            "total": match.group(2),
            "speed": match.group(3),
            "eta": match.group(4)
        }
    return None

# প্রোগ্রেস বার স্টাইল (আপনার স্ক্রিনশটের মতো)
def get_bar(percent):
    done = int(float(percent) / 5)
    return f"[{'█' * done}{'▒' * (20 - done)}]"

# মূল ডাউনলোড ফাংশন (লাইভ প্রোগ্রেস আপডেট সহ)
async def download_video(url, cmd, name, bot, m):
    # cmd থেকে আউটপুট নেওয়ার জন্য newline যোগ করা হয়েছে
    download_cmd = f"{cmd} --newline --no-warnings"
    logging.info(f"Downloading: {name}")
    
    process = await asyncio.create_subprocess_shell(
        download_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    last_update_time = time.time()
    
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        
        line_str = line.decode().strip()
        data = parse_progress(line_str)
        
        # প্রতি ৩ সেকেন্ড পর পর টেলিগ্রামে মেসেজ আপডেট করবে
        if data and time.time() - last_update_time > 3:
            bar = get_bar(data['percent'])
            status_text = (
                f"**Status: DOWNLOADING...**\n\n"
                f"{bar} {data['percent']}%\n"
                f"**⚙️ Process:** {data['total']}\n"
                f"**⚡️ Speed:** {data['speed']}\n"
                f"**⌛️ ETA:** {data['eta']}"
            )
            try:
                await m.edit_text(status_text)
                last_update_time = time.time()
            except:
                pass

    await process.wait()
    
    # ফাইল রিটার্ন করার লজিক
    for ext in ['mp4', 'mkv', 'webm']:
        if os.path.isfile(f"{name}.{ext}"):
            return f"{name}.{ext}"
        if os.path.isfile(f"{name}.mp4.{ext}"):
            return f"{name}.mp4.{ext}"
    return name if os.path.isfile(name) else None

# ভিডিও পাঠানোর ফাংশন
async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    # থাম্বনেইল তৈরি
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:05 -vframes 1 "{filename}.jpg"', shell=True)
    
    await prog.edit_text(f"**Uploading ...** - `{name}`")
    
    thumbnail = f"{filename}.jpg" if thumb == "no" else thumb
    dur = int(duration(filename))
    start_time = time.time()

    try:
        await m.reply_video(
            filename,
            caption=cc,
            supports_streaming=True,
            height=720,
            width=1280,
            thumb=thumbnail,
            duration=dur,
            progress=progress_bar,
            progress_args=(prog, start_time)
        )
    except Exception:
        await m.reply_document(
            filename,
            caption=cc,
            progress=progress_bar,
            progress_args=(prog, start_time)
        )
    
    # ফাইল ডিলিট করা
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(f"{filename}.jpg"): os.remove(f"{filename}.jpg")
    await prog.delete()
    
