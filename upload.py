import json, os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get(name):
    raw = os.environ.get(name, "")
    v = raw.strip().strip('"').strip("'").strip()
    if raw != v:
        print("UYARI:", name, "başında/sonunda boşluk, tırnak ya da satır sonu vardı, temizlendi")
    if "\n" in v or " " in v:
        print("UYARI:", name, "içinde boşluk ya da satır sonu var, yanlış yapıştırılmış olabilir")
    return v

cid = get("YT_CLIENT_ID")
sec = get("YT_CLIENT_SECRET")
rt = get("YT_REFRESH_TOKEN")
print("Client ID .apps.googleusercontent.com ile bitiyor mu:", cid.endswith(".apps.googleusercontent.com"), "| ilk 12 karakter:", cid[:12])
print("Client secret GOCSPX- ile başlıyor mu:", sec.startswith("GOCSPX-"), "| uzunluk:", len(sec))
print("Refresh token 1// ile başlıyor mu:", rt.startswith("1//"), "| uzunluk:", len(rt))

creds = Credentials(None, refresh_token=rt, client_id=cid, client_secret=sec,
                    token_uri="https://oauth2.googleapis.com/token")
try:
    creds.refresh(Request())
except Exception as e:
    print("HATA: Google bu üç anahtarı kabul etmedi:", e)
    print("Üçü de aynı OAuth istemcisine ait olmalı ve refresh token o istemciyle alınmış olmalı.")
    sys.exit(1)
print("Giriş başarılı, video yükleniyor...")

video_path = sys.argv[1]
meta = json.load(open(sys.argv[2], encoding="utf-8"))
privacy = os.environ.get("PRIVACY", "public")
yt = build("youtube", "v3", credentials=creds)
title = meta["title"][:88] + " #Shorts"
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
