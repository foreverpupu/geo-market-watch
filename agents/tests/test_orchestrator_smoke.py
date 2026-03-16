"""
Test Orchestrator Smoke - 编排器冒烟测试
"""

import pytest
from scripts.run_v7_orchestrator import V7Orchestrator

from agents.state import GraphState


class TestOrchestratorSmoke:
    """编排器冒烟测试。"""
    
    @pytest.fixture
    def orchestrator(self):
        """创建编排器实例。"""
        return V7Orchestrator()
    
    def test_orchestrator_initialization(self, orchestrator):
        """测试编排器初始化。"""
        assert orchestrator is not None
        assert orchestrator.tracer is not None
        assert orchestrator.console is not None
    
    def test_full_pipeline_execution(self, orchestrator):
        """测试完整流程执行。"""
        input_text = "US and Israel strike Iran, causing fertilizer prices to rise 30%."
        
        state = orchestrator.run(input_text)
        
        # 验证状态类型
        assert isinstance(state, GraphState)
        
        # 验证执行路径
        assert len(state.meta__execution_path) >= 2
        assert "political_analyst" in state.meta__execution_path
        
        # 验证版本递增
        assert state.meta__version > 1
    
    def test_pipeline_with_short_circuit(self, orchestrator):
        """测试带短路的流程。"""
        input_text = "This is a normal weather report with no geopolitical events."
        
        state = orchestrator.run(input_text)
        
        # 验证政治分析师执行了
        assert "political_analyst" in state.meta__execution_path
        
        # 验证最终结果为空
        assert len(state.merged__final_events) == 0
        assert len(state.merged__final_candidates) == 0
    
    def test_state_immutability(self, orchestrator):
        """测试状态不可变性。"""
        input_text = "Test event"
        
        state1 = orchestrator.run(input_text)
        state2 = orchestrator.run(input_text)
        
        # 验证每次运行产生新状态
        assert state1 is not state2
        
        # 验证状态内容
        assert state1.meta__trace_id != state2.meta__trace_id
    
    def test_execution_order(self, orchestrator):
        """测试执行顺序。"""
        input_text = "US strike Iran"
        
        state = orchestrator.run(input_text)
        
        # 验证执行顺序
        path = state.meta__execution_path
        
        # Political Analyst 必须先执行
        if "political_analyst" in path and "market_mapper" in path:
            assert path.index("political_analyst") < path.index("market_mapper")
        
        # Market Mapper 必须在 Critic 之前
        if "market_mapper" in path and "critic_validator" in path:
            assert path.index("market_mapper") < path.index("critic_validator")
    
    def test_trace_file_generation(self, orchestrator):
        """测试追踪文件生成。"""
        import glob
        import os
        
        input_text = "Test event for trace"
        
        state = orchestrator.run(input_text)
        
        # 验证追踪文件存在
        trace_files = glob.glob("/tmp/geo_market_traces/trace_*.json")
        assert len(trace_files) > 0
        
        # 验证文件可读
        latest_file = max(trace_files, key=os.path.getctime)
        assert os.path.getsize(latest_file) > 0
    
    def test_result_printing(self, orchestrator, capsys):
        """测试结果打印。"""
        input_text = "US strike Iran"
        
        state = orchestrator.run(input_text)
        orchestrator.print_results(state)
        
        captured = capsys.readouterr()
        
        # 验证输出包含关键信息
        assert "FINAL RESULTS" in captured.out
        assert "Execution Path:" in captured.out
        assert "Extracted Events" in captured.out
        assert "Mapped Candidates" in captured.out
    
    def test_empty_input_handling(self, orchestrator):
        """测试空输入处理。"""
        state = orchestrator.run("")
        
        # 应该正常完成，但无结果
        assert isinstance(state, GraphState)
        assert len(state.merged__final_events) == 0
