# -*- coding: utf-8 -*-
"""Download all Codex tip posts from fxtwitter into labeled markdown files."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"H:\github\grok-x\codex-tips-posts-截止-2026-08-07-1032")
MANIFEST = ROOT / "_manifest.json"
RAW_DIR = ROOT / "_raw"
RAW_DIR.mkdir(exist_ok=True)

UA = "Mozilla/5.0 (compatible; codex-tips-downloader/1.0)"


def safe(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\n\r\t]', "_", s)
    s = re.sub(r"_+", "_", s).strip(" ._")
    return (s[:80] if s else "unknown")


def type_tag(kind: str) -> str:
    return {
        "article": "是文章",
        "promo-post": "推广帖",
        "post": "普通帖",
    }.get(kind, kind)


def filename(job: dict, extra: str = "") -> str:
    author = safe(job["author"])
    pid = job["id"]
    return f"{job['idx']}_浏览{job['views']}_{type_tag(job['kind'])}_@{author}_{pid}{extra}.md"


def fetch_status(status_id: str) -> dict:
    cache = RAW_DIR / f"status_{status_id}.json"
    if cache.exists() and cache.stat().st_size > 50:
        return json.loads(cache.read_text(encoding="utf-8"))
    url = f"https://api.fxtwitter.com/status/{status_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last_err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data
        except Exception as e:
            last_err = e
            time.sleep(1.2 * (attempt + 1))
    return {"code": 0, "error": str(last_err)}


def article_blocks_to_md(article: dict) -> str:
    if not article:
        return ""
    lines = []
    title = article.get("title")
    if title:
        lines.append(f"# {title}")
        lines.append("")
    preview = article.get("preview_text")
    if preview and not title:
        lines.append(preview)
        lines.append("")
    content = article.get("content") or {}
    blocks = content.get("blocks") or []
    raw_entity_map = content.get("entityMap") or {}
    if isinstance(raw_entity_map, list):
        entity_map = {str(i): e for i, e in enumerate(raw_entity_map)}
    elif isinstance(raw_entity_map, dict):
        entity_map = {str(k): v for k, v in raw_entity_map.items()}
    else:
        entity_map = {}

    def lookup_entity(key):
        if key is None:
            return None
        ent = entity_map.get(str(key))
        if ent is not None:
            return ent
        # list-like entries may store key inside
        for v in entity_map.values():
            if isinstance(v, dict) and str(v.get("key")) == str(key):
                return v
        return None

    for b in blocks:
        btype = b.get("type") or "unstyled"
        text = b.get("text") or ""
        if btype in ("header-one",):
            lines.append(f"# {text}")
            lines.append("")
        elif btype in ("header-two",):
            lines.append(f"## {text}")
            lines.append("")
        elif btype in ("header-three",):
            lines.append(f"### {text}")
            lines.append("")
        elif btype == "blockquote":
            for ln in text.splitlines() or [""]:
                lines.append(f"> {ln}")
            lines.append("")
        elif btype in ("unordered-list-item",):
            lines.append(f"- {text}")
        elif btype in ("ordered-list-item",):
            lines.append(f"1. {text}")
        elif btype == "code-block":
            lines.append("```")
            lines.append(text)
            lines.append("```")
            lines.append("")
        elif btype == "atomic":
            for er in b.get("entityRanges") or []:
                ent = lookup_entity(er.get("key"))
                if not ent:
                    continue
                # entityMap items sometimes {type, data} or nested
                if "value" in ent and isinstance(ent.get("value"), dict):
                    et = ent["value"].get("type") or ent.get("type")
                    data = ent["value"].get("data") or {}
                else:
                    et = ent.get("type")
                    data = ent.get("data") or {}
                if et == "MARKDOWN" and data.get("markdown"):
                    lines.append(data["markdown"])
                    lines.append("")
                elif et == "LINK" and data.get("url"):
                    lines.append(f"[link]({data['url']})")
                elif et == "MEDIA":
                    lines.append(f"[media entity {er.get('key')}]")
                else:
                    if text.strip():
                        lines.append(text)
        else:
            if text.strip():
                lines.append(text)
                lines.append("")
    # cover
    cover = article.get("cover_media") or {}
    mi = (cover.get("media_info") or {})
    if mi.get("original_img_url"):
        lines.append("")
        lines.append(f"![cover]({mi['original_img_url']})")
    # media_entities
    for me in article.get("media_entities") or []:
        info = me.get("media_info") or {}
        u = info.get("original_img_url")
        if u:
            lines.append(f"![]({u})")
    return "\n".join(lines).strip() + "\n"


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
            items = media.get(key) or []
            for it in items:
                if isinstance(it, dict):
                    u = it.get("url") or it.get("thumbnail_url") or it.get("static_url")
                    t = it.get("type") or key
                    if u:
                        out.append(f"{t}: {u}")
                elif isinstance(it, str):
                    out.append(it)
    elif isinstance(media, list):
        for it in media:
            if isinstance(it, dict):
                u = it.get("url")
                if u:
                    out.append(u)
    return out


def render_md(job: dict, body: str, meta: dict) -> str:
    is_article = job.get("entry_is_article") or job["kind"] == "article"
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
        v = meta["views_live"]
        try:
            lines.append(f"- **实时浏览量(抓取时)**: {int(v):,}")
        except Exception:
            lines.append(f"- **实时浏览量(抓取时)**: {v}")
    for k in ("likes", "retweets", "replies", "bookmarks", "quotes"):
        if meta.get(k) is not None:
            v = meta[k]
            try:
                lines.append(f"- **{k}**: {int(v):,}")
            except Exception:
                lines.append(f"- **{k}**: {v}")
    if meta.get("author_name"):
        lines.append(f"- **作者显示名**: {meta['author_name']}")
    if meta.get("article_title"):
        lines.append(f"- **文章标题**: {meta['article_title']}")
    if meta.get("error"):
        lines.append(f"- **抓取错误**: {meta['error']}")
    lines += ["", "---", "", "## 正文", "", body or "(无正文)", ""]
    if meta.get("media"):
        lines += ["## 媒体", ""]
        for m in meta["media"]:
            lines.append(f"- {m}")
        lines.append("")
    if meta.get("quoted"):
        lines += ["## 引用帖", "", meta["quoted"], ""]
    if meta.get("note"):
        lines += [f"> 备注: {meta['note']}", ""]
    return "\n".join(lines)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    jobs = manifest["jobs"]
    status_cache: dict[str, dict] = {}
    ok = 0
    fail = 0
    written = []

    # First download all unique status ids
    status_ids = sorted({j["id"] for j in jobs if j["type"] == "status"})
    print(f"Fetching {len(status_ids)} status posts...")
    for i, sid in enumerate(status_ids, 1):
        data = fetch_status(sid)
        status_cache[sid] = data
        code = data.get("code")
        print(f"  [{i}/{len(status_ids)}] {sid} code={code}")
        time.sleep(0.25)

    # Write each job
    for job in jobs:
        meta = {}
        body = ""
        if job["type"] == "status":
            data = status_cache.get(job["id"]) or fetch_status(job["id"])
            tweet = data.get("tweet") or {}
            if not tweet and data.get("error"):
                meta["error"] = data.get("error")
                body = f"(抓取失败: {data.get('error')})"
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
                text = tweet_text(tweet)
                # long posts sometimes only in article
                art = tweet.get("article")
                if art and not text.strip():
                    text = art.get("preview_text") or art.get("title") or ""
                    meta["note"] = "正文主要在关联 X Article 中，本文件为推广帖摘要；完整文章见同序号「是文章」文件。"
                body = text
                qt = tweet.get("quote") or tweet.get("quoted_tweet") or tweet.get("quoted")
                if isinstance(qt, dict):
                    qa = qt.get("author") or {}
                    qname = qa.get("screen_name") or qa.get("name") or ""
                    meta["quoted"] = f"@{qname}: {tweet_text(qt) or qt.get('text') or ''}"
                # if this status is itself labeled article without separate article id,
                # and has article payload, include full article body
                if job["kind"] == "article" and art:
                    full = article_blocks_to_md(art)
                    if full.strip():
                        body = full
                        meta["article_title"] = art.get("title")
                        meta["note"] = "该条目在榜单中标注为 Article；以下为文章全文（来自推广帖 API）。"
            path = ROOT / filename(job)
            path.write_text(render_md(job, body, meta), encoding="utf-8")
            written.append(path.name)
            ok += 1
        elif job["type"] == "article":
            # find article content from any related status
            art = None
            src_status = None
            for sid in job.get("status_ids") or []:
                data = status_cache.get(sid) or fetch_status(sid)
                tweet = data.get("tweet") or {}
                if tweet.get("article"):
                    art = tweet["article"]
                    src_status = sid
                    author = tweet.get("author") or {}
                    meta.update(
                        {
                            "url": f"https://x.com/i/article/{job['id']}",
                            "timestamp": art.get("created_at") or tweet.get("created_at"),
                            "views_live": tweet.get("views"),
                            "likes": tweet.get("likes"),
                            "retweets": tweet.get("retweets"),
                            "replies": tweet.get("replies"),
                            "bookmarks": tweet.get("bookmarks"),
                            "author_name": author.get("name") if isinstance(author, dict) else None,
                            "article_title": art.get("title"),
                            "note": f"文章正文自推广帖 status/{sid} 的 article 字段提取。",
                        }
                    )
                    break
            if not art:
                # try any status cache that matches article id
                for sid, data in status_cache.items():
                    tweet = (data or {}).get("tweet") or {}
                    a = tweet.get("article") or {}
                    if str(a.get("id")) == str(job["id"]):
                        art = a
                        src_status = sid
                        meta.update(
                            {
                                "url": f"https://x.com/i/article/{job['id']}",
                                "article_title": art.get("title"),
                                "views_live": tweet.get("views"),
                                "note": f"文章正文自 status/{sid} 提取。",
                            }
                        )
                        break
            if art:
                body = article_blocks_to_md(art)
            else:
                meta["error"] = "未能从推广帖提取文章正文"
                meta["url"] = f"https://x.com/i/article/{job['id']}"
                body = f"(未能提取文章全文)\n\nArticle: https://x.com/i/article/{job['id']}\n"
                fail += 1
            path = ROOT / filename(job)
            path.write_text(render_md(job, body, meta), encoding="utf-8")
            written.append(path.name)
            ok += 1

    index_lines = [
        "# Codex tips 下载索引",
        "",
        f"- 来源: `{manifest['source']}`",
        f"- 条目: {manifest['entries_count']}",
        f"- 文件任务: {manifest['jobs_count']}",
        f"- 已写入: {len(written)}",
        "",
        "| 文件 | 序号 | 浏览量 | 类型 | 作者 | 主题 |",
        "|---|---:|---:|---|---|---|",
    ]
    for job in jobs:
        name = filename(job)
        index_lines.append(
            f"| [{name}](./{name}) | {job['idx']} | {job['views']:,} | {type_tag(job['kind'])} | @{job['author']} | {job['topic'][:40]} |"
        )
    (ROOT / "00_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    summary = {
        "written": len(written),
        "ok": ok,
        "fail_article_extract": fail,
        "files": written,
    }
    (ROOT / "_download_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
