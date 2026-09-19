# Flatrouter 待发推文（@aehyok）

发布方式：引用官方帖  
https://x.com/flatrouter/status/2097573764720705764

专属链接：把文末 `https://flatrouter.com` 换成你的 UTM / ref 链接。

配图建议（任选 1–3 张，比纯文字转化高）：
1. Codex / Cursor 里改 `OPENAI_BASE_URL` 的截图
2. Flatrouter 控制台一条请求的模型 / token / 花费
3. GPT Image 2.5 直接出的 4K 图（你今天刚做过 2 vs 2.5 对比，很适合）

---

## 主推（推荐直接发）

8月份是属于开源模型的，9月上旬绝对属于闭源模型的。
前有Fable 5.1。现有 GPT-6 Astra 和 GPT Image 2.5。

但是模型越来越强，我越来越不敢用了。 
不是模型不行。
是官方 API 太贵了。

$10 / 1M input tokens，比 GPT-5.6 Sol 翻了一倍。
Codex、Claude Code 挂一晚上，自己改、自己测、自己修，天亮一看账单，你再也不敢让他深夜自己跑长程任务了。

今天把 @flatrouter 接进自己的工作流里，只改了一行：

OPENAI_BASE_URL=https://api.flatrouter.com/v1

streaming、tool call、vision 原样能用。
不是换 SDK，不是换协议，随时还能切回官方。

价格这块把口径说清楚：

GPT-6 Astra 走 Advanced 套餐，折算有效单价大约 $0.76 / 1M input。
不是全场一个价，不同套餐折算率不同。
但这个差价已经够把「不敢跑」变成「多跑几轮」。

出图更直接。
GPT Image 2.5 的 Flare / Sunburst 都上了，一张 ¥0.05，1K、2K、4K 同价。
按张计费，不按分辨率。
以前为了省钱先出 1K 看看，现在直接冲 4K。
100 张封面 / UI 原型，也就 5 块钱。

稳定性我比较在意。
多区域账号池 + 熔断 + 自动故障转移，节点被限流会切到下一个健康节点。
不敢说永远不挂，但至少不是凌晨三点死在一个 429 上。

而且新用户一次性 ¥19.9，拿 700 计费积分，按平台口径大约等于 $100 官方用量额度，30 天有效。
积分是预付的用量额度，不是现金，不能提现也不能转。
到期前续费，没用完的滚进新周期；到期不续，剩下的就作废。

一顿早饭的钱，够把手头那个一直想跑的 Agent 完整跑一遍，再决定要不要留下。

试用入口：https://flatrouter.com

---

## 短版（不想发太长时用）

GPT-6 Astra 官方 $10 / 1M input，比上一代贵一倍。
模型是真能干活，也是真不敢放开用。

同一个 Astra，走 @flatrouter 的 Advanced 套餐，折算有效单价大约 $0.76。
不是换弱模型，是换一行 base_url：

OPENAI_BASE_URL=https://api.flatrouter.com/v1

Codex、Cursor 直接认，streaming / tool call / vision 原样能用。

GPT Image 2.5 也同步了，一张 ¥0.05，1K / 2K / 4K 同价。
批量出封面、UI 原型，别再先出个 1K 看看，直接冲 4K。

新用户 ¥19.9 拿 700 计费积分，按平台口径大约等于 $100 官方用量额度，30 天有效。
积分是用量额度，不是现金；到期前续费才滚存。

一顿早饭的钱，够把你手头那个 Agent 完整跑一遍。

https://flatrouter.com

---

## 评论区可补一句

官网试用：https://flatrouter.com
（换成你的专属链接）

口径补充：上面 $0.76 是 Advanced 套餐折算的有效单价，不同套餐折算率不同。积分是预付用量额度，不可提现、不可转让。
