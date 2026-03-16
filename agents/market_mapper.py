"""
Market Mapper Agent

市场映射 Agent 的最小 stub 实现。
"""

from agents.state import GraphState
from agents.state_update import AgentStateUpdate


class MarketMapperAgent:
    """市场映射 Agent。"""
    
    NAME = "market_mapper"
    
    # 事件类型到资产的映射
    EVENT_ASSET_MAP = {
        "military_strike": [
            {"symbol": "BDRY", "asset_type": "etf", "direction": "long"},
            {"symbol": "USO", "asset_type": "etf", "direction": "long"},
        ],
        "shipping_disruption": [
            {"symbol": "BDRY", "asset_type": "etf", "direction": "long"},
            {"symbol": "CMRE", "asset_type": "stock", "direction": "mixed"},
        ],
        "commodity_supply_shock": [
            {"symbol": "DBA", "asset_type": "etf", "direction": "long"},
            {"symbol": "CF", "asset_type": "stock", "direction": "long"},
            {"symbol": "NTR", "asset_type": "stock", "direction": "long"},
        ],
        "energy_supply_shock": [
            {"symbol": "USO", "asset_type": "etf", "direction": "long"},
            {"symbol": "UNG", "asset_type": "etf", "direction": "long"},
            {"symbol": "XLE", "asset_type": "etf", "direction": "long"},
        ],
        "sanction": [
            {"symbol": "RSX", "asset_type": "etf", "direction": "short"},
        ],
        "conflict": [
            {"symbol": "GLD", "asset_type": "etf", "direction": "long"},
            {"symbol": "VIX", "asset_type": "index", "direction": "long"},
        ],
    }
    
    # 地区到资产的映射
    REGION_ASSET_MAP = {
        "Middle East": [
            {"symbol": "USO", "asset_type": "etf", "rationale": "Middle East oil exposure"},
        ],
        "Asia-Pacific": [
            {"symbol": "AAXJ", "asset_type": "etf", "rationale": "Asia ex-Japan exposure"},
        ],
    }
    
    @classmethod
    def run(cls, state: GraphState) -> AgentStateUpdate:
        """
        执行市场映射。
        
        Args:
            state: 当前全局状态
        
        Returns:
            AgentStateUpdate
        """
        # 获取事件
        events = state.political_analyst__events
        
        # 检查是否有事件可映射
        if not events:
            return AgentStateUpdate.create_short_circuit(
                cls.NAME,
                "No events to map",
                {"candidates": [], "mapping_confidence": 0.0}
            )
        
        # 映射候选
        candidates = cls._map_events_to_candidates(events)
        
        # 计算映射置信度
        mapping_confidence = cls._calculate_mapping_confidence(
            candidates, events, state
        )
        
        # 检查置信度短路（包括无候选或置信度太低的情况）
        if mapping_confidence < 0.3 or not candidates:
            return AgentStateUpdate.create_short_circuit(
                cls.NAME,
                f"Mapping confidence too low: {mapping_confidence}",
                {"candidates": candidates, "mapping_confidence": mapping_confidence}
            )
        
        return AgentStateUpdate(
            agent_name=cls.NAME,
            outputs={
                "candidates": candidates,
                "mapping_confidence": mapping_confidence,
            },
            confidence=mapping_confidence,
            completed=True,
        )
    
    @classmethod
    def _map_events_to_candidates(cls, events: list) -> list:
        """将事件映射到候选资产。"""
        candidates = []
        seen_symbols = set()
        
        for event in events:
            event_type = event.get("event_type", "")
            region = event.get("region", "")
            
            # 基于事件类型映射
            assets = cls.EVENT_ASSET_MAP.get(event_type, [])
            for asset in assets:
                symbol = asset["symbol"]
                if symbol not in seen_symbols:
                    candidate = {
                        "symbol": symbol,
                        "asset_type": asset["asset_type"],
                        "direction": asset["direction"],
                        "time_horizon": cls._determine_time_horizon(event),
                        "confidence": cls._calculate_candidate_confidence(event, asset),
                        "rationale": cls._generate_rationale(event, asset),
                    }
                    candidates.append(candidate)
                    seen_symbols.add(symbol)
            
            # 基于地区映射
            region_assets = cls.REGION_ASSET_MAP.get(region, [])
            for asset in region_assets:
                symbol = asset["symbol"]
                if symbol not in seen_symbols:
                    candidate = {
                        "symbol": symbol,
                        "asset_type": asset["asset_type"],
                        "direction": "long",
                        "time_horizon": "weeks",
                        "confidence": 0.6,
                        "rationale": asset.get("rationale", "Regional exposure"),
                    }
                    candidates.append(candidate)
                    seen_symbols.add(symbol)
        
        return candidates[:5]  # 最多5个候选
    
    @classmethod
    def _determine_time_horizon(cls, event: dict) -> str:
        """确定时间窗口。"""
        severity = event.get("impact_severity", "medium")
        event_type = event.get("event_type", "")
        
        if severity == "high":
            return "weeks"
        elif event_type in ["military_strike", "energy_supply_shock"]:
            return "weeks"
        else:
            return "days"
    
    @classmethod
    def _calculate_candidate_confidence(cls, event: dict, asset: dict) -> float:
        """计算候选置信度。"""
        base_confidence = 0.6
        
        # 事件置信度影响
        event_confidence = event.get("confidence", 0.7)
        
        # 严重程度加成
        if event.get("impact_severity") == "high":
            severity_bonus = 0.1
        else:
            severity_bonus = 0.0
        
        return min(base_confidence * event_confidence + severity_bonus, 0.9)
    
    @classmethod
    def _generate_rationale(cls, event: dict, asset: dict) -> str:
        """生成候选理由。"""
        event_type = event.get("event_type", "event")
        symbol = asset["symbol"]
        direction = asset["direction"]
        
        rationales = {
            "military_strike": f"{symbol} benefits from energy/transport disruption",
            "shipping_disruption": f"{symbol} exposed to shipping rate volatility",
            "commodity_supply_shock": f"{symbol} positioned for supply shortage",
            "energy_supply_shock": f"{symbol} tracks energy price movement",
            "sanction": f"{symbol} impacted by trade restrictions",
        }
        
        return rationales.get(event_type, f"{symbol} mapped to {event_type}")
    
    @classmethod
    def _calculate_mapping_confidence(cls, candidates: list, events: list, state: GraphState) -> float:
        """计算整体映射置信度。"""
        if not candidates:
            return 0.0
        
        # 基于候选平均置信度
        avg_candidate_confidence = sum(c["confidence"] for c in candidates) / len(candidates)
        
        # 事件分析器置信度
        analyst_confidence = state.political_analyst__confidence
        
        # 映射覆盖率
        coverage = min(len(candidates) / len(events), 1.0) if events else 0.0
        
        return avg_candidate_confidence * 0.4 + analyst_confidence * 0.4 + coverage * 0.2
