"""
Test Short Circuit - 短路机制测试
"""

from agents.market_mapper import MarketMapperAgent
from agents.political_analyst import PoliticalAnalystAgent

from agents.state import GraphState


class TestPoliticalAnalystShortCircuit:
    """测试政治分析师短路。"""
    
    def test_short_circuit_no_events(self):
        """测试无事件时短路。"""
        state = GraphState(
            raw_input_text="This is a normal text without any geopolitical events.",
        )
        
        update = PoliticalAnalystAgent.run(state)
        
        assert update.short_circuit is True
        assert "No political events detected" in update.short_circuit_reason
        assert update.outputs["events"] == []
    
    def test_no_short_circuit_with_events(self):
        """测试有事件时不短路。"""
        state = GraphState(
            raw_input_text="US and Israel strike Iran, causing fertilizer prices to rise.",
        )
        
        update = PoliticalAnalystAgent.run(state)
        
        assert update.short_circuit is False
        assert len(update.outputs["events"]) > 0
        assert update.completed is True


class TestMarketMapperShortCircuit:
    """测试市场映射器短路。"""
    
    def test_short_circuit_low_confidence(self):
        """测试低置信度时短路。"""
        state = GraphState(
            raw_input_text="Test",
            political_analyst__events=[{"type": "test", "confidence": 0.1}],
            political_analyst__confidence=0.1,
        )
        
        update = MarketMapperAgent.run(state)
        
        assert update.short_circuit is True
        assert "Mapping confidence too low" in update.short_circuit_reason
    
    def test_short_circuit_no_events(self):
        """测试无事件时短路。"""
        state = GraphState(
            raw_input_text="Test",
            political_analyst__events=[],
            political_analyst__confidence=0.0,
        )
        
        update = MarketMapperAgent.run(state)
        
        assert update.short_circuit is True
        assert "No events to map" in update.short_circuit_reason
    
    def test_no_short_circuit_normal(self):
        """测试正常情况不短路。"""
        state = GraphState(
            raw_input_text="US strike Iran, fertilizer prices rise",
            political_analyst__events=[{
                "event_type": "military_strike",
                "entities": ["US", "Iran", "fertilizer"],
                "region": "Middle East",
                "impact_severity": "high",
                "confidence": 0.8,
            }],
            political_analyst__confidence=0.8,
        )
        
        update = MarketMapperAgent.run(state)
        
        assert update.short_circuit is False
        assert len(update.outputs["candidates"]) > 0
        assert update.completed is True


class TestShortCircuitPropagation:
    """测试短路传播。"""
    
    def test_political_short_circuit_stops_pipeline(self):
        """测试政治分析师短路阻止后续执行。"""
        from scripts.run_v7_orchestrator import V7Orchestrator
        
        orchestrator = V7Orchestrator()
        
        # 使用无事件文本
        state = orchestrator.run("This is a normal text without any events.")
        
        # 检查执行路径
        assert "political_analyst" in state.meta__execution_path
        # Market Mapper 不应该执行（被短路）
        assert "market_mapper" not in state.meta__execution_path
    
    def test_normal_flow_completes_all_agents(self):
        """测试正常流程完成所有 Agent。"""
        from scripts.run_v7_orchestrator import V7Orchestrator
        
        orchestrator = V7Orchestrator()
        
        # 使用有事件文本
        state = orchestrator.run("US strike Iran, oil prices surge")
        
        # 检查所有 Agent 都执行了
        assert "political_analyst" in state.meta__execution_path
        assert "market_mapper" in state.meta__execution_path
        assert "critic_validator" in state.meta__execution_path
