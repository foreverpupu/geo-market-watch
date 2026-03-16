"""
Price Repository

价格数据存储接口与实现（模拟数据）。
"""

from datetime import datetime, timedelta
from typing import Protocol

from v2.domain.models import PricePoint


class PriceRepository(Protocol):
    """价格数据存储接口协议。"""
    
    def get_price_data(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[PricePoint]:
        """获取价格数据。"""
        ...
    
    def add_price_point(self, point: PricePoint) -> None:
        """添加价格点。"""
        ...


class MockPriceRepository:
    """
    模拟价格数据存储。
    
    生成模拟价格数据用于 MVP 测试。
    """
    
    def __init__(self):
        self._data: dict[str, list[PricePoint]] = {}
    
    def get_price_data(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[PricePoint]:
        """获取价格数据（生成模拟数据）。"""
        
        # 如果没有该 symbol 的数据，生成模拟数据
        if symbol not in self._data:
            self._generate_mock_data(symbol, start_time, end_time)
        
        # 过滤时间范围
        points = [
            p for p in self._data.get(symbol, [])
            if start_time <= p.timestamp <= end_time
        ]
        
        # 如果没有数据，实时生成
        if not points:
            points = self._generate_mock_data(symbol, start_time, end_time)
        
        return sorted(points, key=lambda x: x.timestamp)
    
    def _generate_mock_data(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[PricePoint]:
        """生成模拟价格数据。"""
        import random
        
        points = []
        current_time = start_time
        
        # 基础价格（根据 symbol）
        base_prices = {
            "BDRY": 15.0,  # 航运 ETF
            "USO": 70.0,   # 原油 ETF
            "GLD": 180.0,  # 黄金 ETF
            "SPY": 450.0,  # 标普 500
            "MSCI": 120.0, # MSCI 新兴市场
        }
        base_price = base_prices.get(symbol, 100.0)
        
        # 生成每分钟的价格数据
        current_price = base_price
        while current_time <= end_time:
            # 随机游走
            change = random.gauss(0, 0.001)  # 0.1% 标准差
            current_price = current_price * (1 + change)
            
            # 计算波动率（使用最近 20 个点的标准差）
            volatility = abs(change) * 100  # 简化计算
            
            point = PricePoint(
                timestamp=current_time,
                symbol=symbol,
                price=round(current_price, 2),
                volume=random.randint(1000, 100000),
                volatility=round(volatility, 4),
            )
            points.append(point)
            
            # 下一分钟
            current_time += timedelta(minutes=1)
        
        self._data[symbol] = points
        return points
    
    def add_price_point(self, point: PricePoint) -> None:
        """添加价格点。"""
        if point.symbol not in self._data:
            self._data[point.symbol] = []
        self._data[point.symbol].append(point)
    
    def inject_market_move(
        self,
        symbol: str,
        start_time: datetime,
        duration_minutes: int,
        move_percent: float,
    ) -> None:
        """
        注入市场变动（用于测试）。
        
        Args:
            symbol: 资产代码
            start_time: 开始时间
            duration_minutes: 持续时间
            move_percent: 变动百分比（如 0.05 表示 5%）
        """
        if symbol not in self._data:
            return
        
        points = self._data[symbol]
        for point in points:
            if start_time <= point.timestamp <= start_time + timedelta(minutes=duration_minutes):
                # 应用变动
                progress = (point.timestamp - start_time).total_seconds() / (duration_minutes * 60)
                point.price = point.price * (1 + move_percent * progress)
                point.price = round(point.price, 2)
