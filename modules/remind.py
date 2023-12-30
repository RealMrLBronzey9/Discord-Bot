import requests

async def check_youtube_channel(channel_id, api_key):
    base_url = "https://www.googleapis.com/youtube/v3"
    search_url = f"{base_url}/search"
    
    params = {
        "key": api_key,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 1
    }
    
    response = requests.get(search_url, params=params)
    data = response.json()
    
    if "items" in data:
        if data["items"]:
            video_title = data["items"][0]["snippet"]["title"]
            video_id = data["items"][0]["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            return video_title, video_url, video_id

