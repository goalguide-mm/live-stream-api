from flask import Flask, jsonify
from flask_cors import CORS  # CORS အတွက် ထပ်ထည့်ထားသည်
import requests
import re
import os

app = Flask(__name__)
CORS(app) # Website ကနေ API ခေါ်လို့ရအောင် ခွင့်ပြုခြင်း

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
            r = requests.get(site, headers=HEADERS, timeout=8)
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            
            for l in links:
                found_links.append({
                    "title": f"Live Link from {site.split('//')[1].split('/')[0]}",
                    "url": l,
                    "source": site
                })
        except:
            continue
            
    return found_links

# Frontend က ခေါ်နေတဲ့ /get-live endpoint ကို ဖန်တီးခြင်း
@app.route('/get-live')
def get_live():
    data = scrape_live_links()
    if not data:
        return jsonify([{"title": "No Matches Found", "url": "", "source": "System"}])
    return jsonify(data)

# Home route အတွက်ပါ ထားပေးထားသည်
@app.route('/')
def home():
    return jsonify({"status": "API is running", "endpoint": "/get-live"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
