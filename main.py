# Don't Remove Credit Tg - @VJ_Bots
import os, sys, time, asyncio
import core as helper
from pyromod import listen
from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from pyrogram.errors import MessageNotModified

# আপনার ক্রেডেনশিয়ালস
API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Bot is Running'

def run_web():
    app.run(host='0.0.0.0', port=10000)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nএটি আপনার প্রিমিয়াম ডাউনলোডার।\n\n✅ সব প্ল্যাটফর্ম আনলকড\n✅ অটো ৩৬০পি ডাউনলোড\n✅ /upload দিয়ে .TXT ফাইল পাঠান।</b>")

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # এরর ফিক্স করার জন্য হেডার এবং কমান্ড সেটআপ
    header_str = '--user-agent "Mozilla/5.0" --no-check-certificate --geo-bypass'
    
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        header_str += ' --referer "https://iframe.mediadelivery.net/"'
    elif "shikho" in url:
        header_str += ' --referer "https://shikho.com/"'

    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {header_str} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            try:
                await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            except MessageNotModified:
                pass
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ লিঙ্কটি কাজ করছে না অথবা ফাইলটি পাওয়া যায়নি।")
    except Exception as e:
        # একই টেক্সট হলে এডিট না করে সরাসরি নতুন মেসেজ বা পাস করার লজিক
        try:
            await msg.edit_text(f"❌ এরর: `{str(e)[:100]}`")
        except MessageNotModified:
            pass

@bot.on_message(filters.command(["upload"]))
async def upload_file(bot, m):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    try:
        input_msg = await bot.listen(editable.chat.id)
        x = await input_msg.download()
        await input_msg.delete(True)
        
        with open(x, "r") as f:
            content = f.read().split("\n")
        links = [i.split("://", 1) for i in content if "://" in i]
        os.remove(x)
        
        await editable.edit(f"**টোটাল লিঙ্ক:** {len(links)}\nপ্রসেসিং শুরু হচ্ছে...")
        
        for i in range(len(links)):
            try:
                n, u = links[i][0].strip(), "https://" + links[i][1].strip()
                out = f"{str(i+1).zfill(3)}) {n}"[:50]
                
                # রিফায়ার লজিক
                ref = '--referer "https://iframe.mediadelivery.net/" ' if "b-cdn.net" in u else ""
                cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {ref} "{u}" -o "{out}.mp4"'
                
                p = await m.reply_text(f"📥 ডাউনলোড হচ্ছে: {n}")
                res = await helper.download_video(u, cmd, out)
                await helper.send_vid(bot, m, f"🎬 **Name:** {n}\n👤 **Owner:** @TG_Classes", res, "no", out, p)
            except:
                continue
    except Exception as e:
        await editable.edit(f"Error: {e}")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.run()
    
