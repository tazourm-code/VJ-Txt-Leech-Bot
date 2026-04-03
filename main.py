# Don't Remove Credit Tg - @VJ_Bots
import os, time, asyncio
import core as helper
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# আপনার ক্রেডেনশিয়ালস
API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

app = Flask(__name__)
@app.route('/')
def hello_world(): return 'Bot is Running'

def run_web(): 
    app.run(host='0.0.0.0', port=10000)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\n✅ লাইভ প্রোগ্রেস বার একটিভ করা হয়েছে।\n✅ অটো ৩৬০পি ডাউনলোড হবে।\n✅ প্রোটেক্টেড লিঙ্ক আনলকড।</b>")

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    # শুরুতে মেসেজ পাঠিয়ে সেই অবজেক্টটি স্টোর করা হচ্ছে প্রোগ্রেস আপডেটের জন্য
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # কুকি ফাইল চেক
    cookie_path = "cookies.txt"
    cookie_cmd = f"--cookies {cookie_path}" if os.path.exists(cookie_path) else ""

    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass'
    ]
    
    # সঠিক রেফারার সেটআপ
    if "edgecoursebd.com" in url or "b-cdn.net" in url:
        headers.append('--referer "https://edgecoursebd.com/"')
    else:
        headers.append('--referer "https://player.vimeo.com/"')
    
    header_str = " ".join(headers)
    
    # yt-dlp কমান্ড (৩৬০পি)
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {cookie_cmd} {header_str} --merge-output-format mp4'
    
    try:
        # এখানে 'bot' এবং 'msg' পাঠানো হচ্ছে যাতে core.py লাইভ আপডেট করতে পারে
        res_file = await helper.download_video(url, cmd, name, bot, msg)
        
        if res_file and os.path.exists(res_file):
            # ভিডিও পাঠানোর সময়ও প্রোগ্রেস বার কাজ করবে
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ ডাউনলোড ব্যর্থ হয়েছে। কুকি বা লিঙ্ক চেক করুন।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    bot.run()
        
