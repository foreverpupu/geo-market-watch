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


class ExposureTargetType(str, Enum):
    """暴露目标类型。"""
    COUNTRY = "country"
    SECTOR = "sector"
    INDUSTRY = "industry"
    COMPANY = "company"
    COMMODITY = "commodity"
    ASSET = "asset"
    ETF = "etf"
    ROUTE = "route"
    FACILITY = "facility"
    THEME = "theme"


class ExposureDirection(str, Enum):
    """暴露方向。"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    UNCERTAIN = "uncertain"


class ExposureChannel(str, Enum):
    """暴露渠道。"""
    SUPPLY_SHOCK = "supply_shock"
    DEMAND_SHOCK = "demand_shock"
    LOGISTICS_DISRUPTION = "logistics_disruption"
    REGULATORY_RISK = "regulatory_risk"
    FINANCING_RISK = "financing_risk"
    SANCTIONS_RISK = "sanctions_risk"
    PRICING_POWER_SHIFT = "pricing_power_shift"
    SUBSTITUTION_EFFECT = "substitution_effect"
    GEOPOLITICAL_PREMIUM = "geopolitical_premium"
    CYBER_RISK = "cyber_risk"
    POLICY_UNCERTAINTY = "policy_uncertainty"


class ExposureSourceType(str, Enum):
    """暴露来源类型。"""
    DIRECT_RULE = "direct_rule"
    TEMPLATE = "template"
    GRAPH_PROPAGATION = "graph_propagation"


class ExposureHorizon(str, Enum):
    """影响时间范围。"""
    INTRADAY = "intraday"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    STRUCTURAL = "structural"


class SignalClass(str, Enum):
    """信号等级。"""
    MAJOR_SHOCK = "major_shock"
    HIGH_PRIORITY = "high_priority"
    WATCHLIST_UPGRADE = "watchlist_upgrade"
    MONITOR = "monitor"
    LOW_SIGNAL = "low_signal"


class SignalStatus(str, Enum):
    """信号状态。"""
    GENERATED = "generated"
    QUEUED = "queued"
    CONFIRMED = "confirmed"
    DISMISSED = "dismissed"
    ARCHIVED = "archived"


class QueueType(str, Enum):
    """队列类型。"""
    TRIAGE = "triage"
    ACTIVE_EVENT = "active_event"
    CONFLICT = "conflict"
    WATCHLIST = "watchlist"
    POSTMORTEM = "postmortem"


class ReviewActionType(str, Enum):
    """分析师操作类型。"""
    MARK_AS_RELEVANT = "mark_as_relevant"
    MARK_AS_IRRELEVANT = "mark_as_irrelevant"
    ADD_TO_WATCHLIST = "add_to_watchlist"
    ARCHIVE = "archive"
    COMMENT = "comment"
    ESCALATE = "escalate"
    CLAIM = "claim"


class TriageStatus(str, Enum):
    """Triage 队列项状态。"""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    EXPIRED = "expired"


class WatchlistStatus(str, Enum):
    """Watchlist 项状态。"""
    ACTIVE = "active"
    ARCHIVED = "archived"


class EventTypeCategory(str, Enum):
    """事件类型分类。"""
    DIRECTIONALITY = "directionality"  # 方向性事件（如关税）
    VOLATILITY = "volatility"  # 波动性事件（如军事演习）


class SignalUsefulnessRating(str, Enum):
    """信号效用评级。"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    FALSE_ALARM = "false_alarm"
