# -*- coding: utf-8 -*-
"""Parse workbuddy tips list and download posts via fxtwitter."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

SRC = Path(r"H:\github\grok-x\workbuddy-tips-top50-截止-2026-08-07-1054.md")
ROOT = Path(r"H:\github\grok-x\workbuddy-tips-posts-截止-2026-08-07-1054")
RAW = ROOT / "_raw"
ROOT.mkdir(exist_ok=True)
RAW.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (compatible; workbuddy-tips-downloader/1.0)"


def parse_views(s: str) -> int:
    s = s.strip().replace("~", "").replace(",", "").replace(" ", "").lower()
    if s.endswith("k"):
        return int(float(s[:-1]) * 1000)
    try:
        return int(float(s))
    except Exception:
        return 0


def safe(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\n\r\t]', "_", s)
    s = re.sub(r"_+", "_", s).strip(" ._")
    return (s[:80] if s else "unknown")


def type_tag(kind: str) -> str:
    return {"article": "是文章", "promo-post": "推广帖", "post": "普通帖"}.get(kind, kind)


def parse_entries(text: str):
    entries = []
    # Top 50
    for m in re.finditer(
        r"^\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*@?([^\s|]+)\s*\|\s*([^|]+)\|\s*(.+?)\s*\|$",
        text,
        re.M,
    ):
        rank, views_raw, date, lang, author, topic, links = m.groups()
        if "浏览量" in views_raw:
            continue
        status_ids = re.findall(r"/status/(\d+)", links)
        article_ids = re.findall(r"/i/article/(\d+)", links)
        if not status_ids and not article_ids:
            continue
        link_labels = re.findall(r"\[([^\]]+)\]\((https://x\.com/[^)]+)\)", links)
        is_art = bool(article_ids) or any(lab.strip().lower() == "article" for lab, _ in link_labels)
        entries.append(
            {
                "section": "top50",
                "rank": int(rank),
                "views_raw": views_raw.strip(),
                "views": parse_views(views_raw),
                "date": date.strip(),
                "lang": lang.strip(),
                "author": author.strip().lstrip("@"),
                "topic": re.sub(r"\*\*", "", topic).strip(),
                "status_ids": status_ids,
                "article_ids": article_ids,
                "links": links.strip(),
                "is_article_entry": is_art,
            }
        )

    # Extension after 扩展榜
    if "## 扩展榜" in text:
        ext = text.split("## 扩展榜")[1].split("### 官方")[0]
        for line in ext.splitlines():
            m = re.match(
                r"^\|\s*(~?[\d.,]+k?|—|-)\s*\|\s*([^|]+)\|\s*@?([^\s|]+)\s*\|\s*([^|]+)\|\s*(.+?)\s*\|$",
                line,
            )
            if not m:
                continue
            views_raw, date, author, topic, links = m.groups()
            if "浏览量" in views_raw or views_raw.strip() in ("---:", "---"):
                continue
            status_ids = re.findall(r"/status/(\d+)", links)
            article_ids = re.findall(r"/i/article/(\d+)", links)
            if not status_ids and not article_ids:
                continue
            link_labels = re.findall(r"\[([^\]]+)\]\((https://x\.com/[^)]+)\)", links)
            is_art = bool(article_ids) or any(
                lab.strip().lower() == "article" for lab, _ in link_labels
            )
            entries.append(
                {
                    "section": "ext",
                    "rank": None,
                    "views_raw": views_raw.strip(),
                    "views": parse_views(views_raw) if views_raw not in ("—", "-") else 0,
                    "date": date.strip(),
                    "lang": "ZH",
                    "author": author.strip().lstrip("@"),
                    "topic": re.sub(r"\*\*", "", topic).strip(),
                    "status_ids": status_ids,
                    "article_ids": article_ids,
                    "links": links.strip(),
                    "is_article_entry": is_art,
                }
            )
    return entries


def build_jobs(entries):
    jobs = []
    for i, e in enumerate(entries, 1):
        base = f"{i:03d}"
        for sid in e["status_ids"]:
            if e["article_ids"]:
                kind = "promo-post"
            elif e["is_article_entry"]:
                kind = "article"
            else:
                kind = "post"
            jobs.append({**e, "idx": base, "kind": kind, "type": "status", "id": sid})
        for aid in e["article_ids"]:
            jobs.append({**e, "idx": base, "kind": "article", "type": "article", "id": aid})
    seen = set()
    unique = []
    for j in jobs:
        key = (j["type"], j["id"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(j)
    return unique


def fetch_status(sid: str) -> dict:
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
    return {"code": 0, "error": str(last)}


def as_text(val) -> str:
    if val is None:
        return ""
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, dict):
        for k in ("text", "content", "raw_text", "description"):
            if isinstance(val.get(k), str):
                return val[k].strip()
        return ""
    return str(val).strip()


def tweet_text(tweet: dict) -> str:
    note = tweet.get("note_tweet")
    note_text = note.get("text") if isinstance(note, dict) else None
    return as_text(tweet.get("text") or tweet.get("raw_text") or note_text)


def media_list(tweet: dict) -> list[str]:
    out = []
    media = tweet.get("media") or {}
    if isinstance(media, dict):
        for key in ("photos", "videos", "all"):
            for it in media.get(key) or []:
                if isinstance(it, dict):
                    u = it.get("url") or it.get("thumbnail_url")
                    if u:
                        out.append(f"{it.get('type') or key}: {u}")
    return out


def article_blocks_to_md(article: dict) -> str:
    if not article:
        return ""
    lines = []
    if article.get("title"):
        lines += [f"# {article['title']}", ""]
    content = article.get("content") or {}
    blocks = content.get("blocks") or []
    raw_map = content.get("entityMap") or {}
    if isinstance(raw_map, list):
        entity_map = {str(i): e for i, e in enumerate(raw_map)}
    elif isinstance(raw_map, dict):
        entity_map = {str(k): v for k, v in raw_map.items()}
    else:
        entity_map = {}

    def lookup(key):
        return entity_map.get(str(key))

    for b in blocks:
        btype = b.get("type") or "unstyled"
        text = b.get("text") or ""
        if btype == "header-one":
            lines += [f"# {text}", ""]
        elif btype == "header-two":
            lines += [f"## {text}", ""]
        elif btype == "header-three":
            lines += [f"### {text}", ""]
        elif btype == "blockquote":
            for ln in text.splitlines() or [""]:
                lines.append(f"> {ln}")
            lines.append("")
        elif btype == "unordered-list-item":
            lines.append(f"- {text}")
        elif btype == "ordered-list-item":
            lines.append(f"1. {text}")
        elif btype == "code-block":
            lines += ["```", text, "```", ""]
        elif btype == "atomic":
            for er in b.get("entityRanges") or []:
                ent = lookup(er.get("key"))
                if not ent:
                    continue
                if "value" in ent and isinstance(ent.get("value"), dict):
                    et = ent["value"].get("type") or ent.get("type")
                    data = ent["value"].get("data") or {}
                else:
                    et = ent.get("type")
                    data = ent.get("data") or {}
                if et == "MARKDOWN" and data.get("markdown"):
                    lines += [data["markdown"], ""]
                elif et == "LINK" and data.get("url"):
                    lines.append(f"[link]({data['url']})")
        else:
            if text.strip():
                lines += [text, ""]
    cover = ((article.get("cover_media") or {}).get("media_info") or {}).get("original_img_url")
    if cover:
        lines += ["", f"![cover]({cover})"]
    for me in article.get("media_entities") or []:
        u = ((me.get("media_info") or {}).get("original_img_url"))
        if u:
            lines.append(f"![]({u})")
    return "\n".join(lines).strip() + "\n"


def filename(job: dict) -> str:
    return f"{job['idx']}_浏览{job['views']}_{type_tag(job['kind'])}_@{safe(job['author'])}_{job['id']}.md"


def render(job: dict, body: str, meta: dict) -> str:
    is_article = job.get("is_article_entry") or job["kind"] == "article"
    lines = [
        f"# {job['topic']}",
        "",
        f"- **序号**: {job['idx']}",
        f"- **榜单浏览量**: {job['views_raw']}（约 {job['views']:,}）",
        f"- **是否文章**: {'是' if is_article else '否'}",
        f"- **文件类型**: {job['kind']}",
        f"- **作者**: @{job['author']}",
        f"- **发布时间(榜单)**: {job.get('date', '')}",
        f"- **语言**: {job.get('lang', '')}",
        f"- **分区**: {job.get('section', '')}",
        f"- **排名**: {job.get('rank') if job.get('rank') is not None else '扩展榜'}",
        f"- **对象类型**: {job['type']}",
        f"- **ID**: {job['id']}",
        f"- **关联 Status**: {', '.join(job.get('status_ids') or []) or '-'}",
        f"- **关联 Article**: {', '.join(job.get('article_ids') or []) or '-'}",
        f"- **榜单链接**: {job.get('links', '')}",
    ]
    if meta.get("url"):
        lines.append(f"- **URL**: {meta['url']}")
    if meta.get("timestamp"):
        lines.append(f"- **帖子时间**: {meta['timestamp']}")
    if meta.get("views_live") is not None:
        try:
            lines.append(f"- **实时浏览量(抓取时)**: {int(meta['views_live']):,}")
        except Exception:
            lines.append(f"- **实时浏览量(抓取时)**: {meta['views_live']}")
    for k in ("likes", "retweets", "replies", "bookmarks", "quotes"):
        if meta.get(k) is not None:
            try:
                lines.append(f"- **{k}**: {int(meta[k]):,}")
            except Exception:
                lines.append(f"- **{k}**: {meta[k]}")
    if meta.get("author_name"):
        lines.append(f"- **作者显示名**: {meta['author_name']}")
    if meta.get("article_title"):
        lines.append(f"- **文章标题**: {meta['article_title']}")
    if meta.get("error"):
        lines.append(f"- **抓取错误**: {meta['error']}")
    if meta.get("note"):
        lines.append(f"- **备注**: {meta['note']}")
    lines += ["", "---", "", "## 正文", "", body or "(无正文)", ""]
    if meta.get("media"):
        lines += ["## 媒体", ""]
        for m in meta["media"]:
            lines.append(f"- {m}")
        lines.append("")
    if meta.get("quoted"):
        lines += ["## 引用帖", "", meta["quoted"], ""]
    return "\n".join(lines)


def main():
    text = SRC.read_text(encoding="utf-8")
    entries = parse_entries(text)
    jobs = build_jobs(entries)
    manifest = {
        "source": str(SRC),
        "out_dir": str(ROOT),
        "entries_count": len(entries),
        "jobs_count": len(jobs),
        "entries": entries,
        "jobs": jobs,
    }
    (ROOT / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"entries={len(entries)} jobs={len(jobs)}")

    status_ids = sorted({j["id"] for j in jobs if j["type"] == "status"})
    status_cache = {}
    print(f"Fetching {len(status_ids)} status posts...")
    for i, sid in enumerate(status_ids, 1):
        data = fetch_status(sid)
        status_cache[sid] = data
        print(f"  [{i}/{len(status_ids)}] {sid} code={data.get('code')}")
        time.sleep(0.2)

    written = []
    fail = 0
    for job in jobs:
        meta = {}
        body = ""
        if job["type"] == "status":
            data = status_cache.get(job["id"]) or fetch_status(job["id"])
            tweet = data.get("tweet") or {}
            if not tweet:
                meta["error"] = data.get("error") or "no tweet"
                body = f"(抓取失败: {meta['error']})"
                fail += 1
            else:
                author = tweet.get("author") or {}
                meta.update(
                    {
                        "url": tweet.get("url")
                        or f"https://x.com/{job['author']}/status/{job['id']}",
                        "timestamp": tweet.get("created_at") or tweet.get("date"),
                        "views_live": tweet.get("views"),
                        "likes": tweet.get("likes"),
                        "retweets": tweet.get("retweets"),
                        "replies": tweet.get("replies"),
                        "bookmarks": tweet.get("bookmarks"),
                        "quotes": tweet.get("quotes"),
                        "author_name": author.get("name") if isinstance(author, dict) else None,
                        "media": media_list(tweet),
                    }
                )
                text_body = tweet_text(tweet)
                art = tweet.get("article")
                if art and not text_body.strip():
                    text_body = art.get("preview_text") or art.get("title") or ""
                    meta["note"] = "正文主要在关联 X Article 中"
                body = text_body
                if job["kind"] == "article" and art:
                    full = article_blocks_to_md(art)
                    if full.strip():
                        body = full
                        meta["article_title"] = art.get("title")
                qt = tweet.get("quote") or tweet.get("quoted_tweet") or tweet.get("quoted")
                if isinstance(qt, dict):
                    qa = qt.get("author") or {}
                    meta["quoted"] = f"@{qa.get('screen_name') or ''}: {tweet_text(qt)}"
        else:
            art = None
            for sid in job.get("status_ids") or []:
                tweet = (status_cache.get(sid) or {}).get("tweet") or {}
                if tweet.get("article"):
                    art = tweet["article"]
                    meta.update(
                        {
                            "url": f"https://x.com/i/article/{job['id']}",
                            "timestamp": art.get("created_at") or tweet.get("created_at"),
                            "views_live": tweet.get("views"),
                            "likes": tweet.get("likes"),
                            "retweets": tweet.get("retweets"),
                            "replies": tweet.get("replies"),
                            "bookmarks": tweet.get("bookmarks"),
                            "article_title": art.get("title"),
                            "note": f"文章正文自推广帖 status/{sid} 提取",
                        }
                    )
                    break
            if not art:
                for sid, data in status_cache.items():
                    tweet = (data or {}).get("tweet") or {}
                    a = tweet.get("article") or {}
                    if str(a.get("id")) == str(job["id"]):
                        art = a
                        meta.update(
                            {
                                "url": f"https://x.com/i/article/{job['id']}",
                                "article_title": art.get("title"),
                                "views_live": tweet.get("views"),
                                "note": f"自 status/{sid} 提取",
                            }
                        )
                        break
            if art:
                body = article_blocks_to_md(art)
            else:
                meta["error"] = "未能提取文章全文"
                meta["url"] = f"https://x.com/i/article/{job['id']}"
                body = f"(未能提取)\n\nhttps://x.com/i/article/{job['id']}\n"
                fail += 1

        path = ROOT / filename(job)
        path.write_text(render(job, body, meta), encoding="utf-8")
        written.append(path.name)

    # index
    idx = [
        "# WorkBuddy tips 下载索引",
        "",
        f"- 来源: `{SRC}`",
        f"- 条目: {len(entries)}",
        f"- 文件任务: {len(jobs)}",
        f"- 已写入: {len(written)}",
        f"- 失败近似: {fail}",
        "",
        "| 文件 | 序号 | 浏览量 | 类型 | 作者 | 主题 |",
        "|---|---:|---:|---|---|---|",
    ]
    for job in jobs:
        name = filename(job)
        idx.append(
            f"| [{name}](./{name}) | {job['idx']} | {job['views']:,} | {type_tag(job['kind'])} | @{job['author']} | {job['topic'][:40]} |"
        )
    (ROOT / "00_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    summary = {"written": len(written), "fail": fail, "files": written}
    (ROOT / "_download_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2)[:2000])
    print("DONE written=", len(written), "fail=", fail)


if __name__ == "__main__":
    main()
