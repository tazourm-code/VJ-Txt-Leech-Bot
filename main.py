# এই ফিল্টারটি Vimeo Player এবং সাধারণ লিঙ্ক সব হ্যান্ডেল করবে
@bot.on_message(filters.text & ~filters.command(["start", "stop", "upload", "up"]))
async def direct_download(bot, m):
    url = m.text.strip()
    if not url.startswith("http"): return
    
    msg = await m.reply_text("🔎 **লিঙ্ক চেক করছি...**")
    name = f"video_{int(time.time())}"
    
    # আলটিমেট হেডার সেট (সব ধরণের প্রোটেকশন বাইপাস করতে)
    headers = [
        '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"',
        '--no-check-certificate',
        '--geo-bypass',
        '--referer "https://player.vimeo.com/"' # ডিফল্ট রেফারার হিসেবে রাখা হলো
    ]
    
    # স্পেসিফিক ডোমেইন ভিত্তিক রেফারার লজিক
    if "b-cdn.net" in url or "mediadelivery.net" in url:
        headers.append('--referer "https://iframe.mediadelivery.net/"')
    elif "vimeo.com" in url:
        headers.append('--referer "https://vimeo.com/"')
    elif "shikho" in url:
        headers.append('--referer "https://shikho.com/"')
    
    header_str = " ".join(headers)
    
    # ৩৬০পি রেজোলিউশন এবং ফরম্যাট হ্যান্ডলিং (Vimeo Player এর জন্য [ext=mp4] অনেক সময় ভালো কাজ করে)
    cmd = f'yt-dlp -f "bestvideo[height<=360]+bestaudio/best[height<=360]/best" {header_str} --merge-output-format mp4 "{url}" -o "{name}.mp4"'
    
    try:
        await msg.edit_text("📥 **ডাউনলোড হচ্ছে (360p)...**")
        res_file = await helper.download_video(url, cmd, name)
        
        # যদি helper থেকে ফাইল পাথ ফিরে আসে এবং ফাইলটি হার্ডড্রাইভে থাকে
        if res_file and os.path.exists(res_file):
            await msg.edit_text("✅ **ডাউনলোড শেষ! এখন আপলোড হচ্ছে...**")
            await helper.send_vid(bot, m, f"🎬 **Owner:** @TG_Classes", res_file, "no", name, msg)
            
            # আপলোড শেষে ফাইল ডিলিট করে দেওয়া ভালো (ডিস্ক স্পেস বাঁচাতে)
            if os.path.exists(res_file):
                os.remove(res_file)
        else:
            await msg.edit_text("❌ লিঙ্কটি প্রোটেক্টেড অথবা কাজ করছে না। রেন্ডার রিস্টার্ট দিয়ে আবার দেখুন।")
    except Exception as e:
        await msg.edit_text(f"❌ এরর: `{str(e)[:150]}`")
        
