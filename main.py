# Don't Remove Credit Tg - @VJ_Bots
import os, sys, time, asyncio
import core as helper
from pyromod import listen
from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from pyrogram.errors import MessageNotModified, FloodWait

# আপনার আইডিগুলো
API_ID = 32681138
API_HASH = "c809aa4537888310e0f29e49afe13466"
BOT_TOKEN = "8752628916:AAGeJwdqtWIuwZImPK_H6VwEDuJwgdOqTDw"

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Bot is Running - Tech VJ'

def run_web():
    app.run(host='0.0.0.0', port=10000)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# স্টার্ট কমান্ড
@bot.on_message(filters.command(["start"]) & filters.private)
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nএটি আপনার প্রিমিয়াম ডাউনলোডার।\n\n✅ সব প্ল্যাটফর্ম আনলকড\n✅ অটো ৩৬০পি ডাউনলোড\n✅ /upload দিয়ে .TXT ফাইল পাঠান।</b>")

# সরাসরি লিঙ্ক ডাউনলোড (ফিল্টার ঠিক করা হয়েছে যাতে ২ বার না আসে)
@bot.on_message(filters.text & ~filters.command(["start", "upload", "stop"]) & filters.private)
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"):
        return

    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # পাওয়ারফুল হেডার
    headers = '--user-agent "Mozilla/5.0" --no-check-certificate --geo-bypass'
    
    # রিফারার চেক
    if "b-cdn.net" in url or "mediadelivery.net" in url or "tenbytecdn" in url:
        headers += ' --referer "https://iframe.mediadelivery.net/"'
    elif "shikho" in url:
        headers += ' --referer "https://shikho.com/"'

    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {headers} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            try:
                await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            except MessageNotModified: pass
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ লিঙ্কটি প্রোটেক্টেড অথবা কাজ করছে না।")
    except Exception as e:
        try:
            await msg.edit_text(f"❌ এরর: `{str(e)[:100]}`")
        except:
            pass

# ফাইল আপলোড কমান্ড
@bot.on_message(filters.command(["upload"]) & filters.private)
async def upload_file(bot, m):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    try:
        input_msg = await bot.listen(editable.chat.id)
        path = await input_msg.download()
        await input_msg.delete(True)
        
        with open(path, "r") as f:
            content = f.read().split("\n")
        
        links = []
        for line in content:
            if "://" in line:
                links.append(line.strip())
        
        os.remove(path)
        await editable.edit(f"**টোটাল লিঙ্ক:** {len(links)}\nপ্রসেসিং শুরু হচ্ছে...")
        
        for i, link_data in enumerate(links):
            try:
                # নাম ও লিঙ্ক আলাদা করা (যদি থাকে)
                if ":" in link_data and "://" not in link_data.split(":",1)[0]:
                    n, u = link_data.split(":", 1)
                else:
                    n, u = f"Video_{i+1}", link_data
                
                n, u = n.strip(), u.strip()
                out = f"{str(i+1).zfill(3)}) {n}"[:50]
                
                h = '--referer "https://iframe.mediadelivery.net/" ' if "b-cdn.net" in u or "tenbytecdn" in u else ""
                cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {h} "{u}" -o "{out}.mp4"'
                
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
    
