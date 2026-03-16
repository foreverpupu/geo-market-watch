"""
Candidate Builder

把输入样本转换为统一的 EventCandidate 对象。
"""

import uuid
from datetime import datetime

from v2.domain.models import EventCandidate
from v2.services.entity_normalizer import normalize_entities


def _generate_candidate_id() -> str:
    """生成候选 ID。"""
    return f"CAND_{uuid.uuid4().hex[:12].upper()}"


def build_candidate_from_dict(payload: dict, now: datetime) -> EventCandidate:
    """
    从字典构建 EventCandidate。
    
    字段映射：
    - candidate_id: 自动生成（若无）
    - source_id: 从 candidate_id 派生（若无）
    - title: 必需
    - summary: 默认为空字符串
    - event_type: 必需
    - region: 可选
    - country_codes: 默认为空列表
    - entity_names: 默认为空列表
    - normalized_entities: 自动标准化
    - occurred_at: 可选
    - detected_at: 使用 now（若无）
    - embedding: 允许外部传入
    - metadata: 默认为空字典
    
    Args:
        payload: 输入字典
        now: 当前时间
        
    Returns:
        EventCandidate
    """
    # 生成或获取 ID
    candidate_id = payload.get("candidate_id") or _generate_candidate_id()
    source_id = payload.get("source_id") or candidate_id
    
    # 获取并标准化实体
    entity_names = payload.get("entity_names", [])
    if isinstance(entity_names, str):
        entity_names = [entity_names]
    normalized_entities = normalize_entities(entity_names)
    
    # 解析时间
    occurred_at = payload.get("occurred_at")
    if isinstance(occurred_at, str):
        occurred_at = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    
    detected_at = payload.get("detected_at")
    if isinstance(detected_at, str):
        detected_at = datetime.fromisoformat(detected_at.replace("Z", "+00:00"))
    else:
        detected_at = now
    
    # 获取 embedding
    embedding = payload.get("embedding")
    
    return EventCandidate(
        candidate_id=candidate_id,
        source_id=source_id,
        title=payload.get("title", ""),
        summary=payload.get("summary", ""),
        event_type=payload.get("event_type", ""),
        region=payload.get("region"),
        country_codes=payload.get("country_codes", []),
        entity_names=entity_names,
        normalized_entities=normalized_entities,
        occurred_at=occurred_at,
        detected_at=detected_at,
        embedding=embedding,
        metadata=payload.get("metadata", {}),
    )


def build_candidates_from_list(items: list[dict], now: datetime) -> list[EventCandidate]:
    """
    批量从字典列表构建 EventCandidate。
    
    Args:
        items: 输入字典列表
        now: 当前时间
        
    Returns:
        EventCandidate 列表
    """
    return [build_candidate_from_dict(item, now) for item in items]
