"""Kullanım:
  python make_video.py --auto --out video.mp4 --meta meta.json   (başlangıç tarihine göre bugünün videosu)
  python make_video.py --day 3 --out video.mp4 --meta meta.json
"""
import argparse, datetime, json, os, shutil, subprocess, sys, tempfile
from multiprocessing import Pool
import video
from topics import TOPICS
from audio import make_audio

FPS = 30
_day = None
def job(i):
    video.frame(_day, i / FPS).save(os.path.join(_tmp, "f_%05d.jpg" % i), quality=93)
    return i

def pick_day(auto):
    here = os.path.dirname(os.path.abspath(__file__))
    start = datetime.date.fromisoformat(open(os.path.join(here, "baslangic.txt")).read().strip())
    n = (datetime.datetime.utcnow().date() - start).days
    if n < 0:
        sys.exit("Başlangıç tarihi henüz gelmedi: " + str(start))
    day = n % 30 + 1
    # henüz kodlanmamış günlerde, hazır günleri sırayla tekrar kullan
    ready = sorted(TOPICS)
    return day if day in TOPICS else ready[(day - 1) % len(ready)]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true"); ap.add_argument("--day", type=int)
    ap.add_argument("--out", default="video.mp4"); ap.add_argument("--meta", default="meta.json")
    a = ap.parse_args()
    _day = pick_day(True) if a.auto else a.day
    topic = TOPICS[_day]
    _tmp = tempfile.mkdtemp()
    n = int(video.DUR * FPS)
    with Pool(os.cpu_count()) as pool:
        for _ in pool.imap_unordered(job, range(n), chunksize=8): pass
    wav = os.path.join(_tmp, "a.wav")
    make_audio(_day, video.events(_day), video.DUR, wav)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(_tmp, "f_%05d.jpg"),
                    "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", a.out], check=True)
    shutil.rmtree(_tmp)
    json.dump({"day": _day, "title": topic["title"]}, open(a.meta, "w"), ensure_ascii=False)
    print("Hazır: gün", _day, "-", topic["title"])
