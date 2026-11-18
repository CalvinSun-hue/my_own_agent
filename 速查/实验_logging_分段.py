"""速查 · logging 分段实验。

右键 Run 本文件，从上往下读输出（每个"实验"一个标题）。
stdout 和日志走的是不同流，PyCharm 控制台里偶尔交错，按标题找就行。

看这份文件之前，先读 速查/日志与logging速查.md 的 §0~§4。
"""

import io
import logging


def show(title: str) -> None:
    print(f"\n===== {title} =====", flush=True)   # flush：让标题和日志的顺序不乱


# ---------------------------------------------------------------------------
# 实验 1：什么都不配置时，日志是什么样的？
# ---------------------------------------------------------------------------
show("实验 1：不配置 logging（root 默认 WARNING）")
log1 = logging.getLogger("demo.levels")
log1.debug("debug：看不到")
log1.info("info：看不到")
log1.warning("warning：看得到")   # root 没 Handler 时，logging 用 lastResort（WARNING 起，写 stderr）
log1.error("error：看得到")


# ---------------------------------------------------------------------------
# 实验 2：入口 basicConfig —— 把 root 调到 INFO
# ---------------------------------------------------------------------------
show("实验 2：basicConfig(level=INFO)")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
log2 = logging.getLogger("demo.info")
log2.debug("debug：还是看不到（INFO 不够低）")
log2.info("info：这次看得到")
log2.error("error：也看得到")


# ---------------------------------------------------------------------------
# 实验 3：给单个 logger 自己开 DEBUG（不用改 root）
# ---------------------------------------------------------------------------
show("实验 3：logger.setLevel(DEBUG)")
log3 = logging.getLogger("demo.debug")
log3.setLevel(logging.DEBUG)
log3.debug("debug：看得到（这个 logger 自己开了 DEBUG）")


# ---------------------------------------------------------------------------
# 实验 4：log.error vs log.exception —— 差一个"调用栈"
# ---------------------------------------------------------------------------
show("实验 4：error 只有一句话，exception 带栈")
log4 = logging.getLogger("demo.trace")
log4.setLevel(logging.INFO)
try:
    1 / 0
except ZeroDivisionError:
    log4.error("error：只有一句话")
    log4.exception("exception：带完整调用栈")


# ---------------------------------------------------------------------------
# 实验 5：换出口 —— Handler 把日志抓进内存（这就是 capture_logs 的原理）
# ---------------------------------------------------------------------------
show("实验 5：Handler 重定向（内存版 capture_logs）")
stream = io.StringIO()                                   # 一个"假文件"
handler = logging.StreamHandler(stream)                  # 往它写的处理器
handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))

root = logging.getLogger()
old_level = root.level                                   # 记下旧级别（收工时还原）
root.addHandler(handler)
root.setLevel(logging.DEBUG)

log5 = logging.getLogger("demo.capture")
log5.info("工具 %s 返回 %s", "add", 5)                   # 业务代码只管写，不管去哪

root.removeHandler(handler)                              # 摘掉 = 停止抓
root.setLevel(old_level)                                 # 还原级别 = 不污染后面
print("抓到的内容：", stream.getvalue().strip(), flush=True)


# ---------------------------------------------------------------------------
# 实验 6：logger 名字 + 冒泡（为什么 capture_logs 挂在 root 上就能抓到"agent"的日志）
# ---------------------------------------------------------------------------
show("实验 6：子 logger 冒泡到 root")
log6 = logging.getLogger("demo.child")
log6.setLevel(logging.INFO)
log6.info("我属于 demo.child，冒泡上去被 root 的 handler 写出来")
log6.propagate = False
log6.info("这行在 root 上就看不到了（propagate=False）")
