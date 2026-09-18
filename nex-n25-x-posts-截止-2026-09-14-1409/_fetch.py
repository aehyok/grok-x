# -*- coding: utf-8 -*-
"""Fetch full tweet JSON + photos from fxtwitter, then render markdown archives."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "_raw"
MEDIA = ROOT / "_media"
RAW.mkdir(exist_ok=True)
MEDIA.mkdir(exist_ok=True)

UA = "Mozilla/5.0 (compatible; nex-n25-post-downloader/1.0)"
FETCH_AT = "2026-09-14 14:09 CST"

HOOKS = {
    "2099350645497364592": "Astra 额度不够，Nex-2.5-Pro 接 Blender MCP 做游戏建模",
    "2099343167644725647": "客餐厅图推进成可交互 3D 模型",
    "2099337229982421253": "Space Invaders 六模型盲测，Nex 在 B 位",
    "2099120171994501575": "Nex 接 Zcode 实测 Computer Use 打开 Blender",
    "2099038178753573027": "六轮破坏测试：它说 6 tests passed，测试是红的",
    "2099026372484341910": "Pi + Blender MCP 做鹈鹕骑车，再一句话做成动画",
    "2098999471199945167": "小白用 AI 全自动做 Google 广告站赚美金",
    "2098812240069787948": "从 0 手搓可玩 3D 趣味闯关游戏",
    "2098660483016593490": "OpenRouter 新免费模型鹈鹕对比 + Mini 本地 50 tk/s",
    "2098658544065171807": "锁鲜枸杞：不会编程也能做成时间互动页",
    "2098593615585140923": "雾海上的旅人变成能玩的小游戏",
    "2098570136588570674": "名画变成电影，下一刀怎么剪",
    "2098567332406915522": "大象骑滑板车 SVG 三模型对比",
    "2098410976533987362": "低调对标 Astra：搭出可调光虚拟摄影棚",
    "2098360464799592732": "Three.js 网页 3D Logo：NEX 金属字",
    "2098317357353677133": "一句话让 Nex 打开 Blender 建机械臂",
    "2098286819326714349": "WorkBuddy + Nex 枪战闯关，群友打到 12 关",
    "2098281328945049621": "不懂代码也能让 AI 干活赚钱",
    "2098267288114000134": "Blender MCP 工业 Loft：1113 对象六段推进",
    "2098220638909722815": "一张 2D 蓝图复刻席尔弗顿铁路蒸汽机车",
    "2098192976761729279": "画橘猫 SVG 先被 token 坑了两回",
    "2098152649380278501": "Nex-N2.5 Pro 实测：从回答到执行",
    "2098101813883080989": "Nex Mini 35B：文档识别 token 只要十分之一",
    "2098040991869771881": "订单报价测算器实测：不是程序员也能用",
    "2097998014875074781": "开源 Agent 开始能工作：Blender / Pokémon / 前端",
    "2097968067552665780": "看懂屏幕再操作电脑：三档选型与本地部署",
    "2097958358036980031": "手摇拖拉机可玩 3D 游戏，已开源可试玩",
    "2097956824184218037": "真实操作 Blender 与 CAD：Computer Use 工程边界",
    "2097954702017315121": "对标 Astra 的 397B 多模态：写出来变成用得了",
    "2097919160189919678": "CAD Agent 从零建模机械臂，交付 SolidWorks",
}


def http_get(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_status(sid: str) -> dict:
    cache = RAW / f"status_{sid}.json"
    if cache.exists() and cache.stat().st_size > 80:
        return json.loads(cache.read_text(encoding="utf-8"))
    url = f"https://api.fxtwitter.com/status/{sid}"
    last = None
    for attempt in range(5):
        try:
            data = json.loads(http_get(url).decode("utf-8", errors="replace"))
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data
        except Exception as e:
            last = e
            time.sleep(1.4 * (attempt + 1))
    err = {"error": str(last), "tweet_id": sid}
    cache.write_text(json.dumps(err, ensure_ascii=False, indent=2), encoding="utf-8")
    return err


def ext_from_url(url: str, fallback: str = ".bin") -> str:
    path = url.split("?")[0].rsplit("/", 1)[-1]
    if "." in path:
        ext = "." + path.rsplit(".", 1)[-1].lower()
        if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov"}:
            return ".jpg" if ext == ".jpeg" else ext
    return fallback


def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 20:
        return True
    try:
        data = http_get(url, timeout=90)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def collect_media(tweet: dict) -> list[dict]:
    media = tweet.get("media") or {}
    items = media.get("all") or []
    out = []
    for m in items:
        kind = (m.get("type") or "photo").lower()
        url = m.get("url") or ""
        thumb = m.get("thumbnail_url") or m.get("thumbnail") or ""
        if kind == "photo" and not url:
            url = thumb
        out.append(
            {
                "type": kind,
                "url": url,
                "thumbnail_url": thumb,
                "duration": m.get("duration"),
                "width": m.get("width"),
                "height": m.get("height"),
            }
        )
    return out


def author_replies_from_fxtwitter(data: dict, screen: str) -> list[dict]:
    """Best-effort: some fxtwitter payloads include thread / conversation."""
    tweet = data.get("tweet") or {}
    replies = []
    for key in ("thread", "conversation", "replies_list"):
        block = tweet.get(key) or data.get(key)
        if isinstance(block, list):
            for item in block:
                if not isinstance(item, dict):
                    continue
                a = ((item.get("author") or {}).get("screen_name")) or item.get("screen_name")
                text = item.get("text") or ""
                tid = str(item.get("id") or "")
                if text:
                    replies.append({"id": tid, "author": a or "", "text": text, "url": item.get("url") or ""})
    return replies


def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", s)


def fmt_int(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n or 0)


def first_line(text: str) -> str:
    for line in (text or "").splitlines():
        t = line.strip()
        if t:
            return t[:80]
    return ""


def render_one(rank: int, src: dict, data: dict, extra_thread: list[dict], full_text_override: str = "") -> str:
    sid = src["tweet_id"]
    tweet = data.get("tweet") or {}
    author = tweet.get("author") or {}
    handle = author.get("screen_name") or src["username"]
    name = author.get("name") or handle
    url = tweet.get("url") or src["post_url"]
    live_text = (tweet.get("text") or "").strip()
    input_text = (src.get("full_text") or "").strip()
    override = (full_text_override or "").strip()
    body = max([live_text, input_text, override], key=len)
    article_url = ""
    for blob in (live_text, input_text, json.dumps(tweet.get("raw_text") or {}, ensure_ascii=False)):
        m = re.search(r"https://x\.com/i/article/\d+", blob)
        if m:
            article_url = m.group(0)
            break
    views = tweet.get("views") if tweet.get("views") is not None else src.get("view_count")
    likes = tweet.get("likes") if tweet.get("likes") is not None else src.get("like_count")
    rts = tweet.get("retweets") if tweet.get("retweets") is not None else src.get("retweet_count")
    quotes = tweet.get("quotes") if tweet.get("quotes") is not None else src.get("quote_count")
    replies = tweet.get("replies") if tweet.get("replies") is not None else src.get("reply_count")
    bookmarks = tweet.get("bookmarks")
    created = tweet.get("created_at") or src.get("post_created_at")
    is_note = bool(tweet.get("is_note_tweet") or article_url)
    hook = HOOKS.get(sid) or first_line(body)
    media_items = collect_media(tweet)
    prefix = f"P{rank:02d}"
    local_media_lines = []
    for i, m in enumerate(media_items, 1):
        kind = m["type"]
        remote = m["url"]
        thumb = m.get("thumbnail_url") or ""
        if kind == "photo" and remote:
            ext = ext_from_url(remote, ".jpg")
            dest = MEDIA / f"{prefix}_{sid}_p{i}{ext}"
            ok = download_file(remote, dest)
            rel = f"./_media/{dest.name}"
            if ok:
                local_media_lines.append(f"- photo: [{rel}]({rel})\n  - 原链: {remote}")
            else:
                local_media_lines.append(f"- photo: {remote}")
        elif kind in {"video", "gif"}:
            if thumb:
                ext = ext_from_url(thumb, ".jpg")
                dest = MEDIA / f"{prefix}_{sid}_p{i}_thumb{ext}"
                ok = download_file(thumb, dest)
                rel = f"./_media/{dest.name}"
                thumb_md = f"[{rel}]({rel})" if ok else thumb
            else:
                thumb_md = ""
            dur = m.get("duration")
            dur_s = f" · {dur}s" if dur else ""
            local_media_lines.append(
                f"- {kind}{dur_s}: {remote}" + (f"\n  - 封面: {thumb_md}" if thumb_md else "")
            )
        else:
            local_media_lines.append(f"- {kind}: {remote}")

    quote = tweet.get("quote") or {}
    quote_block = ""
    if quote:
        q_author = (quote.get("author") or {}).get("screen_name") or ""
        q_text = (quote.get("text") or "").strip()
        q_url = quote.get("url") or ""
        quote_block = f"\n## 引用帖\n\n- 作者: @{q_author}\n- 链接: {q_url}\n\n{q_text}\n"

    thread_bits = extra_thread[:]
    thread_bits.extend(author_replies_from_fxtwitter(data, handle))
    seen = set()
    uniq_thread = []
    for item in thread_bits:
        key = (item.get("id") or "") + "|" + (item.get("text") or "")[:40]
        if key in seen:
            continue
        seen.add(key)
        if (item.get("text") or "").strip() == body.strip():
            continue
        uniq_thread.append(item)

    thread_md = ""
    if uniq_thread:
        lines = ["\n## 续帖 / 作者补充\n"]
        for i, item in enumerate(uniq_thread, 1):
            a = item.get("author") or handle
            u = item.get("url") or (f"https://x.com/{a}/status/{item['id']}" if item.get("id") else "")
            lines.append(f"{i}. {u}\n")
            lines.append((item.get("text") or "").strip() + "\n")
        thread_md = "\n".join(lines)

    article_flag = "是" if is_note else "否"
    file_type = "article" if is_note else "post"
    md = f"""# {hook}

- **序号**: {prefix}
- **是否文章**: {article_flag}
- **文件类型**: {file_type}
- **作者**: {name} @{handle}
- **排名(按浏览)**: {rank}
- **Status ID**: {sid}
- **帖子**: {url}
- **发布时间**: {created}
- **抓取时间**: {FETCH_AT}
- **浏览**: {fmt_int(views)}
- **likes**: {fmt_int(likes)}
- **retweets**: {fmt_int(rts)}
- **replies**: {fmt_int(replies)}
- **bookmarks**: {fmt_int(bookmarks) if bookmarks is not None else "—"}
- **quotes**: {fmt_int(quotes)}
- **原始列表浏览**: {fmt_int(src.get("view_count"))}
- **boosted_by_me**: {src.get("boosted_by_me")}
- **my_boost_count**: {src.get("my_boost_count")}
- **X Article**: {article_url or "否"}

---

## 正文

{body}
{quote_block}{thread_md}
## 媒体

{chr(10).join(local_media_lines) if local_media_lines else "（无）"}

## 原始链接

{url}
"""
    fname = f"{prefix}_浏览{int(src.get('view_count') or views or 0)}_{'是文章' if is_note else '普通帖'}_@{handle}_{sid}.md"
    return safe_name(fname), md, {
        "file": fname,
        "rank": rank,
        "sid": sid,
        "handle": handle,
        "name": name,
        "url": url,
        "views": int(src.get("view_count") or 0),
        "live_views": views,
        "likes": src.get("like_count"),
        "retweets": src.get("retweet_count"),
        "quotes": src.get("quote_count"),
        "replies": src.get("reply_count"),
        "hook": hook,
        "is_note": is_note,
        "boosted": bool(src.get("boosted_by_me")),
        "media_count": len(media_items),
        "text_len": len(body),
        "ok": data.get("code") == 200 or bool(tweet),
    }


def load_json(name: str, default):
    path = RAW / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_extra_threads() -> dict[str, list[dict]]:
    return load_json("extra_threads.json", {})


def load_full_texts() -> dict[str, str]:
    return load_json("full_texts.json", {})


def main() -> None:
    posts = json.loads((RAW / "input_posts.json").read_text(encoding="utf-8"))
    posts_sorted = sorted(posts, key=lambda p: int(p.get("view_count") or 0), reverse=True)
    extra = load_extra_threads()
    full_texts = load_full_texts()
    index_rows = []
    fail = 0
    for i, src in enumerate(posts_sorted, 1):
        sid = src["tweet_id"]
        data = fetch_status(sid)
        tweet = data.get("tweet") or {}
        print(
            f"[{i:02d}/{len(posts_sorted)}] {sid} @{src['username']} "
            f"code={data.get('code')} text={len((tweet.get('text') or ''))} "
            f"media={len(((tweet.get('media') or {}).get('all') or []))}"
        )
        if not tweet:
            fail += 1
        fname, md, meta = render_one(i, src, data, extra.get(sid, []), full_texts.get(sid, ""))
        for old in ROOT.glob(f"P{i:02d}_*.md"):
            if old.name != fname:
                old.unlink()
        (ROOT / fname).write_text(md, encoding="utf-8")
        index_rows.append(meta)
        time.sleep(0.2)

    lines = [
        "# Nex-N2.5 相关 X 帖 · 全文归档",
        "",
        f"样本：用户给定 **{len(posts)}** 条 · 截止抓取 **{FETCH_AT}** · fxtwitter 失败 {fail}",
        "",
        "排序：文件名 `P01…P30` 按用户提供的 **浏览（曝光）** 降序，和本仓库其他截流目录一致。",
        "正文优先用线上抓取全文；若线上短于原始列表，则回退原始 `full_text`。",
        "图片已下载到 `_media/`；视频只保存直链和封面，避免体积过大。",
        "",
        "---",
        "",
        "## 索引（浏览降序）",
        "",
        "| 文件 | 浏览 | 赞 | 转 | 引 | 评 | 作者 | 钩子 |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in index_rows:
        flag = " ★已助推" if r["boosted"] else ""
        lines.append(
            f"| [{r['file']}](./{r['file']}) | {r['views']:,} | {r['likes']} | {r['retweets']} | "
            f"{r['quotes']} | {r['replies']} | @{r['handle']}{flag} | {r['hook']} |"
        )
    total_views = sum(r["views"] for r in index_rows)
    total_likes = sum(int(r["likes"] or 0) for r in index_rows)
    total_rt = sum(int(r["retweets"] or 0) for r in index_rows)
    total_q = sum(int(r["quotes"] or 0) for r in index_rows)
    total_rp = sum(int(r["replies"] or 0) for r in index_rows)
    lines += [
        "",
        f"合计浏览 **{total_views:,}** · 合计赞 {total_likes:,} / 转 {total_rt:,} / 引 {total_q:,} / 评 {total_rp:,}",
        "",
        "## 原始链接清单",
        "",
    ]
    for src in posts:
        lines.append(f"- https://x.com/{src['username']}/status/{src['tweet_id']}")
    (ROOT / "00_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (RAW / "index_meta.json").write_text(
        json.dumps(index_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"DONE fail={fail} files={len(index_rows)}")


if __name__ == "__main__":
    main()
