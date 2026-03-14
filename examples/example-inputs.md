# Example Inputs

This file provides example prompts and inputs for testing **Geo Market Watch**.

Use these examples to validate that the Skill produces correctly structured outputs.

---

## Example 1: Energy Infrastructure Strike

**Input:**
```
https://www.reuters.com/world/middle-east/us-conducts-strikes-iranian-military-targets-kharg-island-2026-03-14/

请分析这个事件对能源市场的影响，生成三地观察池。
```

**Expected behavior:**
- Identify Kharg Island as critical Iranian export node
- Apply Fog of War Rule (damage not yet confirmed)
- Map transmission path: event -> oil risk premium -> shipping/insurance -> sector ETFs
- Generate watchlist across US, A-share, and HK markets
- Include trigger signals and invalidation conditions

---

## Example 2: Shipping Route Disruption

**Input:**
```
https://www.bbc.com/news/world-middle-east-12345678
https://www.cnbc.com/2026/03/14/suez-canal-traffic-disrupted.html

苏伊士运河通行受阻，请生成市场观察框架。
```

**Expected behavior:**
- Assess route status and alternative paths
- Identify tanker and container shipping exposure
- Note data fallback needs (spot freight rates may be paywalled)
- Map beneficiaries: tanker operators, alternative route ports, insurance
- Include 数据滞后/缺失 annotation where appropriate

---

## Example 3: Sanctions / Export Controls

**Input:**
```
美国宣布对某国实施新的半导体出口管制
https://www.reuters.com/technology/us-new-semiconductor-export-controls-2026-03-14/

请分析对中美港三地科技股的影响。
```

**Expected behavior:**
- Identify policy scope and affected entities
- Map direct vs indirect beneficiaries
- Note asymmetry (impact likely stronger in US/China than HK)
- Include equipment makers, alternative suppliers, domestic substitution plays
- Label hedge vs beneficiary clearly

---

## Example 4: Contested Early Conflict Reporting

**Input:**
```
早期报道显示某港口设施受损，但不同信源说法不一
https://example.com/news1
https://example.com/news2

请基于现有信息生成观察框架。
```

**Expected behavior:**
- Explicitly state that damage extent remains contested
- Do not force certainty
- Summarize competing claims briefly
- State what evidence would resolve the dispute
- Keep scenario logic conditional

---

## Example 5: Narrow Thematic Event

**Input:**
```
某特定稀土加工设施发生事故，可能影响全球供应
https://www.example.com/rare-earth-incident

请生成观察池。
```

**Expected behavior:**
- Prefer node-specific proxies (processing exposure, not generic mining)
- Avoid padding weak names
- If clean list is smaller than 5, return fewer names with （未强行补足）note
- Focus on direct mapping over storytelling

---

## Example 6: Sensational Low-Trust Source

**Input:**
```
https://sensational-news-site.com/apocalyptic-supply-shock-coming

这个报道说全球供应链即将崩溃，请分析。
```

**Expected behavior:**
- Explicitly state that the source is emotional/low-trust
- Do not mirror its tone
- Re-anchor analysis on independently verified public facts
- Apply anti-hype filtering
- Downrank extreme rhetoric without boundaries

---

## Test Checklist

When testing with any of these examples, verify:

- [ ] Output includes all 9 required sections
- [ ] Confirmed Facts only uses Tier 1 sources
- [ ] Market Interpretation uses Tier 2 appropriately
- [ ] Fog of War Rule applied where facts are disputed
- [ ] 数据滞后/缺失标注在数据不可用时出现
- [ ] Each watchlist name has trigger signal and invalidation condition
- [ ] Risk Warning appears at the end
- [ ] （未强行补足）used when list is shorter than 5
- [ ] Hedge vs beneficiary clearly labeled
- [ ] Anti-hype filtering applied to emotional sources
