from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    target_sites = [
        "https://m.yuyantv.cn/", 
        "https://www.thscore.mobi/",
        "https://www.98sports.com/"
    ]
    found_links = []
    for site in target_sites:
        try:
            r = requests.get(site, timeout=5)
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            for l in links:
                found_links.append({"source": site, "url": l})
        except:
            continue
    return jsonify(found_links)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
