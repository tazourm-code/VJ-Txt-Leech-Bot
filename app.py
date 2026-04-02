from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Tech VJ - Bot is Running'

if __name__ == "__main__":
    # রেন্ডারের পোর্ট অটোমেটিক ডিটেক্ট করার জন্য এটি দরকার
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
