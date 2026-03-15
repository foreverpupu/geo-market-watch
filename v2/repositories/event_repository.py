"""
Event Repository

事件存储接口与实现。
"""

from datetime import datetime
from typing import Protocol, Optional
from v2.domain.models import CanonicalEvent


class EventRepository(Protocol):
    """事件存储接口协议。"""
    
    def list_recent_events(
        self,
        event_type: str,
        region: Optional[str],
        since: datetime,
    ) -> list[CanonicalEvent]:
        """列出最近的事件。"""
        ...
    
    def get_event(self, event_id: str) -> Optional[CanonicalEvent]:
        """获取单个事件。"""
        ...
    
    def create_event(self, event: CanonicalEvent) -> CanonicalEvent:
        """创建事件。"""
        ...
    
    def update_event(self, event: CanonicalEvent) -> CanonicalEvent:
        """更新事件。"""
        ...
    
    def list_all_events(self) -> list[CanonicalEvent]:
        """列出所有事件。"""
        ...


class InMemoryEventRepository:
    """内存事件存储实现（MVP 阶段）。"""
    
    def __init__(self):
        self._events: dict[str, CanonicalEvent] = {}
    
    def list_recent_events(
        self,
        event_type: str,
        region: Optional[str],
        since: datetime,
    ) -> list[CanonicalEvent]:
        """列出最近的事件，按 event_type 和 region 过滤。"""
        results = []
        for event in self._events.values():
            # 过滤 event_type
            if event.event_type != event_type:
                continue
            
            # 过滤时间窗口
            if event.last_seen_at < since:
                continue
            
            # region 过滤（如果指定了）
            if region is not None and event.region != region:
                continue
            
            results.append(event)
        
        return results
    
    def get_event(self, event_id: str) -> Optional[CanonicalEvent]:
        """获取单个事件。"""
        return self._events.get(event_id)
    
    def create_event(self, event: CanonicalEvent) -> CanonicalEvent:
        """创建事件。"""
        if event.event_id in self._events:
            raise ValueError(f"Event {event.event_id} already exists")
        self._events[event.event_id] = event
        return event
    
    def update_event(self, event: CanonicalEvent) -> CanonicalEvent:
        """更新事件。"""
        if event.event_id not in self._events:
            raise ValueError(f"Event {event.event_id} not found")
        self._events[event.event_id] = event
        return event
    
    def list_all_events(self) -> list[CanonicalEvent]:
        """列出所有事件。"""
        return list(self._events.values())
    
    def clear(self) -> None:
        """清空所有事件（测试用）。"""
        self._events.clear()
    
    def count(self) -> int:
        """返回事件数量。"""
        return len(self._events)
