"""
Tests for minimal intake adapter.

Validates RSS fetching, parsing, and normalization.
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from geo_market_watch.intake.adapter import (
    RSSIntakeAdapter,
    RawEvent,
    NormalizedEvent,
)


class TestRSSIntakeAdapter:
    """Test RSS intake adapter functionality."""
    
    def test_adapter_initialization(self):
        """Adapter can be initialized with default or custom URL."""
        # Default URL
        adapter1 = RSSIntakeAdapter()
        assert adapter1.feed_url == RSSIntakeAdapter.DEFAULT_FEED_URL
        
        # Custom URL
        adapter2 = RSSIntakeAdapter("https://example.com/feed")
        assert adapter2.feed_url == "https://example.com/feed"
    
    def test_detect_category_geo(self):
        """Category detection for geo events."""
        adapter = RSSIntakeAdapter()
        
        # Conflict keywords
        cat, meta = adapter._detect_category("中东冲突升级")
        assert cat == "conflict"
        assert meta["total_matches"] >= 1
        
        cat, _ = adapter._detect_category("导弹袭击")
        assert cat == "conflict"
        
        # Energy keywords
        cat, _ = adapter._detect_category("石油价格上涨")
        assert cat == "energy"
        
        cat, _ = adapter._detect_category("OPEC会议")
        assert cat == "energy"
        
        # Shipping keywords
        cat, _ = adapter._detect_category("红海航运中断")
        assert cat == "shipping"
    
    def test_detect_category_tech(self):
        """Category detection for tech events."""
        adapter = RSSIntakeAdapter()
        
        # Chip keywords
        cat, _ = adapter._detect_category("芯片短缺")
        assert cat == "chip_launch"
        
        cat, _ = adapter._detect_category("台积电")
        assert cat == "chip_launch"
        
        # AI keywords
        cat, _ = adapter._detect_category("AI大模型发布")
        assert cat == "ai_model_release"
    
    def test_detect_category_crypto(self):
        """Category detection for crypto events."""
        adapter = RSSIntakeAdapter()
        
        # Regulatory keywords
        cat, _ = adapter._detect_category("SEC监管")
        assert cat == "regulatory"
        
        cat, _ = adapter._detect_category("合规牌照")
        assert cat == "regulatory"
        
        # Exchange keywords
        cat, _ = adapter._detect_category("交易所被黑")
        assert cat == "exchange_hack"
    
    def test_detect_category_unknown(self):
        """Unknown category returns None with metadata."""
        adapter = RSSIntakeAdapter()
        
        # No matching keywords
        cat, meta = adapter._detect_category("普通新闻")
        assert cat is None
        assert meta["total_matches"] == 0
        
        cat, meta = adapter._detect_category("今天天气不错")
        assert cat is None
        assert meta["total_matches"] == 0
    
    def test_detect_region(self):
        """Region detection from text."""
        adapter = RSSIntakeAdapter()
        
        assert adapter._detect_region("中东局势") == "Middle East"
        assert adapter._detect_region("美国制裁") == "US"
        assert adapter._detect_region("中国政策") == "China"
        assert adapter._detect_region("欧洲经济") == "Europe"
        assert adapter._detect_region("日本市场") == "Asia"
        assert adapter._detect_region("全球趋势") == "Global"
    
    def test_normalize_event(self):
        """Normalize raw event to canonical format."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test-001",
            title="中东冲突升级",
            content="地区局势紧张",
            published_at=datetime.now(),
            source_url="https://example.com/1",
            source_name="test"
        )
        
        normalized = adapter.normalize(raw)
        
        assert normalized is not None
        assert normalized.event_id == "test-001"
        assert normalized.category == "conflict"
        assert normalized.region == "Middle East"
        assert normalized.source_name == "test"
        assert "title_length" in normalized.raw_features
    
    def test_normalize_unknown_category(self):
        """Normalize returns unknown category if no match."""
        adapter = RSSIntakeAdapter()
        
        raw = RawEvent(
            event_id="test-002",
            title="普通新闻标题",
            content="没有关键词",
            published_at=datetime.now(),
            source_url="https://example.com/2",
            source_name="test"
        )
        
        normalized = adapter.normalize(raw)
        
        assert normalized is not None
        assert normalized.category == "unknown"


class TestRSSParsing:
    """Test RSS XML parsing."""
    
    def test_parse_atom_feed(self):
        """Parse Atom format RSS feed."""
        adapter = RSSIntakeAdapter()
        
        # Sample Atom XML (no namespace for simplicity)
        xml_data = b"""<?xml version="1.0" encoding="utf-8"?>
        <feed>
            <title>Test Feed</title>
            <entry>
                <id>entry-001</id>
                <title>Test Title</title>
                <content>Test Content</content>
                <published>2026-03-18T12:00:00+00:00</published>
                <link href="https://example.com/1"/>
            </entry>
        </feed>
        """
        
        events = adapter._parse_xml(xml_data, limit=10)
        
        assert len(events) == 1
        assert events[0].event_id == "entry-001"
        assert events[0].title == "Test Title"
        assert events[0].content == "Test Content"
        assert events[0].source_url == "https://example.com/1"
    
    def test_parse_multiple_entries(self):
        """Parse multiple entries from feed."""
        adapter = RSSIntakeAdapter()
        
        xml_data = b"""<?xml version="1.0" encoding="utf-8"?>
        <feed>
            <entry><id>1</id><title>Title 1</title><content>Content 1</content></entry>
            <entry><id>2</id><title>Title 2</title><content>Content 2</content></entry>
            <entry><id>3</id><title>Title 3</title><content>Content 3</content></entry>
        </feed>
        """
        
        events = adapter._parse_xml(xml_data, limit=2)
        
        assert len(events) == 2  # Limited to 2
        assert events[0].event_id == "1"
        assert events[1].event_id == "2"
    
    def test_parse_invalid_xml(self):
        """Handle invalid XML gracefully."""
        adapter = RSSIntakeAdapter()
        
        xml_data = b"not valid xml"
        
        events = adapter._parse_xml(xml_data, limit=10)
        
        assert events == []


class TestIntakeIntegration:
    """Integration tests with mocked RSS fetch."""
    
    @patch('urllib.request.urlopen')
    def test_fetch_and_normalize(self, mock_urlopen):
        """End-to-end fetch and normalize."""
        # Mock response
        mock_response = MagicMock()
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <feed>
            <entry>
                <id>test-001</id>
                <title>中东冲突升级</title>
                <content>地区局势紧张，石油供应受影响</content>
                <published>2026-03-18T12:00:00+00:00</published>
                <link href="https://example.com/1"/>
            </entry>
            <entry>
                <id>test-002</id>
                <title>芯片短缺影响</title>
                <content>半导体供应链紧张</content>
                <published>2026-03-18T13:00:00+00:00</published>
                <link href="https://example.com/2"/>
            </entry>
        </feed>
        """
        mock_response.read.return_value = xml_content.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        adapter = RSSIntakeAdapter()
        events = adapter.fetch_and_normalize(limit=10)
        
        assert len(events) == 2
        
        # First event - geo (energy or conflict, both are geo)
        assert events[0].category in ["energy", "conflict"]
        assert events[0].region == "Middle East"
        
        # Second event - tech
        assert events[1].category == "chip_launch"
    
    @patch('urllib.request.urlopen')
    def test_fetch_network_error(self, mock_urlopen):
        """Handle network errors gracefully."""
        from urllib.error import URLError
        mock_urlopen.side_effect = URLError("Network error")
        
        adapter = RSSIntakeAdapter()
        events = adapter.fetch_feed(limit=10)
        
        assert events == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])