# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, sys, time, asyncio, subprocess
import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message

# বট অবজেক্ট ডিফাইন
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nএটি একটি প্রিমিয়াম অল-ইন-ওয়ান ডাউনলোডার।\n\n✅ সাপোর্ট: Bunny Net, Vimeo, YouTube, FB.\n✅ ফিচার: অটো ৩৬০পি এবং হাই-স্পিড ডাউনলোড।\n✅ /upload কমান্ড দিয়ে .TXT ফাইল পাঠান।</b>")

@bot.on_message(filters.command("stop"))
async def stop_handler(_, m):
    await m.reply_text("**বট থামানো হয়েছে!** 🚦")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    msg = await m.reply_text("🔎 **লিঙ্ক যাচাই করছি...**")
    
    name = f"video_{int(time.time())}"
    
    # --- অ্যাডভান্সড হেডার লজিক (যা সব প্ল্যাটফর্ম সাপোর্ট করায়) ---
    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass',
        '--add-header "Accept: */*"',
        '--add-header "Accept-Language: en-US,en;q=0.9"'
    ]
    
    # প্ল্যাটফর্ম চেনা এবং সঠিক Referer সেট করা
    if "b-cdn.net" in url or "mediadelivery.net" in url or "iframe.mediadelivery.net" in url:
        headers.append('--referer "https://iframe.mediadelivery.net/"')
    elif "vimeo" in url:
        headers.append('--referer "https://vimeo.com/"')
    elif "youtube" in url or "youtu.be" in url:
        headers.append('--referer "https://www.youtube.com/"')
    
    header_str = " ".join(headers)
    
    # ৩৬০পি ফরম্যাট এবং সিকিউরিটি হেডারসহ কমান্ড
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {header_str} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ লিঙ্কটি প্রোটেক্টেড অথবা কাজ করছে না।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")

@bot.on_message(filters.command(["upload"]))
async def upload_file(bot, m):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    try:
        input_msg = await bot.listen(editable.chat.id)
        x = await input_msg.download()
        await input_msg.delete(True)
        
        with open(x, "r") as f:
            content = f.read().split("\n")
        
        # খালি লাইন বাদ দিয়ে লিঙ্ক ফিল্টার করা
        links = []
        for line in content:
            if "://" in line:
                parts = line.split("://", 1)
                links.append(parts)
        
        os.remove(x)
        
        await editable.edit(f"**টোটাল লিঙ্ক:** {len(links)}\nসবগুলো অটো ৩৬০পি-তে প্রসেস হচ্ছে...")
        
        for i in range(len(links)):
            try:
                n, u = links[i][0].strip(), "https://" + links[i][1].strip()
                out = f"{str(i+1).zfill(3)}) {n}"[:50]
                
                # লুপের ভেতরেও Bunny Net বাইপাস লজিক
                h = '--referer "https://iframe.mediadelivery.net/" ' if "b-cdn.net" in u or "mediadelivery.net" in u else ""
                cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {h} "{u}" -o "{out}.mp4"'
                
                p = await m.reply_text(f"📥 ডাউনলোড হচ্ছে: {n}")
                res = await helper.download_video(u, cmd, out)
                await helper.send_vid(bot, m, f"🎬 **Name:** {n}\n👤 **Owner:** @TG_Classes", res, "no", out, p)
            except: continue
    except Exception as e:
        await editable.edit(f"Error: {e}")
    
    await m.reply_text("**সব কাজ শেষ! 😎**")

if __name__ == "__main__":
    bot.run()
    
