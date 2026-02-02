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

# कैटेगरीज़ में 'shorts' जोड़ा गया है ताकि छोटे वीडियो मिलें
CATEGORIES = {
    "Life_Lessons": "life lessons hindi movie shorts",
    "Motivational": "best motivational status hindi shorts",
    "Sad_Dramas": "Pakistani drama emotional status shorts",
    "Attitude_Killer": "South movie attitude entry shorts",
    "Podcast_Clips": "viral podcast clips hindi shorts",
    "News_Debates": "funny and aggressive news debate shorts"
}

def fetch_from_youtube():
    print("--- चरण 1: YouTube से स्टेटस वीडियो खोज रहा हूँ ---")
    for folder, query in CATEGORIES.items():
        print(f"चेक कर रहा हूँ: {folder}")
        
        # हम 5 वीडियो सर्च करेंगे और पहला छोटा वीडियो उठा लेंगे
        cmd = [
            'yt-dlp', f"ytsearch5:{query}", 
            '--format', 'best[ext=mp4]', 
            '--match-filter', 'duration < 150', # 2.5 मिनट से कम
            '--max-filesize', '20M', 
            '--output', 'temp_status.mp4', '--no-playlist'
        ]
        try:
            subprocess.run(cmd, check=True)
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
                print(f"⚠️ {folder}: कोई छोटा वीडियो नहीं मिला।")
        except Exception as e:
            print(f"❌ {folder} में दिक्कत: {e}")

def update_json_list():
    """Cloudinary से सभी वीडियो की लिस्ट बनाकर JSON अपडेट करना"""
    print("--- चरण 2: वेबसाइट की लिस्ट अपडेट हो रही है ---")
    video_list = []
    try:
        response = cloudinary.api.resources(resource_type="video", type="upload", max_results=500)
        for asset in response.get('resources', []):
            if "samples/" not in asset['public_id']:
                video_list.append({
                    "url": asset['secure_url'],
                    "public_id": asset['public_id']
                })
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        print(f"🚀 मिशन पूरा! कुल {len(video_list)} वीडियो मिले।")
    except Exception as e:
        print(f"❌ JSON एरर: {e}")

if __name__ == "__main__":
    fetch_from_youtube()
    update_json_list()
