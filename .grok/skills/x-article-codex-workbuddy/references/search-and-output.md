# 检索式与输出模板

## 1. 严格 Article 检索

```text
# Codex
url:x.com/i/article (Codex OR "Codex CLI" OR "OpenAI Codex") since:YYYY-MM-DD
url:x.com/i/article Codex (agent OR CLI OR GPT OR skill OR security OR plugin)

# WorkBuddy
url:x.com/i/article (WorkBuddy OR workbuddy OR "workbuddy.ai") since:YYYY-MM-DD
url:x.com/i/article WorkBuddy (Hy3 OR 腾讯 OR Agent OR free OR 免费)

# 兜底
"x.com/i/article" (Codex OR WorkBuddy) since:YYYY-MM-DD
```

## 2. 错误检索（会混进普通帖）

```text
# 不要单独用这些当 Article 榜
Codex min_faves:50 since:YYYY-MM-DD
WorkBuddy free since:YYYY-MM-DD
```

## 3. 噪音排除清单

- Codex Granatensis / 中世纪写本
- Bridge Codex（足球）
- DNC Codex / Digimon
- 用户名含 Codex 但正文无关（如 SSI、日常杂谈）
- 口语 “work buddy”（非产品）

## 4. Markdown 输出（仅两张表，无其它章节）

```markdown
# Codex · X Article 流量 Top 10

| 排名 | 推广帖浏览 | 互动 | 语言 | 作者 | 文章主题 | Article 链接 | 推广帖 |
|:---:|---:|------|:---:|------|----------|-------------|--------|
| 1 | ... | ... | ... | ... | ... | [Article](...) | [帖](...) |

# WorkBuddy · X Article 流量 Top 10

| 排名 | 推广帖浏览 | 互动 | 语言 | 作者 | 文章主题 | Article 链接 | 推广帖 |
|:---:|---:|------|:---:|------|----------|-------------|--------|
| 1 | ... | ... | ... | ... | ... | [Article](...) | [帖](...) |
```

## 5. 文件命名

```text
codex-workbuddy-x-articles-top10-截止-YYYY-MM-DD-HHmm.md   # 严格 Article 榜单表
codex-workbuddy-x-posts-top10-截止-YYYY-MM-DD-HHmm.md      # 普通帖榜单表（仅用户明确要求时）
{topic}-x-top10-截止-YYYY-MM-DD-HHmm/                      # 下载正文时的文件夹（默认）
```

`topic` 为用户指定主题短名。下载正文时不要只写根目录单文件。

## 6. 截止时间

在 shell 中取本地时间：

```powershell
Get-Date -Format 'yyyy-MM-dd-HHmm'
```

## 7. 下载文件夹（正文）

用户要「下载」「建文件夹」「帖子内容」时，在项目根目录建：

```text
{topic}-x-top10-截止-YYYY-MM-DD-HHmm/
  00_INDEX.md
  A01_浏览{views}_是文章_@{handle}_{statusOrArticleId}.md
  P01_浏览{views}_普通帖_@{handle}_{statusId}.md
```

`00_INDEX.md` 含窗口/截止时间、文章数、普通帖数，以及链到各文件的表。

单篇 md：

```markdown
# {主题}

- **序号**: P01
- **榜单浏览量**: ...
- **是否文章**: 否
- **文件类型**: post
- **作者**: 显示名 @handle
- **语言**: 中
- **排名**: 1
- **Status ID**: ...
- **帖子**: https://x.com/{handle}/status/{id}
- **发布时间**: ...
- **实时浏览量(抓取时)**: ...
- **likes / retweets / replies / bookmarks / quotes**: ...

---

## 正文

...

## 引用帖

...

## 媒体

- photo/video: ...
```

