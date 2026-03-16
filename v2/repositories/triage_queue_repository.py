"""
Triage Queue Repository

Triage 队列存储接口与实现。
"""

from typing import Protocol

from v2.domain.models import TriageQueueItem


class TriageQueueRepository(Protocol):
    """Triage 队列存储接口协议。"""
    
    def add_item(self, item: TriageQueueItem) -> None:
        """添加队列项。"""
        ...
    
    def get_item(self, signal_id: str) -> TriageQueueItem | None:
        """获取队列项。"""
        ...
    
    def list_items(self, status: str | None = None, assigned_to: str | None = None) -> list[TriageQueueItem]:
        """列出队列项。"""
        ...
    
    def update_item(self, item: TriageQueueItem) -> None:
        """更新队列项。"""
        ...
    
    def clear(self) -> None:
        """清空存储。"""
        ...


class InMemoryTriageQueueRepository:
    """内存 Triage 队列存储实现。"""
    
    def __init__(self):
        self._items: dict[str, TriageQueueItem] = {}
    
    def add_item(self, item: TriageQueueItem) -> None:
        """添加队列项。"""
        self._items[item.signal_id] = item
    
    def get_item(self, signal_id: str) -> TriageQueueItem | None:
        """获取队列项。"""
        return self._items.get(signal_id)
    
    def list_items(self, status: str | None = None, assigned_to: str | None = None) -> list[TriageQueueItem]:
        """列出队列项。"""
        items = list(self._items.values())
        if status:
            items = [i for i in items if i.status == status]
        if assigned_to:
            items = [i for i in items if i.assigned_to == assigned_to]
        return items
    
    def update_item(self, item: TriageQueueItem) -> None:
        """更新队列项。"""
        self._items[item.signal_id] = item
    
    def clear(self) -> None:
        """清空存储。"""
        self._items.clear()
    
    def count(self) -> int:
        """返回队列项数量。"""
        return len(self._items)
