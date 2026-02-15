from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re
import os

app = Flask(__name__)
CORS(app) # ဒါက Browser block မဖြစ်အောင် အရေးကြီးပါတယ်

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_live_links():
    target_sites = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mm.m3u",
        "https://m.yuyantv.cn/",
        "https://www.thscore.mobi/"
    ]
    found_links = []
    for site in target_sites:
        try:
            r = requests.get(site, headers=HEADERS, timeout=10)
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            for l in links:
                found_links.append({
                    "title": f"Live - {site.split('//')[1].split('/')[0]}",
                    "url": l,
                    "source": site
                })
        except:
            continue
    return found_links

# Endpoint နာမည်ကို Frontend က ခေါ်တာနဲ့ ကိုက်အောင် /get-live ပေးရပါမယ်
@app.route('/get-live')
def get_live():
    links = scrape_live_links()
    return jsonify(links if links else [{"title": "Updating...", "url": "", "source": "System"}])

@app.route('/')
def home():
    return "API is Running. Use /get-live to get data."

if __name__ == "__main__":
    # Render အတွက် Port setup
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
