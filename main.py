# Don't Remove Credit Tg - @VJ_Bots
import os, sys, time, asyncio
import core as helper
from pyromod import listen
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

app = Flask(__name__)
@app.route('/')
def hello_world(): return 'Bot is Running - Tech VJ'

def run_web(): app.run(host='0.0.0.0', port=10000)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\n✅ লাইভ প্রোগ্রেস বার সচল করা হয়েছে।\n✅ লিঙ্ক পাঠান, অটো ডাউনলোড হবে।</b>")

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass'
    ]
    
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        headers.append('--referer "https://iframe.mediadelivery.net/"')
    
    header_str = " ".join(headers)
    # আপনার অরিজিনাল কমান্ড
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best" {header_str} "{url}" -o "{name}.mp4"'
    
    try:
        # এখানে msg পাঠানো হয়েছে যাতে প্রোগ্রেস বার আপডেট হয়
        res_file = await helper.download_video(url, cmd, name, msg)
        
        if res_file and os.path.exists(res_file):
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ ডাউনলোড ব্যর্থ হয়েছে।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.run()
    
