# Don't Remove Credit Tg - @VJ_Bots
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn flask

# পোর্ট সচল রাখতে সরাসরি ১০০০০ বাইন্ড করা হয়েছে
CMD gunicorn app:app --bind 0.0.0.0:10000 --workers 1 --threads 1 & python3 main.py
