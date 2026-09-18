# -*- coding: utf-8 -*-
"""Fetch UU远程 Top 10 posts via fxtwitter and download media."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "_raw"
MEDIA = ROOT / "_media"
RAW.mkdir(exist_ok=True)
MEDIA.mkdir(exist_ok=True)

UA = "Mozilla/5.0 (compatible; uu-remote-top10-downloader/1.0)"

POSTS = [
    {"rank": 1, "id": "2086627878410842194", "handle": "imwritingbugs"},
    {"rank": 2, "id": "2087548246810075352", "handle": "LawrenceW_Zen"},
    {"rank": 3, "id": "2091773817739964782", "handle": "aehyok"},
    {"rank": 4, "id": "2089924072566321443", "handle": "ZeroZ_JQ"},
    {"rank": 5, "id": "2086990476734062749", "handle": "indie_maker_fox"},
    {"rank": 6, "id": "2088279542721065390", "handle": "vincemask"},
    {"rank": 7, "id": "2086758158492717551", "handle": "_cosine_x"},
    {"rank": 8, "id": "2082736537192845820", "handle": "aikangarooking"},
    {"rank": 9, "id": "2086733035211522268", "handle": "taresky"},
    {"rank": 10, "id": "2088510482886123601", "handle": "aronhouyu"},
]

# Author self-replies / extra quoted posts to also cache.
EXTRA_IDS = [
    "2088279662350966958",  # P06 续帖
    "2086476497678979305",  # P01 引用
    "2087435220538818721",  # P02 引用
    "2086727188439843227",  # P07 引用
    "2082402085367164931",  # P08 引用
    "2086729000429445422",  # P09 引用
]


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception as e:
            last = e
            time.sleep(1.2 * (attempt + 1))
    return {"error": str(last)}


def fetch_status(sid: str) -> dict:
    cache = RAW / f"status_{sid}.json"
    if cache.exists() and cache.stat().st_size > 50:
        return json.loads(cache.read_text(encoding="utf-8"))
    data = http_json(f"https://api.fxtwitter.com/status/{sid}")
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def ext_from_url(url: str, fallback: str) -> str:
    path = url.split("?", 1)[0]
    name = path.rsplit("/", 1)[-1]
    if "." in name:
        ext = name.rsplit(".", 1)[-1].lower()
        if ext in {"jpg", "jpeg", "png", "webp", "gif", "mp4", "mov"}:
            return ext
    return fallback


def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  FAIL media {dest.name}: {e}")
        return False


def collect_media(tweet: dict, prefix: str) -> list[dict]:
    items = []
    media = tweet.get("media") or {}
    photos = media.get("photos") or []
    videos = media.get("videos") or []
    if isinstance(media, list):
        for m in media:
            t = (m.get("type") or "").lower()
            url = m.get("url") or m.get("thumbnail_url")
            if url:
                items.append({"type": t or "unknown", "url": url, "prefix": prefix})
        return items
    for i, p in enumerate(photos, 1):
        url = p.get("url") if isinstance(p, dict) else None
        if url:
            items.append({"type": "photo", "url": url, "prefix": f"{prefix}_p{i}"})
    for i, v in enumerate(videos, 1):
        url = None
        if isinstance(v, dict):
            url = v.get("url")
            variants = v.get("variants") or []
            best = None
            for var in variants:
                if not isinstance(var, dict):
                    continue
                u = var.get("url") or ""
                if ".mp4" in u:
                    br = var.get("bitrate") or 0
                    if best is None or br > best[0]:
                        best = (br, u)
            if best:
                url = best[1]
            elif not url:
                url = v.get("thumbnail_url")
        if url:
            items.append({"type": "video", "url": url, "prefix": f"{prefix}_v{i}"})
    return items


def orig_photo(url: str) -> str:
    if "pbs.twimg.com/media/" in url and "name=" not in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}name=orig"
    return url


saved = []
all_ids = [p["id"] for p in POSTS] + EXTRA_IDS
seen = set()
for sid in all_ids:
    if sid in seen:
        continue
    seen.add(sid)
    data = fetch_status(sid)
    tw = data.get("tweet") or {}
    text = tw.get("text") or ""
    print(f"{sid} code={data.get('code')} text_len={len(text)} quote={bool(tw.get('quote'))}")
    time.sleep(0.2)

for post in POSTS:
    sid = post["id"]
    data = fetch_status(sid)
    tw = data.get("tweet") or {}
    rank = post["rank"]
    items = collect_media(tw, f"P{rank:02d}_{sid}")
    quote = tw.get("quote") or {}
    if quote:
        qid = quote.get("id") or quote.get("id_str") or "quote"
        items.extend(collect_media(quote, f"P{rank:02d}_quote_{qid}"))
    for item in items:
        url = item["url"]
        kind = item["type"]
        if kind == "photo":
            url = orig_photo(url)
        ext = ext_from_url(url, "mp4" if kind == "video" else "jpg")
        dest = MEDIA / f"{item['prefix']}.{ext}"
        ok = download_file(url, dest)
        print(f"  media {dest.name} {'ok' if ok else 'fail'} {url[:80]}")
        saved.append({"rank": rank, "id": sid, "type": kind, "file": dest.name, "url": url, "ok": ok})
        time.sleep(0.15)

summary = ROOT / "_download_summary.json"
summary.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")
print("DONE", len(saved), "media items")
