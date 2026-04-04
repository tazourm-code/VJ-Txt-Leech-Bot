# Don't Remove Credit Tg - @VJ_Bots
import os, time, asyncio, subprocess, re
from pyrogram import Client
from pyrogram.types import Message
from utils import progress_bar

def duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def get_prog_bar(percent):
    done = int(percent / 5)
    return f"{'█' * done}{'░' * (20 - done)}"

# 🎬 Quality detect
def detect_quality(name):
    if "1080" in name: return "1080p"
    if "720" in name: return "720p"
    if "480" in name: return "480p"
    if "360" in name: return "360p"
    return "Auto"

# 🧠 Clean filename
def clean_filename(name):
    return name.replace(".", " ").replace("_", " ")

async def download_video(url, cmd, name, m: Message):

    # 🔴 Initial screen
    try:
        await m.edit_text(
            "**🔴 TG Classes DOWNLOADER**\n\n"
            "🎞️ Buffering stream...\n"
            "Please wait..."
        )
    except:
        pass

    process = await asyncio.create_subprocess_shell(
        f"{cmd} --newline",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    last_edit = 0
    quality = detect_quality(name)
    clean_name = clean_filename(name)

    while True:
        line = await process.stdout.readline()
        if not line:
            break

        out = line.decode().strip()

        percent = None
        size = "—"
        speed = "—"
        eta = "—"

        match = re.search(
            r"(\d+\.\d+)% of\s+([\d\.]+\w+) at\s+([\d\.]+\w+/s) ETA\s+([\d:]+)",
            out
        )

        if match:
            percent = float(match.group(1))
            size = match.group(2)
            speed = match.group(3)
            eta = match.group(4)
        else:
            simple = re.search(r"(\d+\.?\d*)%", out)
            if simple:
                percent = float(simple.group(1))

        if percent is not None and (time.time() - last_edit) > 2:
            bar = get_prog_bar(percent)

            status = (
                f"**🔴 TG Classes DOWNLOADER**\n\n"
                f"🎬 **{clean_name}**\n"
                f"📺 Quality: `{quality}`\n\n"
                f"`{bar}`\n"
                f"**{percent:.1f}% Complete**\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📦 {size}   ⚡ {speed}\n"
                f"⏳ ETA: {eta}\n"
                f"━━━━━━━━━━━━━━━━━━"
            )

            try:
                await m.edit_text(status)
                last_edit = time.time()
            except:
                pass

    await process.wait()

    for ext in ['mp4', 'mkv', 'webm']:
        if os.path.exists(f"{name}.{ext}"):
            return f"{name}.{ext}"

    return name if os.path.exists(name) else None


async def send_vid(bot, m, cc, filename, thumb, name, prog):

    subprocess.run(
        f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"',
        shell=True
    )

    await prog.delete(True)

    clean_name = clean_filename(name)

    reply = await m.reply_text(
        "**🔴 TG Classes UPLOADER**\n\n"
        "📤 Uploading to server...\n"
        f"🎬 `{clean_name}`"
    )

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
            progress_args=(reply, start_time)
        )
    except:
        await m.reply_document(
            filename,
            caption=cc,
            progress=progress_bar,
            progress_args=(reply, start_time)
        )

    if os.path.exists(filename):
        os.remove(filename)

    if os.path.exists(f"{filename}.jpg"):
        os.remove(f"{filename}.jpg")

    await reply.delete(True)
