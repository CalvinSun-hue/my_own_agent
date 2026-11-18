# 日志是什么？`logging` 速查

> 补基础用。阶段 4 一上来就假设"你会用日志"，其实这一课一直没人给你补——本文补上。
> 配一个可右键 Run 的实验文件：`速查/实验_logging_分段.py`，边看边跑。

## 0. 一句话：日志是程序的"行车记录仪"

**日志（log）= 程序在运行时自动留下的、带格式的记录：什么时候、哪个模块、什么级别、发生了什么。**

三个关键词：

| 词 | 意思 | 例子 |
|---|---|---|
| 时间 | 什么时候发生的 | `2026-11-18 08:40:01` |
| 出处 | 哪个模块/日志器记的 | `agent`（`logging.getLogger(__name__)`） |
| 级别 + 消息 | 多重要、什么事 | `INFO 调用工具 add，参数 {"a": 2}` |

它**不是**给用户看的输出（那是 `print` / 界面），而是**给"查案"用的证据**：程序没崩但行为不对、线上偶发失败、模型答非所问时，翻日志看"当时到底发生了什么"。

C 类比：`fprintf(stderr, ...)` 的正式版——多了级别、出处、开关、可重定向，还能在出错时自动带上调用栈。

## 1. 为什么不直接用 `print`

| 维度 | `print` | `logging` |
|---|---|---|
| 开关 | 只能删代码 | `setLevel(WARNING)` 一行过滤，代码不动 |
| 级别 | 没有 | DEBUG / INFO / WARNING / ERROR / CRITICAL |
| 出处 | 没有 | 每条自带 logger 名（模块名） |
| 去处 | 只能往屏幕 | `Handler` 决定：屏幕 / 文件 / 内存 / 网络 |
| 异常 | 只能打印 `str(e)`，没有栈 | `log.exception()` 自动带完整 traceback |
| 性能 | 每次都算字符串 | 懒格式化：被过滤时连字符串都不算 |
| 能否测试 | 拦 `print` 很脏 | **能**：换个 Handler 就抓得到（阶段 4 的核心） |

## 2. `logging` 的四个角色

```
代码: log.info("...")
  │
  ▼
Logger（日志器）        ← 你在代码里拿到的对象；决定"级别门槛"，自带名字（通常 __name__）
  │  propagate（冒泡）
  ▼
root Logger（根日志器）  ← 所有没设 propagate=False 的 logger 最后都冒泡到这里
  │
  ▼
Handler（处理器）        ← 决定"写到哪"：StreamHandler(屏幕) / FileHandler(文件) / ...
  │
  ▼
Formatter（格式器）      ← 决定"每行长什么样"：%(levelname)s %(name)s %(message)s
```

一句话分工：**Logger 决定"要不要说"，Handler 决定"说给谁听"，Formatter 决定"怎么说"**。

## 3. 最小可运行例子

```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s %(name)s %(message)s")
log = logging.getLogger(__name__)

log.debug("这条看不到：级别比 INFO 低")
log.info("第 %d 轮请求，历史 %d 条", 1, 2)
try:
    1 / 0
except ZeroDivisionError:
    log.exception("调用模型失败")     # ERROR + 完整调用栈
```

输出大意：

```
INFO __main__ 第 1 轮请求，历史 2 条
ERROR __main__ 调用模型失败
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```

三个要点：

1. `basicConfig` 只需要在**入口**调一次（以后每个模块用 `getLogger(__name__)` 就行）；
2. **不配 `basicConfig` 时 `INFO` 看不到**——root 默认级别是 `WARNING`，这是"日志写了却看不到"的头号原因；
3. `%s` / `%d` 是**懒格式化**：日志被过滤掉时不会去算字符串（f-string 会提前算，所以规范写法用占位符）。

## 4. 五个级别 + 过滤规则

| 级别 | 数值 | 什么时候用 | 本项目哪里用过 |
|---|---|---|---|
| `DEBUG` | 10 | 排查细节：参数、内部状态 | 没有直接写；`capture_logs` 把 root 调到 DEBUG 才抓得到 INFO |
| `INFO` | 20 | 正常流程的关键节点 | `agent.py`：第几轮请求、调用工具、工具返回 |
| `WARNING` | 30 | 能继续，但有隐患 | 无（阶段 3 砍了重试） |
| `ERROR` | 40 | 某个操作失败，程序还能活 | `log.exception`（模型调用失败） |
| `CRITICAL` | 50 | 程序没法继续 | 无 |

**过滤是"两道门"**：

```
记录级别 >= Logger 的有效级别？  ──否──▶ 丢弃
   │是
记录级别 >= Handler 的级别？     ──否──▶ 丢弃
   │是
输出
```

- **有效级别（effective level）**：logger 自己没设 level 时，**向上继承**父级，一直到 root；root 默认 `WARNING`；
- `Logger.setLevel(logging.DEBUG)` 把第一道门开到最低；
- `Handler` 默认 level 是 `0`（NOTSET），第二道门不拦。

## 5. 常用 API 小抄

| 要干什么 | 写法 | 备注 |
|---|---|---|
| 拿日志器 | `log = logging.getLogger(__name__)` | 模块级，一个模块一个 |
| 拿根日志器 | `logging.getLogger()` | **不传名字**就是 root |
| 入口配置 | `logging.basicConfig(level=..., format=...)` | 只生效一次 |
| 设级别 | `log.setLevel(logging.INFO)` | 也接受数字 |
| 读级别 | `log.level`（属性，数字） | root 用 `logging.getLogger().level` |
| 挂处理器 | `log.addHandler(h)` / `root.addHandler(h)` | 也能挂到子 logger |
| 摘处理器 | `log.removeHandler(h)` | 用完必须摘，否则串味 |
| 屏幕处理器 | `logging.StreamHandler()` | 默认写 stderr |
| 文件处理器 | `logging.FileHandler(path, encoding="utf-8")` | 中文必须显式 utf-8 |
| 内存处理器 | `logging.StreamHandler(io.StringIO())` | 测试里常用 |
| 设格式 | `h.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))` | 不设则只输出消息 |
| 记日志 | `log.debug/info/warning/error/exception(msg, *args)` | `exception` 额外带栈 |
| 关闭 | `h.close()` | FileHandler 必须关，否则可能没落盘 |
| 冒泡 | `log.propagate`（默认 True） | 设 False 后 root 抓不到 |

## 6. 阶段 4 里日志怎么接起来的

**业务侧（`阶段3/agent.py`）三处**：

| 位置 | 记什么 | 事后能回答 |
|---|---|---|
| `chat()` 每轮开头 | 第几轮 + 历史条数 | 模型当时看的是多长的对话 |
| 工具执行前 | 工具名 + 参数原文 | 模型到底要什么、给了什么参数 |
| 工具执行后 | 工具名 + 结果 | 工具是没跑，还是跑错了 |
| `_call_model()` 异常分支 | `log.exception` 然后 `raise` | 哪一行炸的、谁调上来的 |

**测试侧（`阶段4/support.py` 的 `capture_logs`）**：

```
with 块开始 → root.addHandler(临时 FileHandler) + root.setLevel(DEBUG)
   业务代码跑 → log.info(...) 冒泡到 root → 写进临时 .log 文件
with 块结束 → removeHandler + close（落盘）+ 恢复 root 级别
读文件 → assertIn("5", text)    ← 日志变成"可断言的对象"
```

这就是"日志能被测试"的全部秘密：**业务代码只认 `log`，出口由 Handler 决定，测试换出口即可**。

## 7. 七个坑（按踩到的频率排序）

1. **写了 `log.info` 但看不到**：没配 `basicConfig` / root 还是 WARNING。不是没写对，是门关着。
2. **`capture_logs` 抓不到 INFO**：`__enter__` 里 `setLevel(self.old_level)`（把原级别设回去 = 没调），应 `setLevel(DEBUG)` 或 `setLevel(self.level)`。
3. **读到的日志文件是空的**：忘了 `handler.close()`，缓冲区没刷盘。
4. **测试互相污染**：`__exit__` 没恢复 root 级别，或没 `removeHandler`。
5. **中文乱码**：`FileHandler` 不写 `encoding="utf-8"`，Windows 默认 GBK 写、按 UTF-8 读就乱。
6. **在 `except` 外面调 `log.exception`**：没有"当前异常"，只会输出 `NoneType: None`。
7. **`log.propagate = False` 的子日志器**：root 抓不到，`capture_logs` 就会"什么都没抓到"。

## 8. 自测（答完再往下走）

1. `print` 和 `log.info` 最本质的区别是什么？（提示：出口能不能换）
2. 不配 `basicConfig` 时，为什么 `log.info` 看不到、而 `log.warning` 看得到？
3. `setLevel` 设的是"Logger 的级别"，那 `Handler` 的级别管什么？两道门分别在哪？
4. 为什么 `log.exception` 必须写在 `except` 块里？
5. `capture_logs` 为什么"不用改业务代码"就能抓到日志？
6. 为什么 `FileHandler` 一定要 `close()`、一定要写 `encoding="utf-8"`？

答不上来就去看 `速查/实验_logging_分段.py` 对应实验的输出，比看文字快。
