# Prompt 01 · 用 @Chrome 采集点赞 1 万+ 图文链接

先在 Chrome 登录小红书网页版，再把下面整段发给 Codex。一次只跑一个类目，目标 12–15 条，凑满 100 条再停。

```text
@Chrome

工作目录：./xiaohongshu-cover-lab
样本表：./templates/samples.csv（追加写入，不要覆盖已有行）

任务：在已经登录的小红书网页版里，采集「图文笔记」封面样本。
这是个人研究，只读不互动。

硬规则：
1. 只用当前 Chrome 登录态。不要新开无痕，不要退出登录。
2. 只收图文，不收视频、直播、商品卡、合集。
3. 点赞数必须 ≥ 10000。把「1万」「1.2万」「10万+」换算成整数后再判断。
4. 封面信息要完整：能看出标题或大字，不是纯明星海报、不是只有脸没有信息。
5. 不要靠明星 / 超大 IP 本身取胜的封面。
6. 不点赞、不收藏、不评论、不关注、不私信、不改搜索设置以外的账号资料。
7. 遇到验证码、风控、登录墙：立刻停，把屏幕状态写进 00_INDEX.md，等我处理。
8. 滚动要慢。每个关键词最多翻 4 屏。两条之间停 2–4 秒。
9. 去重：note_id 已在 samples.csv 里就跳过。
10. 链接必须是当前地址栏可重新打开的完整 URL。如果带 xsec_token / xsec_source，原样保存。
11. 本轮只做「当前类目」，目标 12–15 条有效样本，不要一次搜完全站。

本轮类目：{{CATEGORY}}
搜索词按顺序使用，每个词找到 2–4 条就换下一个：
{{KEYWORDS}}

操作步骤：
1. 打开 https://www.xiaohongshu.com
2. 确认已登录。未登录就停止。
3. 搜索第一个词，切换到「图文」。
4. 对每张卡片读取：封面大字、点赞数、笔记链接。
5. 打开笔记确认是图文、点赞仍 ≥ 10000、封面可分析。
6. 追加一行到 samples.csv。
7. 在 ./covers/_inbox.md 记下：id、标题、点赞、url。
8. 本轮结束时更新 ./00_INDEX.md：本轮类目、新增条数、累计条数、失败原因。

samples.csv 字段：
id,note_id,url,title_on_cover,likes_raw,likes,category,cover_file,author,has_face,has_number,skip_reason,collected_at

id 从现有最大编号 +1。cover_file 本轮先留空。
完成后只输出：新增 N 条、累计 M 条、被丢弃的原因 Top 3。
```
