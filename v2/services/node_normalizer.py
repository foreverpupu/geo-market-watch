"""
Node Normalizer

统一 graph edge、template target、event entity 的命名标准化。
复用 Step 1 的 entity normalizer 逻辑。
"""

from v2.services.entity_normalizer import normalize_entity_name


def normalize_node_id(node_id: str) -> str:
    """
    标准化节点 ID。
    
    格式: <type>:<id>
    例如: route:red_sea, sector:container_shipping
    
    Args:
        node_id: 原始节点 ID
        
    Returns:
        标准化后的节点 ID
    """
    if ":" not in node_id:
        # 如果没有类型前缀，假设是 theme 类型
        return f"theme:{normalize_entity_name(node_id)}"
    
    node_type, node_name = node_id.split(":", 1)
    normalized_name = normalize_entity_name(node_name)
    return f"{node_type}:{normalized_name}"


def normalize_target_id(target_type: str, target_id: str) -> str:
    """
    标准化 target ID。
    
    Args:
        target_type: 目标类型
        target_id: 目标 ID
        
    Returns:
        标准化后的 target ID
    """
    normalized_id = normalize_entity_name(target_id)
    return f"{target_type}:{normalized_id}"


def parse_node_id(node_id: str) -> tuple[str, str]:
    """
    解析节点 ID 为 (type, id) 元组。
    
    Args:
        node_id: 节点 ID
        
    Returns:
        (type, id) 元组
    """
    if ":" not in node_id:
        return "theme", normalize_entity_name(node_id)
    
    node_type, node_name = node_id.split(":", 1)
    return node_type, normalize_entity_name(node_name)


def normalize_entity_to_node_id(entity: str, default_type: str = "theme") -> str:
    """
    将事件中的 entity 转换为标准化的 node ID。
    
    Args:
        entity: 实体名称
        default_type: 默认类型
        
    Returns:
        标准化节点 ID
    """
    normalized = normalize_entity_name(entity)
    
    # 尝试推断类型
    type_hints = {
        "route": ["route", "canal", "strait", "passage"],
        "country": ["china", "usa", "egypt", "germany", "japan"],
        "commodity": ["oil", "gas", "gallium", "graphite", "lithium", "copper"],
        "sector": ["shipping", "logistics", "energy", "technology", "finance"],
    }
    
    for node_type, hints in type_hints.items():
        if any(hint in normalized for hint in hints):
            return f"{node_type}:{normalized}"
    
    return f"{default_type}:{normalized}"
