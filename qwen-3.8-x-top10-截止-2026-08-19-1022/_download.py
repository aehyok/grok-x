# -*- coding: utf-8 -*-
"""Download Qwen 3.8 Top 10 articles + posts via fxtwitter."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "_raw"
RAW.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (compatible; qwen38-top10-downloader/1.0)"

ARTICLES = [
    {
        "rank": 1,
        "views": 120314,
        "lang": "英",
        "author": "0xBakeer",
        "author_name": "0xBakeer",
        "topic": "单台 DGX Spark：7.88 → 75 tok/s，16 路合计 256",
        "article_id": "2089076470865854466",
        "status_id": "2089090318905774558",
        "likes": 241,
        "reposts": 26,
        "bookmarks": 429,
        "replies": 10,
    },
    {
        "rank": 2,
        "views": 73533,
        "lang": "英",
        "author": "QwenDevs",
        "author_name": "Qwen Developers",
        "topic": "官方指南：reasoning 深度 + YaRN 扩到 1M + vLLM/SGLang/Unsloth 部署",
        "article_id": "2088276657245446144",
        "status_id": "2088289608031510811",
        "likes": 1173,
        "reposts": 102,
        "bookmarks": 928,
        "replies": 21,
    },
    {
        "rank": 3,
        "views": 28896,
        "lang": "日",
        "author": "fujikawa",
        "author_name": "藤川 忠彦",
        "topic": "实务周报：Claude Code / Qwen 用法、OpenRouter 与 Cursor",
        "article_id": "2089126424489902080",
        "status_id": "2089127156819599523",
        "likes": 8,
        "reposts": 1,
        "bookmarks": 1,
        "replies": 0,
    },
    {
        "rank": 4,
        "views": 26215,
        "lang": "英",
        "author": "no_stp_on_snek",
        "author_name": "Tom Turney",
        "topic": "升级但非跃迁：Qwen3.8 把 reasoning 拉满会破坏诚实性",
        "article_id": "2088373516962013184",
        "status_id": "2088375653162717680",
        "likes": 42,
        "reposts": 7,
        "bookmarks": 51,
        "replies": 13,
    },
    {
        "rank": 5,
        "views": 6030,
        "lang": "日",
        "author": "fujikawa",
        "author_name": "藤川 忠彦",
        "topic": "周报总览：Cursor 收购传闻、Gemini 3.7 Flash、Qwen 3.8",
        "article_id": "2088413575144763392",
        "status_id": "2088413825158742313",
        "likes": 11,
        "reposts": 0,
        "bookmarks": 0,
        "replies": 1,
    },
    {
        "rank": 6,
        "views": 4124,
        "lang": "英",
        "author": "ttunguz",
        "author_name": "Tomasz Tunguz",
        "topic": "笔记本级即可接近云端：把 Qwen3.8-27B 换进自己的 agent",
        "article_id": "1976764453166465024",
        "status_id": "2089761618259591354",
        "likes": 39,
        "reposts": 3,
        "bookmarks": 50,
        "replies": 3,
    },
    {
        "rank": 7,
        "views": 2491,
        "lang": "日",
        "author": "fujikawa",
        "author_name": "藤川 忠彦",
        "topic": "Cursor Origin / 本地 LLM：Qwen 等模型下的开发环境主导权",
        "article_id": "2089489623919804416",
        "status_id": "2089489914891301064",
        "likes": 4,
        "reposts": 0,
        "bookmarks": 0,
        "replies": 0,
    },
    {
        "rank": 8,
        "views": 2319,
        "lang": "日",
        "author": "superdoccimo",
        "author_name": "美濃加茂まむ",
        "topic": "从等模型到测模型：Qwen3.8-27B 要用自己的机器复现",
        "article_id": "2088419676095406080",
        "status_id": "2088431541689200807",
        "likes": 1,
        "reposts": 0,
        "bookmarks": 1,
        "replies": 0,
    },
    {
        "rank": 9,
        "views": 1852,
        "lang": "英",
        "author": "MichaelGannotti",
        "author_name": "Mike Gannotti",
        "topic": "Qwen3.8-27B 数学实测：Thinking On vs Off",
        "article_id": "2089282997027475456",
        "status_id": "2089283433688170961",
        "likes": 12,
        "reposts": 1,
        "bookmarks": 15,
        "replies": 1,
    },
    {
        "rank": 10,
        "views": 1344,
        "lang": "中",
        "author": "LiuweijiaVip",
        "author_name": "Wei佳",
        "topic": "M2 Max 本地跑 Qwen3.8 27B 有点吃力",
        "article_id": "2088656899449479168",
        "status_id": "2088667649089982898",
        "likes": 5,
        "reposts": 0,
        "bookmarks": 0,
        "replies": 3,
    },
]

POSTS = [
    {
        "rank": 1,
        "views": 7267181,
        "lang": "英",
        "author": "OrcaRouter",
        "author_name": "OrcaRouter",
        "topic": "发布 Qwen3.8-27B Uncensored FP8 权重（红队/安全研究）",
        "status_id": "2088527721282588852",
        "likes": 6944,
        "reposts": 645,
        "bookmarks": 6449,
        "replies": 125,
    },
    {
        "rank": 2,
        "views": 5394443,
        "lang": "英",
        "author": "Alibaba_Qwen",
        "author_name": "Qwen",
        "topic": "官方开源 Qwen3.8-27B + Qwen3.8-2.4T-A95B（Apache 2.0，262K/1M）",
        "status_id": "2088280182356611304",
        "likes": 15756,
        "reposts": 2116,
        "bookmarks": 4825,
        "replies": 814,
    },
    {
        "rank": 3,
        "views": 2371757,
        "lang": "英",
        "author": "OrcaRouter",
        "author_name": "OrcaRouter",
        "topic": "官方 Uncensored MLX：2/4/6/8-bit，Mac 本地无审查 27B",
        "status_id": "2089385980080148726",
        "likes": 5200,
        "reposts": 390,
        "bookmarks": 7665,
        "replies": 133,
    },
    {
        "rank": 4,
        "views": 1523234,
        "lang": "英",
        "author": "Alibaba_Qwen",
        "author_name": "Qwen",
        "topic": "官方续帖：Qwen3.8-27B 评测图（对标闭源旗舰）",
        "status_id": "2088280188362867185",
        "likes": 3293,
        "reposts": 304,
        "bookmarks": 869,
        "replies": 115,
    },
    {
        "rank": 5,
        "views": 1194887,
        "lang": "英",
        "author": "sudoingX",
        "author_name": "Sudo su",
        "topic": "传言：27B 本地打赢 Opus 4.6 Max 后 Anthropic CEO 求监管",
        "status_id": "2088551892901327198",
        "likes": 11566,
        "reposts": 597,
        "bookmarks": 2595,
        "replies": 368,
    },
    {
        "rank": 6,
        "views": 996799,
        "lang": "日",
        "author": "shimarin",
        "author_name": "嶋田大貴",
        "topic": "只想查 IP 摄像头口碑，本地 27B 却开始反汇编固件",
        "status_id": "2089663036475031802",
        "likes": 1292,
        "reposts": 189,
        "bookmarks": 356,
        "replies": 2,
    },
    {
        "rank": 7,
        "views": 977992,
        "lang": "英",
        "author": "UnslothAI",
        "author_name": "Unsloth AI",
        "topic": "17GB RAM 即可本地跑 Qwen3.8-27B（Dynamic GGUF + NVFP4）",
        "status_id": "2088281537427235320",
        "likes": 5116,
        "reposts": 617,
        "bookmarks": 2723,
        "replies": 197,
    },
    {
        "rank": 8,
        "views": 690914,
        "lang": "英",
        "author": "sgl_project",
        "author_name": "SGLang",
        "topic": "Day-0：单卡 5090 上 206 tok/s，DGX Spark 38 tok/s",
        "status_id": "2088281320422322413",
        "likes": 1119,
        "reposts": 126,
        "bookmarks": 767,
        "replies": 64,
    },
    {
        "rank": 9,
        "views": 666801,
        "lang": "英",
        "author": "lmstudio",
        "author_name": "LM Studio",
        "topic": "LM Studio 上架 Qwen3.8-27B：笔记本级、约 17GB 可跑",
        "status_id": "2088284427826643052",
        "likes": 4764,
        "reposts": 407,
        "bookmarks": 1686,
        "replies": 123,
    },
    {
        "rank": 10,
        "views": 474484,
        "lang": "英",
        "author": "0xkydo",
        "author_name": "Kydo",
        "topic": "mlxfast：Apple Silicon 上密集 27B 相对基线 +153% / MTP 2.5×",
        "status_id": "2088709460701458437",
        "likes": 1479,
        "reposts": 110,
        "bookmarks": 1425,
        "replies": 76,
    },
]


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


def apply_inline(text: str, styles: list, entities: list, entity_map: dict) -> str:
    marks = []
    for st in styles or []:
        start = int(st.get("offset") or 0)
        end = start + int(st.get("length") or 0)
        style = (st.get("style") or "").lower()
        if style in ("bold", "italic", "code"):
            marks.append((start, end, style))
    links = []
    for er in entities or []:
        ent = entity_map.get(str(er.get("key")))
        if not ent:
            continue
        data = ent.get("data") or {}
        if "value" in ent and isinstance(ent.get("value"), dict):
            et = ent["value"].get("type") or ent.get("type")
            data = ent["value"].get("data") or data
        else:
            et = ent.get("type")
        if et == "LINK" and data.get("url"):
            start = int(er.get("offset") or 0)
            end = start + int(er.get("length") or 0)
            links.append((start, end, data["url"]))
    if not marks and not links:
        return text
    events = []
    for start, end, style in marks:
        wrap = {"bold": "**", "italic": "*", "code": "`"}[style]
        events.append((start, 0, wrap))
        events.append((end, 1, wrap))
    for start, end, url in links:
        events.append((start, 0, "["))
        events.append((end, 1, f"]({url})"))
    events.sort(key=lambda x: (x[0], x[1]))
    out = []
    last = 0
    for pos, _kind, token in events:
        if pos > last:
            out.append(text[last:pos])
        out.append(token)
        last = pos
    out.append(text[last:])
    return "".join(out)


def article_blocks_to_md(article: dict) -> str:
    if not article:
        return ""
    lines = []
    if article.get("title"):
        lines += [f"# {article['title']}", ""]
    if article.get("preview_text"):
        lines += [f"> {article['preview_text']}", ""]
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

    list_buf = []
    list_kind = None

    def flush_list():
        nonlocal list_buf, list_kind
        if list_buf:
            lines.extend(list_buf)
            lines.append("")
        list_buf = []
        list_kind = None

    for b in blocks:
        btype = b.get("type") or "unstyled"
        text = apply_inline(
            b.get("text") or "",
            b.get("inlineStyleRanges") or [],
            b.get("entityRanges") or [],
            entity_map,
        )
        if btype not in ("unordered-list-item", "ordered-list-item"):
            flush_list()
        if btype == "header-one":
            lines += [f"# {text}", ""]
        elif btype == "header-two":
            lines += [f"## {text}", ""]
        elif btype == "header-three":
            lines += [f"### {text}", ""]
        elif btype == "blockquote":
            for ln in (text.splitlines() or [""]):
                lines.append(f"> {ln}")
            lines.append("")
        elif btype == "unordered-list-item":
            if list_kind != "ul":
                flush_list()
                list_kind = "ul"
            list_buf.append(f"- {text}")
        elif btype == "ordered-list-item":
            if list_kind != "ol":
                flush_list()
                list_kind = "ol"
            list_buf.append(f"{len(list_buf) + 1}. {text}")
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
                    label = text or data.get("url")
                    lines.append(f"[{label}]({data['url']})")
                elif et in ("IMAGE", "MEDIA") or data.get("src") or data.get("url"):
                    src = data.get("src") or data.get("url") or data.get("original_img_url")
                    if src:
                        lines.append(f"![]({src})")
        else:
            if text.strip():
                lines += [text, ""]
    flush_list()
    cover = ((article.get("cover_media") or {}).get("media_info") or {}).get("original_img_url")
    if cover:
        lines += ["", f"![cover]({cover})"]
    for me in article.get("media_entities") or []:
        u = ((me.get("media_info") or {}).get("original_img_url"))
        if u:
            lines.append(f"![]({u})")
    return "\n".join(lines).strip() + "\n"


def fmt_num(v):
    try:
        return f"{int(v):,}"
    except Exception:
        return str(v)


def header_lines(kind: str, item: dict, tweet: dict, extra: dict) -> list[str]:
    author = tweet.get("author") or {}
    display = extra.get("author_name") or item["author_name"]
    handle = author.get("screen_name") or item["author"]
    lines = [
        f"# {extra.get('title') or item['topic']}",
        "",
        f"- **序号**: {kind}{item['rank']:02d}",
        f"- **榜单浏览量**: {fmt_num(item['views'])}",
        f"- **是否文章**: {'是' if kind == 'A' else '否'}",
        f"- **文件类型**: {'article' if kind == 'A' else 'post'}",
        f"- **作者**: {display} - @{handle}",
        f"- **语言**: {item['lang']}",
        f"- **排名**: {item['rank']}",
    ]
    if kind == "A":
        lines += [
            f"- **Article ID**: {item['article_id']}",
            f"- **关联 Status**: {item['status_id']}",
            f"- **Article 链接**: https://x.com/i/article/{item['article_id']}",
            f"- **推广帖**: https://x.com/{handle}/status/{item['status_id']}",
        ]
    else:
        lines += [
            f"- **Status ID**: {item['status_id']}",
            f"- **帖子**: https://x.com/{handle}/status/{item['status_id']}",
        ]
    if extra.get("timestamp"):
        lines.append(f"- **发布时间**: {extra['timestamp']}")
    if extra.get("views_live") is not None:
        lines.append(f"- **实时浏览量(抓取时)**: {fmt_num(extra['views_live'])}")
    for k in ("likes", "retweets", "replies", "bookmarks", "quotes"):
        if extra.get(k) is not None:
            lines.append(f"- **{k}**: {fmt_num(extra[k])}")
    if extra.get("error"):
        lines.append(f"- **抓取错误**: {extra['error']}")
    if extra.get("note"):
        lines.append(f"- **备注**: {extra['note']}")
    return lines


def write_md(path: Path, header: list[str], body: str, tweet: dict):
    parts = header + ["", "---", "", "## 正文", "", body.strip() or "(无正文)", ""]
    media = media_list(tweet)
    if media:
        parts += ["## 媒体", ""]
        for m in media:
            parts.append(f"- {m}")
        parts.append("")
    qt = tweet.get("quote") or tweet.get("quoted_tweet") or tweet.get("quoted")
    if isinstance(qt, dict):
        qa = qt.get("author") or {}
        handle = qa.get("screen_name") or ""
        parts += [
            "## 引用帖",
            "",
            f"**@{handle}** · {qt.get('url') or ''}",
            "",
            tweet_text(qt) or "(无正文)",
            "",
        ]
    path.write_text("\n".join(parts), encoding="utf-8")


def extra_from_tweet(tweet: dict) -> dict:
    return {
        "timestamp": tweet.get("created_at") or tweet.get("date"),
        "views_live": tweet.get("views"),
        "likes": tweet.get("likes"),
        "retweets": tweet.get("retweets"),
        "replies": tweet.get("replies"),
        "bookmarks": tweet.get("bookmarks"),
        "quotes": tweet.get("quotes"),
        "author_name": (tweet.get("author") or {}).get("name"),
    }


def main():
    status_ids = [a["status_id"] for a in ARTICLES] + [p["status_id"] for p in POSTS]
    cache = {}
    print(f"Fetching {len(status_ids)} statuses...")
    for i, sid in enumerate(status_ids, 1):
        data = fetch_status(sid)
        cache[sid] = data
        tweet = data.get("tweet") or {}
        art = tweet.get("article") or {}
        print(
            f"  [{i}/{len(status_ids)}] {sid} code={data.get('code')} "
            f"blocks={len(((art.get('content') or {}).get('blocks') or []))}"
        )
        time.sleep(0.15)

    written = []
    fail = 0
    for item in ARTICLES:
        data = cache.get(item["status_id"]) or {}
        tweet = data.get("tweet") or {}
        extra = extra_from_tweet(tweet) if tweet else {"error": data.get("error") or "no tweet"}
        art = tweet.get("article") if tweet else None
        if art and str(art.get("id")) != str(item["article_id"]):
            extra["note"] = (
                f"推广帖关联 Article {art.get('id')}，榜单 Article 为 {item['article_id']}"
            )
        if art:
            body = article_blocks_to_md(art)
            extra["title"] = art.get("title")
            extra["note"] = (extra.get("note") + "；" if extra.get("note") else "") + (
                f"文章正文自推广帖 status/{item['status_id']} 提取"
            )
            if not body.strip():
                fail += 1
                extra["error"] = "文章 blocks 为空"
                body = tweet_text(tweet)
        else:
            fail += 1
            extra["error"] = extra.get("error") or "未能提取文章全文"
            body = tweet_text(tweet) or f"(未能提取)\n\nhttps://x.com/i/article/{item['article_id']}\n"
        name = f"A{item['rank']:02d}_浏览{item['views']}_是文章_@{item['author']}_{item['article_id']}.md"
        write_md(ROOT / name, header_lines("A", item, tweet, extra), body, tweet)
        written.append(name)

    for item in POSTS:
        data = cache.get(item["status_id"]) or {}
        tweet = data.get("tweet") or {}
        extra = extra_from_tweet(tweet) if tweet else {"error": data.get("error") or "no tweet"}
        if not tweet:
            fail += 1
            body = f"(抓取失败: {extra['error']})"
        else:
            body = tweet_text(tweet)
        name = f"P{item['rank']:02d}_浏览{item['views']}_普通帖_@{item['author']}_{item['status_id']}.md"
        write_md(ROOT / name, header_lines("P", item, tweet, extra), body, tweet)
        written.append(name)

    idx = [
        "# Qwen 3.8 · X Top 10 下载索引",
        "",
        "窗口：2026-08-12 ~ 2026-08-19 10:22 · 截止：2026-08-19 10:22",
        "",
        f"- 文章：{len(ARTICLES)}",
        f"- 普通帖：{len(POSTS)}",
        f"- 已写入：{len(written)}",
        f"- 失败近似：{fail}",
        "",
        "## Article",
        "",
        "| 文件 | 排名 | 浏览 | 作者 | 主题 |",
        "|---|---:|---:|---|---|",
    ]
    for item in ARTICLES:
        name = f"A{item['rank']:02d}_浏览{item['views']}_是文章_@{item['author']}_{item['article_id']}.md"
        idx.append(
            f"| [{name}](./{name}) | {item['rank']} | {item['views']:,} | @{item['author']} | {item['topic']} |"
        )
    idx += [
        "",
        "## 普通帖",
        "",
        "| 文件 | 排名 | 浏览 | 作者 | 主题 |",
        "|---|---:|---:|---|---|",
    ]
    for item in POSTS:
        name = f"P{item['rank']:02d}_浏览{item['views']}_普通帖_@{item['author']}_{item['status_id']}.md"
        idx.append(
            f"| [{name}](./{name}) | {item['rank']} | {item['views']:,} | @{item['author']} | {item['topic']} |"
        )
    (ROOT / "00_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    summary = {"written": len(written), "fail": fail, "files": written}
    (ROOT / "_download_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
