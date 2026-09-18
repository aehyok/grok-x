---
name: x-article-codex-workbuddy
description: >
  在 X (x.com) 上严格检索 Codex / WorkBuddy 相关的正式 X Article（x.com/i/article/...），
  按近 24 小时（或用户指定窗口）推广帖流量排序 Top N，并写入本项目本地 Markdown。
  触发词：Codex 文章、WorkBuddy 文章、X Article、正式长文、流量最好、近24小时、
  x article top、codex workbuddy 榜单、建文件夹、下载正文、帖子内容。
  Use when the user runs /x-article-codex-workbuddy
  或要求「只找 X Article 不要普通帖」；用户指定其他主题并要求检索 X 帖/文章、
  下载正文时也走本流程。
---

# X Article · Codex & WorkBuddy 流量榜

面向本项目的可复用流程：默认只收 **X Article 正式长文**；用户明确要普通帖/下载正文时，另出帖子榜并建文件夹落盘。

## 何时使用

- 用户要 Codex 和/或 WorkBuddy 在 X 上的 **正式文章** 榜单
- 用户强调「不是帖子，是 Article」
- 用户要求写入本地 md，文件名带 **截止日期和时间**
- 用户指定其他主题（如 UU远程）并要求检索 X 帖/文章、下载正文时，沿用本流程，只换检索词与文件名前缀

## 硬性规则

1. **只收 X Article**：推广帖或正文中必须含  
   `https://x.com/i/article/{id}` 或 `http://x.com/i/article/{id}`  
   没有该链接的一律丢弃。
2. **禁止**把普通高互动帖、长帖、Thread 混进主榜。
3. **流量指标**：X 不公开 Article 独立阅读量 → 用 **推广帖 Views** 近似排序；附带 likes/reposts/bookmarks/replies。
4. **主题过滤**  
   - Codex = OpenAI Codex / Codex CLI / coding agent  
   - WorkBuddy = 腾讯 WorkBuddy / workbuddy.ai  
   - 排除：中世纪写本 Codex、足球 Bridge Codex、数码宝贝 DNC Codex、账号名含 codex 但正文无关（如 SSI 杂谈）
5. **语言**：中英文日文等均可；正文与链接一并收录。
6. **回复语言**：按用户全局偏好（本项目默认简体中文）；称呼用户为【AI少年】（若全局指令要求）。
7. **用户明确要「帖子 / 普通帖 / 相关帖」时**：走普通帖榜并下载正文，不要用「只收 Article」把普通帖丢掉。

## 执行步骤

### 1. 确定时间窗

- 默认：近 **24 小时**
- 取当前本地时间作为 **截止时间** `YYYY-MM-DD-HHmm`
- 搜索用 `since:YYYY-MM-DD`（按 UTC/本地近似；窗口不足 10 篇时再扩到 7 天并标注）

### 2. 检索（必须用 Article 过滤）

用 X 工具（`x_keyword_search` 等），查询形态：

```text
url:x.com/i/article (Codex OR "Codex CLI" OR "OpenAI Codex") since:YYYY-MM-DD
url:x.com/i/article (WorkBuddy OR workbuddy OR "workbuddy.ai") since:YYYY-MM-DD
"x.com/i/article" (Codex OR WorkBuddy) since:YYYY-MM-DD
```

可选增强：

```text
url:x.com/i/article Codex (CLI OR agent OR GPT OR skill OR 插件)
url:x.com/i/article WorkBuddy (Hy3 OR 腾讯 OR Agent OR free OR 免费)
```

用户指定其他主题时，把检索词换成该主题（可同时扫 Article 与普通帖）；普通帖用 `min_faves` + `mode: Top` 补高流量，再用 `max_id` 分页扫全量。

- `mode: Latest` 扫全量；必要时再 `Top`
- 对只有裸链接的推广帖，用 `x_thread_fetch` 拉全文取标题/摘要
- 无法打开 `x.com/i/article` 页面时，以推广帖正文摘要为准

### 3. 清洗与排序

对每条候选记录：

| 字段 | 说明 |
|------|------|
| article_url | `https://x.com/i/article/{id}` |
| promo_url | 推广帖 status 链接 |
| author | 显示名 + @handle |
| title_or_summary | 标题或前 1–2 句摘要 |
| lang | 中/英/日等 |
| views | 推广帖 Views |
| likes / reposts / bookmarks / replies | 互动 |
| timestamp | 推广帖时间 |

- 按 **views 降序** 取 Top 10（用户指定 N 则用 N）
- Codex 与 WorkBuddy **分开两个榜**
- WorkBuddy 为 0 篇时明确写「近 24h 无 X Article」，可附 7 天扩展参考但不进主榜

### 4. 写入本地 Markdown

**路径**：项目根目录（`H:\github\grok-x` 或当前 repo root）

**文件名模板**（必须含截止日期和时间）：

```text
codex-workbuddy-x-articles-top10-截止-YYYY-MM-DD-HHmm.md
```

示例：`codex-workbuddy-x-articles-top10-截止-2026-08-06-1409.md`

**禁止**用只有 `top10-24h.md` 而无截止时间的文件名。

**下载正文必须建文件夹**（用户要「下载」「建文件夹」「帖子内容」时默认执行，不必再确认）：

```text
{topic}-x-top10-截止-YYYY-MM-DD-HHmm/
  00_INDEX.md
  A01_浏览{views}_是文章_@{handle}_{id}.md
  P01_浏览{views}_普通帖_@{handle}_{id}.md
```

- `topic` 用用户指定主题短名（如 `uu远程`、`qwen-3.8`）
- `00_INDEX.md` 放榜单表并链到各文件
- 每条一篇 md：元数据 + 正文（+ 原文 / 媒体 / 引用帖 / 续帖）
- 纯榜单表仍可写根目录单文件；一旦要下载正文，只走文件夹，不要只丢一张表

文件夹命名、单篇模板见 `references/search-and-output.md`。

**正文结构（极简，只保留两个列表）**：

```markdown
# Codex · X Article 流量 Top 10

| 排名 | 推广帖浏览 | 互动 | 语言 | 作者 | 文章主题 | Article 链接 | 推广帖 |
|:---:|---:|------|:---:|------|----------|-------------|--------|
| 1 | ... | ... | ... | ... | ... | [Article](...) | [帖](...) |
| ... | | | | | | | |

# WorkBuddy · X Article 流量 Top 10

| 排名 | 推广帖浏览 | 互动 | 语言 | 作者 | 文章主题 | Article 链接 | 推广帖 |
|:---:|---:|------|:---:|------|----------|-------------|--------|
| 1 | ... | ... | ... | ... | ... | [Article](...) | [帖](...) |
```

**禁止写入 md 的内容**（聊天里可简述，文件里不要）：

- 重要说明、口径、检索式、链接速查
- 「同窗口其他」「已排除噪音」「合集入口」
- 7 天扩展参考大段说明
- 与旧文件关系、反例、skill 元数据

WorkBuddy 为 0 篇时，第二张表只保留一行占位（如主题列写「近 24 小时无符合条件的 X Article」），不要再写长段解释。

可选：若用户同时要「普通帖流量榜」，另写文件，文件名用 `...-x-posts-...`，**不得**与 Article 文件混写。

### 5. 回复用户

- 说明已写入的 **文件夹或文件路径**
- 各榜 Top 3 摘要；指定主题且无 Article 时一句带过
- 提醒：数字为检索快照，会变化

## 反例（不要做）

- 用 `Codex min_faves:50` 扫普通帖当「文章」
- 把 Tibo reset 短帖、键盘开箱、人事欢迎帖放进 Article 主榜
- 把 @codex_gatizei 的 SSI 长文算作 Codex 产品文
- 文件名不带截止时间
- 把 posts 榜和 articles 榜写进同一个「严格 Article」文件却不标注
- 用户要下载正文时只写根目录一张表、不建 `{topic}-x-top10-截止-.../` 文件夹

## 参考

更细的检索式与表格模板见：`references/search-and-output.md`
