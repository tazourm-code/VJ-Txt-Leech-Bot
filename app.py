from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Tech VJ - Bot is Active'

if __name__ == "__main__":
    # পোর্ট সরাসরি ১০০০০ দিন যাতে রেন্ডার খুঁজে পায়
    app.run(host='0.0.0.0', port=10000)
