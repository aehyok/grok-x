# Prompt 02 · 下载封面图

先跑完采集，确认 samples.csv 里已有链接，再发这段。

```text
@Chrome

工作目录：./xiaohongshu-cover-lab
读取：./templates/samples.csv
保存封面到：./covers/
命名：{id}_likes{likes}_{category}_{note_id}.jpg
同时回写 samples.csv 的 cover_file 列。

任务：给每一行还没有封面文件的样本，下载封面图。

规则：
1. 优先从笔记页第一张图 / 卡片封面 img 下载。
2. 请求时带上浏览器里同样的 Cookie 和 Referer（当前笔记页）。
3. 下载失败、403、空白图、小于 20KB：不要死磕接口。改为对封面区域截图，保存为同名 jpg。
4. 不要下载正文里的第 2 张及以后的图。
5. 不要下载头像、二维码、水印条。
6. 每张间隔 2 秒。失败写 skip_reason，继续下一张。
7. 做完输出：成功 N、截图兜底 K、失败列表。
```
