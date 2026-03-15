"""
Review Actions Repository

分析师操作记录存储接口与实现。
"""

from typing import Protocol
from v2.domain.models import ReviewAction


class ReviewActionsRepository(Protocol):
    """分析师操作记录存储接口协议。"""
    
    def save_action(self, action: ReviewAction) -> None:
        """保存操作记录。"""
        ...
    
    def list_actions(self, signal_id: str | None = None) -> list[ReviewAction]:
        """列出操作记录。"""
        ...
    
    def clear(self) -> None:
        """清空存储。"""
        ...


class InMemoryReviewActionsRepository:
    """内存分析师操作记录存储实现。"""
    
    def __init__(self):
        self._actions: list[ReviewAction] = []
    
    def save_action(self, action: ReviewAction) -> None:
        """保存操作记录。"""
        self._actions.append(action)
    
    def list_actions(self, signal_id: str | None = None) -> list[ReviewAction]:
        """列出操作记录。"""
        if signal_id:
            return [a for a in self._actions if a.signal_id == signal_id]
        return self._actions.copy()
    
    def clear(self) -> None:
        """清空存储。"""
        self._actions.clear()
    
    def count(self) -> int:
        """返回操作记录数量。"""
        return len(self._actions)
