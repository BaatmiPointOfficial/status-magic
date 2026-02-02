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

CATEGORIES = {
    "Life_Lessons": "deep life lesson movie scenes hindi shorts",
    "Motivational": "best motivational status clips hindi",
    "Sad_Dramas": "Pakistani drama emotional dialogue status",
    "Attitude_Killer": "South movie attitude entry status hindi",
    "Podcast_Clips": "viral podcast clips hindi life lessons",
    "News_Debates": "funny and aggressive news debate moments status"
}

def fetch_from_youtube():
    print("--- YouTube से नया माल (Content) ला रहा हूँ ---")
    for folder, query in CATEGORIES.items():
        # हमने duration को 90 तक बढ़ाया है ताकि वीडियो आसानी से मिलें
        cmd = [
            'yt-dlp', f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', 
            '--match-filter', 'duration < 90', 
            '--output', 'temp_status.mp4', '--no-playlist'
        ]
        try:
            subprocess.run(cmd, check=True)
            
            # सबसे ज़रूरी सुधार: पहले चेक करो कि फाइल बनी भी है या नहीं
            if os.path.exists("temp_status.mp4"):
                cloudinary.uploader.upload(
                    "temp_status.mp4", 
                    resource_type="video", 
                    folder=f"StatusMagic/{folder}",
                    tags=[folder, "auto_youtube"]
                )
                print(f"✅ {folder} का वीडियो अपलोड हुआ।")
                os.remove("temp_status.mp4")
            else:
                print(f"⚠️ {folder}: कोई वीडियो फिल्टर में फिट नहीं बैठा, स्किप किया।")
                
        except Exception as e:
            print(f"❌ {folder} में गड़बड़: {e}")

def update_json_list():
    """वेबसाइट के लिए JSON लिस्ट अपडेट करना"""
    print("--- वेबसाइट के लिए JSON लिस्ट अपडेट कर रहा हूँ ---")
    video_list = []
    try:
        response = cloudinary.api.resources(
            resource_type="video", type="upload", max_results=500 
        )
        for asset in response.get('resources', []):
            if "samples/" not in asset['public_id']:
                video_list.append({
                    "url": asset['secure_url'],
                    "public_id": asset['public_id']
                })
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        print(f"🚀 मिशन पूरा! अब लिस्ट में कुल {len(video_list)} वीडियो हैं।")
    except Exception as e:
        print(f"❌ JSON एरर: {e}")

if __name__ == "__main__":
    fetch_from_youtube()
    update_json_list()
