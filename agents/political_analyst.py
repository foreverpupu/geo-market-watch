"""
Political Analyst Agent

事件提取 Agent 的最小 stub 实现。
"""

from agents.state import GraphState
from agents.state_update import AgentStateUpdate


class PoliticalAnalystAgent:
    """政治分析师 Agent。"""
    
    NAME = "political_analyst"
    
    # 关键词映射到事件类型（支持中英文）
    EVENT_KEYWORDS = {
        # 英文
        "strike": "military_strike",
        "attack": "military_strike",
        "war": "conflict",
        "sanction": "sanction",
        "tariff": "tariff",
        "trade": "trade_disruption",
        "shipping": "shipping_disruption",
        "fertilizer": "commodity_supply_shock",
        "oil": "energy_supply_shock",
        "gas": "energy_supply_shock",
        # 中文
        "打击": "military_strike",
        "袭击": "military_strike",
        "冲突": "conflict",
        "制裁": "sanction",
        "关税": "tariff",
        "贸易": "trade_disruption",
        "航运": "shipping_disruption",
        "海运": "shipping_disruption",
        "化肥": "commodity_supply_shock",
        "尿素": "commodity_supply_shock",
        "石油": "energy_supply_shock",
        "天然气": "energy_supply_shock",
    }
    
    # 地区关键词（支持中英文）
    REGION_KEYWORDS = {
        # 英文
        "middle east": "Middle East",
        "iran": "Middle East",
        "israel": "Middle East",
        "china": "Asia-Pacific",
        "us": "North America",
        "america": "North America",
        "europe": "Europe",
        # 中文
        "中东": "Middle East",
        "伊朗": "Middle East",
        "以色列": "Middle East",
        "中国": "Asia-Pacific",
        "美国": "North America",
        "欧洲": "Europe",
    }
    
    @classmethod
    def run(cls, state: GraphState) -> AgentStateUpdate:
        """
        执行事件提取。
        
        Args:
            state: 当前全局状态
        
        Returns:
            AgentStateUpdate
        """
        # 获取输入文本
        text = state.raw_input_text.lower()
        
        # 提取事件
        events = cls._extract_events(text)
        
        # 计算置信度
        confidence = cls._calculate_confidence(events, text)
        
        # 检查是否应该短路（无事件）
        if len(events) == 0:
            return AgentStateUpdate.create_short_circuit(
                cls.NAME,
                "No political events detected in text",
                {"events": [], "confidence": 0.0}
            )
        
        return AgentStateUpdate(
            agent_name=cls.NAME,
            outputs={
                "events": events,
                "confidence": confidence,
            },
            confidence=confidence,
            completed=True,
        )
    
    @classmethod
    def _extract_events(cls, text: str) -> list:
        """从文本中提取事件。"""
        events = []
        
        for keyword, event_type in cls.EVENT_KEYWORDS.items():
            if keyword in text:
                # 提取实体
                entities = cls._extract_entities(text)
                
                # 确定地区
                region = cls._extract_region(text)
                
                # 确定严重程度
                severity = cls._determine_severity(text, event_type)
                
                event = {
                    "event_type": event_type,
                    "entities": entities,
                    "region": region,
                    "impact_severity": severity,
                    "confidence": 0.7,  # 基于关键词匹配的默认置信度
                }
                
                # 避免重复
                if not any(e["event_type"] == event_type for e in events):
                    events.append(event)
                    print(f"    Found event: {event_type} (keyword: {keyword})")
        
        return events
    
    @classmethod
    def _extract_entities(cls, text: str) -> list:
        """提取实体。"""
        entities = []
        
        # 检查地区实体
        for keyword, region in cls.REGION_KEYWORDS.items():
            if keyword in text and region not in entities:
                entities.append(region)
        
        # 检查商品实体（中英文）
        commodities = ["fertilizer", "oil", "gas", "wheat", "corn", "urea",
                       "化肥", "尿素", "石油", "天然气", "小麦", "玉米"]
        for comm in commodities:
            if comm in text and comm not in entities:
                entities.append(comm)
        
        return entities[:5]  # 最多5个实体
    
    @classmethod
    def _extract_region(cls, text: str) -> str:
        """提取地区。"""
        for keyword, region in cls.REGION_KEYWORDS.items():
            if keyword in text:
                return region
        return "Global"
    
    @classmethod
    def _determine_severity(cls, text: str, event_type: str) -> str:
        """确定严重程度。"""
        high_severity_keywords = ["war", "strike", "attack", "crisis", "shortage",
                                   "战争", "打击", "袭击", "危机", "短缺"]
        
        for keyword in high_severity_keywords:
            if keyword in text:
                return "high"
        
        if event_type in ["military_strike", "energy_supply_shock"]:
            return "high"
        
        return "medium"
    
    @classmethod
    def _calculate_confidence(cls, events: list, text: str) -> float:
        """计算整体置信度。"""
        if not events:
            return 0.0
        
        # 基于事件数量和文本长度计算
        base_confidence = 0.6
        
        # 多个事件增加置信度
        event_bonus = min(len(events) * 0.05, 0.2)
        
        # 文本长度因子（太短或太长都降低置信度）
        text_length = len(text.split())
        if 20 <= text_length <= 200:
            length_factor = 0.1
        else:
            length_factor = 0.0
        
        return min(base_confidence + event_bonus + length_factor, 0.95)
