"""
AgentStateUpdate - Agent 状态更新定义

每个 Agent 返回的结构化更新，用于状态合并。
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentStateUpdate:
    """
    Agent 状态更新包。
    
    强制要求：
    1. agent_name: 必须匹配 Agent 注册名
    2. outputs: Agent 产生的结构化输出
    3. confidence: 0.0-1.0 的置信度
    4. completed: 是否完成执行
    5. short_circuit: 是否触发短路终止
    """
    
    agent_name: str
    outputs: dict = field(default_factory=dict)
    confidence: float = 0.0
    completed: bool = False
    short_circuit: bool = False
    short_circuit_reason: str = ""
    
    def validate(self) -> bool:
        """验证更新包完整性。"""
        if not self.agent_name:
            return False
        if not 0.0 <= self.confidence <= 1.0:
            return False
        return True
    
    @classmethod
    def create_empty(cls, agent_name: str) -> "AgentStateUpdate":
        """创建空的更新包。"""
        return cls(agent_name=agent_name, completed=False)
    
    @classmethod
    def create_short_circuit(
        cls, 
        agent_name: str, 
        reason: str,
        outputs: dict = None
    ) -> "AgentStateUpdate":
        """创建短路终止更新包。"""
        return cls(
            agent_name=agent_name,
            outputs=outputs or {},
            completed=True,
            short_circuit=True,
            short_circuit_reason=reason,
        )
