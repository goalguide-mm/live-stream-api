from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re
import os

app = Flask(__name__)
CORS(app)  # Browser ကနေ လှမ်းခေါ်ရင် Block မဖြစ်အောင် လုပ်ပေးတာပါ

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scrape_live_links():
    target_sites = [
        "https://m.yuyantv.cn/", 
        "https://www.thscore.mobi/",
        "https://www.98sports.com/",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mm.m3u"
    ]
    
    found_links = []
    
    for site in target_sites:
        try:
            # timeout ကို ၅ စက္ကန့်ပဲ ထားပါ (Render က ကြာရင် ပိတ်တတ်လို့ပါ)
            r = requests.get(site, headers=HEADERS, timeout=5)
            # m3u8 လင့်ခ်တွေကို ရှာဖွေခြင်း
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            
            for l in links:
                found_links.append({
                    "title": f"Live Link ({site.split('//')[1].split('/')[0]})",
                    "url": l,
                    "source": site
                })
        except Exception as e:
            print(f"Error scraping {site}: {e}")
            continue
            
    return found_links

# Frontend က ခေါ်နေတဲ့ /get-live endpoint ကို တိတိကျကျ ပေးထားရမယ်
@app.route('/get-live')
def get_live():
    data = scrape_live_links()
    if not data:
        return jsonify([{"title": "Data Updating... Please Refresh", "url": "", "source": "System"}])
    return jsonify(data)

@app.route('/')
def home():
    return jsonify({"status": "API is online", "endpoint": "/get-live"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
