import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Goal Guide API is Live and Auto-Updating!"

# ၁။ Live Stream ရှာရန် API
@app.route('/get-live')
def get_live():
    target_url = "https://www.meetbsd.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        
        # .m3u8 လင့်ခ် သို့မဟုတ် YouTube Live link တွေကို ရှာမယ်
        m3u8_links = re.findall(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', response.text)
        youtube_links = re.findall(r'https?://(?:www\.)?youtube\.com/embed/[^\s"\'<>?]+', response.text)

        if m3u8_links:
            return jsonify({"status": "success", "url": m3u8_links[0]})
        elif youtube_links:
            return jsonify({"status": "success", "type": "youtube", "url": youtube_links[0]})
            
        return jsonify({
            "status": "error", 
            "message": "No live stream detected at the moment",
        }), 404
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ၂။ ပွဲစဉ်ဇယား (Matches) များကို Auto Scrape လုပ်ရန် API
@app.route('/get-matches')
def get_matches():
    target_url = "https://www.meetbsd.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches_list = []
        
        # MeetBSD ၏ Structure အလိုက် match item များကို ရှာဖွေခြင်း
        # မှတ်ချက် - class အမည်များ ပြောင်းလဲပါက ဤနေရာတွင် ပြင်ရန်လိုအပ်သည်
        items = soup.select('.match-item, .live-match, .match-card') 
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        for item in items[:15]: # အများဆုံး ၁၅ ပွဲစာ ယူမယ်
            text = item.get_text(separator=" ", strip=True)
            
            # ပွဲစဉ်ဒေတာများကို ပုံစံသွင်းခြင်း
            matches_list.append({
                "time": "Updated",
                "home": text if len(text) < 50 else text[:47] + "...",
                "away": "Live Info",
                "league": "MeetBSD Schedule",
                "last_update": current_time
            })

        # ရှာမတွေ့ပါက Placeholder data ပြပေးရန်
        if not matches_list:
            matches_list = [{
                "time": "Soon",
                "home": "No Upcoming Matches",
                "away": "Check later",
                "league": "Daily Update",
                "last_update": current_time
            }]
            
        return jsonify({"status": "success", "matches": matches_list})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
