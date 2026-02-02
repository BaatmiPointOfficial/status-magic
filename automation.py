import os
import json
import subprocess
import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. Cloudinary सेटअप
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# कैटेगरीज़ को और बेहतर बनाया गया है ताकि छोटे वीडियो मिलें
CATEGORIES = {
    "Life_Lessons": "life lessons hindi shorts",
    "Motivational": "best motivational status hindi shorts",
    "Sad_Dramas": "Pakistani drama emotional status shorts",
    "Attitude_Killer": "South movie attitude entry shorts",
    "Podcast_Clips": "viral podcast hindi shorts",
    "News_Debates": "funny news debate shorts hindi"
}

def fetch_from_youtube():
    print("--- चरण 1: YouTube से नया कंटेंट डाउनलोड कर रहा हूँ ---")
    
    # सबसे पहले yt-dlp को अपडेट करने की कोशिश करें
    try:
        subprocess.run(['pip', 'install', '-U', 'yt-dlp'], check=True)
    except:
        pass

    for folder, query in CATEGORIES.items():
        print(f"चेक कर रहा हूँ: {folder}")
        
        # हमने duration filter को 180 (3 मिनट) कर दिया है ताकि वीडियो 'मिस' न हों
        cmd = [
            'yt-dlp', 
            f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', 
            '--match-filter', 'duration < 180', 
            '--no-check-certificates',
            '--geo-bypass',
            '--output', 'temp_status.mp4', 
            '--no-playlist'
        ]
        
        try:
            # वीडियो डाउनलोड करना
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists("temp_status.mp4"):
                cloudinary.uploader.upload(
                    "temp_status.mp4", 
                    resource_type="video", 
                    folder=f"StatusMagic/{folder}",
                    tags=[folder, "auto_youtube"]
                )
                print(f"✅ सफलता: {folder} का वीडियो अपलोड हुआ।")
                os.remove("temp_status.mp4")
            else:
                print(f"⚠️ {folder}: वीडियो नहीं मिला या बहुत बड़ा था।")
                
        except Exception as e:
            print(f"❌ {folder} में एरर: {e}")

def update_json_list():
    """Cloudinary से सभी वीडियो की लिस्ट बनाकर JSON अपडेट करना"""
    print("--- चरण 2: JSON लिस्ट अपडेट हो रही है ---")
    video_list = []
    try:
        # max_results=500 ताकि आपके सभी वीडियो आ जाएँ
        response = cloudinary.api.resources(
            resource_type="video", 
            type="upload", 
            max_results=500 
        )
        
        for asset in response.get('resources', []):
            p_id = asset['public_id']
            # सैंपल वीडियो को छोड़कर बाकी सब जोड़ें
            if "samples/" not in p_id:
                video_list.append({
                    "url": asset['secure_url'],
                    "public_id": p_id
                })
        
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        print(f"🚀 मिशन पूरा! अब लिस्ट में कुल {len(video_list)} वीडियो हैं।")
        
    except Exception as e:
        print(f"❌ JSON एरर: {e}")

if __name__ == "__main__":
    fetch_from_youtube()
    update_json_list()
