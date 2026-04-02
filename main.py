@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    msg = await m.reply_text("⚡ **লিঙ্ক প্রসেস করছি...**")
    
    # ফাইলের নাম এবং ইউনিক আইডি
    name = f"video_{int(time.time())}"
    
    # Bunny Net, Vimeo এবং সাধারণ সিকিউরড লিঙ্কের জন্য হেডার সেটআপ
    headers = '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" '
    if "b-cdn.net" in url or "iframe.mediadelivery.net" in url:
        headers += '--referer "https://iframe.mediadelivery.net/" '
    elif "vimeo" in url:
        headers += '--referer "https://vimeo.com/" '
    
    # yt-dlp কমান্ড (৩৬০পি এবং সিকিউরিটি হেডারসহ)
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {headers} "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        if os.path.exists(res_file):
            await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
        else:
            await msg.edit_text("❌ ফাইলটি ডাউনলোড করা যায়নি। লিঙ্কটি চেক করুন।")
            
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")
        
