"""
Exposure Rules

基于 event_type + entities + region 的直接暴露规则。
这是最高确定性来源。
"""

import uuid
from v2.config import ExposureConfig
from v2.domain.models import CanonicalEvent, ExposureCandidate, ExposureTraceStep
from v2.domain.enums import (
    ExposureTargetType, ExposureDirection, ExposureChannel,
    ExposureSourceType, ExposureHorizon
)


def _generate_exposure_id() -> str:
    """生成暴露 ID。"""
    return f"EXP_{uuid.uuid4().hex[:12].upper()}"


def _create_direct_exposure(
    event: CanonicalEvent,
    target_type: str,
    target_id: str,
    target_name: str,
    direction: str,
    channel: str,
    score: float,
    confidence: float,
    horizon: str,
    rule_name: str,
) -> ExposureCandidate:
    """创建直接暴露候选。"""
    trace_step = ExposureTraceStep(
        step_type=ExposureSourceType.DIRECT_RULE.value,
        step_ref=rule_name,
        source_target=event.event_id,
        target=f"{target_type}:{target_id}",
        score_contribution=score,
        hop_count=0,
    )
    
    return ExposureCandidate(
        target_type=target_type,
        target_id=target_id,
        target_name=target_name,
        exposure_channel=channel,
        direction=direction,
        score=score,
        confidence=confidence,
        horizon=horizon,
        source_type=ExposureSourceType.DIRECT_RULE.value,
        source_ref=rule_name,
        reasoning_trace=f"direct_rule: {rule_name} -> {target_type}:{target_id}",
        trace_steps=[trace_step],
    )


def _rule_shipping_disruption(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """
    Rule 1: Shipping Disruption
    
    直接影响：
    - affected route (negative)
    - container shipping sector (mixed)
    - import-dependent regions/theme (negative)
    """
    exposures = []
    base_score = config.direct_exposure_base_score
    
    # 从 entities 中提取 route
    route = None
    for entity in event.normalized_entities:
        if any(r in entity for r in ["route", "canal", "strait", "passage", "sea"]):
            route = entity
            break
    
    # 如果没有找到 route，使用 region
    if not route and event.region:
        route = event.region
    
    if route:
        # Route 直接受影响 (negative)
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.ROUTE.value,
            target_id=route.replace(" ", "_"),
            target_name=route.title(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            score=base_score,
            confidence=0.80,
            horizon=ExposureHorizon.DAYS.value,
            rule_name="shipping_disruption_route",
        ))
    
    # Container shipping sector (mixed - 航运公司可能受益也可能受损)
    exposures.append(_create_direct_exposure(
        event=event,
        target_type=ExposureTargetType.SECTOR.value,
        target_id="container_shipping",
        target_name="Container Shipping",
        direction=ExposureDirection.MIXED.value,
        channel=ExposureChannel.PRICING_POWER_SHIFT.value,
        score=base_score * 0.85,
        confidence=0.65,
        horizon=ExposureHorizon.WEEKS.value,
        rule_name="shipping_disruption_sector",
    ))
    
    # Import supply chain theme (negative)
    exposures.append(_create_direct_exposure(
        event=event,
        target_type=ExposureTargetType.THEME.value,
        target_id="import_supply_chain",
        target_name="Import Supply Chain",
        direction=ExposureDirection.NEGATIVE.value,
        channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
        score=base_score * 0.90,
        confidence=0.70,
        horizon=ExposureHorizon.WEEKS.value,
        rule_name="shipping_disruption_theme",
    ))
    
    return exposures


def _rule_port_closure(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """Rule 2: Port Closure"""
    exposures = []
    base_score = config.direct_exposure_base_score
    
    # Facility/port 本身
    port = None
    for entity in event.normalized_entities:
        if any(p in entity for p in ["port", "terminal", "hub"]):
            port = entity
            break
    
    if port:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.FACILITY.value,
            target_id=port.replace(" ", "_"),
            target_name=port.title(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            score=base_score,
            confidence=0.85,
            horizon=ExposureHorizon.DAYS.value,
            rule_name="port_closure_facility",
        ))
    
    # Shipping/logistics sector
    exposures.append(_create_direct_exposure(
        event=event,
        target_type=ExposureTargetType.SECTOR.value,
        target_id="logistics",
        target_name="Logistics",
        direction=ExposureDirection.NEGATIVE.value,
        channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
        score=base_score * 0.85,
        confidence=0.75,
        horizon=ExposureHorizon.DAYS.value,
        rule_name="port_closure_logistics",
    ))
    
    # Related country export supply
    for country in event.country_codes[:2]:  # 最多前两个国家
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.COUNTRY.value,
            target_id=country.lower(),
            target_name=country.upper(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.SUPPLY_SHOCK.value,
            score=base_score * 0.70,
            confidence=0.65,
            horizon=ExposureHorizon.WEEKS.value,
            rule_name="port_closure_country",
        ))
    
    return exposures


def _rule_sanction(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """Rule 3: Sanction"""
    exposures = []
    base_score = config.direct_exposure_base_score
    
    # Target country
    for country in event.country_codes[:2]:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.COUNTRY.value,
            target_id=country.lower(),
            target_name=country.upper(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.SANCTIONS_RISK.value,
            score=base_score,
            confidence=0.80,
            horizon=ExposureHorizon.MONTHS.value,
            rule_name="sanction_country",
        ))
    
    # Sanctions risk theme
    exposures.append(_create_direct_exposure(
        event=event,
        target_type=ExposureTargetType.THEME.value,
        target_id="sanctions_risk",
        target_name="Sanctions Risk",
        direction=ExposureDirection.NEGATIVE.value,
        channel=ExposureChannel.SANCTIONS_RISK.value,
        score=base_score * 0.85,
        confidence=0.75,
        horizon=ExposureHorizon.MONTHS.value,
        rule_name="sanction_theme",
    ))
    
    return exposures


def _rule_export_control(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """Rule 4: Export Control"""
    exposures = []
    base_score = config.direct_exposure_base_score
    
    # Restricted commodity
    commodity = None
    for entity in event.normalized_entities:
        if any(c in entity for c in ["gallium", "graphite", "lithium", "copper", "oil", "gas", "rare earth"]):
            commodity = entity
            break
    
    if commodity:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.COMMODITY.value,
            target_id=commodity.replace(" ", "_"),
            target_name=commodity.title(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.SUPPLY_SHOCK.value,
            score=base_score,
            confidence=0.80,
            horizon=ExposureHorizon.WEEKS.value,
            rule_name="export_control_commodity",
        ))
    
    # Exporting country
    for country in event.country_codes[:1]:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.COUNTRY.value,
            target_id=country.lower(),
            target_name=country.upper(),
            direction=ExposureDirection.MIXED.value,
            channel=ExposureChannel.REGULATORY_RISK.value,
            score=base_score * 0.70,
            confidence=0.65,
            horizon=ExposureHorizon.MONTHS.value,
            rule_name="export_control_country",
        ))
    
    return exposures


def _rule_labor_strike(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """Rule 7: Labor Strike"""
    exposures = []
    base_score = config.direct_exposure_base_score
    
    # Facility/port/company
    facility = None
    for entity in event.normalized_entities:
        if any(f in entity for f in ["port", "factory", "plant", "mine"]):
            facility = entity
            break
    
    if facility:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.FACILITY.value,
            target_id=facility.replace(" ", "_"),
            target_name=facility.title(),
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            score=base_score,
            confidence=0.80,
            horizon=ExposureHorizon.DAYS.value,
            rule_name="labor_strike_facility",
        ))
    
    # Logistics or affected industry
    exposures.append(_create_direct_exposure(
        event=event,
        target_type=ExposureTargetType.SECTOR.value,
        target_id="logistics",
        target_name="Logistics",
        direction=ExposureDirection.NEGATIVE.value,
        channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
        score=base_score * 0.75,
        confidence=0.70,
        horizon=ExposureHorizon.WEEKS.value,
        rule_name="labor_strike_sector",
    ))
    
    return exposures


def _rule_generic(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """Generic rule for unhandled event types"""
    exposures = []
    base_score = config.direct_exposure_base_score * 0.60
    
    # Region exposure
    if event.region:
        exposures.append(_create_direct_exposure(
            event=event,
            target_type=ExposureTargetType.THEME.value,
            target_id=f"{event.event_type}_risk",
            target_name=f"{event.event_type.replace('_', ' ').title()} Risk",
            direction=ExposureDirection.NEGATIVE.value,
            channel=ExposureChannel.GEOPOLITICAL_PREMIUM.value,
            score=base_score,
            confidence=0.50,
            horizon=ExposureHorizon.WEEKS.value,
            rule_name="generic_event_risk",
        ))
    
    return exposures


# 规则映射表
EXPOSURE_RULES = {
    "shipping_disruption": _rule_shipping_disruption,
    "port_closure": _rule_port_closure,
    "sanction": _rule_sanction,
    "export_control": _rule_export_control,
    "labor_strike": _rule_labor_strike,
}


def compute_direct_exposures(
    event: CanonicalEvent,
    config: ExposureConfig,
) -> list[ExposureCandidate]:
    """
    计算事件的直接暴露。
    
    基于 event_type 调用对应的规则函数。
    
    Args:
        event: 规范化事件
        config: 配置
        
    Returns:
        暴露候选列表
    """
    rule_func = EXPOSURE_RULES.get(event.event_type, _rule_generic)
    return rule_func(event, config)
