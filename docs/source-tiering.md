# Source Tiering

## Tier 1: Factual Anchors

**Use for**: `[已确认事实 / Confirmed Facts]` section only

**Typical Sources**:
- Official government, regulator, military, ministry statements
- Top-tier wire services (Reuters, AP, Bloomberg) confirming concrete facts
- Public company filings and exchange notices
- ETF issuer pages and holdings disclosures
- Official route/port authority notices
- Official institution data and documented metrics

**Important Distinctions**:
- Official **rhetoric** ≠ confirmed market impact
- **Threats** and **adjectives** are statements, not facts
- Tier 1 anchors **concrete facts only**, not interpretations or forecasts

**Source Tags**:
- `[官方]` - Official government/military statements
- `[通讯社]` - Wire services and primary reporting
- `[公司文件]` - Company filings and disclosures
- `[交易所/ETF发行方]` - Exchange notices, ETF holdings
- `[官方机构/航运通告]` - Port authorities, shipping notices

---

## Tier 2: Structural Analysis

**Use for**: `[市场解读 / Market Interpretation]` section

**Typical Sources**:
- Domain specialists with track record
- Reputable industry analysts
- Expert threads with verifiable claims
- Structural explainers identifying:
  - Infrastructure dependencies
  - Bottlenecks and choke points
  - Alternative routes and backup options
  - Transmission paths

**Quality Markers**:
- Provides verifiable variables
- Offers explicit boundaries
- Cites sources
- Separates fact from interpretation

---

## Low-Trust / Emotional Amplifiers

**Downrank or ignore**:
- Extreme rhetoric without boundary conditions
- Absolute claims without evidence
- Commentary confused with reporting
- Viral tone, certainty theater, unverified extrapolation

**Exception**:
Strong tone alone doesn't disqualify if source still provides:
- Verifiable variables
- Explicit boundaries
- Source support
- Clear fact/interpretation separation

---

## Handling Problematic Sources

### User-Provided Links
If the user's link is:
- **Emotional** or **low-trust**
- **Broken** or **thin**
- **Incomplete**

**Action**:
1. Explicitly state the source quality issue
2. Re-anchor analysis on independently verified public facts
3. Preserve the same output structure
4. Do not mirror the source's tone

### Fog of War Situations
When credible sources conflict on material facts:
- State explicitly: `**仍存在争议**`
- List conflicting claims briefly
- Note what to watch for resolution
- Do not collapse into false certainty

---

## Data Fallback Protocol

When key financial/logistics data is:
- Paywalled
- Delayed
- Unavailable
- Disputed

**Explicitly state**: `数据滞后/缺失`

**Acceptable Public Proxies**:
- Related shipping/tanker equities relative performance
- Sector ETF relative strength
- Official route closure/reopening announcements
- ETF issuer-reported holdings
- Company filings or management commentary
- Major benchmark commodity moves
