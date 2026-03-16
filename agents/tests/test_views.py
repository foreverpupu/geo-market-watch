"""
Test Views - 视图构建测试
"""

from agents.state import GraphState
from agents.views import ShortCircuitChecker, ViewBuilder


class TestViewBuilder:
    """测试视图构建器。"""
    
    def test_political_analyst_view(self):
        """测试政治分析师视图。"""
        state = GraphState(
            raw_input_text="Test input",
            raw_input_metadata={"source": "test"},
            political_analyst__events=[{"type": "event"}],
        )
        
        view = ViewBuilder.build_view("political_analyst", state, "test prompt")
        
        assert view.agent_name == "political_analyst"
        assert "raw_input_text" in view.context
        assert "raw_input_metadata" in view.context
        assert "political_analyst__events" not in view.context  # 不应该看到自己的输出
    
    def test_market_mapper_view(self):
        """测试市场映射器视图。"""
        state = GraphState(
            raw_input_text="Test input",
            political_analyst__events=[{"type": "event"}],
            political_analyst__confidence=0.8,
            market_mapper__candidates=[{"symbol": "TEST"}],
        )
        
        view = ViewBuilder.build_view("market_mapper", state, "test prompt")
        
        assert "raw_input_text" in view.context
        assert "political_analyst__events" in view.context  # 可以看到上游输出
        assert "political_analyst__confidence" in view.context
        assert "market_mapper__candidates" not in view.context  # 不应该看到自己的输出
    
    def test_critic_validator_view(self):
        """测试批评验证器视图。"""
        state = GraphState(
            raw_input_text="Test input",
            political_analyst__events=[{"type": "event"}],
            market_mapper__candidates=[{"symbol": "TEST"}],
            market_mapper__mapping_confidence=0.75,
        )
        
        view = ViewBuilder.build_view("critic_validator", state, "test prompt")
        
        assert "raw_input_text" in view.context
        assert "political_analyst__events" in view.context
        assert "market_mapper__candidates" in view.context
        assert "market_mapper__mapping_confidence" in view.context
    
    def test_view_isolation(self):
        """测试视图隔离。"""
        state = GraphState(
            raw_input_text="Test",
            political_analyst__events=[{"type": "event"}],
            market_mapper__candidates=[{"symbol": "TEST"}],
            critic_validator__is_valid=True,
        )
        
        # Political Analyst 只能看到原始输入
        pa_view = ViewBuilder.build_view("political_analyst", state, "")
        assert len(pa_view.context) == 2  # raw_input_text, raw_input_metadata
        
        # Market Mapper 可以看到 Political Analyst 的输出
        mm_view = ViewBuilder.build_view("market_mapper", state, "")
        assert "political_analyst__events" in mm_view.context
        assert "market_mapper__candidates" not in mm_view.context


class TestShortCircuitChecker:
    """测试短路检查器。"""
    
    def test_political_analyst_short_circuit_no_events(self):
        """测试政治分析师无事件时短路。"""
        state = GraphState(
            political_analyst__events=[],
        )
        
        should_short, reason = ShortCircuitChecker.check("political_analyst", state)
        
        assert should_short is True
        assert "No political events detected" in reason
    
    def test_political_analyst_no_short_circuit_with_events(self):
        """测试政治分析师有事件时不短路。"""
        state = GraphState(
            political_analyst__events=[{"type": "event"}],
        )
        
        should_short, reason = ShortCircuitChecker.check("political_analyst", state)
        
        assert should_short is False
    
    def test_market_mapper_short_circuit_low_confidence(self):
        """测试市场映射器低置信度时短路。"""
        state = GraphState(
            market_mapper__mapping_confidence=0.2,
        )
        
        should_short, reason = ShortCircuitChecker.check("market_mapper", state)
        
        assert should_short is True
        assert "Mapping confidence too low" in reason
    
    def test_market_mapper_no_short_circuit_high_confidence(self):
        """测试市场映射器高置信度时不短路。"""
        state = GraphState(
            market_mapper__mapping_confidence=0.8,
        )
        
        should_short, reason = ShortCircuitChecker.check("market_mapper", state)
        
        assert should_short is False
    
    def test_unknown_agent_no_short_circuit(self):
        """测试未知 Agent 不短路。"""
        state = GraphState()
        
        should_short, reason = ShortCircuitChecker.check("unknown_agent", state)
        
        assert should_short is False
