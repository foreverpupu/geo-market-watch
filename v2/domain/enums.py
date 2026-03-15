"""
V2 Domain Enums

定义决策类型、事件状态、phase 等枚举。
"""

from enum import Enum


class ResolutionDecisionType(str, Enum):
    """Resolution 决策类型。"""
    NEW_EVENT = "NEW_EVENT"
    UPDATE_EVENT = "UPDATE_EVENT"
    NEW_EVENT_IN_EXISTING_CLUSTER = "NEW_EVENT_IN_EXISTING_CLUSTER"
    REJECT_CANDIDATE = "REJECT_CANDIDATE"


class EventStatus(str, Enum):
    """事件状态。"""
    DETECTED = "detected"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    MONITORING = "monitoring"
    RESOLVED = "resolved"


class EventPhase(str, Enum):
    """事件阶段。"""
    WARNING = "warning"
    IMPLEMENTATION = "implementation"
    ESCALATION = "escalation"
