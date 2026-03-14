# 🤖 定时监控与自动化指南 (Scheduled Monitoring)

> **⚠️ 核心说明 (Disclaimer)**
> 本仓库的核心交付物是一个"分析框架（Skill / Prompt）"，**本仓库代码本身不包含后台挂机或定时调度功能**。
> 以下指南展示的是一种**推荐的每日监控工作流（Recommended daily monitoring pattern）**。教你如何将本 Skill 与主流的定时任务系统（如 ChatGPT Tasks, OpenClaw Cron, Make.com 或 Coze 等）结合，打造一个全自动的地缘雷达。

---

## v5.5 Minimal Agent Loop

Starting in v5.5, Geo Market Watch includes a **minimal runnable local agent loop**:

- **News intake** — Load and normalize event items
- **Event dedupe** — Filter duplicate events
- **Score + trigger** — Compute signal scores and escalation decisions
- **Notify / handoff** — Generate notifications or handoff to full analysis

This enables **local end-to-end execution** of the monitoring workflow:

```bash
python scripts/run_agent_loop.py \
  --input data/intake-sample.json \
  --memory data/dedupe-memory.json \
  --output outputs/
```

However, the repository **still does not include** a built-in persistent background scheduler or hosted automation service.

The agent loop is:
- ✅ Runnable on demand
- ✅ Deterministic and reproducible
- ✅ Zero external dependencies
- ❌ Not a persistent daemon
- ❌ Not a hosted service

To run this on a schedule, you must integrate with an external scheduler (cron, OpenClaw, etc.).

---

## 💡 设计思路：双模式架构 (Dual Mode)

---

## 💡 设计思路：双模式架构 (Dual Mode)

大语言模型（LLM）执行复杂投研框架时，极易面临 API 超时、死循环和信息轰炸（Alert Fatigue）的问题。因此，在自动化部署时，我们强烈建议采用**"双模式拦截"**：

1. **侦察模式 (Discovery Mode)**：挂载在定时任务上（如每日早 8:00 执行）。配有极严苛的"搜索次数限制"和"主线过滤网"，只做初筛，**绝不直接生成长报告**。若无大事，仅输出监控名单。
2. **分析模式 (Analysis Mode)**：仅当侦察模式报告"发现高价值事件"并建议升级时，再由人工（或 Webhook）将新闻链接喂入主控的 `SKILL.md`，输出完整的 9 段式三地市场观察池。

---

## 📡 推荐的定时任务 Prompt (Scout Prompt)

请在你的定时任务系统（Scheduled Tasks）中，将触发周期设定为你需要的时间（如每日早晨），并将以下内容作为任务的**执行指令（Prompt）**：

```text
Task: 扫描过去 24 小时的全球地缘市场事件。

【硬性执行限制（防超时机制）】
1. 搜索限制：最多只能调用 3 次 web_search 工具。一旦获得足够信息，立刻停止搜索，不做补充研究。
2. 来源限制：仅需搜索 Reuters, Bloomberg 或主流权威财经信源，拒绝搜索自媒体平台。
3. 领域限制：不要搜索泛政治新闻。仅关注与以下四条主线发生"物理碰撞"的事件：
 - 【1. 能源断供 / 油气设施受损】
 - 【2. 航运受阻 / 海峡危机】
 - 【3. 金属矿产制裁 / 出口禁令】
 - 【4. 东亚核心供应链冲击】

【筛选与输出规则】
搜索结束后，立刻执行以下步骤：
1. 快速去重：合并同一事件的多条报道。
2. 快速评估每个事件的：物理传导强度 和 市场可映射性。
3. 输出规则：
 - 若无足够强的新事件：输出"当前没有足够强的新事件值得完整刷新观察池"，并列出 3 个继续监控的暗流及验证点。
 - 若有足够强的新事件：只输出 1 个主事件摘要，包含：a) 主事件中文名（English name）；b) 升级理由（1-2句）；c) 需继续验证的关键点；d) 是否建议进入完整 geo-market-watch 分析：是 / 否。
4. 警告：不要在本任务中直接生成完整的 geo-market-watch 九段长报告！总输出尽量控制在简洁范围内。
```

---

## 🛠️ 主流平台配置示例

### 1. OpenClaw Cron (推荐)

```bash
openclaw cron add \
  --name "Geo Market Watch Scout" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --light-context \
  --timeout 300000 \
  --message "[上方 Scout Prompt 内容]" \
  --announce \
  --channel qqbot \
  --to "qqbot:c2c:YOUR_QQ_ID"
```

### 2. ChatGPT Tasks

在 ChatGPT 中：
1. 创建新 Task
2. 设置触发时间：每日 8:00 AM
3. 粘贴 Scout Prompt 作为指令
4. 配置输出目的地（如邮件、Slack）

### 3. Make.com (Integromat)

1. 创建 Scenario
2. 添加 **HTTP** 模块调用 LLM API
3. 添加 **Router** 判断输出内容
4. 若检测到"建议升级"，触发 **Webhook** 或发送通知

### 4. Coze (扣子)

1. 创建 Bot
2. 在**触发器**中设置定时任务
3. 粘贴 Scout Prompt 作为系统提示词
4. 配置输出到飞书/钉钉/微信

---

## 🔄 工作流示意图

```
┌─────────────────┐
│  定时任务触发    │  (每日 8:00)
└────────┬────────┘
         ▼
┌─────────────────┐
│  侦察模式执行    │  (Scout Prompt)
│  - 最多3次搜索   │
│  - 只筛不分析    │
└────────┬────────┘
         ▼
    ┌─────────┐
    │ 有大事? │
    └────┬────┘
   是 /    \ 否
      /      \
     ▼        ▼
┌─────────┐  ┌─────────────┐
│输出升级 │  │输出监控名单 │
│建议卡片 │  │(3个暗流)    │
└────┬────┘  └─────────────┘
     ▼
┌─────────────────┐
│ 人工/Webhook    │
│ 触发分析模式    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  完整 9 段报告   │  (Analysis Mode)
│  三地观察池      │
└─────────────────┘
```

---

## ⚠️ 关键注意事项

### 1. 超时保护
- 务必设置 timeout（建议 5 分钟）
- 严格限制搜索次数（最多 3 次）
- 使用 `--light-context` 减少上下文负担

### 2. 信息过滤
- 只关注"物理碰撞"事件
- 剔除外交表态、口水战
- 拒绝自媒体情绪化内容

### 3. 避免 Alert Fatigue
- 无大事时只输出监控名单
- 不要每天生成长报告
- 只在真正重要时升级

### 4. 多平台备份
- 重要推送配置多个渠道
- 设置失败重试机制
- 定期检查任务运行状态

---

## 📊 监控与调试

### 查看任务状态

```bash
# OpenClaw
openclaw cron list
openclaw cron runs --id <job-id> --limit 10

# 其他平台
# 在各自平台的 Dashboard 中查看
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 任务超时 | 搜索或分析耗时过长 | 检查搜索限制是否生效 |
| 无输出 | 过滤条件过于严格 | 适当放宽领域限制 |
| 输出过长 | 未限制生成长度 | 确认 prompt 中的字数限制 |
| 重复推送 | 同一事件多次触发 | 加强去重逻辑 |

---

## 📝 进阶配置

### 多时段监控

```bash
# 早盘前（8:00）- 主监控
openclaw cron add --name "GW Morning" --cron "0 8 * * *" ...

# 午盘前（12:30）- 补充检查
openclaw cron add --name "GW Noon" --cron "30 12 * * *" ...

# 收盘后（16:00）- 复盘
openclaw cron add --name "GW Evening" --cron "0 16 * * *" ...
```

### 周末模式

```bash
# 仅工作日运行
--cron "0 8 * * 1-5"
```

### 条件触发

在 Scout Prompt 中添加：
```text
【升级阈值】
只有当事件同时满足以下条件时才建议升级：
- 物理传导强度 >= 8/10
- 市场可映射性 >= 7/10
- 时效性 >= 6/10
```

---

## 🔗 相关文档

- [SKILL.md](../SKILL.md) - 核心技能定义（分析模式）
- [docs/methodology.md](methodology.md) - 完整方法论
- [docs/Automation_Guide.md](Automation_Guide.md) - OpenClaw 自动化配置参考
- [examples/example-inputs.md](../examples/example-inputs.md) - 测试用例

---

**免责声明**：本指南仅供学习和研究使用，不构成投资建议。市场有风险，投资需谨慎。
