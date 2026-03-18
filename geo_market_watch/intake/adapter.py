"""
Minimal Intake Adapter for geo_market_watch.

Connects real RSS feeds to the canonical signal chain.
Purpose: Validate that the system can process real-world inputs.

Scope:
- Single RSS source (财联社电报)
- Simple category detection from title/content
- One-shot processing (no continuous scheduler)
- Minimal output (print/return, no persistence)

Non-scope:
- Multiple sources
- Complex NLP
- Scheduler/cron
- Database persistence
- Error recovery
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
import urllib.request
import urllib.error


@dataclass
class RawEvent:
    """Minimal event structure from RSS feed."""
    event_id: str  # RSS entry ID
    title: str
    content: str
    published_at: datetime
    source_url: str
    source_name: str = "cls_telegraph"


@dataclass  
class NormalizedEvent:
    """Event normalized for canonical chain processing."""
    event_id: str
    title: str
    content: str
    category: str  # Mapped to pack category
    region: str    # Extracted or default
    published_at: datetime
    source_url: str
    source_name: str
    raw_features: Dict[str, Any]  # For scoring


class RSSIntakeAdapter:
    """
    Minimal RSS intake adapter.
    
    Fetches RSS feed, parses entries, normalizes to canonical event format.
    """
    
    # 财联社电报 RSS (via pyrsshub)
    DEFAULT_FEED_URL = "https://pyrsshub.vercel.app/cls/telegraph/"
    
    # Simple keyword-based category detection
    # Maps keywords to canonical categories
    CATEGORY_KEYWORDS = {
        # Geo categories (higher priority for hard news)
        "conflict": ["冲突", "战争", "袭击", "导弹", "军事", "爆炸", "打击", "空袭", "轰炸", "交火"],
        "sanctions": ["制裁", "禁运", "关税", "贸易", "贸易战", "反制", "限制措施"],
        "shipping": ["航运", "海运", "港口", "运河", "海峡", "航道", "船只", "油轮", "集装箱"],
        "energy": ["石油", "原油", "天然气", "能源", "OPEC", "油价", "供应中断", "停产"],
        "election": ["选举", "投票", "大选", "公投", "换届"],
        # Tech categories  
        "chip_launch": ["芯片", "半导体", "晶圆", "台积电", "NVDA", "英伟达", "光刻机", "制程"],
        "ai_model_release": ["AI", "人工智能", "大模型", "GPT", "生成式", "OpenAI", "ChatGPT"],
        "export_restriction": ["出口管制", "技术封锁", "禁售", "断供", "实体清单"],
        # Crypto categories
        "regulatory": ["监管", "SEC", "合规", "牌照", "央行", "数字货币", "比特币", "加密货币"],
        "exchange_hack": ["黑客", "盗币", "交易所", "安全漏洞", "跑路", "暴雷"],
        # Market categories (fallback)
        "market_movement": ["股市", "大盘", "指数", "涨跌", "暴跌", "暴涨", "熔断", "牛市", "熊市"],
        "earnings": ["财报", "业绩", "营收", "利润", "亏损", "预增", "预减", "分红"],
        "macro": ["央行", "加息", "降息", "通胀", "CPI", "PPI", "GDP", "美联储", "货币政策"],
    }
    
    # Category priority for disambiguation (higher = preferred when multi-hit)
    CATEGORY_PRIORITY = {
        "conflict": 100,      # Hard news highest priority
        "sanctions": 95,
        "shipping": 90,
        "energy": 85,
        "election": 80,
        "chip_launch": 75,
        "export_restriction": 70,
        "ai_model_release": 65,
        "regulatory": 60,
        "exchange_hack": 60,
        "earnings": 40,       # Market news lower priority
        "macro": 35,
        "market_movement": 30,
    }
    
    def __init__(self, feed_url: Optional[str] = None):
        self.feed_url = feed_url or self.DEFAULT_FEED_URL
    
    def fetch_feed(self, limit: int = 10) -> List[RawEvent]:
        """
        Fetch and parse RSS feed.
        
        Args:
            limit: Maximum number of entries to fetch
            
        Returns:
            List of RawEvent objects
        """
        try:
            with urllib.request.urlopen(self.feed_url, timeout=10) as response:
                xml_data = response.read()
        except urllib.error.HTTPError as e:
            print(f"RSS fetch HTTP error {e.code}: {e.reason}")
            return []
        except urllib.error.URLError as e:
            reason = e.reason
            if isinstance(reason, OSError):
                print(f"RSS fetch network error: {reason}")
            else:
                print(f"RSS fetch URL error: {reason}")
            return []
        except TimeoutError:
            print("RSS fetch timeout")
            return []
        except Exception as e:
            print(f"RSS fetch unexpected error: {type(e).__name__}: {e}")
            return []
        
        # Validate response content
        if not xml_data:
            print("RSS fetch returned empty content")
            return []
        
        if len(xml_data) < 100:
            print(f"RSS fetch returned suspiciously small content ({len(xml_data)} bytes)")
            return []
        
        return self._parse_xml(xml_data, limit)
    
    def _parse_xml(self, xml_data: bytes, limit: int) -> List[RawEvent]:
        """Parse Atom/RSS XML to RawEvent objects."""
        events = []
        
        # Handle empty or whitespace-only content
        if not xml_data or not xml_data.strip():
            print("XML parse: empty content")
            return []
        
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            print(f"XML parse error: {e}")
            return []
        except UnicodeDecodeError as e:
            print(f"XML decode error: {e}")
            return []
        
        # Handle Atom format (财联社 uses Atom)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns) or root.findall('entry')
        
        for entry in entries[:limit]:
            # Extract fields (avoid 'or' due to Element __bool__ behavior in Python 3.12+)
            id_elem = entry.find('atom:id', ns)
            if id_elem is None:
                id_elem = entry.find('id')
            
            title_elem = entry.find('atom:title', ns)
            if title_elem is None:
                title_elem = entry.find('title')
            
            content_elem = entry.find('atom:content', ns)
            if content_elem is None:
                content_elem = entry.find('content')
            
            published_elem = entry.find('atom:published', ns)
            if published_elem is None:
                published_elem = entry.find('published')
            
            link_elem = entry.find('atom:link', ns)
            if link_elem is None:
                link_elem = entry.find('link')
            
            event_id = id_elem.text if id_elem is not None else ""
            title = title_elem.text if title_elem is not None and title_elem.text else ""
            content = content_elem.text if content_elem is not None and content_elem.text else ""
            
            # Parse published time
            published_at = datetime.now()
            if published_elem is not None and published_elem.text:
                try:
                    # Atom format: 2026-03-18T16:36:57+00:00
                    published_at = datetime.fromisoformat(published_elem.text.replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            # Get link
            source_url = ""
            if link_elem is not None:
                source_url = link_elem.get('href', '')
            
            event = RawEvent(
                event_id=event_id,
                title=title,
                content=content,
                published_at=published_at,
                source_url=source_url,
                source_name="cls_telegraph"
            )
            events.append(event)
        
        return events
    
    def normalize(self, raw_event: RawEvent) -> Optional[NormalizedEvent]:
        """
        Normalize RawEvent to canonical format.
        
        Detects category from title/content keywords.
        Returns None if cannot determine category.
        """
        # Detect category with explainability
        category, category_metadata = self._detect_category(raw_event.title + " " + raw_event.content)
        
        if category is None:
            # Cannot categorize - use unknown but preserve metadata
            category = "unknown"
        
        # Extract region (simple heuristic)
        region, region_metadata = self._detect_region_with_explain(raw_event.title + " " + raw_event.content)
        
        # Build raw features for scoring
        # These would be filled by more sophisticated NLP in production
        raw_features = {
            "title_length": len(raw_event.title),
            "content_length": len(raw_event.content),
            "has_numbers": any(c.isdigit() for c in raw_event.title),
            "category_detection": category_metadata,
            "region_detection": region_metadata,
        }
        
        return NormalizedEvent(
            event_id=raw_event.event_id,
            title=raw_event.title,
            content=raw_event.content,
            category=category,
            region=region,
            published_at=raw_event.published_at,
            source_url=raw_event.source_url,
            source_name=raw_event.source_name,
            raw_features=raw_features
        )
    
    def _detect_category(self, text: str) -> tuple[Optional[str], dict]:
        """
        Detect category from keywords in text.
        
        Returns:
            tuple: (selected_category, detection_metadata)
            detection_metadata includes multi-hit info and candidate categories
        """
        text_lower = text.lower()
        
        # Track all matching categories with their matched keywords
        matches = {}  # category -> {"keywords": [], "priority": int}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            matched_keywords = []
            for keyword in keywords:
                if keyword in text or keyword in text_lower:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                priority = self.CATEGORY_PRIORITY.get(category, 0)
                matches[category] = {
                    "keywords": matched_keywords,
                    "priority": priority,
                }
        
        # Build detection metadata
        metadata = {
            "total_matches": len(matches),
            "candidate_categories": list(matches.keys()),
            "match_details": matches,
        }
        
        if not matches:
            return None, metadata
        
        # Select by priority (highest wins), tie-break by keyword count
        best_category = max(
            matches.keys(),
            key=lambda c: (matches[c]["priority"], len(matches[c]["keywords"]))
        )
        
        metadata["selected"] = best_category
        metadata["selection_rule"] = "priority_based"
        metadata["priority"] = matches[best_category]["priority"]
        
        return best_category, metadata
    
    def _detect_region(self, text: str) -> str:
        """Detect region from keywords (simple heuristic)."""
        region, _ = self._detect_region_with_explain(text)
        return region
    
    def _detect_region_with_explain(self, text: str) -> Tuple[str, dict]:
        """Detect region with explainability metadata."""
        text_lower = text.lower()
        
        # Region keywords with priority
        REGION_KEYWORDS = {
            "Middle East": ["中东", "伊朗", "沙特", "以色列", "霍尔木兹", "也门", "胡塞", "哈马斯", "黎巴嫩"],
            "US": ["美国", "美國", "US", "特朗普", "拜登", "华盛顿", "美联储", "美股", "纳斯达克", "道琼斯"],
            "China": ["中国", "中國", "北京", "上海", "深圳", "香港", "A股", "港股", "沪指", "深成指", "创业板"],
            "Europe": ["欧洲", "欧盟", "德国", "法国", "英国", "意大利", "欧股", "欧洲央行"],
            "Asia": ["日本", "韩国", "亚洲", "东京", "首尔", "日经", "韩国KOSPI"],
        }
        
        matches = {}
        for region, keywords in REGION_KEYWORDS.items():
            matched = [kw for kw in keywords if kw in text_lower]
            if matched:
                matches[region] = matched
        
        metadata = {
            "total_matches": len(matches),
            "candidate_regions": list(matches.keys()),
            "match_details": matches,
        }
        
        if not matches:
            metadata["selected"] = "Global"
            metadata["selection_rule"] = "fallback"
            return "Global", metadata
        
        # Simple priority: first match wins (could be enhanced)
        selected = list(matches.keys())[0]
        metadata["selected"] = selected
        metadata["selection_rule"] = "first_match"
        
        return selected, metadata
    
    def fetch_and_normalize(self, limit: int = 10) -> List[NormalizedEvent]:
        """
        Fetch RSS and normalize all events.
        
        Convenience method for one-shot processing.
        """
        raw_events = self.fetch_feed(limit)
        normalized = []
        
        for raw in raw_events:
            norm = self.normalize(raw)
            if norm:
                normalized.append(norm)
        
        return normalized


def demo_intake():
    """
    Demo: Fetch RSS and show normalized events.
    
    Run this to verify intake adapter works:
    python -m geo_market_watch.intake.adapter
    """
    adapter = RSSIntakeAdapter()
    
    print("Fetching RSS feed...")
    events = adapter.fetch_and_normalize(limit=5)
    
    print(f"\nFetched {len(events)} events:\n")
    
    for i, event in enumerate(events, 1):
        print(f"--- Event {i} ---")
        print(f"Title: {event.title[:60]}...")
        print(f"Category: {event.category}")
        print(f"Region: {event.region}")
        print(f"Published: {event.published_at}")
        print()


if __name__ == "__main__":
    demo_intake()