# 自动化运行指南 (Automation Guide)

本文档介绍如何将 Geo Market Watch 配置为自动运行的晨间地缘雷达。

---

## 🎯 目标

每天早上 8:00（北京时间），自动：
1. 扫描过去 24 小时全球地缘政治事件
2. 筛选出最值得关注的 1 个主事件
3. 生成精简版升级建议卡片
4. 推送到 QQ/微信/钉钉等渠道

---

## 📋 前置要求

- OpenClaw 已安装并配置好 Gateway
- 已安装 `geo-market-watch` 技能
- 已配置消息推送渠道（QQ/微信/钉钉等）

---

## 🚀 快速配置

### 1. 创建 Cron 任务

```bash
openclaw cron add \
  --name "Geo Market Watch Morning Scan" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --exact \
  --session isolated \
  --light-context \
  --timeout 300000 \
  --message "Task: 扫描过去 24 小时的全球地缘市场事件。

【硬性执行限制（防超时）】
1. 最多只能调用 3 次 web_search 工具。
2. 仅搜索 Reuters、Bloomberg 或其他主流权威财经信源；不要搜索自媒体、社交平台或泛资讯网站。
3. 不要搜索泛政治新闻。仅关注与以下四条主线发生物理碰撞的事件：
 - 能源断供 / 油气设施受损
 - 航运受阻 / 海峡危机
 - 金属矿产制裁 / 出口禁令
 - 东亚核心供应链冲击
4. 一旦获得足够信息，立即停止搜索，不做补充研究。
5. 不要展开长篇背景介绍，不要写成宏观时评。

【筛选与处理规则】
搜索结束后，立刻执行以下步骤：
1. 快速去重：合并同一事件的多条报道。
2. 快速筛选：剔除外交表态、政策喊话、口水战、无实质物理冲击的新闻。
3. 快速判断每个候选事件的两个核心维度：
 - 物理传导强度
 - 市场可映射性
4. 优先选择 1 个最值得关注的主事件；如无足够强主事件，则不要强行升级。

【输出规则】
A. 如果没有足够强的新事件：
输出：
当前没有足够强的新事件值得完整刷新观察池
然后仅列出 3 个继续监控的暗流，每个暗流只写：
- 事件名称
- 为什么要监控（1句）
- 下一步验证点（1句）

B. 如果存在足够强的新事件：
不要直接生成完整 geo-market-watch 九段长报告。
只输出一个升级建议卡片，包含：
1. 主事件名称
2. 升级理由（2句内）
3. 主要传导链条（1句）
4. 仍需验证的关键点（最多 2 条）
5. 是否建议进入完整 geo-market-watch 分析：是

【格式要求】
1. 全文保持简洁，优先短句。
2. 总输出尽量控制在 400-600 字内。
3. 中文输出时，关键实体首次出现必须使用双语格式：中文名（English name）
4. 同一实体后文可只使用中文简称。
5. 不要输出推理过程，不要解释你如何搜索，只输出最终结果。" \
  --announce \
  --channel qqbot \
  --to "qqbot:c2c:YOUR_QQ_ID_HERE"
```

### 2. 替换 YOUR_QQ_ID_HERE

将 `YOUR_QQ_ID_HERE` 替换为你的实际 QQ 用户 ID。

获取方式：
```bash
openclaw directory --channel qqbot
```

### 3. 验证任务

```bash
# 查看所有 cron 任务
openclaw cron list

# 手动触发测试（立即执行）
openclaw cron run <job-id> --expect-final --timeout 300000

# 查看运行历史
openclaw cron runs --id <job-id> --limit 10
```

---

## ⚙️ 配置详解

### 时间设置

| 参数 | 说明 | 示例 |
|------|------|------|
| `--cron "0 8 * * *"` | 每天早上 8:00 | 可改为 `0 9 * * *` 等 |
| `--tz "Asia/Shanghai"` | 北京时间 | 可根据需要调整 |

### 执行限制

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `--timeout 300000` | 5 分钟超时 | 防止任务无限运行 |
| `--session isolated` | 隔离会话 | 避免上下文污染 |
| `--light-context` | 轻量级上下文 | 减少 token 消耗 |

### 消息推送

支持多种渠道：

```bash
# QQ
--channel qqbot --to "qqbot:c2c:USER_ID"

# 微信（需配置 wechat-tool）
--channel wechat --to "wechat:USER_ID"

# 钉钉（需配置 ddingtalk）
--channel ddingtalk --to "ddingtalk:USER_ID"

# 多渠道同时推送
--channel qqbot --to "qqbot:c2c:USER1" \
--channel wechat --to "wechat:USER2"
```

---

## 🔧 高级配置

### 多时段扫描

创建多个 cron 任务覆盖不同时段：

```bash
# 早盘前（8:00）
openclaw cron add --name "GW Morning" --cron "0 8 * * *" ...

# 午盘前（12:30）
openclaw cron add --name "GW Noon" --cron "30 12 * * *" ...

# 收盘后（16:00）
openclaw cron add --name "GW Evening" --cron "0 16 * * *" ...
```

### 周末模式

只在工作日运行：

```bash
# 周一到周五早上 8:00
--cron "0 8 * * 1-5"
```

### 条件触发

只在特定条件下推送（需配合 webhook）：

```bash
# 仅当发现高优先级事件时推送
--message "...如果事件评分 >= 7 分，则推送；否则静默..."
```

---

## 📊 监控与调试

### 查看任务状态

```bash
openclaw cron list
```

输出示例：
```
ID                                   Name                     Schedule              Next    Last    Status
3b1eb0c3-cacc-4628-be03-8fb545895302 Geo Market Watch Morning Scan  cron 0 8 * * * @ Asia/Shanghai  in 8h   -       idle
```

### 查看运行历史

```bash
openclaw cron runs --id <job-id> --limit 5
```

输出示例：
```json
{
  "entries": [
    {
      "ts": 1773496279911,
      "jobId": "...",
      "action": "finished",
      "status": "ok",
      "runAtMs": 1773492679899,
      "durationMs": 120000,
      "deliveryStatus": "delivered"
    }
  ]
}
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 任务超时 | 搜索或分析耗时过长 | 已设置 5 分钟超时，简化 prompt |
| 无消息推送 | 渠道配置错误 | 检查 `--to` 参数 |
| 输出过长 | 未限制输出长度 | prompt 中明确要求 < 600 字 |
| token 消耗高 | 上下文累积 | 使用 `--light-context` |

---

## 🎛️ 自定义配置

### 修改搜索范围

编辑 prompt 中的搜索限制：

```
仅搜索 Reuters、Bloomberg...
↓ 改为 ↓
仅搜索 Reuters、Bloomberg、Financial Times...
```

### 调整关注领域

修改四条主线：

```
【1. 能源断供 / 油气设施受损】
【2. 航运受阻 / 海峡危机】
【3. 金属矿产制裁 / 出口禁令】
【4. 东亚核心供应链冲击】
↓ 添加 ↓
【5. 半导体 / 芯片出口管制】
```

### 调整输出长度

修改字数限制：

```
总输出尽量控制在 400-600 字内
↓ 改为 ↓
总输出尽量控制在 200-300 字内（极简版）
```

---

## 📝 最佳实践

1. **先手动测试** - 创建 cron 前，先用相同 prompt 手动测试几次
2. **设置超时** - 务必设置 `--timeout`，防止无限运行
3. **监控运行** - 定期检查 `openclaw cron runs` 确保任务正常
4. **简化优先** - 晨间扫描以"发现事件"为主，详细分析留到人工判断
5. **多渠道备份** - 重要推送配置多个渠道，防止单点故障

---

## 🔗 相关文档

- [SKILL.md](../SKILL.md) - 核心技能定义
- [docs/methodology.md](methodology.md) - 完整方法论
- [docs/validation-checklist.md](validation-checklist.md) - 验证清单
- [examples/example-inputs.md](../examples/example-inputs.md) - 测试用例

---

如有问题，欢迎提交 Issue 或 PR。
