import urllib.request
import json
import ssl
import sys

JELLYFIN_URL = "https://jellyfin.typhon0.com"
API_KEY = "7c9be5d3d4ab482cb19b4798d5681999"
USER_ID = "1b7ca926887a4b498f664d50915f8d15"

HEADERS = {
    "Authorization": f'MediaBrowser Token="{API_KEY}"',
    "Accept": "application/json"
}

ctx = ssl.create_default_context()

def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
        return json.loads(response.read().decode('utf-8'))

def resolve_image_url(item):
    if not item:
        return ""
    item_id = item.get("Id")
    
    # 1. Item's own Backdrop if Backdrop tags exist
    backdrop_tags = item.get("BackdropImageTags") or []
    if len(backdrop_tags) > 0:
        return f"{JELLYFIN_URL}/Items/{item_id}/Images/Backdrop?maxWidth=1920&quality=90"
        
    # 2. Parent's Backdrop if Parent Backdrop tags exist (TV episodes)
    parent_backdrop_id = item.get("ParentBackdropItemId")
    parent_backdrop_tags = item.get("ParentBackdropImageTags") or []
    if parent_backdrop_id and len(parent_backdrop_tags) > 0:
        return f"{JELLYFIN_URL}/Items/{parent_backdrop_id}/Images/Backdrop?maxWidth=1920&quality=90"
        
    # 3. Series Backdrop if SeriesId exists
    series_id = item.get("SeriesId")
    if series_id:
        return f"{JELLYFIN_URL}/Items/{series_id}/Images/Backdrop?maxWidth=1920&quality=90"

    # 4. Item's Thumb if Thumb tag exists
    image_tags = item.get("ImageTags") or {}
    if "Thumb" in image_tags:
        return f"{JELLYFIN_URL}/Items/{item_id}/Images/Thumb?maxWidth=1920&quality=90"

    # 5. Item's Primary (Cover / Thumbnail)
    if "Primary" in image_tags:
        return f"{JELLYFIN_URL}/Items/{item_id}/Images/Primary?maxWidth=1920&quality=90"

    return f"{JELLYFIN_URL}/Items/{item_id}/Images/Primary?maxWidth=1920&quality=90"

def main():
    result = {
        "state": "idle",
        "Name": "",
        "SeriesName": "",
        "media_title": "Aucune lecture",
        "media_artist": "",
        "ParentBackdropItemId": "",
        "entity_picture": "",
        "is_paused": False,
        "device": "",
        "client": ""
    }

    try:
        sessions = get_json(f"{JELLYFIN_URL}/Sessions")
        playing_session = None
        for s in sessions:
            if s.get("NowPlayingItem"):
                if s.get("UserId") == USER_ID or not playing_session:
                    playing_session = s
        
        if playing_session:
            item = playing_session.get("NowPlayingItem", {})
            play_state = playing_session.get("PlayState", {})
            is_paused = play_state.get("IsPaused", False)
            result["state"] = "paused" if is_paused else "playing"
            result["is_paused"] = is_paused
            result["device"] = playing_session.get("DeviceName", "")
            result["client"] = playing_session.get("Client", "")
            
            name = item.get("Name", "")
            series_name = item.get("SeriesName", "")
            result["Name"] = name
            result["SeriesName"] = series_name
            result["media_title"] = name
            result["media_artist"] = series_name
            result["ParentBackdropItemId"] = item.get("ParentBackdropItemId") or item.get("SeriesId") or item.get("Id") or ""
            result["entity_picture"] = resolve_image_url(item)
    except Exception:
        pass

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
