# -*- coding: utf-8 -*-
"""Write one post markdown from a JSON payload on stdin or argv path."""
import json
import re
import sys
from pathlib import Path

OUT = Path(r"H:\github\grok-x\codex-tips-posts-截止-2026-08-07-1032")


def safe(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\n\r\t]', "_", s)
    s = re.sub(r"_+", "_", s).strip(" ._")
    return s[:80] if s else "unknown"


def filename(job: dict) -> str:
    idx = job["idx"]
    views = job["views"]
    # 是否文章：article / promo-post / post
    kind = job["kind"]
    if kind == "article":
        type_tag = "是文章"
    elif kind == "promo-post":
        type_tag = "推广帖"
    else:
        type_tag = "普通帖"
    author = safe(job["author"])
    pid = job["id"]
    return f"{idx}_浏览{views}_{type_tag}_@{author}_{pid}.md"


def render(job: dict, payload: dict) -> str:
    views_list = job["views_raw"]
    views_live = payload.get("views_live")
    lines = [
        f"# {job['topic']}",
        "",
        f"- **序号**: {job['idx']}",
        f"- **榜单浏览量**: {views_list}（约 {job['views']:,}）",
        f"- **是否文章**: {'是' if job.get('entry_is_article') or job['kind'] == 'article' else '否'}",
        f"- **文件类型**: {job['kind']}",
        f"- **作者**: @{job['author']}",
        f"- **发布时间**: {job.get('date', '')}",
        f"- **语言**: {job.get('lang', '')}",
        f"- **分区**: {job.get('section', '')}",
        f"- **排名**: {job.get('rank') if job.get('rank') is not None else '扩展榜'}",
        f"- **Status ID**: {job['id'] if job['type']=='status' else '-'}",
        f"- **Article ID**: {job['id'] if job['type']=='article' else (','.join(job.get('article_ids') or []) or '-')}",
        f"- **链接**: {job.get('links', '')}",
    ]
    if views_live is not None:
        lines.append(f"- **实时浏览量(抓取时)**: {views_live:,}")
    for k in ("likes", "reposts", "replies", "bookmarks"):
        if payload.get(k) is not None:
            lines.append(f"- **{k}**: {payload[k]:,}" if isinstance(payload[k], int) else f"- **{k}**: {payload[k]}")
    if payload.get("timestamp"):
        lines.append(f"- **帖子时间**: {payload['timestamp']}")
    if payload.get("url"):
        lines.append(f"- **URL**: {payload['url']}")
    lines += ["", "---", "", "## 正文", ""]
    content = payload.get("content") or payload.get("error") or "(无正文)"
    lines.append(content)
    if payload.get("media"):
        lines += ["", "## 媒体", ""]
        for m in payload["media"]:
            lines.append(f"- {m}")
    if payload.get("quoted"):
        lines += ["", "## 引用帖", "", payload["quoted"]]
    if payload.get("thread"):
        lines += ["", "## 线程续帖", "", payload["thread"]]
    if payload.get("note"):
        lines += ["", f"> 备注: {payload['note']}"]
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        data = json.loads(sys.stdin.read())
    job = data["job"]
    payload = data.get("payload") or {}
    name = filename(job)
    path = OUT / name
    path.write_text(render(job, payload), encoding="utf-8")
    print(path.name)


if __name__ == "__main__":
    main()
