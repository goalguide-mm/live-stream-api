import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
# CORS ကို အားလုံးအတွက် ခွင့်ပြုပေးထားပါတယ်
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "API is Running Successfully!"

@app.route('/get-live')
def get_live():
    # Target Website (yuyantv.cn)
    target_url = "https://m.yuyantv.cn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/04.1',
        'Referer': 'https://m.yuyantv.cn/'
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        response.encoding = 'utf-8' # စာသားတွေ မမှားအောင် encoding သတ်မှတ်ပေးတယ်
        
        # ပိုမိုစုံလင်သော m3u8 ရှာဖွေမှုစနစ် (Regex patterns)
        patterns = [
            r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*',
            r'//[^\s"\'<>]+?\.m3u8'
        ]
        
        found_url = None
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                found_url = match.group(0)
                # လင့်ခ်က // နဲ့စရင် https: ထည့်ပေးမယ်
                if found_url.startswith('//'):
                    found_url = 'https:' + found_url
                break

        if found_url:
            return jsonify({
                "status": "success", 
                "url": found_url,
                "provider": "yuyantv"
            })
            
        return jsonify({"status": "error", "message": "No live link found"}), 404
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render အတွက် Port သတ်မှတ်ချက်
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
