import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Running Successfully!"

@app.route('/get-live')
def get_live():
    target_url = "https://m.yuyantv.cn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/04.1',
        'Referer': 'https://m.yuyantv.cn/'
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        
        # နည်းလမ်း (၁) - တိုက်ရိုက် m3u8 လင့်ခ်ကို ရှာမယ်
        links = re.findall(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', response.text)
        
        # နည်းလမ်း (၂) - ပုန်းနေတဲ့ link တွေကို ရှာမယ်
        if not links:
            links = re.findall(r'["\'](//[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)["\']', response.text)
            links = ["https:" + l if l.startswith("//") else l for l in links]

        if links:
            # ပထမဆုံးလင့်ခ်ကို ပြန်ပေးမယ်
            return jsonify({"status": "success", "url": links[0]})
            
        return jsonify({
            "status": "error", 
            "message": "Link not found in page source",
            "check_this": response.text[:100] # Debug အတွက် စာသားအနည်းငယ်ပြမယ်
        }), 404
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
