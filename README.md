# PythonProject —— 跟着 StudyMate 手册学 Python

学习方式：**参考实现驱动 + 红绿循环 + 骨架逐级撤除**（见 [学习方法.md](学习方法.md)；骨架等级 L1–L5）。
参照项目：与本项目**同级**的 `studymate/`（《Python × Agent 项目式学习手册》配套代码，不在本仓库内）。

每个阶段统一流程：**划最小范围 → 按等级给骨架/需求 → 出验收测试（先在参考实现上跑绿）→ 一次填一个函数 → 全绿后审查/判卷 → 回答 3 个原理问题**。

> 2026-11-18：阶段目录由 `阶段N_重写` 统一改名为 **`阶段N`**（用 `git mv` 改的，历史里能看到改名记录）。

## 现在到哪了

> 这里只是索引；**详细进度以 [交接文档.md](交接文档.md) §0/§3 为准**（同一件事不写两处）。

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| 1 | 任务数据层：dataclass、自定义异常、JSON 持久化、排序/筛选 | ✅ **结业** | 29/29 测试绿，`__main__` 自测跑通 |
| 2 | 配置 + 模型客户端：`.env` 解析、Config、FakeClient、create_client | ✅ **结业** | 21/21 测试绿；`main.py` 真机调用 DeepSeek 通过 |
| 3 | 工具注册表 + agent 循环 | ✅ **结业** | 28/28 测试绿（`test_tools` 15 + `test_agent` 13） |
| 4 | 单元测试与工程化：自己写测试 + 日志 | 🚧 **部分结业** | 6/6 测试绿（工具 4 + 日志 2）；`agent.py` 三处日志已接；判卷/补课待做 |
| 5 | 笔记检索（简易 RAG：bigram 打分 + 路径防护） | 🚧 **进行中** | 准备包已就位（需求清单 + 3 篇样例笔记 + 速查 + 实验）；按 L4 六步法自己搭骨架 |
| 6 | MCP 服务器 | ⬜ 未开始 | — |

## 目录地图

```
PythonProject/
├── main.py                 ← 成品入口：load_config() + create_client()，已真机跑通
├── README.md               ← 本文件：项目地图 + 阶段索引
├── 学习方法.md              ← 固定学习流程（骨架等级 L1-L5 / 六步流程 / 提示阶梯）
├── 学习记录.md              ← 骨架等级账本：等级/求助次数/卡点/下次等级/回顾日期
├── AGENTS.md               ← 给 AI 的入口：硬性规矩 + 骨架等级
├── 交接文档.md              ← 换新对话/换 AI 时先看它（进度、下一步、偏好）
├── .env                    ← 本地密钥（被 .gitignore 忽略，绝不提交）
├── learning-skill/          ← 学习法的可移植成品（SKILL.md / 精简提示词 / zip）
├── 速查/                    ← 实验脚本、速查表、笔记（**不进阶段目录**）
│   ├── 基础语法卡点.md             self / dataclass / 装饰器 / with 等 14 条
│   ├── 英文命名对照.md             英文名/缩写的中文意思，按阶段分节（§0 是索引）
│   ├── 字符串与路径速查表.md        字符串/路径方法速查
│   ├── 日志与logging速查.md         日志是什么、logging 四件套、七个坑（阶段 4 补课用）
│   ├── RAG与笔记检索速查.md         RAG/bigram/打分/路径安全（阶段 5 用）
│   ├── 实验_方法速查.py            跑一下确认某个行为
│   ├── 实验_装饰器_分段.py          装饰器分段实验
│   ├── 实验_logging_分段.py         日志分段实验（7 段）
│   └── 实验_检索打分_分段.py        检索打分分段实验（7 段）
│
├── 阶段1/              ← ✅ 结业
│   ├── task.py             你的实现（Task / TaskStore / parse_due）
│   ├── test_task.py        29 个验收测试
│   ├── 说明_为什么.md       15 节"为什么" + C 对照表
│   └── 结构总览.md          类/方法/import/调用关系全景图
│
├── 阶段2/              ← ✅ 结业
│   ├── llm_config.py       你的实现（.env / Config / FakeClient / create_client 合在一个文件）
│   ├── test_llm_config.py  21 个验收测试
│   ├── 说明_为什么.md       12 节"为什么" + 4 个坑
│   └── 结构总览.md
│
├── 阶段3/              ← ✅ 结业
│   ├── tools.py            工具注册表（Tool / ToolRegistry / @tool / schemas / execute）
│   ├── agent.py            agent 循环（Agent.__init__ / _call_model / chat + 3 处日志）
│   ├── test_tools.py       15 个验收测试
│   ├── test_agent.py       13 个验收测试（内含"能假装要工具"的假客户端）
│   ├── 说明_为什么.md       11 节"为什么" + 5 个坑 + C 对照表
│   ├── 结构总览.md
│   └── 结构总览.html       可视化版（可折叠 + 步进演示）
│
├── 阶段4/              ← 🚧 部分结业
│   ├── support.py          测试支撑：sys.path 桥 / TmpDirTest / build_registry /
│   │                       FakeToolClient / capture_logs（日志重定向）
│   ├── test_tools.py       4 条自写测试（schema 必填/类型/描述、execute 返回字符串、默认值）
│   ├── test_agent_log.py   2 条日志测试（工具名+参数、工具结果）
│   ├── 说明_为什么.md       为什么这样写测试/日志、六个坑、C 对照表、判卷说明
│   └── 结构总览.md          部件表、两条数据流、判卷对照
│
├── 阶段5/              ← 🚧 进行中（只有准备包，代码还没写）
│   ├── 需求与部件清单.md    L4 起手包：部件清单 / 边界 / 13 条验收标准 / 写作顺序
│   └── notes/              3 篇样例笔记（C语言 / 高数 / Python）
│
└── 草稿/                    ← 归档区：练过的、练废的，只挪不删
    ├── tasks.py            474 行的手册 v2 版（无持久化，已被阶段 1 超越）
    ├── 参考task.py         最早的 JSON 持久化尝试（有 6 处语法错误，PyCharm 标红属正常）
    ├── register.py         阶段 3 的早期练习（工具注册表）
    └── tools.py            阶段 3 的早期练习（add / multiply）
```

## 四条规矩

1. **根目录只放"成品"和"索引"**：`main.py`、`README.md`、`学习方法.md`、`learning-skill/`。学习代码一律进 `阶段N/` 目录。
2. **每个 `阶段N/` 目录自包含**：自己的实现 + 自己的测试 + 自己的说明，**不跨目录 import**。这样任何一阶段都能单独跑、单独删。
   （唯一破例：`阶段4/support.py` 用 `sys.path` 指向 `阶段3/`，因为测试层天然横切——这是交接文档里定过的例外。）
3. **草稿区只进不出**：不确定的先挪进 `草稿/`，确认没用了再删（有 `.git`，挪动留痕，比直接删安全）。
4. **阶段目录里只放四件套**：`你的实现` + `test_xxx.py` + `说明_为什么.md` + `结构总览.md`。实验脚本、方法速查、临时笔记一律放根目录的 `速查/`。
   （L4/L5 阶段开头会先放一份 `需求与部件清单.md` 当"起手包"，写完代码后补四件套。）

## 怎么跑（PyCharm）

1. 解释器：`Settings → Project: PythonProject → Python Interpreter` → `.venv\Scripts\python.exe`
2. 跑某阶段测试：右键该阶段的 `test_xxx.py` → `Run 'Unittests in test_xxx'`
3. 看自测输出：右键实现文件 → `Run 'xxx'`
4. 阶段 5：`notes.py` 还没写，先右键 `速查/实验_检索打分_分段.py` → Run

> ⚠️ **别点基类**：`阶段1` 的 `StoreTest`、`阶段2` 的 `Base`、`阶段4` 的 `TmpDirTest` 都只有 0 个测试，点了会显示"没有发现测试"。要跑就点具体子类，或者点整个文件。
> `阶段4/support.py` 是支撑文件（不是测试文件），单独点它没有意义。

## 三个环境坑（都踩过）

| 现象 | 原因 | 解法 |
|---|---|---|
| `UnicodeEncodeError: 'gbk' codec can't encode` | cmd/PowerShell 默认 GBK，编不了 `✓` | PyCharm 的 Run 窗口是 UTF-8，直接用；命令行加 `$env:PYTHONIOENCODING='utf-8'` |
| `ModuleNotFoundError: No module named 'llm_config'` | 中文目录名不能当 Python 包 import | 在调用方加 `sys.path.insert(0, str(Path(__file__).parent))` |
| PyCharm 右键 Run 时 `ModuleNotFoundError: No module named 'support'` | unittest 运行器是**按文件路径** import 测试文件，测试目录不会自动进 `sys.path` | 测试文件开头先 `sys.path.insert(0, str(Path(__file__).parent))`，再 import 本目录模块（阶段 4 踩过） |

## 参考代码映射（studymate → 本仓库）

| 阶段 | studymate 里的文件 | 本仓库 | 状态 |
|---|---|---|---|
| 1 | `studymate/tasks.py`（159 行） | `阶段1/task.py` | ✅ |
| 2 | `studymate/config.py` + `llm.py`（189 行） | `阶段2/llm_config.py`（合并成一个文件） | ✅ |
| 3 | `studymate/tools.py` + `study_tools.py` + `agent.py` | `阶段3/tools.py` + `agent.py`（9 个工具砍到 2 个） | ✅ |
| 4 | `tests/test_studymate.py` | `阶段4/support.py` + `test_tools.py` + `test_agent_log.py`（自己写 6 条） | 🚧 判卷待补 |
| 5 | `studymate/notes.py` + `notes/` | `阶段5/notes.py`（待写）+ `阶段5/notes/`（样例已备） | 🚧 |
| 6 | `studymate/mcp_server.py` | `阶段6/`（待建） | ⬜ |

## 学习法相关文件（给 AI 看的）

- 开工前读：`AGENTS.md` → `交接文档.md` §0/§3/§4 → `学习方法.md` → 本文件
- 等级账本：`学习记录.md`（每次开工把最近一行贴给 AI，由它决定给多少骨架）
- 可移植学习法：`learning-skill/`（`SKILL.md` + `精简提示词.md` + zip）
