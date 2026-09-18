论文已发布。权重已开源。现在是时候让 Apodex 1.1 开始工作了。

使用最新版本构建：
🛠️ 开源框架：
https://github.com/ApodexAI/FrontierAgent
🤗 开放权重：
https://huggingface.co/collections/apodex/apodex-11

另外提供：
1. Apodex 1.1 核心模型 API — 免费两周：apodex-1.1 和 apodex-1.1-mini 🔌 获取您的 API 密钥：https://platform.apodex.ai 

2. 代理 API — 首月自动享受 20% 折扣。

3. 对于 Apodex 1.0 网络应用的早期付费用户：🎁 您的账户中已添加 2,000 感谢积分。无需额外操作，只需继续使用 Apodex 1.1 实时工作台进行构建：





Tailscale 又开源了一个更轻量的工具 Tailcat,让 SSH 远程连接更加方便了。

你可以不用安装 Tailsale，不用注册账号，不用开端口，不用 root，也不改你的路由和 DNS。两台机器，发个短 token 过去，直接就连上了，全程端到端加密。

来看看它的主要功能:

1、P2P 加密连接：基于 WireGuard，自动 NAT 穿透，失败可走 DERP 中继。
2、端口转发：远程访问本地 Web、API、Ollama、LM Studio 等服务。
3、SSH 远程连接：支持临时 SSH、远程执行命令。
4、文件传输：支持单文件、文件夹、SCP、SFTP。
5、文件共享：可共享目录，也能做只允许上传的“临时收件箱”。
6、SOCKS5 代理：通过另一台电脑访问网络。
7、Exit Node：让流量通过另一台机器出口。
8、网络检测：支持 Ping，可查看当前是 P2P 直连还是 DERP 中继。
9、临时 / 固定 Token：无需账号，分享 Token 即可连接，也支持长期固定密钥。
10、跨平台：支持 macOS、Linux、Windows、Docker。
11、还有更多功能有待挖掘

最后附上开源项目地址：https://github.com/tailscale/tailcat



你可以使用 Tailcat 来直接
Tailcat 就是一个不需要 Tailscale 账号、也不依赖 Tailscale 控制面的点对点加密连接工具。

想给朋友传个大文件，用微信文件传输有大小限制，还得绕道网盘上传下载一大圈，很麻烦。

最近 Tailscale 团队出了个 tailcat，把两台电脑直接连上的看家本事，单独拆分做了文件传输工具。

用起来很简单，一台电脑作为接收端，屏幕上会给出一串短代码，另一台输入这串代码就连上了，文件和代码就能直接发给对方。

GitHub：http://github.com/tailscale/tailcat

连接先由官方服务器牵线，之后两台电脑就直接对传，不再绕任何第三方，传输全程是加密的。

碰到实在连不通的网络，才退回服务器帮忙中转，保证怎么都能传得动。

不用注册账号，不用管理员权限，也不改系统网络设置，就是个装上就能用的小工具。

还有个网页版，打开浏览器就能和对面互传文件和文字，Linux、Windows 也都有现成安装包



Tailscale 自己出手，做了个反直觉的东西，Tailcat，一句话概括就是：没有 Tailscale 的 Tailscale。

不用注册账号，不用装 VPN，不用开端口，不用 root，也不改你的路由和 DNS。两台机器，发个短 token 过去，直接就连上了，全程 WireGuard 端到端加密。打得通走直连，打不通自动走 DERP 中继，一点不耽误。

连上之后能干嘛？我给你数数：


两台电脑互传文件

把本地端口甩出去

直接 SSH 进去

当 SOCKS5 代理

当出口节点

浏览器里也能传

Go 写的，全程用户态，官方开源。像 netcat，但走的是 Tailscale 的数据面。


https://tailscale.github.io/tailcat/



万万没想到一个语音识别还能这么玩。原来我一直以为 OpenAI 的 Whisper 已经到了语音识别的天花板了。看来是我认知太浅薄了。

由于老婆就是川渝那边的，方言的味道绝对十足。如果走在街上，加上外界环境的嘈杂声，我之前用的 Whisper 测试过简直就是个瞎子，识别出来叽里呱啦的一大串乱七八糟的字符真的有点神奇。

这两天无意间看到了这个开源的模型，Hojo-ASR-Multi-V1，据说是语音识别领域的“新星”。

🔥Open ASR Leaderboard 多语言榜全球第 7，开源多语言 ASR 第 1。
🎉五语种平均 WER 3.54%，模型权重开放、评测公开、结果可复现。
😄同时支持普通话、英语、粤语和四川话等多语言、多方言识别。

特意找来测试了一下，发现真的有意思。

更有意思的是 Hojo 的处理过程：声音 → Qwen3-Omni 音频编码器听懂声音 → Adapter 转换特征 → Qwen3-4B 生成文字。

通俗一点的讲就是：声音进来 → 音频编码器先“听懂”声音 → Adapter 把声音信息翻译成大模型能理解的格式 → Qwen3-4B 再把它变成文字。

而 Whisper：声音进来 → 转成频谱图 → Whisper 编码器提取声音信息 → Whisper 解码器直接生成文字

两者对比就是Whisper 的重点是 听声音 → 写文字，而 Hojo 则更偏向 听声音 → 理解声音 → 再根据理解生成文字。

所以最后我在本机做了一个测试结果还是非常不错的。
先解释两个百分比，CER = Character Error Rate，字符错误率。
然后可以看看我的视频 Hojo 和 whisper的对比，做了三个例子，川渝话、广东话、普通话。

川渝话：hojo CER= 0%, whisper CER=42.9%
广东话：hojo CER=18.8%, whisper CER=43.8%
普通话：hojo CER=16.7%, whisper CER=25.0%

应该说 hojo这一套效果还是非常不错的。
最后附上他们的开源模型，有兴趣的可以本地部署玩玩看：https://huggingface.co/HojoAI/Hojo-ASR-Multi-V1






给我的 Grok Bot 配上了一个金融情报官，看看它能不能帮我赚个三瓜俩枣。

Grok Bot 不能直接对接第三方API
Grok Bot 的额度消耗比较快
手机、电脑、无论安卓还是苹果都可以直接远程云电脑

所以，我想直接让 Grok Bot 专门搭建一个「金融情报官」的Agent，来给我打工，专门就是帮我分析各路上市公司。

那么如何进行搭建呢？

第一个首先


