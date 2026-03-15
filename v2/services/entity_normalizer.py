"""
Entity Normalizer

实体名标准化、alias 映射、去重。
"""

import re
from typing import List


# 实体别名映射表
ENTITY_ALIAS_MAP = {
    "houthi rebels": "houthis",
    "ansar allah": "houthis",
    "red sea route": "red sea",
    "suez shipping lane": "suez canal",
    "container shipping": "container ships",
    "shipping container": "container ships",
}


def normalize_entity_name(name: str) -> str:
    """
    标准化单个实体名。
    
    步骤：
    1. 去首尾空格
    2. 转小写
    3. 多空格压缩
    4. alias 映射
    
    Args:
        name: 原始实体名
        
    Returns:
        标准化后的实体名
    """
    # 去首尾空格并转小写
    normalized = name.strip().lower()
    
    # 多空格压缩
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # alias 映射
    normalized = ENTITY_ALIAS_MAP.get(normalized, normalized)
    
    return normalized


def normalize_entities(names: List[str]) -> List[str]:
    """
    批量标准化实体名列表。
    
    步骤：
    1. 逐个标准化
    2. 去空字符串
    3. 去重
    4. 排序（保证 deterministic）
    
    Args:
        names: 实体名列表
        
    Returns:
        标准化并排序后的实体名列表
    
    Example:
        >>> normalize_entities([" Red Sea ", "Houthi Rebels", "red sea", "Ansar Allah"])
        ["houthis", "red sea"]
    """
    # 逐个标准化
    normalized = [normalize_entity_name(name) for name in names]
    
    # 去空字符串
    normalized = [n for n in normalized if n]
    
    # 去重并保持顺序（使用 dict.fromkeys）
    seen = set()
    unique = []
    for n in normalized:
        if n not in seen:
            seen.add(n)
            unique.append(n)
    
    # 排序
    return sorted(unique)
