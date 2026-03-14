# Example Inputs

## Example 1: Shipping Disruption

**User Prompt**:
> Analyze these news links about the Red Sea shipping crisis:
> - https://www.reuters.com/world/middle-east/...
> - https://www.bloomberg.com/news/articles/...
> 
> Generate a Chinese market watchlist across US stocks, A-shares, and Hong Kong stocks.

**Expected Handling**:
- Extract confirmed facts about route closures, vessel diversions, insurance costs
- Identify Tier 1 vs Tier 2 sources
- Map transmission: shipping costs → container rates → inflation → consumer goods
- Build watchlists around: tankers, container lines, insurers, energy exporters

---

## Example 2: Energy Infrastructure Strike

**User Prompt**:
> What is the market impact of the recent drone attacks on Saudi oil facilities?
> Links: [provided]

**Expected Handling**:
- Verify damage claims through Tier 1 sources
- Distinguish confirmed damage from initial reports
- Map: supply disruption → oil price → inflation → sector impacts
- Watchlists: oil producers, refiners, alternatives, transports

---

## Example 3: Export Controls

**User Prompt**:
> Analyze the new US export controls on advanced semiconductors to China.

**Expected Handling**:
- Confirm specific products, companies, and effective dates
- Map: equipment makers → chip designers → downstream users
- Consider retaliation scenarios
- Watchlists: equipment, materials, design tools, alternatives

---

## Example 4: Incomplete Information (Fog of War)

**User Prompt**:
> There's breaking news about a military strike in the Gulf. What should I watch?

**Expected Handling**:
- Flag that full-workflow confidence is reduced without links
- If proceeding, explicitly mark contested facts
- Use Fog of War Rule for disputed damage reports
- Provide conditional watchlists based on scenarios

---

## Example 5: Low-Trust Source Provided

**User Prompt**:
> This blog says WW3 is starting and oil will hit $200. Analyze: [link to sensationalist blog]

**Expected Handling**:
- Explicitly state source quality issue
- Re-anchor on independently verified facts
- Do not mirror the blog's tone or certainty
- Provide balanced, bounded analysis
