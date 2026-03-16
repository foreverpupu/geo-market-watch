"""
GraphState - 全局状态定义

所有 Agent 共享的状态容器，采用不可变更新模式。
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class GraphState:
    """
    全局状态容器。
    
    字段命名规范：
    - 原始输入: raw_*
    - Agent 输出: agent_name__field_name
    - 合并结果: merged__field_name
    - 元数据: meta__*
    """
    
    # 原始输入
    raw_input_text: str = ""
    raw_input_metadata: dict = field(default_factory=dict)
    
    # Political Analyst 输出
    political_analyst__events: list = field(default_factory=list)
    political_analyst__confidence: float = 0.0
    political_analyst__completed: bool = False
    
    # Market Mapper 输出
    market_mapper__candidates: list = field(default_factory=list)
    market_mapper__mapping_confidence: float = 0.0
    market_mapper__completed: bool = False
    
    # Critic Validator 输出
    critic_validator__validation_result: dict = field(default_factory=dict)
    critic_validator__is_valid: bool = False
    critic_validator__feedback: str = ""
    critic_validator__completed: bool = False
    
    # 合并结果
    merged__final_events: list = field(default_factory=list)
    merged__final_candidates: list = field(default_factory=list)
    merged__validation_passed: bool = False
    
    # 元数据
    meta__created_at: datetime = field(default_factory=datetime.now)
    meta__updated_at: datetime = field(default_factory=datetime.now)
    meta__version: int = 1
    meta__execution_path: list = field(default_factory=list)
    meta__trace_id: str = ""
    
    def with_update(self, **kwargs) -> "GraphState":
        """创建更新后的状态（不可变模式）。"""
        from dataclasses import replace
        updates = {
            **kwargs,
            "meta__updated_at": datetime.now(),
            "meta__version": self.meta__version + 1,
        }
        return replace(self, **updates)
    
    def add_execution_step(self, step: str) -> "GraphState":
        """添加执行步骤记录。"""
        new_path = self.meta__execution_path + [step]
        return self.with_update(meta__execution_path=new_path)
    
    def set_trace_id(self, trace_id: str) -> "GraphState":
        """设置追踪 ID。"""
        return self.with_update(meta__trace_id=trace_id)
