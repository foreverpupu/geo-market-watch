"""
Test State Merge - 状态合并测试
"""

import pytest

from agents.merge import StateMergeError, StateMerger
from agents.state import GraphState
from agents.state_update import AgentStateUpdate


class TestStateMerge:
    """测试状态合并。"""
    
    def test_merge_set_operation(self):
        """测试 set 操作合并。"""
        state = GraphState()
        
        update = AgentStateUpdate(
            agent_name="political_analyst",
            outputs={
                "events": [{"type": "test"}],
                "confidence": 0.8,
            },
            confidence=0.8,
            completed=True,
        )
        
        new_state = StateMerger.merge(state, update, operation="set")
        
        assert new_state.political_analyst__events == [{"type": "test"}]
        assert new_state.political_analyst__confidence == 0.8
        assert new_state.political_analyst__completed is True
    
    def test_merge_append_operation(self):
        """测试 append 操作合并。"""
        state = GraphState(
            political_analyst__events=[{"type": "existing"}]
        )
        
        update = AgentStateUpdate(
            agent_name="political_analyst",
            outputs={"events": {"type": "new"}},
            completed=True,
        )
        
        new_state = StateMerger.merge(state, update, operation="append")
        
        assert len(new_state.political_analyst__events) == 2
        assert new_state.political_analyst__events[-1] == {"type": "new"}
    
    def test_merge_field_not_found(self):
        """测试字段不存在时抛出错误。"""
        state = GraphState()
        
        update = AgentStateUpdate(
            agent_name="unknown_agent",
            outputs={"some_field": "value"},
            completed=True,
        )
        
        with pytest.raises(StateMergeError):
            StateMerger.merge(state, update)
    
    def test_merge_type_mismatch(self):
        """测试类型不匹配时抛出错误。"""
        state = GraphState(
            political_analyst__confidence=0.5  # float
        )
        
        update = AgentStateUpdate(
            agent_name="political_analyst",
            outputs={"confidence": "high"},  # string
            completed=True,
        )
        
        with pytest.raises(StateMergeError):
            StateMerger.merge(state, update)
    
    def test_merge_final_results(self):
        """测试最终结果合并。"""
        state = GraphState(
            political_analyst__events=[{"type": "event"}],
            political_analyst__completed=True,
            market_mapper__candidates=[{"symbol": "TEST"}],
            market_mapper__completed=True,
            critic_validator__is_valid=True,
            critic_validator__completed=True,
        )
        
        new_state = StateMerger.merge_final_results(state)
        
        assert new_state.merged__final_events == [{"type": "event"}]
        assert new_state.merged__final_candidates == [{"symbol": "TEST"}]
        assert new_state.merged__validation_passed is True
    
    def test_invalid_update(self):
        """测试无效更新包。"""
        state = GraphState()
        
        update = AgentStateUpdate(
            agent_name="",  # 空名称
            outputs={},
            completed=True,
        )
        
        with pytest.raises(StateMergeError):
            StateMerger.merge(state, update)
    
    def test_invalid_operation(self):
        """测试无效操作类型。"""
        state = GraphState()
        
        update = AgentStateUpdate(
            agent_name="political_analyst",
            outputs={"events": []},
            completed=True,
        )
        
        with pytest.raises(StateMergeError):
            StateMerger.merge(state, update, operation="invalid_op")
