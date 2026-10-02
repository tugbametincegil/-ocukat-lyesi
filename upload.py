"""video.mp4 dosyasını YouTube'a yükler. Gizli bilgiler GitHub Secrets'tan gelir."""
import json, os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

video_path = sys.argv[1]
meta = json.load(open(sys.argv[2], encoding="utf-8"))
privacy = os.environ.get("PRIVACY", "public")

creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                    token_uri="https://oauth2.googleapis.com/token")
yt = build("youtube", "v3", credentials=creds)
title = (meta["title"][:88] + " #Shorts")
body = {
    "snippet": {
        "title": title,
        "description": meta["title"] + "\n\nÇocuk Atölyesi'nde her gün yeni bir yemek ya da tamir sürprizi!\n#Shorts #çocuk #animasyon #çizgifilm",
        "tags": ["çocuk", "animasyon", "çizgi film", "shorts", "yemek", "tamir"],
        "categoryId": "1",
    },
    "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": True, "madeForKids": True},
}
req = yt.videos().insert(part="snippet,status", body=body,
                         media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4"))
resp = None
while resp is None:
    status, resp = req.next_chunk()
print("Yüklendi: https://www.youtube.com/watch?v=" + resp["id"], "| gizlilik:", resp["status"]["privacyStatus"])
