# -*- coding: utf-8 -*-
import re
import json
from pathlib import Path

src = Path(r"H:\github\grok-x\codex-tips-top50-截止-2026-08-07-1032.md")
text = src.read_text(encoding="utf-8")
out_dir = Path(r"H:\github\grok-x\codex-tips-posts-截止-2026-08-07-1032")
out_dir.mkdir(exist_ok=True)


def parse_views(s: str) -> int:
    s = s.strip().replace("~", "").replace(",", "").replace(" ", "").lower()
    if s.endswith("k"):
        return int(float(s[:-1]) * 1000)
    try:
        return int(float(s))
    except Exception:
        return 0


entries = []

for m in re.finditer(
    r"^\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*@?([^\s|]+)\s*\|\s*([^|]+)\|\s*(.+?)\s*\|$",
    text,
    re.M,
):
    rank, views_raw, date, lang, author, topic, links = m.groups()
    author = author.strip().lstrip("@")
    status_ids = re.findall(r"/status/(\d+)", links)
    article_ids = re.findall(r"/i/article/(\d+)", links)
    link_labels = re.findall(r"\[([^\]]+)\]\((https://x\.com/[^)]+)\)", links)
    is_article_entry = bool(article_ids) or any(
        lab.strip().lower() == "article" for lab, _ in link_labels
    )
    entries.append(
        {
            "section": "top50",
            "rank": int(rank),
            "views_raw": views_raw.strip(),
            "views": parse_views(views_raw),
            "date": date.strip(),
            "lang": lang.strip(),
            "author": author,
            "topic": re.sub(r"\*\*", "", topic).strip(),
            "status_ids": status_ids,
            "article_ids": article_ids,
            "links": links.strip(),
            "is_article_entry": is_article_entry,
        }
    )

ext = (
    text.split("## 扩展榜")[1].split("## 技巧主题聚类")[0]
    if "## 扩展榜" in text
    else ""
)
current_sub = "ext"
for line in ext.splitlines():
    if line.startswith("### "):
        current_sub = line[4:].strip()
        continue
    m = re.match(
        r"^\|\s*(~?[\d.,]+k?)\s*\|\s*([^|]+)\|\s*@?([^\s|]+(?:\s+[^|]*?)?)\s*\|\s*([^|]+)\|\s*(.+?)\s*\|$",
        line,
    )
    if not m:
        continue
    views_raw, date, author_raw, topic, links = m.groups()
    if "浏览量" in views_raw or views_raw.strip() in ("---:", "---"):
        continue
    author = re.sub(r"\s+.*", "", author_raw.strip()).lstrip("@")
    status_ids = re.findall(r"/status/(\d+)", links)
    article_ids = re.findall(r"/i/article/(\d+)", links)
    if not status_ids and not article_ids:
        continue
    link_labels = re.findall(r"\[([^\]]+)\]\((https://x\.com/[^)]+)\)", links)
    is_article_entry = bool(article_ids) or any(
        lab.strip().lower() == "article" for lab, _ in link_labels
    )
    entries.append(
        {
            "section": f"ext-{current_sub}",
            "rank": None,
            "views_raw": views_raw.strip(),
            "views": parse_views(views_raw),
            "date": date.strip(),
            "lang": "",
            "author": author,
            "topic": re.sub(r"\*\*", "", topic).strip(),
            "status_ids": status_ids,
            "article_ids": article_ids,
            "links": links.strip(),
            "is_article_entry": is_article_entry,
        }
    )

jobs = []
for i, e in enumerate(entries, 1):
    views = e["views"]
    base_idx = f"{i:03d}"
    for sid in e["status_ids"]:
        if e["article_ids"]:
            kind = "promo-post"
        elif e["is_article_entry"]:
            kind = "article"
        else:
            kind = "post"
        jobs.append(
            {
                "idx": base_idx,
                "kind": kind,
                "type": "status",
                "id": sid,
                "views": views,
                "views_raw": e["views_raw"],
                "author": e["author"],
                "topic": e["topic"],
                "section": e["section"],
                "rank": e["rank"],
                "date": e["date"],
                "lang": e["lang"],
                "entry_is_article": e["is_article_entry"],
                "article_ids": e["article_ids"],
                "status_ids": e["status_ids"],
                "links": e["links"],
            }
        )
    for aid in e["article_ids"]:
        jobs.append(
            {
                "idx": base_idx,
                "kind": "article",
                "type": "article",
                "id": aid,
                "views": views,
                "views_raw": e["views_raw"],
                "author": e["author"],
                "topic": e["topic"],
                "section": e["section"],
                "rank": e["rank"],
                "date": e["date"],
                "lang": e["lang"],
                "entry_is_article": True,
                "article_ids": e["article_ids"],
                "status_ids": e["status_ids"],
                "links": e["links"],
            }
        )

seen = set()
unique_jobs = []
for j in jobs:
    key = (j["type"], j["id"])
    if key in seen:
        continue
    seen.add(key)
    unique_jobs.append(j)

manifest = {
    "source": str(src),
    "out_dir": str(out_dir),
    "entries_count": len(entries),
    "jobs_count": len(unique_jobs),
    "entries": entries,
    "jobs": unique_jobs,
}
manifest_path = out_dir / "_manifest.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"entries={len(entries)} jobs={len(unique_jobs)} out={out_dir}")
print("status", sum(1 for j in unique_jobs if j["type"] == "status"))
print("article", sum(1 for j in unique_jobs if j["type"] == "article"))
