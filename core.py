import os, time, asyncio, subprocess, re, logging
from pyrogram import Client
from pyrogram.types import Message
from utils import progress_bar

# ডিউরেশন ও অন্যান্য ফাংশন আপনার দেওয়াটাই আছে
def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

# আপনার স্ক্রিনশটের মতো প্রোগ্রেস বার তৈরি করার ফাংশন
def get_progress_bar(percent):
    done = int(percent / 5)
    return f"[{'█' * done}{'▒' * (20 - done)}]"

# ডাউনলোড ফাংশন - যা লাইভ প্রোগ্রেস আপডেট করবে
async def download_video(url, cmd, name, m: Message):
    # yt-dlp থেকে লাইভ ডাটা রিড করার জন্য
    process = await asyncio.create_subprocess_shell(
        f"{cmd} --newline",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    last_edit_time = 0
    while True:
        line = await process.stdout.readline()
        if not line: break
        
        output = line.decode().strip()
        # পার্সেন্টেজ, সাইজ, স্পিড ও ETA রিড করা
        match = re.search(r"(\d+\.\d+)% of\s+([\d\.]+\w+) at\s+([\d\.]+\w+/s) ETA\s+([\d:]+)", output)
        
        if match and (time.time() - last_edit_time) > 4: # প্রতি ৪ সেকেন্ডে আপডেট
            percent = float(match.group(1))
            total_size = match.group(2)
            speed = match.group(3)
            eta = match.group(4)
            bar = get_progress_bar(percent)
            
            status_text = (
                f"**Status: DOWNLOADING...**\n\n"
                f"{bar} {percent}%\n"
                f"**⚙️ Process:** {total_size}\n"
                f"**⚡️ Speed:** {speed}\n"
                f"**⌛️ ETA:** {eta}"
            )
            try:
                await m.edit_text(status_text)
                last_edit_time = time.time()
            except: pass

    await process.wait()
    # ফাইল রিটার্ন লজিক (আপনার কোড অনুযায়ী)
    for ext in ['mp4', 'mkv', 'webm']:
        if os.path.isfile(f"{name}.{ext}"): return f"{name}.{ext}"
    return name

async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    thumbnail = f"{filename}.jpg" if thumb == "no" else thumb
    dur = int(duration(filename))
    start_time = time.time()
    try:
        await m.reply_video(filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply, start_time))
    except:
        await m.reply_document(filename, caption=cc, progress=progress_bar, progress_args=(reply, start_time))
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(f"{filename}.jpg"): os.remove(f"{filename}.jpg")
    await reply.delete(True)
    
