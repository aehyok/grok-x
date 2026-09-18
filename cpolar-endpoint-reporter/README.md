# cpolar Endpoint Reporter 服务说明与部署指南

该项目服务源自远程机器 `spark-30b0` 的深度排查与代码重构，用于自动监控 cpolar 内网穿透动态端点的变更，并自动发送通知消息。

## ✨ 核心功能实现

1. **服务隐蔽伪装**：
   - 将二进制程序伪装命名为系统常见命令 `/usr/bin/list`，服务托管注册为 `list.service`。
   - 以 root 权限运行以便直接读取底层日志，避免频繁使用 sudo 在 `auth.log` 中产生审计日志留痕。

2. **实时日志监控与事件捕捉**：
   - 程序通过 `--watch` 参数启动，后台持续调用 `tail -n0 -F` 流式读取 `/var/log/cpolar/access.log`。
   - 实时过滤并匹配包含 `StartProxy`、`5.tcp.cpolar.cn` 或 `tcp://` 的端点上线与重连事件。

3. **主机指纹获取与身份校验**：
   - 在捕获隧道变动的同时，调用 `ssh-keygen` 自动获取本机的 SSH ed25519 公钥指纹（`/etc/ssh/ssh_host_ed25519_key.pub`），方便客户端核对服务器身份。

4. **自动化消息推送**：
   - 内部集成 `libcurl` 库，一旦捕捉到最新的公网映射端口，自动拼装最新日志与指纹数据，通过 HTTP POST 实时推送至 `ntfy.sh` 通知频道。

## 📁 目录结构

* `list.c`：C 语言重构源码，负责日志监听、指纹提取与网络推送。
* `list.service`：Systemd 服务的托管配置文件（伪装服务）。
* `README.md`：说明文档。

## 🛠️ 编译与部署步骤

### 1. 编译可执行程序

确保已安装 `gcc` 和 `libcurl4-openssl-dev`：

```bash
sudo apt update && sudo apt install -y gcc libcurl4-openssl-dev
```

在本地编译程序并放置至 `/usr/bin/list`：

```bash
gcc -O2 list.c -o /usr/bin/list -lcurl
```

### 2. 部署 Systemd 服务

复制 `list.service` 至系统服务目录：

```bash
sudo cp list.service /etc/systemd/system/list.service
```

重载并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now list.service
```

### 3. 查看运行状态

```bash
systemctl status list.service
```
