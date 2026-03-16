"""
Critic Validator Agent

验证和校验 Agent 的最小 stub 实现。
"""

from agents.state import GraphState
from agents.state_update import AgentStateUpdate


class CriticValidatorAgent:
    """批评验证 Agent。"""
    
    NAME = "critic_validator"
    
    # 验证阈值
    MIN_EVENT_QUALITY = 0.6
    MIN_MAPPING_QUALITY = 0.5
    
    @classmethod
    def run(cls, state: GraphState) -> AgentStateUpdate:
        """
        执行验证。
        
        Args:
            state: 当前全局状态
        
        Returns:
            AgentStateUpdate
        """
        # 获取输入
        events = state.political_analyst__events
        candidates = state.market_mapper__candidates
        mapping_confidence = state.market_mapper__mapping_confidence
        
        # 验证事件质量
        event_quality = cls._validate_event_quality(events)
        
        # 验证映射质量
        mapping_quality = cls._validate_mapping_quality(candidates, mapping_confidence)
        
        # 一致性检查
        consistency = cls._check_consistency(events, candidates)
        
        # 收集问题
        issues = []
        if event_quality < cls.MIN_EVENT_QUALITY:
            issues.append(f"Event quality below threshold: {event_quality:.2f}")
        if mapping_quality < cls.MIN_MAPPING_QUALITY:
            issues.append(f"Mapping quality below threshold: {mapping_quality:.2f}")
        if not consistency["passed"]:
            issues.append(f"Consistency check failed: {consistency['reason']}")
        
        # 确定是否有效
        is_valid = (
            event_quality >= cls.MIN_EVENT_QUALITY and
            mapping_quality >= cls.MIN_MAPPING_QUALITY and
            consistency["passed"]
        )
        
        # 生成反馈
        feedback = cls._generate_feedback(is_valid, issues, event_quality, mapping_quality)
        
        validation_result = {
            "event_quality_score": round(event_quality, 2),
            "mapping_quality_score": round(mapping_quality, 2),
            "consistency_check": "passed" if consistency["passed"] else "failed",
            "issues": issues,
        }
        
        return AgentStateUpdate(
            agent_name=cls.NAME,
            outputs={
                "validation_result": validation_result,
                "is_valid": is_valid,
                "feedback": feedback,
            },
            confidence=(event_quality + mapping_quality) / 2,
            completed=True,
        )
    
    @classmethod
    def _validate_event_quality(cls, events: list) -> float:
        """验证事件提取质量。"""
        if not events:
            return 0.0
        
        scores = []
        for event in events:
            score = 0.6  # 基础分
            
            # 检查必要字段
            if event.get("event_type"):
                score += 0.1
            if event.get("entities"):
                score += 0.1
            if event.get("region"):
                score += 0.1
            if event.get("confidence", 0) > 0.7:
                score += 0.1
            
            scores.append(min(score, 1.0))
        
        return sum(scores) / len(scores)
    
    @classmethod
    def _validate_mapping_quality(cls, candidates: list, mapping_confidence: float) -> float:
        """验证映射质量。"""
        if not candidates:
            return 0.0
        
        # 基于候选质量
        candidate_scores = []
        for candidate in candidates:
            score = 0.5
            
            # 检查必要字段
            if candidate.get("symbol"):
                score += 0.1
            if candidate.get("direction"):
                score += 0.1
            if candidate.get("time_horizon"):
                score += 0.1
            if candidate.get("confidence", 0) > 0.6:
                score += 0.1
            if candidate.get("rationale"):
                score += 0.1
            
            candidate_scores.append(min(score, 1.0))
        
        avg_candidate_score = sum(candidate_scores) / len(candidate_scores)
        
        # 结合映射置信度
        return avg_candidate_score * 0.6 + mapping_confidence * 0.4
    
    @classmethod
    def _check_consistency(cls, events: list, candidates: list) -> dict:
        """检查事件和候选的一致性。"""
        if not events or not candidates:
            return {"passed": False, "reason": "Missing events or candidates"}
        
        # 检查每个事件是否有对应的候选
        event_types = {e.get("event_type") for e in events}
        
        # 简单的启发式检查
        for event in events:
            event_type = event.get("event_type", "")
            entities = set(event.get("entities", []))
            
            # 检查是否有候选匹配
            has_match = False
            for candidate in candidates:
                rationale = candidate.get("rationale", "").lower()
                
                # 检查理由中是否提及相关实体或事件类型
                if any(entity.lower() in rationale for entity in entities):
                    has_match = True
                    break
            
            if not has_match:
                return {
                    "passed": False,
                    "reason": f"Event {event_type} has no matching candidate"
                }
        
        return {"passed": True, "reason": ""}
    
    @classmethod
    def _generate_feedback(
        cls,
        is_valid: bool,
        issues: list,
        event_quality: float,
        mapping_quality: float
    ) -> str:
        """生成验证反馈。"""
        if is_valid:
            return f"Validation passed. Event quality: {event_quality:.2f}, Mapping quality: {mapping_quality:.2f}"
        
        feedback = "Validation failed. Issues:"
        for issue in issues:
            feedback += f"\n- {issue}"
        
        return feedback
