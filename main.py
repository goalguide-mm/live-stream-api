from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

@app.route('/get-live')
def get_live():
    target_url = "https://m.yuyantv.cn/"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/04.1'}
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        # m3u8 link ကို စာသားထဲမှာ လိုက်ရှာတာ
        match = re.search(r'https?://[^\s"\'<>]+?\.m3u8', response.text)
        if match:
            return jsonify({"status": "success", "url": match.group(0)})
        return jsonify({"status": "error", "message": "No live link found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
