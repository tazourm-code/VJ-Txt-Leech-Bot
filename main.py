# Don't Remove Credit Tg - @VJ_Bots
import os, time, asyncio
import core as helper
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# আপনার ক্রেডেনশিয়ালস (এগুলো ঠিক আছে)
API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

# Render-এর জন্য ওয়েব সার্ভার
app = Flask(__name__)
@app.route('/')
def hello_world(): 
    return 'Bot is Running - Tech VJ'

def run_web(): 
    app.run(host='0.0.0.0', port=10000)

# 'bot' অবজেক্ট ডিফাইন করা হলো যাতে NameError না আসে
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\n✅ Cookies Active!\n✅ সব প্রোটেক্টেড লিঙ্ক এখন আনলক।\n✅ অটো ৩৬০পি ডাউনলোড হবে।</b>")

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি (Cookies সহ)...**")
    name = f"video_{int(time.time())}"
    
    # আপনার দেওয়া cookies.txt ফাইল ব্যবহারের কমান্ড
    cookie_path = "cookies.txt"
    cookie_cmd = f"--cookies {cookie_path}" if os.path.exists(cookie_path) else ""

    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass',
        '--referer "https://player.vimeo.com/"'
    ]
    
    header_str = " ".join(headers)
    
    # ৩৬০পি রেজোলিউশন কমান্ড
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {cookie_cmd} {header_str} --merge-output-format mp4 "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if res_file and os.path.exists(res_file):
            await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
            if os.path.exists(res_file): os.remove(res_file)
        else:
            await msg.edit_text("❌ লিঙ্কটি প্রোটেক্টেড অথবা কাজ করছে না। cookies.txt ফাইলটি চেক করুন।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")

if __name__ == "__main__":
    # ওয়েব সার্ভার এবং বট একসাথে চালু করা
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    bot.run()
