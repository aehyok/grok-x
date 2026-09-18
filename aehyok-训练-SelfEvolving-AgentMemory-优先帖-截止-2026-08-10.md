# @aehyok · 模型训练 / Self-Evolving / Agent Memory

- **账号**：[@aehyok](https://x.com/aehyok)
- **截止**：2026-08-10
- **收录规则（硬过滤）**
  - ✅ 只收 **自己发的主帖**（`from:aehyok -filter:replies`）
  - ✅ 自己发的 **X Article** / 带 Article 的主帖
  - ❌ **不收任何评论、回复**（含自己线程里的续楼回复）
  - ❌ 不收别人帖子下的互动

---

## 优先 6 条

| # | 话题 | 主题 | 时间 | 浏览 | 链接 |
|:---:|------|------|:---:|---:|------|
| 1 | Agent Memory | **EverOS 长文（X Article）**：上下文≠记忆、Markdown 记忆层、边界、沉淀 skill | 2026-06-24 | ~8.3k | [推广帖](https://x.com/aehyok/status/2069631779355684919) · [Article](https://x.com/i/article/2069631314291298304) |
| 2 | Memory 工程 | codebase-memory-mcp：代码库知识图谱 | 2026-06-27 | ~2.6万 | [2070851979317006557](https://x.com/aehyok/status/2070851979317006557) |
| 3 | Self-Evolving | autoresearch：评估→优化无限循环 | 2026-03-20 | ~16.1万 | [2034810825026990250](https://x.com/aehyok/status/2034810825026990250) |
| 4 | Self-Evolving | Apodex 白送算力主帖（Self-Evolving 产品叙事线程起点） | 2026-07-21 | ~1.0万 | [2079458784670560550](https://x.com/aehyok/status/2079458784670560550) |
| 5 | 进化闭环 | skill-up：评测→打分→再迭代 | 2026-08-06 | ~4.8k | [2085187079076741215](https://x.com/aehyok/status/2085187079076741215) |
| 6 | 模型训练 | 字节 10 万亿基础模型、不走蒸馏 | 2026-08-08 | ~3.4k | [2085902152099418567](https://x.com/aehyok/status/2085902152099418567) |

### 链接速查

1. 推广帖 https://x.com/aehyok/status/2069631779355684919 · Article https://x.com/i/article/2069631314291298304  
2. https://x.com/aehyok/status/2070851979317006557  
3. https://x.com/aehyok/status/2034810825026990250  
4. https://x.com/aehyok/status/2079458784670560550  
5. https://x.com/aehyok/status/2085187079076741215  
6. https://x.com/aehyok/status/2085902152099418567  

---

## 为何曾漏检：EverOS 长文（检索盲区说明）

| 项目 | 内容 |
|------|------|
| 推广帖 | https://x.com/aehyok/status/2069631779355684919 |
| 正式 Article | https://x.com/i/article/2069631314291298304 |
| 漏检根因 | **关键词搜索只索引「帖子短正文」，不索引 Article 全文**。该推广帖在搜索 API 里显示的 Content 几乎只有 `https://x.com/i/article/2069631314291298304`，正文里的「记忆 / EverOS / 上下文」等词**不进检索倒排**。 |
| 验证 | `from:aehyok (记忆 OR Memory)` 扫不到它；`from:aehyok EverOS` 也扫不到主帖（只扫到别人线程下的短回复）；用 `max_id:` 按时间轴才能看到该 status，且 Content 仅有 Article 链接。 |
| 流程失误 | 曾看到 conversation_id `2069631779355684919` 下的**短回复**，却没打开根帖，误当成闲聊串；也未专项扫 `from:aehyok url:x.com/i/article`。 |
| 补救规则 | 以后扫 Memory 等话题，除关键词外必须加：`from:aehyok url:x.com/i/article`，并对推广帖 `x_thread_fetch` 展开全文。 |

---

## 一、Agent Memory（仅主帖）

| 关联 | 时间 | 浏览 | 主题 | 链接 |
|:---:|:---:|---:|------|------|
| ★★★★★ | 2026-06-24 | ~8.3k | **【补录】EverOS 长文（X Article）**：上下文≠记忆、可维护记忆层、边界、MEMORY.md 起步 | [推广帖](https://x.com/aehyok/status/2069631779355684919) · [Article](https://x.com/i/article/2069631314291298304) |
| ★★★★★ | 2026-06-25 | ~859 | AI Memory 四问 + 可治理记忆 | [2069966554645893337](https://x.com/aehyok/status/2069966554645893337) |
| ★★★★★ | 2026-06-27 | ~2.6万 | codebase-memory-mcp | [2070851979317006557](https://x.com/aehyok/status/2070851979317006557) |
| ★★★★★ | 2026-04-09 | ~1.2万 | Hermes：三层记忆（会话/持久/Skill）+ 自我进化 + 记忆污染 | [2042158128029216858](https://x.com/aehyok/status/2042158128029216858) |
| ★★★★☆ | 2026-05-13 | ~8.9k | Tanka + EverMemOS 长期记忆 + RL 反馈闭环 | [2054385415944335645](https://x.com/aehyok/status/2054385415944335645) |
| ★★★★☆ | 2026-06-10 | ~3.7k | MEMORY.md 六条纪律 | [2064570005707268495](https://x.com/aehyok/status/2064570005707268495) |
| ★★★★☆ | 2026-06-30 | ~4.0k | 8 个 Agent 基建：压缩 / 代码记忆 / Planning with Files | [2071779147509313908](https://x.com/aehyok/status/2071779147509313908) |
| ★★★★☆ | 2026-06-14 | ~8.0万 | 上下文操作：`/btw` 防污染、`/clear`、`/fork` 等 | [2066001128282865920](https://x.com/aehyok/status/2066001128282865920) |
| ★★★☆☆ | 2026-06-27 | ~2.4k | Claude 命令：`/memory` `/compact` `/context` | [2070748612146106808](https://x.com/aehyok/status/2070748612146106808) |
| ★★★☆☆ | 2026-06-19 | ~6.3k | Context / context rot / `/clear` `/compact` | [2067976409344286896](https://x.com/aehyok/status/2067976409344286896) |
| ★★★☆☆ | 2026-07-02 | ~3.4k | Hook→Loop：压缩前摘要，防 `/clear` 丢信息 | [2072684444562178171](https://x.com/aehyok/status/2072684444562178171) |
| ★★★☆☆ | 2026-07-15 | ~2.6万 | ima 知识库 → WorkBuddy / Claude / Codex | [2077290625704308948](https://x.com/aehyok/status/2077290625704308948) |
| ★★★☆☆ | 2026-04-21 | ~7.3万 | NotebookLM 外脑 + 个人知识库工作流 | [2046410878296498597](https://x.com/aehyok/status/2046410878296498597) |
| ★★★☆☆ | 2026-04-22 | ~5.3万 | Obsidian 升维 AI 调度中心（8 工作流） | [2046852321846669404](https://x.com/aehyok/status/2046852321846669404) |
| ★★★☆☆ | 2026-07-28 | ~1.2万 | WorkBuddy Obsidian 技能库 = 第二大脑 | [2081919965352034486](https://x.com/aehyok/status/2081919965352034486) |
| ★★★☆☆ | 2026-08-02 | ~2.2k | WorkBuddy 教程：点名长期记忆 | [2083723710733885691](https://x.com/aehyok/status/2083723710733885691) |
| ★★★☆☆ | 2026-08-05 | ~3.6k | 小红书剪藏 → Obsidian 知识库 | [2084840151822512631](https://x.com/aehyok/status/2084840151822512631) |
| ★★★☆☆ | 2026-05-22 | ~4.9万 | Obsidian 创作台插件 + 知识库 | [2057667538763599892](https://x.com/aehyok/status/2057667538763599892) |
| ★★★☆☆ | 2026-04-30 | ~1.4k | Obsidian + Claudian 多模型第二大脑 | [2049730445039079694](https://x.com/aehyok/status/2049730445039079694) |
| ★★☆☆☆ | 2026-07-03 | ~1.2k | 10 采集项目：RAG 语料链路 | [2073048815314288707](https://x.com/aehyok/status/2073048815314288707) |
| ★★☆☆☆ | 2026-05-31 | ~7.1k | Obsidian 多知识库配置复用 | [2060897273530491033](https://x.com/aehyok/status/2060897273530491033) |

---

## 二、Self-Evolving / 闭环迭代（仅主帖）

| 关联 | 时间 | 浏览 | 主题 | 链接 |
|:---:|:---:|---:|------|------|
| ★★★★★ | 2026-03-20 | ~16.1万 | autoresearch：可度量即可持续优化 | [2034810825026990250](https://x.com/aehyok/status/2034810825026990250) |
| ★★★★★ | 2026-03-25 | ~14.1万 | autoresearch 一图胜千言 | [2036683771676877099](https://x.com/aehyok/status/2036683771676877099) |
| ★★★★★ | 2026-03-25 | ~1.6万 | autoresearch 评分算法（Pass/Fail Eval、双层迭代） | [2036793557827338590](https://x.com/aehyok/status/2036793557827338590) |
| ★★★★★ | 2026-04-09 | ~1.2万 | Hermes：自动提炼 Skill + 反馈后自我进化 | [2042158128029216858](https://x.com/aehyok/status/2042158128029216858) |
| ★★★★☆ | 2026-07-21 | ~1.0万 | Apodex Frontier Program 主帖 | [2079458784670560550](https://x.com/aehyok/status/2079458784670560550) |
| ★★★★☆ | 2026-06-25 | ~1.1万 | **X Article**：Apodex 多角色研究 + Verifier | [2070132059784274066](https://x.com/aehyok/status/2070132059784274066) · [推广帖](https://x.com/aehyok/status/2070493860850274436) |
| ★★★★☆ | 2026-07-23 | ~1.3k | Apodex：审计轨迹 / 自我校验流程 | [2080121573294678499](https://x.com/aehyok/status/2080121573294678499) |
| ★★★★☆ | 2026-08-06 | ~4.8k | skill-up 评测迭代闭环 | [2085187079076741215](https://x.com/aehyok/status/2085187079076741215) |
| ★★★★☆ | 2026-04-27 | ~4.7k | 大模型教小模型 + autoresearch 优化 skill | [2048592876150661218](https://x.com/aehyok/status/2048592876150661218) |
| ★★★★☆ | 2026-04-30 | ~2.1k | 交互式审稿 skill：反复循环打磨工作流 | [2049671877925511192](https://x.com/aehyok/status/2049671877925511192) |
| ★★★★☆ | 2026-07-08 | ~2.2k | Loop Engineering：核心是停止条件/评估准则 | [2074673342473486457](https://x.com/aehyok/status/2074673342473486457) |
| ★★★★☆ | 2026-06-04 | ~7.7万 | workflow + `/goal` `/loop` | [2062373789586063695](https://x.com/aehyok/status/2062373789586063695) |
| ★★★★☆ | 2026-06-13 | ~7.7k | Prompt → Context → Harness → Loop | [2065666854610468890](https://x.com/aehyok/status/2065666854610468890) |
| ★★★☆☆ | 2026-07-02 | ~3.4k | Hook 串成 Loop | [2072684444562178171](https://x.com/aehyok/status/2072684444562178171) |
| ★★★☆☆ | 2026-05-13 | ~8.9k | Tanka：记忆 + 强化学习反馈闭环 | [2054385415944335645](https://x.com/aehyok/status/2054385415944335645) |
| ★★★☆☆ | 2026-03-28 | ~1.0万 | 23 个 Agent Skills：可复用工作流 / 元技能 | [2037805631839908256](https://x.com/aehyok/status/2037805631839908256) |

---

## 三、模型训练过程（仅主帖）

| 关联 | 时间 | 浏览 | 主题 | 链接 |
|:---:|:---:|---:|------|------|
| ★★★★☆ | 2026-08-08 | ~3.4k | 字节训 10 万亿基础模型、明确不走蒸馏 | [2085902152099418567](https://x.com/aehyok/status/2085902152099418567) |
| ★★★☆☆ | 2026-02-24 | ~2.4k | Anthropic：数据训练 / 会话训练 / 蒸馏争议 | [2026233840096923901](https://x.com/aehyok/status/2026233840096923901) |
| ★★★☆☆ | 2026-06-29 | ~0.9k | Transformer 底层参数科普解读 | [2071394397770715609](https://x.com/aehyok/status/2071394397770715609) |
| ★★★☆☆ | 2026-04-07 | ~31.4万 | 17 skill 合集（含蒸馏 / 反蒸馏 skill，应用层） | [2041355324075225301](https://x.com/aehyok/status/2041355324075225301) |
| ★★☆☆☆ | 2026-07-07 | ~1.4k | Hy3：MoE 参数规格 | [2074376195878350863](https://x.com/aehyok/status/2074376195878350863) |
| ★★☆☆☆ | 2026-06-09 | ~3.3万 | Step 3.7 Flash：稀疏 MoE 规格 + 实测 | [2064257573164052526](https://x.com/aehyok/status/2064257573164052526) |
| ★★☆☆☆ | 2026-04-28 | ~1.0k | Ling-2.6-flash 开源规格 | [2049164379841769519](https://x.com/aehyok/status/2049164379841769519) |

> 说明：未发现「自己从零 fine-tune / SFT」类主帖；训练线以行业资讯 + 架构/参数科普 + 应用层蒸馏 skill 为主。

---

## 建议精选 12 条（仅主帖/文章）

| # | 主题 | 链接 |
|:---:|------|------|
| 1 | Memory 四问 | https://x.com/aehyok/status/2069966554645893337 |
| 2 | codebase-memory-mcp | https://x.com/aehyok/status/2070851979317006557 |
| 3 | autoresearch 方法 | https://x.com/aehyok/status/2034810825026990250 |
| 4 | Apodex 主帖 | https://x.com/aehyok/status/2079458784670560550 |
| 5 | skill-up 闭环 | https://x.com/aehyok/status/2085187079076741215 |
| 6 | 字节 10T 训练 | https://x.com/aehyok/status/2085902152099418567 |
| 7 | Hermes 三层记忆 + 自进化 | https://x.com/aehyok/status/2042158128029216858 |
| 8 | autoresearch 评分算法 | https://x.com/aehyok/status/2036793557827338590 |
| 9 | autoresearch 愿景图 | https://x.com/aehyok/status/2036683771676877099 |
| 10 | MEMORY.md 六条 | https://x.com/aehyok/status/2064570005707268495 |
| 11 | 上下文 /btw 全家桶 | https://x.com/aehyok/status/2066001128282865920 |
| 12 | workflow + /loop | https://x.com/aehyok/status/2062373789586063695 |

---

## 已排除（示例）

| 类型 | 例子 | 原因 |
|------|------|------|
| 别人帖下的回复 | EverOS「跨会话记忆值得实操」、skill 自进化短评等 | 评论/回复 |
| 自己线程续楼 | Apodex 主帖下「Self-Evolving Heavy-Duty Solver」拆解楼 | 属 `filter:replies` 回复，不进本清单 |
| 弱相关主帖 | DotA「影魔的记忆」、纯福利/额度帖 | 话题不相关 |

---

*仅主帖 + 自己文章 · 已剔除全部评论*
