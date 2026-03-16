"""
Views - Agent 视图构建

为每个 Agent 构建隔离的上下文视图，确保只看到所需信息。
"""

from dataclasses import dataclass
from typing import Any

from agents.state import GraphState


@dataclass(frozen=True)
class AgentView:
    """Agent 视图。"""
    agent_name: str
    context: dict[str, Any]
    prompt: str


class ViewBuilder:
    """视图构建器。"""
    
    # Agent 可见字段映射
    VIEW_PERMISSIONS = {
        "political_analyst": {
            "read": ["raw_input_text", "raw_input_metadata"],
            "write": ["political_analyst__*"],
        },
        "market_mapper": {
            "read": [
                "raw_input_text",
                "political_analyst__events",
                "political_analyst__confidence",
            ],
            "write": ["market_mapper__*"],
        },
        "critic_validator": {
            "read": [
                "raw_input_text",
                "political_analyst__events",
                "market_mapper__candidates",
                "market_mapper__mapping_confidence",
            ],
            "write": ["critic_validator__*"],
        },
    }
    
    @classmethod
    def build_view(
        cls,
        agent_name: str,
        state: GraphState,
        prompt: str,
    ) -> AgentView:
        """
        为 Agent 构建视图。
        
        Args:
            agent_name: Agent 名称
            state: 全局状态
            prompt: Agent 提示词
        
        Returns:
            Agent 视图
        """
        permissions = cls.VIEW_PERMISSIONS.get(agent_name, {"read": [], "write": []})
        
        context = {}
        
        # 提取可读字段
        for field_pattern in permissions["read"]:
            if field_pattern.endswith("__*"):
                # 通配符模式
                prefix = field_pattern[:-1]
                for attr in dir(state):
                    if attr.startswith(prefix):
                        context[attr] = getattr(state, attr)
            else:
                # 精确匹配
                if hasattr(state, field_pattern):
                    context[field_pattern] = getattr(state, field_pattern)
        
        return AgentView(
            agent_name=agent_name,
            context=context,
            prompt=prompt,
        )
    
    @classmethod
    def get_agent_prompt_path(cls, agent_name: str) -> str:
        """获取 Agent 提示词文件路径。"""
        return f"agents/prompts/agents/{agent_name}.md"


class ShortCircuitChecker:
    """短路检查器。"""
    
    # 短路规则
    SHORT_CIRCUIT_RULES = {
        "political_analyst": {
            "condition": lambda state: len(state.political_analyst__events) == 0,
            "reason": "No political events detected",
        },
        "market_mapper": {
            "condition": lambda state: state.market_mapper__mapping_confidence < 0.3,
            "reason": "Mapping confidence too low",
        },
    }
    
    @classmethod
    def check(cls, agent_name: str, state: GraphState) -> tuple[bool, str]:
        """
        检查是否应该短路终止。
        
        Returns:
            (should_short_circuit, reason)
        """
        rule = cls.SHORT_CIRCUIT_RULES.get(agent_name)
        if rule is None:
            return False, ""
        
        if rule["condition"](state):
            return True, rule["reason"]
        
        return False, ""
