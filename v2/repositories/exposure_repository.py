"""
Exposure Repository

暴露存储接口与实现。
"""

from typing import Protocol
from v2.domain.models import Exposure


class ExposureRepository(Protocol):
    """暴露存储接口协议。"""
    
    def save_exposures(self, event_id: str, exposures: list[Exposure]) -> None:
        """保存暴露列表。"""
        ...
    
    def list_exposures(self, event_id: str) -> list[Exposure]:
        """列出事件的所有暴露。"""
        ...
    
    def clear(self) -> None:
        """清空存储（测试用）。"""
        ...


class InMemoryExposureRepository:
    """内存暴露存储实现（MVP 阶段）。"""
    
    def __init__(self):
        self._exposures: dict[str, list[Exposure]] = {}
    
    def save_exposures(self, event_id: str, exposures: list[Exposure]) -> None:
        """保存暴露列表。"""
        if event_id not in self._exposures:
            self._exposures[event_id] = []
        self._exposures[event_id].extend(exposures)
    
    def list_exposures(self, event_id: str) -> list[Exposure]:
        """列出事件的所有暴露。"""
        return self._exposures.get(event_id, [])
    
    def clear(self) -> None:
        """清空存储。"""
        self._exposures.clear()
    
    def count(self, event_id: str | None = None) -> int:
        """返回暴露数量。"""
        if event_id:
            return len(self._exposures.get(event_id, []))
        return sum(len(exps) for exps in self._exposures.values())
