import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "MeetBSD API is Live!"

@app.route('/get-live')
def get_live():
    # Target Website ပြောင်းလိုက်ပြီ
    target_url = "https://www.meetbsd.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        
        # .m3u8 လင့်ခ် သို့မဟုတ် YouTube Live link တွေကို ရှာမယ်
        # (MeetBSD က တစ်ခါတလေ YouTube သုံးတတ်လို့ပါ)
        m3u8_links = re.findall(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', response.text)
        youtube_links = re.findall(r'https?://(?:www\.)?youtube\.com/embed/[^\s"\'<>?]+', response.text)

        if m3u8_links:
            return jsonify({"status": "success", "url": m3u8_links[0]})
        elif youtube_links:
            return jsonify({"status": "success", "type": "youtube", "url": youtube_links[0]})
            
        return jsonify({
            "status": "error", 
            "message": "No live stream detected on meetbsd.com",
            "debug": response.text[:200]
        }), 404
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
