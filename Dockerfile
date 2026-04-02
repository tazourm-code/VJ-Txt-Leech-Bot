# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

FROM python:3.10-slim

# প্রয়োজনীয় সিস্টেম প্যাকেজ ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# ডিরেক্টরি সেটআপ
WORKDIR /app
COPY . .

# লাইব্রেরি ইনস্টল
RUN pip install --no-cache-dir -r requirements.txt

# বট রান করার কমান্ড
CMD ["sh", "-c", "gunicorn app:app & python3 main.py"]
