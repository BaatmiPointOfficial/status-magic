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

# आपकी सभी कैटेगरीज़
CATEGORIES = {
    "Life_Lessons": "deep life lesson movie scenes hindi shorts",
    "Motivational": "best motivational status clips hindi",
    "Sad_Dramas": "Pakistani drama emotional dialogue status",
    "Attitude_Killer": "South movie attitude entry status hindi",
    "Podcast_Clips": "viral podcast clips hindi life lessons",
    "News_Debates": "funny and aggressive news debate moments status"
}

def fetch_from_youtube():
    """YouTube से वीडियो ढूंढकर अपलोड करना"""
    for folder, query in CATEGORIES.items():
        print(f"चेक कर रहा हूँ: {folder}")
        cmd = [
            'yt-dlp', f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', 
            '--max-filesize', '15M', 
            '--match-filter', 'duration < 65', 
            '--output', 'temp_status.mp4', '--no-playlist'
        ]
        try:
            subprocess.run(cmd, check=True)
            cloudinary.uploader.upload(
                "temp_status.mp4", 
                resource_type="video", 
                folder=f"StatusMagic/{folder}",
                tags=[folder, "auto_youtube"]
            )
            os.remove("temp_status.mp4")
            print(f"सफलता: {folder} का नया वीडियो अपलोड हुआ।")
        except Exception as e:
            print(f"स्किप किया ({folder}): {e}")

def update_json_list():
    """Cloudinary से सभी वीडियो की लिस्ट बनाकर videos.json अपडेट करना"""
    print("Cloudinary से सभी वीडियो की लिस्ट निकाल रहा हूँ...")
    try:
        # StatusMagic फोल्डर के सभी वीडियो मँगवाना
        resources = cloudinary.api.resources(
            resource_type="video", 
            type="upload", 
            prefix="StatusMagic/", 
            max_results=500
        )
        
        video_list = []
        for asset in resources.get('resources', []):
            video_list.append({
                "url": asset['secure_url'],
                "public_id": asset['public_id']
            })
        
        # videos.json फाइल में लिखना
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        
        print(f"सफलता! अब videos.json में कुल {len(video_list)} वीडियो हैं।")
    except Exception as e:
        print(f"JSON अपडेट में गड़बड़: {e}")

if __name__ == "__main__":
    # पहले नए वीडियो लाओ, फिर पूरी लिस्ट अपडेट करो
    fetch_from_youtube()
    update_json_list()
