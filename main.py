import os, sys, time, asyncio
import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN
from pyromod import listen
from pyrogram import Client, filters

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nবট এখন একদম রেডি!\n\n✅ ডাবল মেসেজ আসা বন্ধ হয়েছে।\n✅ ভিমো ও বানি নেট সাপোর্ট অ্যাড করা হয়েছে।</b>")

# এই ফিল্টারটি ডাবল রেসপন্স হওয়া আটকাবে
@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # পাওয়ারফুল হেডার (সব সাইট বাইপাস করতে)
    headers = '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" --no-check-certificate --geo-bypass '
    
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        headers += '--referer "https://iframe.mediadelivery.net/" '
    elif "vimeo" in url:
        headers += '--referer "https://vimeo.com/" '

    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {headers} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            await msg.edit_text("✅ **আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ লিঙ্কটি কাজ করছে না। পাইথন ভার্সন ৩.১০ নিশ্চিত করুন।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:100]}`")

if __name__ == "__main__":
    bot.run()
    
