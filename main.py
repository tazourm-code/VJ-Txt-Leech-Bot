# Don't Remove Credit Tg - @VJ_Bots
import os, sys, time, asyncio
import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN
from pyromod import listen
from pyrogram import Client, filters

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(f"<b>হ্যালো {m.from_user.mention} 👋\n\nএটি আপনার প্রিমিয়াম ডাউনলোডার।\n\n✅ সব প্ল্যাটফর্ম এখন আনলক করা।\n✅ অটো ৩৬০পি ডাউনলোড হবে।\n✅ /upload দিয়ে .TXT ফাইল পাঠান।</b>")

# এই ফিল্টারটি নিশ্চিত করবে যে ২ বার মেসেজ আসবে না
@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # পাওয়ারফুল হেডার (১৫০০ টাকার বটের সিক্রেট)
    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass'
    ]
    
    # সঠিক Referer সেট করা (যাতে ভিমো বা বানি কাজ করে)
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        headers.append('--referer "https://iframe.mediadelivery.net/"')
    elif "vimeo" in url:
        headers.append('--referer "https://vimeo.com/"')
    elif "shikho" in url:
        headers.append('--referer "https://shikho.com/"')
    
    header_str = " ".join(headers)
    
    # ৩৬০পি রেজোলিউশন লজিক
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {header_str} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ লিঙ্কটি প্রোটেক্টেড। পাইথন ভার্সন ৩.১০ বা কুকি চেক করুন।")
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
        links = [i.split("://", 1) for i in content if "://" in i]
        os.remove(x)
        
        await editable.edit(f"**টোটাল লিঙ্ক:** {len(links)}\nসবগুলো প্রসেস হচ্ছে...")
        
        for i in range(len(links)):
            try:
                n, u = links[i][0].strip(), "https://" + links[i][1].strip()
                out = f"{str(i+1).zfill(3)}) {n}"[:50]
                
                # লুপের ভেতরেও রেফারার লজিক
                h = '--referer "https://iframe.mediadelivery.net/" ' if "b-cdn.net" in u else ""
                cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {h} "{u}" -o "{out}.mp4"'
                
                p = await m.reply_text(f"📥 ডাউনলোড হচ্ছে: {n}")
                res = await helper.download_video(u, cmd, out)
                await helper.send_vid(bot, m, f"🎬 **Name:** {n}\n👤 **Owner:** @TG_Classes", res, "no", out, p)
            except: continue
    except Exception as e:
        await editable.edit(f"Error: {e}")

if __name__ == "__main__":
    bot.run()
    
