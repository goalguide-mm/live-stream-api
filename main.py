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
    # Target Website
    target_url = "https://m.yuyantv.cn/"
    
    # Browser အစစ်ကနေ ဝင်သလိုမျိုး Header တွေကို အပြည့်အစုံထည့်မယ်
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Session ကိုသုံးပြီး Website ကို ပိုမိုနက်ရှိုင်းအောင် ဖတ်မယ်
        session = requests.Session()
        response = session.get(target_url, headers=headers, timeout=20)
        
        # m3u8 link ကို ရှာဖွေခြင်း (Regex ကို ပိုကျယ်ပြန့်အောင် ထားမယ်)
        # quotes တွေကြားထဲက .m3u8 ပါတဲ့ link တွေကို အကုန်ရှာမယ်
        links = re.findall(r'["\'](https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)["\']', response.text)
        
        # ဒုတိယနည်းလမ်း - // နဲ့စတဲ့ link တွေပါ ထပ်ရှာမယ်
        if not links:
            links = re.findall(r'["\'](//[^\s"\'<>]+?\.m3u8[^\s"\'<>]*?)["\']', response.text)
            links = ["https:" + l if l.startswith("//") else l for l in links]

        if links:
            # ပထမဆုံးတွေ့တဲ့ link ကို ယူမယ်
            return jsonify({
                "status": "success", 
                "url": links[0],
                "all_links": links # တွေ့သမျှ link အကုန်လုံးကိုလည်း စစ်လို့ရအောင် ပြပေးမယ်
            })
            
        return jsonify({
            "status": "error", 
            "message": "No live link found",
            "debug_info": response.text[:200] # Website ဘာစာသားပြန်ပေးလဲဆိုတာ သိရအောင် (စစ်ဆေးဖို့)
        }), 404
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
