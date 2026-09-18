# -*- coding: utf-8 -*-
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "_raw", "posts.json")
MEDIA = os.path.join(ROOT, "_media")
os.makedirs(MEDIA, exist_ok=True)

OFFICIAL = "https://x.com/Flatkey_SG/status/2094960597347778782"

with open(RAW, "r", encoding="utf-8") as f:
    posts = json.load(f)


def eng(p):
    return p["likes"] + p["reposts"] + p["quotes"] + p["replies"] + p["bookmarks"]


def render(p):
    e = eng(p)
    er = (e / p["views"] * 100) if p["views"] else 0
    composite = p["views"] / 1000 + e * 2 + p["bookmarks"] * 3
    fname = (
        f"P{p['rank']:02d}_浏览{p['views']}_普通帖_@{p['handle']}_{p['id']}.md"
    )
    lines = []
    lines.append(f"# {p['hook']}")
    lines.append("")
    lines.append(f"- **序号**: P{p['rank']:02d}")
    lines.append("- **是否文章**: 否")
    lines.append("- **文件类型**: post")
    lines.append(f"- **作者**: {p['name']} @{p['handle']}")
    lines.append(f"- **排名(按浏览)**: {p['rank']}")
    lines.append(f"- **Status ID**: {p['id']}")
    lines.append(f"- **帖子**: {p['url']}")
    lines.append(f"- **发布时间**: {p['time']}")
    lines.append("- **抓取时间**: 2026-09-02 18:18 CST")
    lines.append(f"- **浏览**: {p['views']:,}")
    lines.append(f"- **likes**: {p['likes']}")
    lines.append(f"- **retweets**: {p['reposts']}")
    lines.append(f"- **replies**: {p['replies']}")
    lines.append(f"- **bookmarks**: {p['bookmarks']}")
    lines.append(f"- **quotes**: {p['quotes']}")
    lines.append(f"- **互动量**: {e}")
    lines.append(f"- **互动率**: {er:.2f}%")
    lines.append(f"- **综合分**: {composite:.1f}")
    lines.append(f"- **是否引用官方原帖**: {'是' if p.get('quoted') else '否'}")
    lines.append(f"- **官方原帖**: {OFFICIAL}")
    if p.get("note"):
        lines.append(f"- **备注**: {p['note']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 正文")
    lines.append("")
    lines.append(p["text"])
    lines.append("")
    if p.get("thread"):
        lines.append("## 续帖")
        lines.append("")
        for t in p["thread"]:
            lines.append(f"@{t['handle']}：")
            lines.append("")
            lines.append(t["text"])
            lines.append("")
            for m in t.get("media") or []:
                lines.append(f"- 续帖图: {m}")
            lines.append("")
    if p.get("media"):
        lines.append("## 媒体")
        lines.append("")
        for i, m in enumerate(p["media"], 1):
            extra = ""
            if m.get("duration_ms"):
                extra = f" · {m['duration_ms']/1000:.1f}s"
            lines.append(f"{i}. **{m['type']}**{extra}")
            lines.append(f"   {m['url']}")
        lines.append("")
    if p.get("replies_top"):
        lines.append("## 热门回复（抓取时前几条）")
        lines.append("")
        for r in p["replies_top"]:
            lines.append(f"- @{r['handle']}: {r['text']}")
        lines.append("")
    path = os.path.join(ROOT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return fname


def orig_url(url):
    if "pbs.twimg.com/media/" not in url:
        return url
    base, _, _ext = url.rpartition(".")
    name = base.rsplit("/", 1)[-1]
    # keep original extension hint
    fmt = url.rsplit(".", 1)[-1].split("?")[0]
    if fmt not in ("jpg", "png", "webp"):
        fmt = "jpg"
    return f"https://pbs.twimg.com/media/{name}?format={fmt}&name=orig"


def download_photos(posts):
    saved = []
    for p in posts:
        items = list(p.get("media") or [])
        for t in p.get("thread") or []:
            for u in t.get("media") or []:
                items.append({"type": "photo", "url": u})
        n = 0
        for m in items:
            if m.get("type") != "photo":
                continue
            n += 1
            url = orig_url(m["url"])
            ext = "jpg"
            if "format=png" in url or m["url"].endswith(".png"):
                ext = "png"
            dest = os.path.join(MEDIA, f"P{p['rank']:02d}_{p['id']}_p{n}.{ext}")
            if os.path.exists(dest) and os.path.getsize(dest) > 1000:
                saved.append(dest)
                continue
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                with open(dest, "wb") as f:
                    f.write(data)
                saved.append(dest)
                print("saved", dest, len(data))
            except Exception as ex:
                print("fail", url, ex)
    return saved


names = [render(p) for p in posts]
print("wrote", len(names), "markdown files")
saved = download_photos(posts)
print("photos", len(saved))
