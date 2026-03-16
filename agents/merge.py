"""
State Merge - 状态合并核心逻辑

实现严格的状态合并规则，强制类型检查和操作规范。
"""

from typing import Any, get_type_hints

from agents.state import GraphState
from agents.state_update import AgentStateUpdate


class StateMergeError(Exception):
    """状态合并错误。"""
    pass


class StateMerger:
    """状态合并器。"""
    
    # 允许的合并操作
    ALLOWED_OPERATIONS = {"set", "append", "extend", "merge_dict"}
    
    @staticmethod
    def validate_field_exists(state: GraphState, field_name: str) -> bool:
        """验证字段是否存在于状态中。"""
        return hasattr(state, field_name)
    
    @staticmethod
    def validate_type_compatibility(state: GraphState, field_name: str, value: Any) -> bool:
        """验证类型兼容性。"""
        current_value = getattr(state, field_name, None)
        if current_value is None:
            return True
        
        # 获取字段类型提示
        type_hints = get_type_hints(GraphState)
        expected_type = type_hints.get(field_name)
        
        if expected_type is None:
            return True
        
        # 检查类型
        if value is None:
            return True
        
        return isinstance(value, type(current_value))
    
    @classmethod
    def merge(
        cls,
        state: GraphState,
        update: AgentStateUpdate,
        operation: str = "set",
    ) -> GraphState:
        """
        合并 Agent 更新到全局状态。
        
        Args:
            state: 当前全局状态
            update: Agent 状态更新
            operation: 合并操作类型 (set/append/extend/merge_dict)
        
        Returns:
            更新后的全局状态
        
        Raises:
            StateMergeError: 合并失败
        """
        if not update.validate():
            raise StateMergeError(f"Invalid update from {update.agent_name}")
        
        if operation not in cls.ALLOWED_OPERATIONS:
            raise StateMergeError(f"Unknown operation: {operation}")
        
        updates = {}
        
        for key, value in update.outputs.items():
            # 构建完整字段名
            full_field_name = f"{update.agent_name}__{key}"
            
            # 验证字段存在
            if not cls.validate_field_exists(state, full_field_name):
                raise StateMergeError(
                    f"Field {full_field_name} not found in state"
                )
            
            # 验证类型兼容（仅对 set 操作严格检查）
            if operation == "set" and not cls.validate_type_compatibility(state, full_field_name, value):
                current = getattr(state, full_field_name)
                raise StateMergeError(
                    f"Type mismatch for {full_field_name}: "
                    f"expected {type(current)}, got {type(value)}"
                )
            
            # 执行合并
            if operation == "set":
                updates[full_field_name] = value
            elif operation == "append":
                current = list(getattr(state, full_field_name, []))
                current.append(value)
                updates[full_field_name] = current
            elif operation == "extend":
                current = list(getattr(state, full_field_name, []))
                current.extend(value if isinstance(value, list) else [value])
                updates[full_field_name] = current
            elif operation == "merge_dict":
                current = dict(getattr(state, full_field_name, {}))
                current.update(value if isinstance(value, dict) else {})
                updates[full_field_name] = current
        
        # 添加 completed 标记
        updates[f"{update.agent_name}__completed"] = update.completed
        
        return state.with_update(**updates)
    
    @classmethod
    def merge_final_results(cls, state: GraphState) -> GraphState:
        """
        合并所有 Agent 结果到最终结果。
        
        简单的合并策略：直接复制 Agent 输出到 merged 字段。
        """
        updates = {}
        
        # 合并事件
        if state.political_analyst__completed:
            updates["merged__final_events"] = state.political_analyst__events
        
        # 合并候选
        if state.market_mapper__completed:
            updates["merged__final_candidates"] = state.market_mapper__candidates
        
        # 合并验证结果
        if state.critic_validator__completed:
            updates["merged__validation_passed"] = state.critic_validator__is_valid
        
        return state.with_update(**updates)
