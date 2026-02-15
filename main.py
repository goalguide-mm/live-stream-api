from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

def scrape_live_links():
    # ဒီနေရာမှာ Live Video ရှိတတ်တဲ့ ဆိုဒ်တွေကို ထည့်ထားတယ်
    target_sites = ["https://m.yuyantv.cn/", "https://www.thscore.mobi/"]
    found_links = []
    
    for site in target_sites:
        try:
            r = requests.get(site, timeout=10)
            # .m3u8 လင့်ခ်တွေကို ရှာတဲ့ Pattern
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            for l in links:
                found_links.append({"source": site, "url": l})
        except:
            continue
    return found_links

@app.route('/')
def home():
    data = scrape_live_links()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
