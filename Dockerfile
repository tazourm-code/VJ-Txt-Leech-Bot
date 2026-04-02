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

# গানির্কন ছাড়া রান করলে ২ বার মেসেজ আসার সমস্যা থাকবে না
CMD ["python3", "main.py"]
