"""
Audit Trail

审计轨迹记录。
"""

import uuid

from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG, AnalystWorkflowConfig
from v2.domain.models import AuditTrailEntry, ReviewAction
from v2.repositories.audit_trail_repository import (
    AuditTrailRepository,
)


def _generate_entry_id() -> str:
    """生成审计条目 ID。"""
    return f"AUDIT_{uuid.uuid4().hex[:12].upper()}"


def log_audit_trail(
    action: ReviewAction,
    audit_repository: AuditTrailRepository | None = None,
    config: AnalystWorkflowConfig = DEFAULT_ANALYST_WORKFLOW_CONFIG,
) -> AuditTrailEntry | None:
    """
    记录审计轨迹。
    
    Args:
        action: 分析师操作
        audit_repository: 审计存储（可选）
        config: 配置
        
    Returns:
        AuditTrailEntry（如果启用审计）
    """
    if not config.audit_trail_enabled:
        return None
    
    # 构建操作详情
    detail_parts = [f"Action: {action.action_type}"]
    
    if action.comment:
        detail_parts.append(f"Comment: {action.comment}")
    
    if action.exposure_override:
        detail_parts.append(f"Exposure Override: {action.exposure_override}")
    
    if action.severity_override is not None:
        detail_parts.append(f"Severity Override: {action.severity_override}")
    
    if action.agreement_with_ai is not None:
        detail_parts.append(f"Agreement with AI: {action.agreement_with_ai}")
    
    entry = AuditTrailEntry(
        entry_id=_generate_entry_id(),
        signal_id=action.signal_id,
        action_type=action.action_type,
        action_taken_by=action.action_taken_by,
        timestamp=action.action_timestamp,
        action_detail="; ".join(detail_parts),
        metadata={
            "action_id": action.action_id,
            "has_override": action.exposure_override is not None or action.severity_override is not None,
        },
    )
    
    if audit_repository:
        audit_repository.save_entry(entry)
    
    return entry
