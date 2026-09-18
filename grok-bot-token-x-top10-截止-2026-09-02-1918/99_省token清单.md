# Grok Bot 省 Token 清单

来源：`grok-bot-token-x-top10-截止-2026-09-02-1918/` 内 10 帖 + 6 篇 Article。  
口径：Grok Bot、Grok app、Cursor / Codex / Claude Code 是**分开的额度池**。Bot 池最薄，经不起编码循环和浏览器连点。

**一句话：Bot 当包工头，不自己搬砖；一件事一个干净上下文；有真事才叫醒。**

---

## 1. 角色：Bot 只派活

1. 改仓库、写补丁、跑测试，不要在 Bot 聊天里做。丢给 Cursor Cloud Agent / Cursor CLI / Grok Build CLI / Codex / Claude Code。
2. Bot 只写：目标、约束、完成定义（建议不超过 8 行），然后等人带回 PR / 测试结果 / 短摘要。
3. 云电脑装好 CLI 后，写死一条规则：「复杂任务或编程，用云电脑上的 Codex / Claude Code / Cursor / Grok Build 完成，做完再汇报。」做成 skill 比口头说一次更稳。
4. 可选再装 Herdr，专门管这些 CLI 会话。电脑合上，活还在云上跑。
5. 一次只派一个工人。别为了「对比」同时开两个 Agent 打同一补丁——两份 diff、双倍 token。
6. Bot 不要偷看工人跑、不要直播进度、不要把补丁再用更干净的词重写一遍（那是第二次实现）。
7. 简单问答走普通 Grok 聊天；编码走 CLI / Cloud Agent；Bot 只接要多工具、要协调的活。

## 2. 上下文：一件事一个频道

8. 专项任务让 Bot **新建频道**，做完关掉。Elon 引用过这条，也预告了官方自动优化。
9. 别把一条对话用到无限长。routine 每次醒来都会把整段历史再送一遍。
10. 要复用同一任务：把短复盘存进仓库，下次从文件起，不要从旧聊天起。
11. 重要指令和知识放 `.md`，不要只堆在聊天里。Agent 可丢弃，文件要留下。
12. 重复活、定时早报不要挂在主助手的长对话上。主对话只留正在干的事。

## 3. 定时任务：少叫醒、叫醒要干净

13. 定时不要密于每小时。15 分钟一次，一天能跑近 100 次。早报一天一次通常够。
14. 能用事件触发就别轮询（Slack / GitHub / 反应）。没变化也跑，纯烧额度。
15. 事件过滤写窄：指定频道 + 关键词，不要「任何消息都醒」。
16. 一次性 watch / 过期 routine **立刻删**。到 Bot → 对话详情 → Routines 定期清。
17. 新建 routine 必须挂在**新对话**上。挂在长聊天上，每次都会重送全部历史。这是 yunta 说的「多数人 token 问题的真凶」。

## 4. 工具路径：浏览器最贵

18. 有 connector / 官方插件，就不要开浏览器。浏览器 = 点击 + 截图 + 多步，最烧。
19. 同一套网页操作要重复跑：先 computer-use **抓一次**网络请求，下次用同一鉴权直接打 API 脚本。
20. 定期查一个 API，用小脚本，不必上完整 skill；也别打太勤。
21. 能交给 Imagine / 语音的，让 Bot 只转向，不要自己生成长内容。
22. Skill 写短、只干一件事。描述里写清路径，例如 `Skills are in /skills folder`，省得它满盘找。

## 5. 指令：清楚但短，卡住就停

23. 指令不要为了省 token 写到含糊。多几行决策标准，往往比迷路、重试更省。
24. 每条 Bot 描述写上：卡住立刻停并通知人；同一失败步骤最多重试两次。
25. 改之前先展示变更；没新东西就闭嘴；限制输出，不写日记。
26. 一直迭代却不交付：砍循环，别让它「再试一次」。
27. 可让「老板 Bot」审计各 Bot 的用量和指令。有人靠这个把单个 Bot 用量砍到约 20%。人觉得高效的步骤，对 Bot 可能很贵。

## 6. 团队：别开全员频道

28. 默认 1 个 Bot、1 份活。职责装了两套词汇再拆。
29. 派活用 **1:1**。全员频道一条消息会叫醒所有人：5 个 Bot = 5 轮同时跑。
30. 频道只留给全队必须听到的事。记录放共享板 / 日志，不要在频道里广播「我已经记过了」。
31. 真正收口的是专家，就直接跟专家说。经过协调者 = 同一张票走两轮。
32. 记忆当写入过滤器：PROFILE 只放稳定身份和车道规则；SHARED 不进工作笔记、会议残渣、任务列表。
33. 两个协调者不能盯同一频道，否则死循环。Slack 场景里：**标签选工人**（@Cursor 编码，Bot 只看不抢 tag）。

## 7. 账单：分清几块表

34. 长活之前先看 Settings → Usage。Mac / iOS 共用 Bot 周池。
35. 周额度用完可能进 On-Demand，从绑的卡扣费。需要的话在账单页把超额上限设为 `$0`。
36. 连 X 之后，读帖/搜帖走的是 **付费 X API**，不是 Bot 周额度。查自己免费；读帖几美分；搜帖更贵。贵操作会先报估算，看完再确认。
37. Grok app、Grok Bot、Cursor 三池分开。Bot 撞墙时，把仓库交接到另一池，并写清「已经试过什么」，避免对方用自己的额度再踩同一死路。
38. 官方预告会做自动 token 优化；在那之前，上面这些仍靠自己管。

---

## 可粘贴：Bot 描述 / Skill

```
ALWAYS
- 你是协调者，不是编码工人。
- 编程/改仓库：派给云电脑上的 Cursor CLI / Grok Build / Codex / Claude Code，或 Cursor Cloud Agent。
- 有 connector 就不用浏览器。重复的网页操作：抓一次请求，改成 API 脚本。
- 专项任务新建频道，做完关掉；复盘写入仓库文件。
- 输出分开：事实 | 推断 | 已做 | 等批准 | 未决问题。
- 卡住或两次相同失败：立刻停，通知我。

NEVER
- 不要在本聊天里写代码、开目录、直播工人进度、重写补丁。
- 不要为了对比同时开两个工人打同一补丁。
- 不要把一次性 watch 留着；不要把 routine 挂在长对话上。
- 未经明确批准：不发送、不发布、不删除、不购买、不改生产。
```

Routine 优化口令（丢给老板 Bot）：

```
Optimize our routines so each run uses as few tokens as possible.
Minimize context and input; skip extra steps, repetition, and checks;
reduce tool calls; don't fetch the same info twice;
retrieve only what the final result needs; keep output short.
Keep the task's intent, reliability, and quality.
```
