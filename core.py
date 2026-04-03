import os, time, asyncio, subprocess, re
from pyrogram import Client
from pyrogram.types import Message
from utils import progress_bar

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

# আপনার কাঙ্ক্ষিত বার স্টাইল
def get_prog_bar(percent):
    done = int(percent / 5)
    return f"[{'█' * done}{'▒' * (20 - done)}]"

async def download_video(url, cmd, name, m: Message):
    # yt-dlp এর আউটপুট পড়ার জন্য --newline ব্যবহার করা হয়েছে
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
        # আপনার স্ক্রিনশটের মতো ডাটা (Percentage, Size, Speed, ETA) বের করা
        match = re.search(r"(\d+\.\d+)% of\s+([\d\.]+\w+) at\s+([\d\.]+\w+/s) ETA\s+([\d:]+)", output)
        
        if match and (time.time() - last_edit) > 4:
            percent = float(match.group(1))
            bar = get_prog_bar(percent)
            status = (f"**Status: DOWNLOADING...**\n\n{bar} {percent}%\n"
                      f"**⚙️ Process:** {match.group(2)}\n"
                      f"**⚡️ Speed:** {match.group(3)}\n"
                      f"**⌛️ ETA:** {match.group(4)}")
            try:
                await m.edit_text(status)
                last_edit = time.time()
            except: pass

    await process.wait()
    return f"{name}.mp4" if os.path.exists(f"{name}.mp4") else name

async def send_vid(bot, m, cc, filename, thumb, name, prog):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    thumbnail = f"{filename}.jpg" if thumb == "no" else thumb
    dur = int(duration(filename))
    start_time = time.time()
    try:
        # আপলোডের সময় utils.progress_bar কাজ করবে
        await m.reply_video(filename, caption=cc, supports_streaming=True, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply, start_time))
    except:
        await m.reply_document(filename, caption=cc, progress=progress_bar, progress_args=(reply, start_time))
    if os.path.exists(filename): os.remove(filename)
    if os.path.exists(f"{filename}.jpg"): os.remove(f"{filename}.jpg")
    await reply.delete(True)
    
