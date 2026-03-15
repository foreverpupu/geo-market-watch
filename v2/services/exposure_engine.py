"""
Exposure Engine (Step 2a - Direct Rules Only)

Step 2 主入口，当前仅实现 direct exposure rules。
"""

from v2.config import ExposureConfig, DEFAULT_EXPOSURE_CONFIG
from v2.domain.models import CanonicalEvent, ExposureResult
from v2.repositories.exposure_repository import ExposureRepository, InMemoryExposureRepository
from v2.services.exposure_rules import compute_direct_exposures
from v2.services.exposure_aggregation import aggregate_exposures, summarize_net_exposures


def _candidates_to_exposures(candidates, event_id: str) -> list:
    """将候选转换为 Exposure 对象（临时辅助函数）。"""
    import uuid
    from v2.domain.models import Exposure
    
    exposures = []
    for cand in candidates:
        exp = Exposure(
            exposure_id=f"EXP_{uuid.uuid4().hex[:12].upper()}",
            event_id=event_id,
            target_type=cand.target_type,
            target_id=cand.target_id,
            target_name=cand.target_name,
            exposure_channel=cand.exposure_channel,
            direction=cand.direction,
            magnitude_score=round(cand.score, 4),
            confidence_score=round(cand.confidence, 4),
            horizon=cand.horizon,
            source_type=cand.source_type,
            source_ref=cand.source_ref,
            reasoning_trace=cand.reasoning_trace,
            trace_steps=cand.trace_steps,
            metadata=cand.metadata,
        )
        exposures.append(exp)
    return exposures


def compute_event_exposures(
    event: CanonicalEvent,
    exposure_repository: ExposureRepository | None = None,
    config: ExposureConfig = DEFAULT_EXPOSURE_CONFIG,
) -> ExposureResult:
    """
    计算事件的完整暴露（Step 2a - Direct Rules Only）。
    
    Args:
        event: 规范化事件
        exposure_repository: 暴露存储（可选）
        config: 配置
        
    Returns:
        Exposure 结果
    """
    # Step 1: Direct Exposure Rules
    direct_candidates = compute_direct_exposures(event, config)
    direct_exposures = _candidates_to_exposures(direct_candidates, event.event_id)
    
    # Step 2: Aggregation（合并相同 target 的暴露）
    all_candidates = direct_candidates  # Step 2a 只有 direct
    aggregated_exposures = aggregate_exposures(event, all_candidates, config)
    
    # Step 3: Net Exposure Summary
    net_summaries = summarize_net_exposures(aggregated_exposures)
    
    # 保存到 repository（如果提供）
    if exposure_repository:
        exposure_repository.save_exposures(event.event_id, aggregated_exposures)
    
    return ExposureResult(
        event=event,
        direct_exposures=direct_exposures,
        template_exposures=[],  # Step 2a 未实现
        graph_exposures=[],  # Step 2a 未实现
        aggregated_exposures=aggregated_exposures,
        net_exposure_summaries=net_summaries,
    )
