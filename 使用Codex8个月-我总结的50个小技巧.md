# 使用 Codex 8 个月，我总结的 50 个小技巧

用了 Codex 大概八个月。中间踩过很多坑：额度莫名其妙撞墙、一句话让它「帮我写个 App」结果返工三天、上下文烂掉以后 Agent 开始自说自话……

后来我发现，真正拉开差距的不是「会不会问」，而是有没有一套**可复制的工作方式**：规则怎么写、模型怎么拆、目标怎么定、会话怎么管、重复劳动怎么固化成 Skill。

下面 50 条，是我这八个月反复验证、也从社区高流量实践里消化过的干货。每条尽量把**可直接复制的提示词 / 配置 / 步骤**写全。需要配图的地方我留了截图占位，你之后按需替换。

---

## 一、规则层：先把 Agent「按住」（1–8）

### 1. 根目录放一份「极简 AGENTS.md」，比写一百句 prompt 更省 token

AI 写代码最大的浪费，往往不是写错，而是**写多**：多抽象、多兼容层、多重复造轮子。你让它改，它再给你加两百行。

核心就一句话：让 Agent 别像实习生什么都想自己造，而要像干了十年的老油条——能不写就不写，能复用就复用，能简单就别复杂。

一份被验证过的 8 条规则骨架（side project 向，生产请改温和）：

```markdown
# AGENTS.md

1. 不保留向后兼容。过时的直接删，别加兼容层、别写 migration、别留 fallback。
2. 选能满足当前需求的最简单实现。不要预防性抽象，不要多余配置层。
3. 系统分层长：先跑通最小端到端，再往上加。绝不为了未完成的复杂度拆掉能跑的东西。
4. 组件保持模块化，关注点分离。
5. 优先用成熟、有人维护的库。没有明确理由别自己重写。
6. 先看项目里已有依赖能做什么，再考虑加新包或自己写。
7. 架构决策往长了做。不接受「先这样以后再换」的临时方案。
8. 先看成熟产品怎么解决同一问题，用已验证的模式，别从零发明。
```

把文件丢在**项目根目录**。Cursor、Claude Code、Codex、Windsurf 都会自动读。

**生产警告**：第 1 条在生产里很危险，有人差点让 Agent 删了库表。至少改成「默认保留兼容，除非我明确要求删除」。

> 📷 **【截图占位 01】**：项目根目录里的 `AGENTS.md` 全文截图（建议深色编辑器）

---

### 2. AGENTS.md 要当「路由器」，不是作文

光写原则还不够。真正好用的 AGENTS.md 是**路由器**：

- 遇到改 UI → 去读哪个 skill / 文档  
- 遇到支付/权限 → 去读哪份安全约定  
- 遇到测试 → 去读测试清单与写法  
- 默认工作流 → `@` 哪份 `AGENT_WORKFLOW.md`

你可以在文末加一节：

```markdown
## Routing

- UI / 交互：读 `docs/ui-conventions.md`，启用 skill `ui-transitions`
- 后端 API：读 `docs/api.md`，先跑相关测试
- 不确定架构：先 `/plan`，禁止直接大改
- 标准工作流：会话开始先读 `@AGENT_WORKFLOW.md`
```

Agent 第一件事不是瞎搜整个仓库，而是被你指到正确入口。

> 📷 **【截图占位 02】**：带 Routing 段落的 AGENTS.md

---

### 3. 文档前 7 行写「可检索摘要」

每个系统文档开头写 5～7 行摘要：这个系统是什么、边界在哪、关键入口文件、常见坑。要求写进 AGENTS：

> 每个 doc 前 7 行必须能被 grep 命中；Agent 先读摘要再决定是否深入。

好处：Agent 找资料时不需要把整篇文档吞进上下文，省 token，也更准。

> 📷 **【截图占位 03】**：某份文档前 7 行摘要示例

---

### 4. 全局规则用 Simplified Technical English（STE）

Agent 默认爱写长段落、堆断言、绕弯子。在全局规则（如 `~/.codex` 相关配置 / 全局 MD）里加：

```text
Use Simplified Technical English (ASD-STE100 style) for all prose:
short sentences, common words, active voice, no filler.
Never touch code identifiers or technical terms for "simplification".
Prefer lists over paragraphs when explaining steps.
```

你会明显感觉：同一件事，回复更短、更硬、更好扫。

> 📷 **【截图占位 04】**：全局规则文件中 STE 相关片段

---

### 5. 先调研再写代码：GitHub 插件 +「暂不创建文件」

90% 的人把 Codex 用反了。一上来就：

> 帮我写一个 App。

正确姿势：先装 **GitHub 插件**，再发下面这段（把 XXX 换成你的需求）：

```text
我要开发一个 XXX。
暂时不要创建文件，也不要输出代码。

先在 GitHub 调研同类开源项目，筛选出最有参考价值的方案。
分析它们：
- 解决了什么问题
- 采用什么架构
- 依赖哪些技术
- 目前是否活跃
- 有哪些设计值得复用或避开

最后结合我的需求，给出：
1) 技术选型
2) 系统架构
3) MVP 范围
4) 开发顺序

得到我的确认后，再进入实现阶段。
```

这样它会先做三件事：找经过验证的方案 → 研究别人踩过的坑 → 做技术取舍。方向对了再写代码，token 和返工都会掉一大截。

> 📷 **【截图占位 05-1】**：Codex 插件页 / GitHub 插件已安装  
> 📷 **【截图占位 05-2】**：调研阶段输出的架构与选型（未写代码）

---

### 6. 开启「交付工程师模式」：最多 5 问 + 验收清单

Vibe Coding 第一句常常是「帮我把这个功能做出来」。结果经常是半成品——因为它拿到的是需求，不是交付标准。

直接复制这套提示词：

```text
暂时不要写代码。请先确认需求，最多向我提出 5 个决定方案方向的关键问题，每次只问一个；已有信息不要重复确认，非关键细节请自行做合理假设。

提问结束后，把需求整理成一份精简、可验证的验收清单，覆盖：
- 核心流程
- 异常情况
- 空状态
- 加载状态
- 不同设备适配

并单独列出：你的假设、本次范围、明确不做的内容。

等我确认后再开始开发。
完成后必须实际运行项目，按照验收清单逐项验证并汇报结果；
未通过的项目继续修改，直到达到验收标准。
```

换这套以后你会看到：

1. 开发前补齐模糊点，发现逻辑漏洞  
2. 不再改完文件就交差，而是主动跑项目验收  
3. 方向提前对齐，少推倒重来  

> 📷 **【截图占位 06】**：验收清单示例（Checklist 形式）

---

### 7. 收工写 `PROJECT_STATUS.md`，下次会话零成本接手

长对话一旦过长，会塞满失效决定和报错垃圾。Agent 反复重扫代码、重踩旧坑，token 白白烧掉。

阶段结束时用：

```text
当前阶段即将结束。请创建或更新 PROJECT_STATUS.md，把本次工作沉淀成一份可以继续执行的项目交接文档。

文档需要包含：
- 当前目标
- 已完成内容
- 关键技术决策
- 修改过的核心文件
- 测试与验证结果
- 已知问题
- 尝试过但失败的方案
- 下一步开发顺序

请结合当前代码、Git 变更和测试结果核对内容。
只保留后续开发真正需要的信息，不记录无关讨论，
不猜测未确认的结论，也不要写入密码、密钥等敏感信息。
```

下次开工第一句：

```text
请先阅读 PROJECT_STATUS.md，确认当前进度、已知问题和下一步，再继续开发。
```

这份文档不绑某个 Session，也不绑某个平台——Codex、Claude Code、Cursor 甚至人类同事都能接着干。

> 📷 **【截图占位 07】**：一份完整的 PROJECT_STATUS.md

---

### 8. Agent 必须自己跑应用、自己测

规则里写死：

```text
实现过程中必须实际运行应用（或相关服务），
边做边测，发现问题当场修。
禁止「只改文件、不验证」就宣告完成。
异步/无人值守任务同样适用。
```

半成品流水线的特征就是：diff 很多，但页面没打开、测试没跑、接口没打。把「跑起来」写进规则，比事后骂它有用一百倍。

> 📷 **【截图占位 08】**：Agent 自己启动 dev server / 跑测试的终端输出

---

## 二、模型路由：把贵模型当顾问，便宜模型当牛马（9–18）

### 9. 打开 Luna Max（默认隐藏）

很多人用了很久都不知道：**Luna 最强档默认是关的**。

路径：

```text
Settings → Configuration → 打开 Max（Luna Max）
```

打开后，日常实现类任务往往可以大量用 Luna Max：体感质量接近 Sol 中档，额度消耗却友好得多。注意：

- 输出特别长时会慢，可回 High / XHigh  
- 真正难的架构/评审仍可回 Sol  

> 📷 **【截图占位 09】**：Settings → Configuration 中 Max 开关位置

---

### 10. Sol 规划 / Luna 执行：主线程与子代理分工

让 Sol 留在主线程统筹，把边界清晰的活拆给 Luna Max 子代理。

把下面整段发给 Sol：

```text
请在以下路径创建一个名为 luna_worker 的自定义 Agent：
~/.codex/agents/luna-worker.toml

使用以下配置：
model = "gpt-5.6-luna"
model_reasoning_effort = "max"

请为这个 Agent 补充清晰的 description 和 instructions。
luna_worker 只负责处理范围明确、边界清晰、可以独立完成的委派任务，
不负责修改整体任务目标，也不要自行扩大工作范围。

请保留我现有的其他 Codex 配置，不要覆盖或删除无关内容。

创建完成后：
1. 根据我当前安装的 Codex 版本检查配置格式是否兼容；
2. 展示本次修改产生的 diff；
3. 确认配置有效；
4. 后续需要调用子代理时，优先使用 luna_worker。
```

配置后的分工：

| 角色 | 模型 | 职责 |
|:---|:---|:---|
| 主线程 | Sol | 理解目标、拆任务、检查结果、整合输出 |
| 子代理 | Luna Max | 代码审查、模块分析、独立实现、测试排查 |

每个子任务有相对独立上下文，主线程更干净，也方便并行。

> 📷 **【截图占位 10-1】**：`luna-worker.toml` 内容  
> 📷 **【截图占位 10-2】**：主线程委派子代理的界面

---

### 11. Fable 当顾问，Codex 当 workhorse

如果你同时用 Claude 生态：让 **Fable 规划/审查**，让 **Codex（GPT）执行重活**。主模型额度能省一大截——有人实测 24 小时烧 20 亿 token 量级时，Fable 周限额只掉一半左右，Codex 侧再分走执行成本。

原则：

- Fable：架构、任务分解、最终 review  
- Codex：多文件实现、修测试、重构、debug  

把这套写进 skill，会话开头一键启用。

> 📷 **【截图占位 11】**：Fable 编排 + Codex 执行的一次完整流转（对话或技能面板）

---

### 12. Claude Code 里装官方 Codex 插件（一次配置，长期受益）

**Step 1：安装插件**

```text
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
```

**Step 2：让 Fable 完成 setup**

```text
Set up Codex inside this Claude Code environment.
Use the official OpenAI Codex plugin that was just installed.
Run /codex:setup.
If Codex CLI is missing, install it.
If Codex is installed but not authenticated, ask me to authenticate with my ChatGPT account.
After auth is complete, verify that Codex works from inside Claude Code.
Then confirm that the codex:codex-rescue sub-agent is available.
Do not change any project code during setup.
```

**Step 3：鉴权一次**  
按提示用 ChatGPT/Codex 账号登录。

**Step 4：固化委派规则**

```text
From now on, use this workflow:

You are the orchestrator.
- Use Fable for planning, repo understanding, architecture decisions,
  task decomposition, and final review.
- Use codex-rescue as the executor for heavy implementation, debugging,
  test fixing, refactoring, or multi-file code edits.
- When delegating to Codex, use /codex:rescue.
- Prefer a strong Codex model for execution.
- Keep Codex tasks focused and specific.
- After Codex finishes, inspect the result yourself before accepting it.
- Do not blindly trust Codex output.
```

额外习惯：

1. 做成 skill，会话开头加载  
2. 重活用 skill + goal  
3. 有多 subagent 额度就并行 5～7 路  
4. 上下文压缩约 4 次后清会话，用 handoff 保住状态  

> 📷 **【截图占位 12】**：Claude Code 插件安装成功 + codex-rescue 可用

---

### 13. Sol Extra High 规划 + Luna Extra High 执行

同一套「想」和「写」拆开：

- 规划 / 拆解 / 评审：Sol + Extra High  
- 实现 / 改测试 / 修细节：Luna + Extra High  

比全程 Sol 更耐 5 小时限额，也比全程 Luna 更稳方向。

> 📷 **【截图占位 13】**：模型与 reasoning effort 选择界面

---

### 14. 部署 / merge / CI 开新线程用 Luna Max

主会话留给 Sol 做决策；机械性强、验收清晰的运维任务：

```text
新开一个线程，使用 Luna Max：
完成部署检查 / merge 前检查 / CI 失败排查。
只在最终结果与风险点回主线程摘要。
```

省 Sol，也避免主会话被日志淹没。

> 📷 **【截图占位 14】**：主线程 + 运维子线程并排

---

### 15. 装 sol-advisor + savings-prompt，默认省额度路由

社区常见三层：

1. **Repo 层**：安装 sol-advisor  
2. **Prompt 层**：复制 savings-prompt  
3. **Agent 层**：默认指向 Luna，只有必要时升 Sol  

目标：日常路径自动走便宜模型，撞限前少踩雷。装完后在新会话验证：简单改文件是否仍误用顶配。

> 📷 **【截图占位 15】**：sol-advisor / savings-prompt 安装与生效证明

---

### 16. Luna / Terra / Sol 三档路由表

把路由写进 AGENTS 或 skill：

| 任务类型 | 推荐档位 |
|:---|:---|
| 改文案、小 refactor、补测试 | Luna / Terra |
| 模块实现、中等 debug | Luna Max / High |
| 架构决策、跨模块设计、安全审计 | Sol |

禁止：「所有事情默认 Sol Extra High」。

> 📷 **【截图占位 16】**：写在 AGENTS.md 里的路由表

---

### 17. 撞额度时：Router 叠加外部模型，而不是整库切走

正确姿势是 **Codex Router 叠加模型**（Sol / Luna 仍在选择器里），撞限时切 DeepSeek / OpenCode Go / Kimi 等顶上。

错误姿势：按官方单供应商配置把整个 Codex 切走，ChatGPT 模型全没了。

> 📷 **【截图占位 17】**：模型选择器里同时出现 ChatGPT 模型 + 外部模型

---

### 18. 起床前 2 小时用 Luna Light 发 “hi”，拉长白天额度窗

若你的限额按时间窗滚动，可以设自动化：

```text
每天起床前约 2 小时，用最便宜的 Luna Light 发一条 "hi"
```

目的是把「限额窗口」往白天工作段推。**注意：额度策略会变，请以你账号实际行为为准，无效就关掉。**

> 📷 **【截图占位 18】**：Automation / 定时任务配置界面

---

## 三、Goal 与长任务：把「完成」定义成可测条件（19–25）

### 19. 先 research，再 `set_goal`，别直接 `/goal`

直接 `/goal` 的常见问题：目标写糊，Agent 用错误假设长跑。

推荐流程：

```text
1) 先做 requirements gathering + research
2) 产出：范围、约束、验收标准、风险
3) 再用 set_goal 固化
```

一句话原则：

> 所有 prompts 先从调研开始；调研结束后再 set_goal。

> 📷 **【截图占位 19】**：research 摘要 → set_goal 前后对比

---

### 20. 让 Codex 自己 `set_goal`（目标可验证更省）

```text
请基于当前仓库与我的目标，先调研再自己 set_goal。
Goal 必须包含：
- 可验证的完成条件（测试/命令/可观察行为）
- 明确不做
- 失败时如何判定
我只审核 goal，不手写长 goal。
```

可验证目标 = 更少无效轮次。

> 📷 **【截图占位 20】**：Agent 自动生成的 goal 文本

---

### 21. Goal 超长？写 `goal.md`，goal 本体只写一行

Goal 有字符上限（常见约 4000）。别硬塞，改用文件：

**goal 本体：**

```text
Complete the objective and completion criteria in goal.md.
Treat this file as the durable source of truth throughout the run.
```

**goal.md 要点：**

- 「完成」是测试，不是形容词（例如 `npm test` 全绿，而不是「差不多好了」）  
- 写清验收标准、禁止项、里程碑  
- 可在运行中改文件，相当于边跑边改需求真源  

花时间写 goal 文件 = 你在当项目经理；含糊一句 = 模型替你做决策。

> 📷 **【截图占位 21-1】**：`goal.md` 全文  
> 📷 **【截图占位 21-2】**：`/goal` 输入框里那一行引用

---

### 22. Builder 与 Judge 分离；进度页可从手机看

长任务三条军规：

1. **实现者**和**评审者**不要同一上下文自审  
2. 「完成」必须过检查；不过就继续，不允许自我感觉良好收工  
3. 维护 progress 页 / journal，手机也能看进度并轻推一把  

对抗式评审可以 spawn 多个 reviewer 专门找洞，再打回 builder 修。

> 📷 **【截图占位 22】**：progress 页 / goal 运行中状态

---

### 23. 难题长跑工作流（选题 → 提示词 → 长时间 goal）

可复用骨架（不限于数学题）：

1. **选题**：社区在讨论、避开「绑死大猜想」的无底洞  
2. **提示词**必须写清：  
   - 精确问题陈述  
   - 什么叫完整解决  
   - 哪些弱结果不算数  
   - 陷阱与边界  
   - 要求对抗 agent 挑战每条候选论证  
3. **搜索管理**：多路线并行、反证引理、只归约到同难度未证命题则标阻塞  
4. **耐心**：给足时间（数小时到数十小时）  
5. **循环**：attempt → fail → 诊断 → 新路线 → 草稿 → 对抗审计 → 修补  

> 📷 **【截图占位 23】**：长 goal 运行数小时的时间线/日志片段

---

### 24. 用 `set_goal` 代替手搓 `/goal`，Sol 当裁判、Luna 当选手

自动化或 skill 里：

```text
- Luna：按 goal 执行
- Sol：阶段检查 / 终局裁判
- 不通过则打回，通过才收口
```

适合「执行便宜、验收要狠」的场景。

> 📷 **【截图占位 24】**：Luna 执行 + Sol 裁判的对话结构

---

### 25. Sol 规划 → 多 Luna 线程并行

一条 skill 固化：

```text
1. Sol 拆可并行任务列表（互不依赖）
2. 每任务开 Luna 线程
3. wait-any / 汇总
4. Sol 做冲突消解与最终整合
```

切分原则：**块与块之间不需要通信** 才能并行；有硬依赖就走流水线，不要硬拆。

> 📷 **【截图占位 25】**：多线程并行侧边栏

---

## 四、多 Agent 与编排：别只开一个会话（26–33）

### 26. 把 Codex 当「控制台」，不是聊天框

大多数人：开一个会话 → 交代一件事 → 等做完。这只动用了很小一部分能力。

Codex 真正提供的是调度原语：

- 发现项目与会话  
- 创建 / 分叉会话  
- 给别的会话派活  
- 等待回来、观察进展、纠正跑偏  
- 迁移到另一台机器  
- 收口归档  

叠起来，它是跨项目、跨 Git worktree、跨 SSH 主机的 **Agent 运维控制台**。

三个入口：App / CLI / IDE 插件。共享配置和 MCP，但能力不等价——例如 **Worktree 目前主要在桌面 App**。

> 📷 **【截图占位 26】**：侧边栏多 Task 全局视图

---

### 27. 分清 Task 与 Subagent

| | Task | Subagent |
|:---|:---|:---|
| 生命周期 | 长期 | 短 |
| 可见性 | 侧边栏 | 任务内部 |
| 用途 | 持久角色、跨项目 | 临时探索/实现 |
| 上下文 | 完整会话 | 独立窗口，回摘要 |

所有拓扑都建立在这个区分上。别把该开 Task 的活硬塞进一个巨型会话。

> 📷 **【截图占位 27】**：主 Task 下挂多个 Subagent

---

### 28. 并行写代码用 Worktree，别共享一个 checkout

- **Local**：改日常工作区，IDE/dev server 即时可见；多写任务会互踩  
- **Worktree**：每人一份文件树，共享 `.git`；适合并行改、各自测  
- Git 硬约束：**同一分支不能同时在两处 checkout** → 多方案必须独立分支  

多方案竞赛：fork + 每人 worktree + 独立分支，最后用测试和 diff 挑赢家。

> 📷 **【截图占位 28】**：同一仓库多个 worktree 目录结构

---

### 29. 噪声任务一定 spawn 子代理（防 context rot）

主会话应只保留：需求、决策、最终产物。  
探索笔记、测试日志、堆栈、命令输出 → 全部丢给子代理，只回摘要 + `file:line` 证据。

选型判据：

- 读很多才能得到短结论 → 子代理  
- 只是一两处明确编辑 → 主 Agent 自己做  
- 并行读安全；并行写要小心冲突  

出厂子代理类型：`default` / `worker` / `explorer`；也可自定义 TOML（`name`、`description`、`developer_instructions`，可指定 model / sandbox）。

> 📷 **【截图占位 29】**：explorer 子代理只返回带文件行号的摘要

---

### 30. 跨 Agent Review：换模型审，不要自己审自己

在 research / plan / implementation / wrap-up 四个节点都做跨 agent review。

要点：

- 审的模型 ≠ 写的模型  
- 准备 review 文档：看什么、怎么看  
- Persona：可维护性、质量、安全、性能、AI smell、业务域  
- 每个 persona 可「拥有」一批系统文档并负责更新  

Detached Review（独立评审线程）比 inline 自审更狠。

> 📷 **【截图占位 30】**：一次跨模型 review 输出（含问题分级）

---

### 31. 包工头模式（Graph Engineering）

主 Agent = 包工头：

```text
你是包工头，不是一线码农。
1) 把目标拆成依赖图（节点=可交付物，边=依赖）
2) 就绪节点才能开工
3) 每个节点要有可校验产物（schema/路径/测试）
4) 节点完成后再重算就绪集
5) 失败节点：重试 / 改派 / 上报人
禁止一个会话从头干到尾不建图。
```

有硬依赖的发版检查、跨仓改造，都比「一个长对话」稳。

> 📷 **【截图占位 31】**：任务依赖图（手绘或导出图）

---

### 32. 一人公司也可以是 5-Agent 团队

示例角色（名称可改）：

| 角色 | 职责 | 注意 |
|:---|:---|:---|
| Research | 找证据，不编造 | 描述要具体到「去哪找」 |
| Planner | 框架与策略 | 先挑战假设再计划 |
| Writer | 短、狠、可发布 | 禁废话 |
| Reviewer | 对照 research 查硬伤 | 要具体反馈 |
| Devil's Advocate | 专唱反调 | 团队一致时必须找反击点 |

关键：角色 description 要**可执行**。  
坏：`Write content`  
好：`Write short punchy X hooks. No filler. Under 15 words. Strong verbs only.`

> 📷 **【截图占位 32】**：多 Agent 频道/角色面板

---

### 33. 用 `codex exec` 做脚本化 / CI / 隔离 eval

交互 TUI 适合探索；流水线适合：

```bash
codex exec "..."     # 非交互跑完整 agent loop
codex review         # 非交互评审
codex fork --last
codex resume --last
```

原则：**Stop Prompting. Start Looping.**  
完成条件写成命令，而不是感觉：

```text
DONE WHEN: npm test returns 0 AND npm run lint returns 0.
```

> 📷 **【截图占位 33】**：CI 里跑 `codex exec` 的日志

---

## 五、Skill 与资产化：重复三次就该固化（34–41）

### 34. Skill 优先：一次写好，多端复用

先装成熟 skill 集（支持 Codex 的 `agents/openai.yaml` 等），再写自己的。

推荐心智：

- `/grilling`：分轮提问，而不是连珠炮  
- `/prototype`：用可分享的 HTML 原型  
- `/writing-for-agents`：写任何给 Agent 读的东西（AGENTS、system prompt、docs）  
- `/wizard`：交互式配置向导  
- `/wait-what`：听不懂就用领域语言重聚焦  

更新示例：`npx skills update`（以你实际工具链为准）。

> 📷 **【截图占位 34】**：已安装 skill 列表

---

### 35. Agent Plugins：Skills + MCP 一次打包多端用

按开放标准把 Skill 与 MCP 配置打成插件，Codex / ChatGPT / 其他兼容客户端复用。  
原则：连接器归插件，流程归 skill，别散落在聊天记录里。

> 📷 **【截图占位 35】**：插件市场 / 已安装插件

---

### 36. 从近 30 天会话挖重复劳动

每周固定问：

```text
分析我近 30 天的 Codex 会话。
找出我重复做了 ≥3 次的操作模式。
对每类重复劳动建议：
1) 做成 Skill
2) 做成自定义 Agent
3) 做成 Automation
给出优先级与最小可行版本。
```

重复三次，还不固化，就是在交「懒税」。

> 📷 **【截图占位 36】**：重复劳动清单 → Skill 建议表

---

### 37. 用历史 session 迭代 skill（可 backtest）

```text
用 skill X 对照历史 session Y：
- 若当时有 X，哪些步骤可跳过？
- 哪些失败会避免？
- 修改 skill 文案，再对另外 3 个 session 做 backtest。
输出 diff 与是否建议合并。
```

Skill 不是写完就放着，是**用旧会话当测试集**。

> 📷 **【截图占位 37】**：skill 修改前后对比

---

### 38. 踩坑固化成 Skill，而不是修单条成品

做长视频 / 口播 / 图文时，常见坑：

- 音画不同步、字幕切断整句  
- 角色一致性崩、BGM 盖过人声  
- 竖屏参数横屏全失效  
- 渲染到一半磁盘爆  

不要只修这一条成片。把规则逐步写进 Skill，例如：

```text
每次失败必须追加到 skill 的「已知失败模式」：
现象 → 根因 → 检查命令 → 修复动作 → 回归标准
下次流水线自动执行这些检查。
```

Codex 负责调度，生图 / TTS / 时间轴 / 压制各用专长工具，最后用验收清单收口。

> 📷 **【截图占位 38】**：某条 Skill 里的「失败模式」章节

---

### 39. Codex 五件套：AppShots / meta / PLAN.md / Skill / `/goal`

入门组合：

1. **AppShots**：界面问题直接截图给它  
2. **meta 线程**：专门放决策与约束，不和脏实现搅在一起  
3. **PLAN.md**：可改的计划真源  
4. **Skill**：重复流程  
5. **`/goal`**：长程收口  

再配合 Annotate / Fork / Archive / Plan / Plugin 从零练一遍，比看十篇概念文有用。

> 📷 **【截图占位 39】**：PLAN.md + meta 线程 + 当前 goal 一屏

---

### 40. 解释时强制 Visualize

写入 AGENTS：

```text
When explaining architecture, data flow, or multi-step logic,
you MUST produce a visualization (diagram/ascii/mermaid)
before long prose. Prefer one clear diagram + short bullets.
```

减少「看起来懂了其实没懂」。

> 📷 **【截图占位 40】**：Agent 输出的架构图示例

---

### 41. 垂直 skill 直接装，别从零写

动效、转场、组件动画、写作结构、infra wizard……社区已有大量现成 skill。  
原则：**先搜再写**；写自己的只补你业务独有的部分。

> 📷 **【截图占位 41】**：安装某个 UI transition skill 后的调用示例

---

## 六、日常操作与维护：小习惯拉开巨大差距（42–47）

### 42. 归档 one-off session，侧边栏只留活项目

临时排查、一次性脚本、试错会话：做完就 Archive。  
侧边栏只留：

- 长期项目 Task  
- 专用角色（发布、CI、文档）  
- 进行中的 goal  

侧边栏干净，跨会话调度时才找得到「那个管发布的会话」。

> 📷 **【截图占位 42】**：归档前后侧边栏对比

---

### 43. 上下文满了：新 chat + `@` 旧会话续作

硬撑到 context rot 再继续，是最贵的省钱方式。

```text
新开会话。
请 @ 引用上一个会话 / PROJECT_STATUS.md / 关键文件。
先用 10 行复述当前状态，我确认后继续。
```

> 📷 **【截图占位 43】**：新会话中 @ 引用旧会话

---

### 44. 别用内置搜索找旧线程：新开 chat 让 Codex 自己找

内置搜索经常难用。直接：

```text
新开 chat。
帮我找到上周关于 XXX 的会话/结论，
总结关键决策与未完成项，给出会话标题或 ID。
```

> 📷 **【截图占位 44】**：Agent 找回旧线程的结果列表

---

### 45. 编辑「最近一条 prompt」重生成，比新开长对话更省

指令只差一句时：

1. 编辑上一条 prompt  
2. 重生成  

比在污染上下文里继续扯皮更干净、更便宜。

> 📷 **【截图占位 45】**：编辑最近 prompt 的 UI 操作

---

### 46. 高亮文本「Add to chat」注解上一条

浏览器扩展 / 客户端能力：在页面或输出里高亮关键段，一键挂到对话。  
少一次复制粘贴，就少一次上下文丢失。

> 📷 **【截图占位 46】**：高亮 → Add to chat 操作示意

---

### 47. 每周清理缓存 / 旧 thread；磁盘爆了先列清单

**周清理提示词：**

```text
set up a weekly automation that clears out old codex cache,
thread logs, temp files that are safe to remove.
don't touch anything active or recent.
only stale data that's just sitting there taking up space.
run this automatically every week without asking me each time.
```

**扫磁盘（先列清单，先别删）：**

```text
scan my system to find what's eating up storage.
look for large files, old installers, unused apps,
cache folders, stale project folders, and anything else safe to clean up.
list everything by category with size,
and flag what's safe to auto delete vs what needs my review.
don't delete anything yet, just give me the list first.
```

另可让便宜模型定期：杀测试残留 headless 进程、清缓存、巡检机器——电脑从烫到顺，有时只差这一条自动化。

> 📷 **【截图占位 47-1】**：周自动化配置  
> 📷 **【截图占位 47-2】**：磁盘占用分类清单

---

## 七、场景扩展：Codex 不只写代码（48–50）

### 48. 手机遥控 + Computer / Chrome / Gmail / Calendar

配对手机后：路上派活、看 diff、续 goal。  
再接浏览器、邮箱、日历，把「写代码」扩成「推进工作」。

安全建议：

- 不需要遥控就关掉远程连接  
- 最小权限；敏感操作仍确认  

> 📷 **【截图占位 48-1】**：手机端 Codex 控制电脑  
> 📷 **【截图占位 48-2】**：Computer / Chrome 权限设置

---

### 49. USB 插手机 / Kindle，把 Codex 当通用设备 UI

插上设备后：

```text
我把手机（或 Kindle）插到电脑了。
请识别设备，并帮我：
- 清理无用应用 / 整理相册 / 备份
- 处理深层菜单里难找的设置
- 按我的清单找文件或书
先列将执行的操作，危险项等我确认。
```

老设备 UI 不会用时，这比你自己点菜单快一个时代。

> 📷 **【截图占位 49】**：USB 已连接 + Agent 列出可执行操作

---

### 50. 嵌进业务：飞书文档、浏览器自动化、内容流水线、结束汇报

把 Agent 嵌进真实业务，而不是只在 demo 仓库玩：

**飞书文档协作**

```text
用飞书 CLI：创建/更新文档，按模板排版，
改完给出链接与变更摘要。
```

**浏览器自动化**  
订阅内做 Web 流程（打开页、填表、截图验收），适合回归检查。

**内容流水线**  
批量生成 prompt → 生图 → 导出 Adobe 元数据 CSV；模型用 Luna High 等更划算档。

**任务结束自动汇报**

```text
任务结束时，发一封邮件（或消息）总结：
改了什么、测了什么、风险、下一步。
```

总原则不变：

> **可重复的进 Skill，可验收的进清单，贵模型只做决策。**

> 📷 **【截图占位 50-1】**：飞书文档被 Agent 更新后的页面  
> 📷 **【截图占位 50-2】**：内容流水线产物目录 / CSV  
> 📷 **【截图占位 50-3】**：任务结束邮件摘要

---

## 结尾：如果只做 10 条

八个月下来，我会按这个顺序落地：

1. 写 AGENTS.md（规则 + 路由）——技巧 1、2  
2. 交付工程师模式——技巧 6  
3. 先调研再写代码——技巧 5  
4. 开 Luna Max + Sol/Luna 分工——技巧 9、10  
5. research 后 set_goal + goal.md——技巧 19、21  
6. 跨模型 review——技巧 30  
7. 重复劳动固化 Skill——技巧 36  
8. 收工 PROJECT_STATUS——技巧 7  
9. 归档 + 周清理——技巧 42、47  
10. Agent 自己跑应用验收——技巧 8  

其余 40 条，是这 10 条长出来的肌肉。

---

## 截图清单（方便你按号填充）

| 编号 | 建议内容 |
|:---|:---|
| 01 | AGENTS.md 全文 |
| 02 | Routing 段落 |
| 03 | 文档前 7 行摘要 |
| 04 | STE 全局规则 |
| 05-1 / 05-2 | GitHub 插件；调研输出 |
| 06 | 验收清单 |
| 07 | PROJECT_STATUS.md |
| 08 | Agent 跑 app/测试 |
| 09 | Luna Max 开关 |
| 10-1 / 10-2 | luna-worker.toml；委派界面 |
| 11 | Fable+Codex 流转 |
| 12 | Claude 插件安装成功 |
| 13 | 模型与 effort |
| 14 | 主线程+运维线程 |
| 15 | sol-advisor 生效 |
| 16 | 三档路由表 |
| 17 | Router 模型选择器 |
| 18 | 定时自动化 |
| 19 | research→goal |
| 20 | 自动 goal |
| 21-1 / 21-2 | goal.md；/goal 一行 |
| 22 | progress 页 |
| 23 | 长跑时间线 |
| 24 | Sol 裁判结构 |
| 25 | 多线程侧边栏 |
| 26 | 全局 Task 视图 |
| 27 | Subagent 树 |
| 28 | worktree 目录 |
| 29 | 摘要+file:line |
| 30 | 跨模型 review |
| 31 | 依赖图 |
| 32 | 多角色面板 |
| 33 | CI 中 codex exec |
| 34 | skill 列表 |
| 35 | 插件页 |
| 36 | 重复劳动→Skill |
| 37 | skill diff |
| 38 | 失败模式章节 |
| 39 | PLAN+meta+goal |
| 40 | 架构图 |
| 41 | UI skill 调用 |
| 42 | 归档前后 |
| 43 | @ 旧会话 |
| 44 | 找回旧线程 |
| 45 | 编辑最近 prompt |
| 46 | Add to chat |
| 47-1 / 47-2 | 周清理；磁盘清单 |
| 48-1 / 48-2 | 手机遥控；权限 |
| 49 | USB 设备操作列表 |
| 50-1 / 50-2 / 50-3 | 飞书；产物；邮件 |

---

*备份文件：`使用Codex8个月-我总结的50个小技巧.backup-2026-08-07.md`（含引用链接的旧版）*  
*本版：去掉引用，填充可执行正文，截图由你后续替换占位符。*
