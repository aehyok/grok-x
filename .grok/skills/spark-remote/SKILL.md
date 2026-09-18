---
name: spark-remote
description: >
  通过 cpolar SSH 登录远程机 spark-30b0（rowsen@16.tcp.cpolar.top）并执行远端命令。
  只负责连通和跑命令，不负责启停模型、Docker、测评。
  触发词：远程 SSH、连远程、spark-30b0、rowsen、cpolar、远程登录、/spark-remote。
  Use when the user runs /spark-remote 或要求登录这台远程机。
---

# Spark 远程 SSH

项目级 skill。本机 Windows → cpolar → `spark-30b0`。远端默认壳是 **zsh**。

连接参数（高优先在前）：环境变量 `SPARK_SSH_*` → `.grok/secrets/spark-remote.env`（已 gitignore）→ `%USERPROFILE%\.grok\secrets\spark-remote.env`。密码不准写进仓库或 SKILL.md。

## 怎么连

不要手写 `ssh -p ...`，不要用 Windows OpenSSH。一律走封装脚本：

```powershell
powershell -File ".grok/skills/spark-remote/scripts/remote.ps1" -Status
```

```powershell
powershell -File ".grok/skills/spark-remote/scripts/remote.ps1" -Script "hostname; whoami; pwd"
```

```powershell
@'
uname -a
uptime
'@ | powershell -File ".grok/skills/spark-remote/scripts/remote.ps1"
```

脚本会去掉 CRLF，远端执行 `tr -d '\r' | bash -s`。超时用 `-ConnectTimeout 30`。连不上先改 secrets 里的 `SPARK_SSH_PORT`（cpolar 端口会变）。

`-Status` 只确认：主机名、用户、时间、能否登录。

## 禁止

- PowerShell 双引号里塞 `grep -E 'a|b'`（会被拆管道）
- 把密码写进可提交文件
- 用 Auto 模式硬闯远程 SSH；需要用户批准或 always-approve
- 在本 skill 里扩展模型启停、Docker、测评流程
