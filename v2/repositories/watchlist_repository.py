"""
Watchlist Repository

Watchlist 存储接口与实现。
"""

from typing import Protocol

from v2.domain.models import WatchlistEntry


class WatchlistRepository(Protocol):
    """Watchlist 存储接口协议。"""
    
    def add_entry(self, entry: WatchlistEntry) -> None:
        """添加条目。"""
        ...
    
    def list_entries(self, assigned_to: str | None = None) -> list[WatchlistEntry]:
        """列出条目。"""
        ...
    
    def remove_entry(self, signal_id: str, assigned_to: str) -> None:
        """移除条目。"""
        ...
    
    def clear(self) -> None:
        """清空存储。"""
        ...


class InMemoryWatchlistRepository:
    """内存 Watchlist 存储实现。"""
    
    def __init__(self):
        self._entries: dict[tuple[str, str], WatchlistEntry] = {}
    
    def add_entry(self, entry: WatchlistEntry) -> None:
        """添加条目。"""
        key = (entry.signal_id, entry.assigned_to)
        self._entries[key] = entry
    
    def list_entries(self, assigned_to: str | None = None) -> list[WatchlistEntry]:
        """列出条目。"""
        entries = list(self._entries.values())
        if assigned_to:
            entries = [e for e in entries if e.assigned_to == assigned_to]
        return entries
    
    def remove_entry(self, signal_id: str, assigned_to: str) -> None:
        """移除条目。"""
        key = (signal_id, assigned_to)
        if key in self._entries:
            del self._entries[key]
    
    def clear(self) -> None:
        """清空存储。"""
        self._entries.clear()
    
    def count(self, assigned_to: str | None = None) -> int:
        """返回条目数量。"""
        if assigned_to:
            return len([e for e in self._entries.values() if e.assigned_to == assigned_to])
        return len(self._entries)
