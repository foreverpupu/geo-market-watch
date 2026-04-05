"""
Fixture-based tests for RSS intake category detection.

Tests real-world scenarios:
- Real RSS samples from 财联社
- Multi-keyword conflict resolution
- Unknown category handling
"""

import pytest
from geo_market_watch.intake.adapter import RSSIntakeAdapter, RawEvent
from datetime import datetime


class TestRealRSSSamples:
    """Tests with real-world RSS sample data."""
    
    def test_shipping_conflict_priority(self):
        """Shipping + conflict keywords - conflict should win due to priority."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_001",
            title="红海航运遭袭：也门胡塞武装袭击两艘油轮",
            content="也门胡塞武装在红海袭击了两艘油轮，导致航运中断",
            published_at=datetime.now(),
            source_url="http://example.com/1",
        )
        
        result = adapter.normalize(raw)
        
        assert result.category == "conflict"  # Higher priority than shipping
        assert result.region == "Middle East"
        
        # Check explainability
        cat_detection = result.raw_features.get("category_detection", {})
        assert cat_detection["total_matches"] >= 2  # Both conflict and shipping
        assert "conflict" in cat_detection["candidate_categories"]
        assert "shipping" in cat_detection["candidate_categories"]
        assert cat_detection["selected"] == "conflict"
    
    def test_us_chip_export_restriction(self):
        """US chip export restriction - should detect tech category."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_002",
            title="美国升级对华芯片出口管制：英伟达高端GPU断供",
            content="美国商务部宣布新的出口管制措施，限制英伟达向中国出口高端AI芯片",
            published_at=datetime.now(),
            source_url="http://example.com/2",
        )
        
        result = adapter.normalize(raw)
        
        # Should detect export_restriction or chip_launch
        assert result.category in ["export_restriction", "chip_launch"]
        assert result.region == "US"
        
        cat_detection = result.raw_features.get("category_detection", {})
        assert cat_detection["total_matches"] >= 1
    
    def test_china_market_earnings(self):
        """Chinese market earnings - should detect market category."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_003",
            title="A股收盘：沪指涨0.5% 科技股领涨",
            content="今日A股三大指数集体收涨，半导体板块表现强势",
            published_at=datetime.now(),
            source_url="http://example.com/3",
        )
        
        result = adapter.normalize(raw)
        
        # Should detect market_movement or chip_launch
        assert result.category in ["market_movement", "chip_launch"]
        assert result.region == "China"


class TestUnknownCategoryHandling:
    """Tests for unknown/unmatched category handling."""
    
    def test_unknown_when_no_keywords_match(self):
        """When no keywords match, category should be unknown."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_unknown_001",
            title="某公司发布新产品",
            content="这是一篇普通的企业新闻，没有特定关键词",
            published_at=datetime.now(),
            source_url="http://example.com/unknown",
        )
        
        result = adapter.normalize(raw)
        
        assert result.category == "unknown"
        
        # Check metadata shows no matches
        cat_detection = result.raw_features.get("category_detection", {})
        assert cat_detection["total_matches"] == 0
        assert cat_detection["candidate_categories"] == []
    
    def test_unknown_category_still_has_region(self):
        """Unknown category should still attempt region detection."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_unknown_002",
            title="德国某小镇举办节日庆典",
            content="没有财经关键词的新闻",
            published_at=datetime.now(),
            source_url="http://example.com/germany",
        )
        
        result = adapter.normalize(raw)
        
        assert result.category == "unknown"
        assert result.region == "Europe"  # Should still detect region


class TestCategoryPriority:
    """Tests for category priority-based selection."""
    
    def test_conflict_priority_over_market(self):
        """Conflict (priority 100) should win over market_movement (priority 30)."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_priority_001",
            title="战争爆发导致股市暴跌",
            content="中东冲突升级，全球股市应声下跌",
            published_at=datetime.now(),
            source_url="http://example.com/priority",
        )
        
        result = adapter.normalize(raw)
        
        assert result.category == "conflict"
        
        cat_detection = result.raw_features.get("category_detection", {})
        assert "conflict" in cat_detection["candidate_categories"]
        assert "market_movement" in cat_detection["candidate_categories"]
        assert cat_detection["priority"] == 100  # conflict priority
    
    def test_sanctions_priority_over_macro(self):
        """Sanctions (priority 95) should win over macro (priority 35)."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_priority_002",
            title="美国制裁引发通胀担忧",
            content="新的制裁措施可能导致通胀上升",
            published_at=datetime.now(),
            source_url="http://example.com/sanctions",
        )
        
        result = adapter.normalize(raw)
        
        assert result.category == "sanctions"


class TestRegionDetection:
    """Tests for region detection with explainability."""
    
    def test_china_detection(self):
        """Should detect China from various keywords."""
        adapter = RSSIntakeAdapter()
        
        test_cases = [
            ("中国股市今日大涨", "China"),
            ("香港恒生指数下跌", "China"),
            ("北京发布新政策", "China"),
        ]
        
        for title, expected_region in test_cases:
            raw = RawEvent(
                event_id=f"test_region_{title[:10]}",
                title=title,
                content="test content",
                published_at=datetime.now(),
                source_url="http://example.com",
            )
            
            result = adapter.normalize(raw)
            assert result.region == expected_region, f"Failed for: {title}"
            
            # Check explainability
            region_detection = result.raw_features.get("region_detection", {})
            assert region_detection["selected"] == expected_region
    
    def test_global_fallback(self):
        """Should fallback to Global when no region keywords match."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_region_global",
            title="国际原油价格走势分析",
            content="test content",
            published_at=datetime.now(),
            source_url="http://example.com",
        )
        
        result = adapter.normalize(raw)
        
        assert result.region == "Global"
        
        region_detection = result.raw_features.get("region_detection", {})
        assert region_detection["selection_rule"] == "fallback"


class TestMultiHitScenarios:
    """Tests for multi-keyword hit scenarios."""
    
    def test_multiple_conflicting_keywords(self):
        """Multiple categories matched - priority should resolve."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_multihit_001",
            title="美联储制裁伊朗导致石油供应中断股市下跌",
            content="多重因素叠加的新闻",
            published_at=datetime.now(),
            source_url="http://example.com",
        )
        
        result = adapter.normalize(raw)
        
        # Should have multiple matches
        cat_detection = result.raw_features.get("category_detection", {})
        assert cat_detection["total_matches"] >= 3  # sanctions, energy, market_movement
        
        # Highest priority should win
        assert result.category in ["sanctions", "energy"]  # Both high priority
    
    def test_explainability_preserves_all_candidates(self):
        """Explainability should preserve all candidate categories, not just winner."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test_explain_001",
            title="芯片制裁引发AI监管担忧",
            content="多重技术政策新闻",
            published_at=datetime.now(),
            source_url="http://example.com",
        )
        
        result = adapter.normalize(raw)
        
        cat_detection = result.raw_features.get("category_detection", {})
        
        # Should have match details for all candidates
        assert "match_details" in cat_detection
        for cat in cat_detection["candidate_categories"]:
            assert cat in cat_detection["match_details"]
            assert "keywords" in cat_detection["match_details"][cat]
            assert "priority" in cat_detection["match_details"][cat]
