# README 重构变更说明

## 目标
将 README 从"设计文档首页"转为"产品着陆页"，让首次访问者能在 3 分钟内理解项目。

## 变更摘要

### 1. 新增结构（前 200 行内）

**Before:**
- 直接开始系统架构说明
- 大量技术细节 upfront
- 没有明确的用户定位

**After:**
- **What It Does** — 一句话 + 流程图说明核心价值
- **Who This Is For** — 明确目标用户和非目标用户
- **What This Repo Is / Is Not** — 清晰的边界说明表格
- **Quick Start** — 10 分钟上手指南
- **Example Input → Output** — 具体输入输出示例
- **Repository Status** — 当前版本状态表格
- **Documentation Map** — 文档导航

### 2. 信息下沉

将以下详细内容移至二级文档，通过链接引用：
- 完整的四层架构细节 → `docs/institutional-system-architecture.md`
- 数据库设计 → `docs/geo-alpha-database-spec.md`
- Analyst workflow 详情 → `docs/analyst-workflow.md`
- Roadmap 时间线 → `docs/system-evolution-architecture.md`

### 3. 边界说明

新增明确的边界声明：
> "Current limitations: No built-in scheduler, live data feeds, or hosted API. Bring your own data sources."

以及对比表格中的清晰定位：
- ✅ Research framework with runnable local pipeline
- ❌ Hosted production service
- ❌ Live trading execution engine

### 4. 新增示例文件

- `examples/minimal_event.json` — 最简单的输入示例
- `examples/minimal_output/analysis.md` — 对应的输出示例
- `docs/quickstart.md` — 10 分钟快速入门指南

## 改进效果

**Before:**
- 首次访问者需要阅读大量架构内容才能理解项目
- 不清楚自己是否适合使用
- 不知道如何快速尝试

**After:**
- 前 50 行明确回答"这是什么"
- 前 100 行明确回答"适合谁"
- 前 150 行提供"10 分钟上手指南"
- 清晰的输入→输出示例
- 详细的文档导航

## 保留的内容

所有原有重要信息保留，只是位置调整：
- 系统架构 → 移至第 100 行后，并链接到详细文档
- Quickstart 章节 → 保留但优化
- 项目结构 → 保留但简化
- 所有文档链接 → 保留并整合到 Documentation Map

## 验证清单

- [x] 首页前 200 行无过度技术细节
- [x] 明确写出"不是 hosted production service"
- [x] 边界说明包含 scheduler、ingestion backend、hosted API
- [x] 保留专业感但避免信息过载
- [x] 原有重要信息未删除，仅下沉
- [x] 新增 Documentation Map 区块
- [x] 新增最小示例文件
