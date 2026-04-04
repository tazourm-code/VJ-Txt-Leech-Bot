# Don't Remove Credit Tg - @VJ_Bots
import os, sys, time, asyncio
import core as helper
from pyromod import listen
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# আপনার ক্রেডেনশিয়ালস
API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Bot is Running'

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\n✅ Shikho + Hulkenstein (EdgeCourse) ফিক্সড।\n✅ লাইভ প্রোগ্রেস বার সচল।\n✅ অটো ৩৬০পি ডাউনলোড হবে।</b>")

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate', '--geo-bypass'
    ]
    
    # ⚡️ All-in-One Referer Logic (Shikho + Hulk + Vimeo)
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        headers.append('--referer "https://iframe.mediadelivery.net/"')
        
    elif "edgecoursebd.com" in url or "player.vimeo.com" in url:
        # এটি Hulkenstein/EdgeCourse ফিক্স করবে
        headers.append('--referer "https://edgecoursebd.com/"')
        
    elif "shikho" in url or "tenbytecdn.com" in url:
        # এটিই শিখোর সেই সমাধান যা আগে আপনার কাজ করত
        headers.append('--referer "https://shikho.com/"')
        headers.append('--add-header "Origin: https://shikho.com"')
        
    elif "vimeo" in url:
        headers.append('--referer "https://vimeo.com/"')
    
    header_str = " ".join(headers)
    
    # ৩৬০পি ডাউনলোড কমান্ড
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {header_str} "{url}" -o "{name}.mp4"'
    
    try:
        # core.py তে ৪টি আর্গুমেন্ট (msg সহ) যাচ্ছে
        res_file = await helper.download_video(url, cmd, name, msg)
        
        if res_file and os.path.exists(res_file):
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            # ৩৬০পি না পেলে বেস্ট কোয়ালিটি ট্রাই করবে
            cmd_alt = f'yt-dlp -f "best" {header_str} "{url}" -o "{name}.mp4"'
            res_file = await helper.download_video(url, cmd_alt, name, msg)
            if res_file and os.path.exists(res_file):
                await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
            else:
                await msg.edit_text("❌ ডাউনলোড ব্যর্থ হয়েছে।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    bot.run()
    
