# 使用 Codex 8 个月，我总结的 50 个小技巧

> 写在前面：这 50 条不是空想清单，而是我把近一个月 X 上高流量 Codex 技巧帖（含多篇 X Article）全部下载精读后，按「真实可落地、反复被验证、能省额度/提质量」筛出来的。  
> 每条技巧后面都附上**原文出处链接**，方便你对照原文与上下文。  
> 浏览量来自榜单快照，会随时间变化。

**素材来源目录**：`codex-tips-posts-截止-2026-08-07-1032/`  
**榜单文件**：`codex-tips-top50-截止-2026-08-07-1032.md`

---

## 一、规则层：先把 Agent「按住」（1–8）

### 1. 根目录放一份「极简 AGENTS.md」，比写一百句 prompt 更省 token

AI 写代码最大的浪费不是写错，而是**写多**——多抽象、多兼容层、多重复造轮子。把「能不写就不写、能复用就复用、能简单就别复杂」写进 `AGENTS.md`，Cursor / Claude Code / Codex 都会自动读。

生产环境务必改温和：原版「不保留向后兼容」差点删表。

> 📎 参考：[@MarcosHernanz · 60B tokens 的 AGENTS.md](https://x.com/MarcosHernanz/status/2083954734487212511)（约 195.5 万浏览）  
> 📎 中文解读：[@AYi_AInotes · 8 条规则省 Token](https://x.com/AYi_AInotes/status/2084522269745820010)（约 38.6 万）  
> 📎 日文解读：[@so_ainsight · Vercel 8 条](https://x.com/so_ainsight/status/2084629184325030122)（约 6.6 万）

### 2. AGENTS.md 要当「路由器」，不是作文

不要只写哲学口号。写成：遇到 X 去读哪个 skill、哪个文档、哪个工具。Jamon 的整套 agentic 配置里，第 0 条就是这个。

> 📎 参考：[@jamonholmgren · 完整 agentic setup dump](https://x.com/jamonholmgren/status/2076001786700394610)（约 34.6 万）

### 3. 文档前 7 行写「可检索摘要」

每个系统文档开头写可 grep 的摘要；Agent 通过 AGENTS 路由找到后，先读前几行就能判断要不要深入。这是自愈文档体系的地基。

> 📎 参考：同上 [@jamonholmgren](https://x.com/jamonholmgren/status/2076001786700394610)

### 4. 全局规则用 Simplified Technical English（STE）

让 Agent 输出更短、更硬、更少废话。可写入全局 `.codex` / 规则文件；社区也有 STE skill 可直接装。

> 📎 参考：[@DanielLockyer · 启用 STE](https://x.com/DanielLockyer/status/2084208311906218179)（约 28.8 万）  
> 📎 补充：[@topmass · STE 写入全局规则](https://x.com/topmass/status/2084353571852832997)（约 9.4 万）

### 5. 先调研再写代码：GitHub 插件 +「暂不创建文件」

90% 的人一上来就「帮我写个 App」。正确姿势：装 GitHub 插件 → 要求先在 GitHub 调研同类开源 → 给架构/MVP/顺序 → **你确认后再实现**。可显著少返工、少 token。

> 📎 参考：[@BTCqzy1 · 省 ~90% token 调研提示词](https://x.com/BTCqzy1/status/2084268294115316141)（约 32.4 万）

### 6. 开启「交付工程师模式」：最多 5 问 + 验收清单

不要给模糊需求。模板：

1. 暂不写代码  
2. 最多 5 个决定方向的关键问题，一次只问一个  
3. 输出可验证验收清单（主流程/异常/空态/加载/多端）  
4. 列出假设、范围、明确不做  
5. 确认后再开发；完成后**真跑项目**并按清单打勾  

> 📎 参考：[@BTCqzy1 · 交付工程师模式](https://x.com/BTCqzy1/status/2084910817779355868)（约 10 万）

### 7. 收工写 `PROJECT_STATUS.md`，下次会话零成本接手

会话结束前让 Codex 写：做了什么、卡在哪、下一步、关键文件路径。下次新线程 `@` 这个文件，比从零复述省大量 token。

> 📎 参考：[@BTCqzy1 · PROJECT_STATUS 交接](https://x.com/BTCqzy1/status/2085340695444037966)（约 3.8 万）

### 8. Agent 必须自己跑应用、自己测

「改完文件就交差」是半成品流水线。规则写死：实现过程中始终运行 app、边测边修——尤其是异步/无人值守任务。

> 📎 参考：[@jamonholmgren · agents always run the app](https://x.com/jamonholmgren/status/2076001786700394610)

---

## 二、模型路由：把贵模型当顾问，便宜模型当牛马（9–18）

### 9. 打开 Luna Max（默认隐藏）

Settings → Configuration → 打开 Max。很多人体感：质量接近 Sol 中档，但额度消耗低得多。注意输出很长时会慢，复杂任务仍可回 Sol。

> 📎 参考：[@ForwardEditor · Luna Max 隐藏开关](https://x.com/ForwardEditor/status/2083162509692076153)（约 71.2 万）  
> 📎 日文同思路：[@aitech_komoriya · 打开后价差利用](https://x.com/aitech_komoriya/status/2085327528965857745)（约 2.5 万）

### 10. Sol 规划 / Luna 执行：主线程与子代理分工

Sol 留主线程：理解目标、拆任务、验收、整合。  
Luna Max 当子代理：边界清晰的实现、审查、测试排查。  
可让 Sol 直接创建 `~/.codex/agents/luna-worker.toml`。

> 📎 参考：[@Tz_2022 · luna-worker.toml 配置提示词](https://x.com/Tz_2022/status/2083568833164419449)（约 13.5 万）  
> 📎 完整提示词：[@RoundtableSpace · Sol + Luna Max subagent](https://x.com/RoundtableSpace/status/2084130890507329609)（约 6.6 千）  
> 📎 变体：[@xie_Dl · Sol 决策审计 + Luna 执行](https://x.com/xie_Dl/status/2085359731854778752)（约 1.8 万）

### 11. Fable 当顾问，Codex 当 workhorse

在 Claude 生态：Fable 规划/审查，Codex（GPT）执行重活，主模型额度省一大截。官方/社区都有「codex-first」skill。

> 📎 参考：[@steipete · codex-first skill](https://x.com/steipete/status/2074638582418231495)（约 90.8 万）  
> 📎 插件安装：[@cjzafir · Claude Code 内装 Codex 插件](https://x.com/cjzafir/status/2074875092090470469)（约 48.4 万）

### 12. Claude Code 一次装好官方 Codex 插件

```text
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
```

再让 Fable 跑 setup、鉴权，并约定：`/codex:rescue` 做重实现；任务要具体；Codex 完成后主模型自己再审。

> 📎 参考：[@cjzafir · 分步 setup + 委派提示词](https://x.com/cjzafir/status/2074875092090470469)

### 13. Sol Extra High 规划 + Luna Extra High 执行，更不易撞 5h 窗

同一档位下，把「想」和「写」拆到不同模型，5 小时限额更耐用。

> 📎 参考：[@cjzafir · Sol EH 规划 / Luna EH 执行](https://x.com/cjzafir/status/2076483843322962341)（约 6.1 万）

### 14. 部署 / merge / CI 开新线程用 Luna Max，省 Sol

主会话留 Sol 做决策；机械性、可验收的运维任务新开线程甩给 Luna Max。

> 📎 参考：[@MatthewBerman · Luna Max 新线程做 deploy](https://x.com/MatthewBerman/status/2084060433233907875)（约 6.1 万）

### 15. 装 sol-advisor + savings-prompt，默认偏向省额度路由

社区把「能 Luna 就不要 Sol」固化成 skill/提示词，3 分钟可装。

> 📎 参考：[@_0xpainn · sol-advisor + savings-prompt](https://x.com/_0xpainn/status/2084554055968280938)（约 9.5 万）  
> 📎 视频版：[@hank_aibtc · 安装演示](https://x.com/hank_aibtc/status/2085003542889406479)（约 5.1 万）  
> 📎 快速介绍：[@RoundtableSpace · 3 分钟装好](https://x.com/RoundtableSpace/status/2085119907599950307)（约 5.4 万）  
> 📎 模式说明：[@daniel_mac8 · Sol 编排 / Luna 日常](https://x.com/daniel_mac8/status/2084762735229685784)（约 4.1 万）

### 16. Luna / Terra / Sol 三档路由：别凡事顶配

简单改动走轻量档，架构与评审才上 Sol。把路由规则写进 AGENTS 或 skill。

> 📎 参考：[@talwar_divyam · 三档路由省 Sol](https://x.com/talwar_divyam/status/2083648143615517019)（约 2.9 万）

### 17. 撞额度时：Codex Router + OpenCode Go / DeepSeek 备胎

用 Router **叠加**模型而不是替换 ChatGPT 模型；OpenCode Go 等可在限额撞墙时顶上。

> 📎 参考：[@ziwenxu_ · OpenCode Go 接入 Codex](https://x.com/ziwenxu_/status/2084924184740663738)（约 40.4 万）  
> 📎 撞额续航：[@ziwenxu_ · Luna Max 接进 Router](https://x.com/ziwenxu_/status/2085219334280839299)（约 7.4 万）  
> 📎 工具：[@IndieDevHailey · Codex 里跑 Opencode/DeepSeek](https://x.com/IndieDevHailey/status/2085369300769227207)（约 8 千）

### 18. 起床前 2 小时用 Luna Light 发一条 “hi”，拉长白天额度窗

把「限额重置节奏」纳入日程：用自动化 + 最便宜模型轻触发，让白天第一段工作窗口更长。（依赖当时额度策略，请自行验证。）

> 📎 参考：[@ForwardEditor · 起床前 2h Luna Light](https://x.com/ForwardEditor/status/2082800122170093842)（约 11.9 万）

---

## 三、Goal 与长任务：把「完成」定义成可测条件（19–25）

### 19. 先 research，再 `set_goal`，别直接 `/goal`

直接 `/goal` 往往目标写糊。流程：先需求收集与调研 → 再 `set_goal` 固化可执行目标。下游质量差很多。

> 📎 参考：[@reach_vb · research 后 set_goal](https://x.com/reach_vb/status/2076813989598662816)（约 20.7 万）

### 20. 让 Codex 自己 `set_goal`（目标可验证更省）

让模型基于仓库现状起草 goal，你只改验收条件。可验证目标 = 更少无效轮次。

> 📎 参考：[@reach_vb · 自己 set_goal](https://x.com/reach_vb/status/2077136521178517999)（约 7.3 万）

### 21. Goal 超 4000 字符？写 `goal.md`，goal 本体只写一行

```text
Complete the objective and completion criteria in goal.md.
Treat this file as the durable source of truth throughout the run.
```

跑着还能改文件。Goal 文件要花时间写，「完成」必须是测试/检查，不是形容词。

> 📎 参考：[@mattshumer_ · Goal Mode 深度用法](https://x.com/i/article/2074916560041349120) · [推广帖](https://x.com/mattshumer_/status/2075267645058805896)（约 16.1 万）

### 22. Builder 与 Judge 分离；进度页可从手机看

长 goal：实现者与对抗式评审分开；维护 progress 页；「Never let it finish」直到验收真过。Matt 在曼哈顿体素城、Teardown 式游戏等长跑里验证过。

> 📎 参考：同上 [@mattshumer_ Article](https://x.com/i/article/2074916560041349120)

### 23. 数学/难题长跑：选题过滤 + 对抗式 prompt + 足够时间

Qiaoqiao 用 Codex+Sol 5 天解 6 个 Erdős 题的可复用点：

1. 选题：社区在讨论、避开与大猜想硬绑的题  
2. Prompt：精确重述、什么算证明、什么不算、陷阱、对抗 agent  
3. 长时间 goal 跑（数小时到数十小时）  
4. 循环：attempt → fail → 诊断 → 新路线 → 审计 → 修补  

> 📎 参考：[@Qiaoqiao2001 · 工作流与 prompt](https://x.com/Qiaoqiao2001/status/2080003441821163958)（约 157.7 万）

### 24. 用 `set_goal` 代替手搓 `/goal`，并让 Sol 裁判 Luna

自动化/skill 里用 `set_goal`；主模型当裁判、执行模型当选手。

> 📎 参考：[@ForwardEditor · set_goal + Sol 裁判](https://x.com/ForwardEditor/status/2082445284630536370)（约 2.2 万）

### 25. Sol 规划 → 多 Luna 线程并行（用 skill 固化）

一条 skill 把「拆任务 + 多线程 Luna 执行 + 汇总」串起来，适合可并行的实现面。

> 📎 参考：[@ForwardEditor · Sol 规划多 Luna 并行](https://x.com/ForwardEditor/status/2083200492260262033)（约 4.6 万）

---

## 四、多 Agent 与编排：别只开一个会话（26–33）

### 26. 把 Codex 当「控制台」，不是聊天框

Task / Subagent / Worktree / list_threads / wait_threads / handoff… 这些原语叠起来，才是跨项目、跨机器的 Agent 运维台。大多数人只用了 10% 能力。

> 📎 参考：[@riba2534 · 多 Agent 编排百科（Article）](https://x.com/i/article/2082915944100425728) · [推广帖](https://x.com/riba2534/status/2082916383248252976)（约 35.7 万）

### 27. 分清 Task 与 Subagent

- **Task**：长期、侧边栏可见、可跨项目/主机  
- **Subagent**：Task 内短生命周期、独立上下文、回摘要  

拓扑选型都建立在这个区分上。

> 📎 参考：同上 [@riba2534 Article](https://x.com/i/article/2082915944100425728)

### 28. 并行写代码用 Worktree，别共享一个 checkout

Git 同一分支不能多处 checkout。多方案竞赛、并行实现必须一人一 worktree + 独立分支。注意：Worktree 能力目前主要在桌面 App。

> 📎 参考：同上 [@riba2534 Article](https://x.com/i/article/2082915944100425728)

### 29. 噪声任务一定 spawn 子代理（防 context rot）

大量读代码、扫日志、跑测试的中间输出会污染主会话。子代理只回摘要 + `file:line` 证据。

> 📎 参考：同上 [@riba2534 Article](https://x.com/i/article/2082915944100425728)

### 30. 跨 Agent Review：换模型审，不要自己审自己

研究 / 计划 / 实现 / 收尾四个节点都做跨 agent review（Codex vs Claude vs Cursor…），并按可维护性、安全、性能等 persona 分工。

> 📎 参考：[@jamonholmgren · cross-agent review](https://x.com/jamonholmgren/status/2076001786700394610)

### 31. 包工头模式：一段 prompt 做 graph engineering

主 Agent 当包工头，按图拆节点派小弟；节点依赖用结构化产物交接，而不是「口头说好了」。

> 📎 参考：[@ErwinWu000 · graph engineering 提示词](https://x.com/ErwinWu000/status/2083997246920790062)（约 4.4 万）  
> 📎 多模型并行：[@Youngxxxxu · OpenCodex 子代理](https://x.com/Youngxxxxu/status/2084723886717800673)（约 4.8 万）

### 32. 一人公司也可以是 5-Agent 团队

Research / Plan / Write / Review / Devil’s Advocate 分角色、分 runtime（可含 Codex CLI），共享频道与 handoff。关键是角色描述要具体，不要「writer agent」这种空壳。

> 📎 参考：[@sairahul1 · 5-Agent 团队长文](https://x.com/sairahul1/status/2079817450028519801)（约 194.2 万）

### 33. 用 `codex exec` 做脚本化 / CI / 隔离 eval

把 agent 循环当成积木：CI、Makefile、可重试、可隔离。交互 TUI 适合探索；流水线适合 exec。

> 📎 参考：[@reach_vb · codex exec](https://x.com/reach_vb/status/2082609245011198432)（约 1.8 万）  
> 📎 循环哲学：[@shmidtqq · Stop Prompting. Start Looping](https://x.com/i/article/2075991510042951681)（约 8.8 万）

---

## 五、Skill 与资产化：重复三次就该固化（34–41）

### 34. Skill 优先：一次写好，多端复用

Matt skills v1.2 已完整支持 Codex（`agents/openai.yaml`）。优先装成熟 skill 集，再写自己的。

> 📎 参考：[@mattpocockuk · skills v1.2 + Codex](https://x.com/mattpocockuk/status/2084985277102031137)（约 54.9 万）  
> 📎 中文解读：[@Lonely__MH · skills v1.2](https://x.com/Lonely__MH/status/2085154384908796208)（约 2.2 万）  
> 📎 合集：[@Gencoin8 · 26 个免费 Skill](https://x.com/Gencoin8/status/2085254041307660567)（约 1.5 万）

### 35. Agent Plugins：Skills + MCP 打包一次多端用

按开放标准打包插件，Codex / ChatGPT / 其他兼容客户端可复用。

> 📎 参考：[@thsottiaux · Agent Plugins](https://x.com/thsottiaux/status/2085432978856083964)（约 29.7 万）

### 36. 从近 30 天会话挖重复劳动 → Skill / Agent / Automation

每周问一次：这 30 天我重复让 Codex 做了什么？重复 ≥3 次的，固化成 skill 或自动化。

> 📎 参考：[@Saccc_c · 从会话挖重复劳动](https://x.com/Saccc_c/status/2085275196412547133)（约 3.4 万）

### 37. 用历史 session 迭代 skill；可做 backtest

对照旧会话验证 skill 是否真的减少步骤、提高一次成功率。

> 📎 参考：[@reach_vb · 历史 session 迭代 skill](https://x.com/reach_vb/status/2078108681678299194)（约 2 万）  
> 📎 完整 prompt：[@Voxyz_ai · skill backtest](https://x.com/Voxyz_ai/status/2078175217839403150)（约 3.1 万）  
> 📎 周更：[@Ananth7e · 按 session 自动更新 skill](https://x.com/Ananth7e/status/2084507266556801447)（约 1.05 万）  
> 📎 提示词：[@Suu766 · Skill 每周自更新](https://x.com/Suu766/status/2085286515836629151)（约 5.5 千）

### 38. 踩坑固化成 Skill，而不是修单条视频/单次任务

长视频流水线（人生副本）、口播、公众号写作：把失败模式写成规则，沉淀为可复用 Skill，而不是手工修成片。

> 📎 参考：[@Hamburgerai · 人生副本全流水线](https://x.com/i/article/2083404529039757312)（约 22.9 万）  
> 📎 口播：[@Mayii0205 · HeyGen/MiniMax/剪映](https://x.com/Mayii0205/status/2082055667234550070)（约 10.1 万）  
> 📎 公众号：[@canghe · Codex + Obsidian WeSight](https://x.com/i/article/2084949005692526592)（约 10.6 万）

### 39. Codex 五件套：AppShots / meta 线程 / PLAN.md / Skill / `/goal`

入门组合拳：截图给 Agent 看、维护 meta 线程、写 PLAN、装 skill、会用 goal。

> 📎 参考：[@Suu766 · 5 用法](https://x.com/Suu766/status/2084944861908918558)（约 2.6 万）  
> 📎 清单：[@NielsRogge · AppShots 等清单](https://x.com/NielsRogge/status/2080241986024427650)（约 1.7 万）  
> 📎 教程路径：[@huoshan007 · Annotate/Fork/Archive/Plan…](https://x.com/huoshan007/status/2084916064228626584)（约 19.8 万）

### 40. 解释时强制 Visualize skill（写入 AGENTS）

要求复杂解释必须配图/示意，减少「看起来懂了其实没懂」。

> 📎 参考：[@reach_vb · Visualize skill](https://x.com/reach_vb/status/2085408004455981272)（约 5.5 万）

### 41. UI transition 等垂直 skill 直接装，别从零写

动效、转场、组件动画这类，社区已有成熟 skill（Claude/Cursor/Codex 通用）。

> 📎 参考：[@Jakubantalik · 33+ UI transition skill](https://x.com/Jakubantalik/status/2081036752924352811)（约 7.8 万）  
> 📎 工程 skill 库：[@midudev · Addy Osmani agent-skills](https://x.com/midudev/status/2085368038925197697)（约 2.8 万）

---

## 六、日常操作与维护：小习惯拉开巨大差距（42–47）

### 42. 归档 one-off session，侧边栏只留「活项目」

临时排查、一次性脚本跑完就 Archive。侧边栏干净 = 跨会话调度时找得到真正的专用 Task。

> 📎 参考：[@reach_vb · 归档 one-off](https://x.com/reach_vb/status/2078018760741667141)（约 3.3 万）

### 43. 上下文满了：新 chat + `@` 旧会话续作

不要硬撑到腐烂。新会话引用旧线程/关键文件，继续干净上下文。

> 📎 参考：[@so_ainsight · 新 chat @ 旧会话](https://x.com/so_ainsight/status/2085247000770163037)（约 1.7 万）

### 44. 别用内置搜索找旧线程：新开 chat 让 Codex 自己找

内置搜索体验差时，让 Agent 用工具/会话索引定位旧讨论。

> 📎 参考：[@ForwardEditor · 别用内置搜索](https://x.com/ForwardEditor/status/2084974449405952217)（约 6.6 千）

### 45. 编辑「最近一条 prompt」重生成，比新开长对话更省

小改指令后重跑，比带着污染上下文继续聊更便宜、更干净。

> 📎 参考：[@ForwardEditor · 编辑最近 prompt](https://x.com/ForwardEditor/status/2084612061070319695)（约 6.4 千）

### 46. 高亮文本「Add to chat」注解上一条

Chrome 扩展等能力：把页面/输出里的关键片段一键挂到对话，减少复制粘贴丢上下文。

> 📎 参考：[@dkundel · add to chat 注解](https://x.com/dkundel/status/2085415512394326434)（约 4.5 千）

### 47. 每周清理 Codex 缓存 / 旧 thread；顺手扫磁盘

Codex 自己会堆缓存与旧日志。设周自动化只清「陈旧且安全」的数据；磁盘爆了先让它列清单再删。

> 📎 参考：[@Ananth7e · 每周清缓存](https://x.com/Ananth7e/status/2084354538715382188)（约 9.3 万）  
> 📎 扫磁盘：[@Ananth7e · 先列清单再删](https://x.com/Ananth7e/status/2084333430280786115)（约 11.4 万）  
> 📎 清 headless：[@ForwardEditor · Luna 自动化清缓存降温](https://x.com/ForwardEditor/status/2083936363657810177)（约 26 万）

---

## 七、场景扩展：Codex 不只写代码（48–50）

### 48. 手机遥控电脑 + Computer/Chrome/Gmail/Calendar

配对后在手机上派活、看 diff、续 goal；App 侧接浏览器、邮箱、日历做生产力闭环。

> 📎 参考：[@0xSero · Computer+Chrome+Gmail+Calendar+/goal](https://x.com/0xSero/status/2084699762893463950)（约 7.4 万）  
> 📎 入门全景：[@laowangbabababa · 注册到 App/CLI/插件教程](https://x.com/i/article/2074455505171521536)（约 65.2 万）

### 49. USB 插手机/Kindle，把 Codex 当「通用设备 UI」

插上设备后说「我插了手机」：清垃圾应用、整理相册、挖深层菜单、找书……老设备 UI 不会用时尤其香。

> 📎 参考：[@ForwardEditor · USB 控手机/Kindle](https://x.com/ForwardEditor/status/2084714793085055163)（约 8 万）

### 50. 接飞书 / 浏览器自动化 / 内容流水线，把 Agent 嵌进业务

- 飞书 CLI 管文档协作  
- Lightpanda 等做 Web 自动化  
- 批量 prompt → 生图 → metadata CSV  
- 任务结束邮件汇报改动摘要  

原则不变：**可重复的步骤进 skill，可验收的结果进清单，贵模型只做决策。**

> 📎 参考：[@jinchenma_ai · Codex + 飞书 CLI](https://x.com/i/article/2083566013141139456)（约 7.2 万）  
> 📎 浏览器：[@codex_lab_ · Lightpanda + Codex](https://x.com/codex_lab_/status/2085376012414763417)（约 1.2 万）  
> 📎 批量生图：[@geegissss · prompt + 图 + Adobe CSV](https://x.com/geegissss/status/2084843417671274921)（约 8.3 万）  
> 📎 邮件汇报：[@reach_vb · 任务结束发摘要邮件](https://x.com/reach_vb/status/2082445610913878295)（约 1.3 万）

---

## 一张图记住这 50 条（我的 8 个月心法）

| 层级 | 核心动作 | 代表技巧编号 |
|:---|:---|:---|
| **约束** | AGENTS 路由 + 简写规则 + 验收清单 | 1–8 |
| **路由** | Sol 想、Luna 写、撞限有备胎 | 9–18 |
| **长跑** | research → goal.md → 可测完成条件 | 19–25 |
| **编排** | Task/Subagent/Worktree/跨模型审 | 26–33 |
| **资产** | 重复三次就 Skill 化 | 34–41 |
| **卫生** | 归档、清缓存、新会话续作 | 42–47 |
| **场景** | 设备/飞书/内容/自动化 | 48–50 |

如果只让我挑 **10 条立刻做**，按优先级是：

1. 写 AGENTS.md（#1 #2）  
2. 交付工程师模式（#6）  
3. 先调研再写代码（#5）  
4. 开 Luna Max + Sol/Luna 分工（#9 #10）  
5. research 后 set_goal + goal.md（#19 #21）  
6. 跨模型 review（#30）  
7. 重复劳动固化 Skill（#36）  
8. 收工 PROJECT_STATUS（#7）  
9. 归档 + 周清理（#42 #47）  
10. Agent 自己跑应用验收（#8）

---

## 本地对照阅读

完整原文已下载在：

```text
H:\github\grok-x\codex-tips-posts-截止-2026-08-07-1032\
```

索引文件：`00_INDEX.md`（按序号 / 浏览量 / 是否文章命名）。

---

## 免责声明

- 模型名（Sol / Luna / Fable）、限额策略、菜单路径会随产品迭代变化，以你客户端当前版本为准。  
- 生产环境慎用「不保留向后兼容」类激进规则。  
- 第三方额度/Router/免费积分类方案有合规与稳定性风险，自行判断。  
- 本文是对社区高流量技巧的**综合转述与结构化**，不是官方文档。

---

*整理时间：2026-08-07 · 基于 `codex-tips-top50-截止-2026-08-07-1032` 下载库深度精读*
