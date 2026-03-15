"""
Signal Repository

信号存储接口与实现。
"""

from typing import Protocol
from v2.domain.models import Signal


class SignalRepository(Protocol):
    """信号存储接口协议。"""
    
    def save_signal(self, signal: Signal) -> None:
        """保存信号。"""
        ...
    
    def list_signals(self, event_id: str | None = None) -> list[Signal]:
        """列出信号。"""
        ...
    
    def get_signal(self, signal_id: str) -> Signal | None:
        """获取单个信号。"""
        ...
    
    def clear(self) -> None:
        """清空存储（测试用）。"""
        ...


class InMemorySignalRepository:
    """内存信号存储实现（MVP 阶段）。"""
    
    def __init__(self):
        self._signals: dict[str, Signal] = {}
    
    def save_signal(self, signal: Signal) -> None:
        """保存信号。"""
        self._signals[signal.signal_id] = signal
    
    def list_signals(self, event_id: str | None = None) -> list[Signal]:
        """列出信号。"""
        signals = list(self._signals.values())
        if event_id:
            signals = [s for s in signals if s.event_id == event_id]
        return signals
    
    def get_signal(self, signal_id: str) -> Signal | None:
        """获取单个信号。"""
        return self._signals.get(signal_id)
    
    def clear(self) -> None:
        """清空存储。"""
        self._signals.clear()
    
    def count(self) -> int:
        """返回信号数量。"""
        return len(self._signals)
