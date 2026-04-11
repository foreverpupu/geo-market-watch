# data 目录边界说明
## 跟踪保留内容（纳入git版本控制）
- 测试资产：benchmark-events.json、db-seed-events.json、dedupe-memory.sample.json、intake-sample.json
- 示例资产：event-cards-2026-03-15.json、idea-performance-sample.json、trade-ideas-2026-03-15.json、watchlist-2026-03-15.json
- 核心数据：geo_alpha.db
## 运行时产物（不纳入版本控制，存放于runtime/子目录）
- 所有intake产生的临时数据、dedupe内存快照、corrupted文件
- runtime/目录已加入.gitignore，不会被提交
## 遗留文件
- 无，所有文件已按上述规则分类
