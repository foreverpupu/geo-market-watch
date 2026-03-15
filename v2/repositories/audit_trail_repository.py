"""
Audit Trail Repository

审计轨迹存储接口与实现。
"""

from typing import Protocol
from v2.domain.models import AuditTrailEntry


class AuditTrailRepository(Protocol):
    """审计轨迹存储接口协议。"""
    
    def save_entry(self, entry: AuditTrailEntry) -> None:
        """保存审计条目。"""
        ...
    
    def list_entries(self, signal_id: str | None = None) -> list[AuditTrailEntry]:
        """列出审计条目。"""
        ...
    
    def clear(self) -> None:
        """清空存储。"""
        ...


class InMemoryAuditTrailRepository:
    """内存审计轨迹存储实现。"""
    
    def __init__(self):
        self._entries: list[AuditTrailEntry] = []
    
    def save_entry(self, entry: AuditTrailEntry) -> None:
        """保存审计条目。"""
        self._entries.append(entry)
    
    def list_entries(self, signal_id: str | None = None) -> list[AuditTrailEntry]:
        """列出审计条目。"""
        if signal_id:
            return [e for e in self._entries if e.signal_id == signal_id]
        return self._entries.copy()
    
    def clear(self) -> None:
        """清空存储。"""
        self._entries.clear()
    
    def count(self) -> int:
        """返回审计条目数量。"""
        return len(self._entries)
