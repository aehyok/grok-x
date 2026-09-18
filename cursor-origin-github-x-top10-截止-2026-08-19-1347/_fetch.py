# -*- coding: utf-8 -*-
import json, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "_raw"
RAW.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (compatible; origin-github-downloader/1.0)"
IDS = [
    "2089399057659596847",
    "2089575133442711787",
    "2067012220832329782",
    "2089399059488350447",
    "2089758713183613266",
    "2067153200852193339",
    "2066927951212609863",
    "2089409162270965858",
    "2067021327739814112",
    "2089417913002586565",
]


def fetch(sid: str) -> dict:
    cache = RAW / f"status_{sid}.json"
    if cache.exists() and cache.stat().st_size > 50:
        return json.loads(cache.read_text(encoding="utf-8"))
    url = f"https://api.fxtwitter.com/status/{sid}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data
        except Exception as e:
            last = e
            time.sleep(1.2 * (attempt + 1))
    return {"error": str(last)}


for i, sid in enumerate(IDS, 1):
    data = fetch(sid)
    tw = data.get("tweet") or {}
    print(f"[{i}/10] {sid} code={data.get('code')} text_len={len(tw.get('text') or '')} quote={bool(tw.get('quote'))}")
    time.sleep(0.15)
print("DONE")
