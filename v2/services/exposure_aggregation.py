"""
Exposure Aggregation

合并 direct / template / graph propagation 多条路径的暴露。
"""

import uuid
from dataclasses import dataclass, field
from v2.config import ExposureConfig
from v2.domain.models import (
    CanonicalEvent, ExposureCandidate, Exposure,
    ExposureTraceStep, NetExposureSummary
)
from v2.domain.enums import ExposureSourceType, ExposureDirection


def _generate_exposure_id() -> str:
    """生成暴露 ID。"""
    return f"EXP_{uuid.uuid4().hex[:12].upper()}"


def _aggregate_key(candidate: ExposureCandidate) -> tuple:
    """
    生成聚合键。
    
    按 target_type, target_id, direction, exposure_channel 聚合。
    """
    return (
        candidate.target_type,
        candidate.target_id,
        candidate.direction,
        candidate.exposure_channel,
    )


def _combine_scores(scores: list[float]) -> float:
    """
    合并多个分数。
    
    使用保守合并公式：final_score = 1 - Π(1 - score_i)
    
    示例：
    - path1 = 0.40, path2 = 0.30
    - 1 - (1 - 0.4) * (1 - 0.3) = 0.58
    """
    if not scores:
        return 0.0
    
    product = 1.0
    for score in scores:
        product *= (1.0 - score)
    
    return 1.0 - product


def _weighted_average(values: list[float], weights: list[float]) -> float:
    """加权平均。"""
    if not values or not weights or len(values) != len(weights):
        return 0.0
    
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def _merge_trace_steps(steps_list: list[list[ExposureTraceStep]]) -> list[ExposureTraceStep]:
    """合并多个 trace steps，去重。"""
    seen = set()
    merged = []
    
    for steps in steps_list:
        for step in steps:
            key = (step.step_type, step.step_ref, step.target)
            if key not in seen:
                seen.add(key)
                merged.append(step)
    
    return merged


def _build_reasoning_trace(
    target_type: str,
    target_id: str,
    direction: str,
    channel: str,
    trace_steps: list[ExposureTraceStep],
) -> str:
    """构建 reasoning trace 文本。"""
    parts = []
    
    for step in trace_steps:
        if step.step_type == ExposureSourceType.DIRECT_RULE.value:
            parts.append(f"direct_rule: {step.step_ref} -> {target_type}:{target_id}")
        elif step.step_type == ExposureSourceType.TEMPLATE.value:
            parts.append(f"template: {step.step_ref} -> {target_type}:{target_id}")
        elif step.step_type == ExposureSourceType.GRAPH_PROPAGATION.value:
            parts.append(f"graph: {step.source_target} -> {target_type}:{target_id}")
    
    return "; ".join(parts) if parts else f"aggregated exposure for {target_type}:{target_id}"


def aggregate_exposures(
    event: CanonicalEvent,
    candidates: list[ExposureCandidate],
    config: ExposureConfig,
) -> list[Exposure]:
    """
    聚合暴露候选为最终暴露。
    
    按 target_type, target_id, direction, exposure_channel 分组聚合。
    
    Args:
        event: 规范化事件
        candidates: 暴露候选列表
        config: 配置
        
    Returns:
        聚合后的暴露列表
    """
    # 按聚合键分组
    groups: dict[tuple, list[ExposureCandidate]] = {}
    for candidate in candidates:
        key = _aggregate_key(candidate)
        if key not in groups:
            groups[key] = []
        groups[key].append(candidate)
    
    exposures = []
    
    for (target_type, target_id, direction, channel), group in groups.items():
        # 合并分数
        scores = [c.score for c in group]
        final_score = _combine_scores(scores)
        
        # 应用上限
        final_score = min(final_score, config.aggregation_cap)
        
        # 加权平均 confidence
        confidences = [c.confidence for c in group]
        final_confidence = _weighted_average(confidences, scores) if scores else 0.5
        
        # 合并 trace steps
        all_steps = [c.trace_steps for c in group]
        merged_steps = _merge_trace_steps(all_steps)
        
        # 构建 reasoning trace
        reasoning = _build_reasoning_trace(
            target_type, target_id, direction, channel, merged_steps
        )
        
        # 取第一个的 target_name, horizon, source_type, source_ref
        first = group[0]
        
        exposure = Exposure(
            exposure_id=_generate_exposure_id(),
            event_id=event.event_id,
            target_type=target_type,
            target_id=target_id,
            target_name=first.target_name,
            exposure_channel=channel,
            direction=direction,
            magnitude_score=round(final_score, 4),
            confidence_score=round(final_confidence, 4),
            horizon=first.horizon,
            source_type=first.source_type,  # 保留主要来源类型
            source_ref="aggregated",  # 标记为聚合
            reasoning_trace=reasoning,
            trace_steps=merged_steps,
        )
        
        exposures.append(exposure)
    
    # 按分数降序排序
    exposures.sort(key=lambda x: x.magnitude_score, reverse=True)
    
    return exposures


def summarize_net_exposures(exposures: list[Exposure]) -> list[NetExposureSummary]:
    """
    汇总净暴露。
    
    对每个 target 计算 positive 和 negative 的净效果。
    
    Args:
        exposures: 暴露列表
        
    Returns:
        净暴露汇总列表
    """
    # 按 target 分组
    target_groups: dict[tuple, list[Exposure]] = {}
    for exp in exposures:
        key = (exp.target_type, exp.target_id)
        if key not in target_groups:
            target_groups[key] = []
        target_groups[key].append(exp)
    
    summaries = []
    
    for (target_type, target_id), group in target_groups.items():
        target_name = group[0].target_name
        
        # 分离正负
        positive_exps = [e for e in group if e.direction == ExposureDirection.POSITIVE.value]
        negative_exps = [e for e in group if e.direction == ExposureDirection.NEGATIVE.value]
        mixed_exps = [e for e in group if e.direction == ExposureDirection.MIXED.value]
        
        # 计算正负分数
        positive_score = max([e.magnitude_score for e in positive_exps], default=0.0)
        negative_score = max([e.magnitude_score for e in negative_exps], default=0.0)
        
        # 加上 mixed 的一半到两边
        for mixed in mixed_exps:
            mixed_contrib = mixed.magnitude_score * 0.5
            positive_score = max(positive_score, mixed_contrib)
            negative_score = max(negative_score, mixed_contrib)
        
        # 计算净方向
        net_score = positive_score - negative_score
        
        if abs(net_score) < 0.15:
            net_direction = ExposureDirection.MIXED.value
        elif net_score > 0:
            net_direction = ExposureDirection.POSITIVE.value
        else:
            net_direction = ExposureDirection.NEGATIVE.value
        
        # 收集来源
        sources = list(set(e.source_type for e in group))
        
        # 平均 confidence
        avg_confidence = sum(e.confidence_score for e in group) / len(group) if group else 0.0
        
        # 构建 summary
        summary = NetExposureSummary(
            target_type=target_type,
            target_id=target_id,
            target_name=target_name,
            net_direction=net_direction,
            net_score=round(abs(net_score), 4),
            positive_score=round(positive_score, 4),
            negative_score=round(negative_score, 4),
            confidence=round(avg_confidence, 4),
            contributing_sources=sources,
            reasoning_summary=f"net {net_direction}: +{positive_score:.2f} / -{negative_score:.2f}",
        )
        
        summaries.append(summary)
    
    # 按 net_score 降序排序
    summaries.sort(key=lambda x: x.net_score, reverse=True)
    
    return summaries
