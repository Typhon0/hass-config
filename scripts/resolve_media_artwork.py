import sys
import json
import urllib.request
import urllib.parse
import re

def resolve_youtube_thumb(query):
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            if match:
                vid = match.group(1)
                return f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    except Exception:
        pass
    return ""

def main():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZjBhMjFlODZjNWU0ZjFlOTgwYjljNTcyN2Q3YjQyYSIsImlhdCI6MTc5MTgzNjEyMSwiZXhwIjoyMTA3MTk2MTIxfQ.EQAZUCP4dEvHwaO76_Eq3otCVlGeyyN1ugsK4dZSYZ0"
    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request("http://192.168.1.160:8443/api/states/media_player.sejour", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            state_data = json.loads(resp.read().decode('utf-8'))
    except Exception:
        print(json.dumps({"artwork": ""}))
        return

    attrs = state_data.get("attributes", {})
    # 1. If HA already has entity_picture
    entity_pic = attrs.get("entity_picture")
    if entity_pic:
        print(json.dumps({"artwork": entity_pic}))
        return

    # 2. If YouTube
    app_name = (attrs.get("app_name") or "").lower()
    app_id = (attrs.get("app_id") or "").lower()
    media_title = attrs.get("media_title") or ""
    media_artist = attrs.get("media_artist") or ""

    if ("youtube" in app_name or "youtube" in app_id) and media_title:
        query = f"{media_artist} {media_title}".strip()
        thumb = resolve_youtube_thumb(query)
        if thumb:
            print(json.dumps({"artwork": thumb, "query": query}))
            return

    print(json.dumps({"artwork": ""}))

if __name__ == "__main__":
    main()
