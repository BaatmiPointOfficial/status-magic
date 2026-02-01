import cloudinary
import cloudinary.uploader
import yt_dlp
import json
import os

# Cloudinary Setup (यह GitHub Secrets से आपकी जानकारी लेगा)
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

def get_videos(query):
    ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # YouTube पर शॉर्ट्स सर्च करना
        search = ydl.extract_info(f"ytsearch5:{query} shorts", download=False)
        return search['entries']

def main():
    # यहाँ आप अपनी पसंद की कैटेगरी और कीवर्ड्स बदल सकते हैं
    topics = {
        "Jethalal": "Jethalal funny status",
        "PakDrama": "Pakistani drama emotional status",
        "Action": "South action movie status"
    }
    
    final_data = []
    
    for cat, query in topics.items():
        print(f"Fetching {cat}...")
        results = get_videos(query)
        for entry in results[:2]: # हर कैटेगरी के 2 वीडियो लेने के लिए
            try:
                # Cloudinary पर सीधे YouTube URL से अपलोड
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                upload = cloudinary.uploader.upload(video_url, resource_type="video")
                
                final_data.append({
                    "cat": cat,
                    "title": entry['title'][:40],
                    "url": upload['secure_url']
                })
            except Exception as e:
                print(f"Error uploading: {e}")
                continue

    # videos.json फाइल को नए डेटा के साथ अपडेट करना
    with open('videos.json', 'w') as f:
        json.dump(final_data, f, indent=4)
    print("Mission Success: videos.json updated!")

if __name__ == "__main__":
    main()
  
