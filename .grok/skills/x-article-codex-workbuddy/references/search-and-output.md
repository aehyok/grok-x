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
codex-workbuddy-x-articles-top10-截止-YYYY-MM-DD-HHmm.md   # 严格 Article
codex-workbuddy-x-posts-top10-截止-YYYY-MM-DD-HHmm.md      # 普通帖（仅用户明确要求时）
```

## 6. 截止时间

在 shell 中取本地时间：

```powershell
Get-Date -Format 'yyyy-MM-dd-HHmm'
```
