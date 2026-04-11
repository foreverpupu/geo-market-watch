# Geo Market Watch 搜索源策略文档

## 当前正式状态（V2 定版）

| 搜索源 | 状态 | 说明 |
|--------|------|------|
| **Tavily** | ✅ **主源** | D1 链路完整，Scout 消费验证通过 |
| **Brave** | ✅ **备源** | D1 链路完整，Scout 消费验证通过 |
| **Serper** | ❌ **冻结** | API 403 未授权，本轮阻塞，暂不接入 |

**阶段性质**: 恢复版（Tavily D1 恢复链路），非最终正式工具接入版。

---

## 统一路径

- Tavily 输出: `/root/.openclaw/workspace/skills/geo-market-watch/data/tavily_intake/`
- Brave 输出: `/root/.openclaw/workspace/skills/geo-market-watch/data/brave_intake/`
- 日志备份: `/root/.openclaw/workspace/skills/geo-market-watch/logs/`
- 统一执行入口: `/root/.openclaw/workspace/d1_active_gmw.sh`

---

## 备源切换触发条件

满足任一即触发从 Tavily 切至 Brave：

| 场景 | 判断标准 |
|------|----------|
| Tavily 服务异常 | 连续 3 次搜索返回空/超时/非 200 |
| Tavily API Key 失效 | 返回 401/403 认证错误 |
| Tavily 结果质量骤降 | 连续 2 次搜索中，前 5 条结果里与四条主线直接相关的结果少于 2 条 |

---

## 切换执行命令

```bash
# 1. 验证 Brave 可用性（可直接执行）
curl -s "https://api.search.brave.com/res/v1/web/search?q=test&count=1" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
  -H "Accept: application/json" | jq -e '.web.results[0]' >/dev/null \
  && echo "Brave 可用"

# 2. 执行切换：修改 D1 脚本软链接
ln -sf /root/.openclaw/workspace/d1_brave_gmw.sh \
       /root/.openclaw/workspace/d1_active_gmw.sh

# 3. 验证切换成功
/root/.openclaw/workspace/d1_active_gmw.sh "测试关键词"
```

---

## 切换证据留存

```bash
# 记录切换事件
mkdir -p /root/.openclaw/workspace/skills/geo-market-watch/logs/
echo "[$(date -Iseconds)] 主源从 Tavily 切换至 Brave" \
  >> /root/.openclaw/workspace/skills/geo-market-watch/logs/source_switch.log

# 保存切换前后的样本输出（保留最近3份）
BACKUP_DIR="/root/.openclaw/workspace/skills/geo-market-watch/data/tavily_intake_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp /root/.openclaw/workspace/skills/geo-market-watch/data/tavily_intake/*.{json,txt} "$BACKUP_DIR/" 2>/dev/null || true
ls -1 "$BACKUP_DIR" | wc -l | xargs -I {} echo "备份文件数: {}"
```

---

## 人工切回主源规则（非自动）

```bash
# 1. 人工执行 Tavily 探测（连续 2 次）
for i in 1 2; do
  echo "探测 $i..."
  /root/.openclaw/workspace/d1_tavily_gmw.sh "测试" && echo "✓ 成功" || echo "✗ 失败"
  sleep 5
done

# 2. 连续 2 次成功后，手动切回主源
echo "[$(date -Iseconds)] 人工确认：Tavily 探测通过，切回主源" \
  >> /root/.openclaw/workspace/skills/geo-market-watch/logs/source_switch.log

ln -sf /root/.openclaw/workspace/d1_tavily_gmw.sh \
       /root/.openclaw/workspace/d1_active_gmw.sh

echo "✅ 已切回 Tavily 主源"
```

---

## 文档版本信息

- 版本: V2 定版
- 更新时间: 2026-03-27
- 状态: 恢复阶段收口完成
