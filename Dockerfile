# Don't Remove Credit Tg - @VJ_Bots
FROM python:3.10-slim

# প্রয়োজনীয় সিস্টেম প্যাকেজ ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# ডিপেন্ডেন্সি ইনস্টল
RUN pip install --no-cache-dir -r requirements.txt

# পোর্ট এক্সপোজ করা (Render-এর জন্য)
EXPOSE 10000

# গানির্কন এবং মেইন ফাইল একসাথে রান করা
CMD gunicorn app:app --bind 0.0.0.0:10000 & python3 main.py
