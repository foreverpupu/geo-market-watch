import re

def normalize_number(number):
    """
    将不同的数字单位（M, K, 百万等）标准化为数字
    """
    number = number.lower()
    if 'm' in number:
        return float(number.replace('m', '').strip()) * 1e6 # 处理 M -> million
    elif 'k' in number:
        return float(number.replace('k', '').strip()) * 1e3 # 处理 K -> thousand
    elif 'million' in number:
        return float(number.replace('million', '').strip()) * 1e6
    elif 'billion' in number:
        return float(number.replace('billion', '').strip()) * 1e9
    else:
        try:
            return float(number)
        except ValueError:
            return None

def check_number_in_context(number, context, source):
    """
    校验数字是否在提供的 context 中，并支持数字单位归一化
    """
    # 提取数字并进行标准化
    normalized_number = normalize_number(number)
    if normalized_number is None:
        return False

    # 检查 context 中是否包含数字
    context_numbers = re.findall(r'\$?\d+[KkMmBb]?', context) # 匹配数字和单位
    for ctx_num in context_numbers:
        if normalize_number(ctx_num) == normalized_number:
            return True
    
    # 检查 source 是否在 context 中
    if source.lower() not in context.lower():
        return False
    return True

def intercept_payload(payload):
    """
    熔断逻辑：拦截不合规的数字和来源。
    """
    # 检查数字和来源
    if 'USD' in payload and not check_number_in_context(payload['USD'], payload['context'], payload['source']):
        return {"status": "intercepted", "reason": "Invalid number or source"}
    
    if 'percentage' in payload and not check_number_in_context(payload['percentage'], payload['context'], payload['source']):
        return {"status": "intercepted", "reason": "Invalid number or source"}
    
    # 在这里增加其他熔断逻辑

    return {"status": "valid"}

# 示例：
payload = {
    "USD": "200M", # 测试百万单位
    "percentage": "25%", # 测试百分比
    "context": "This is a claim from Reuters about the shipment disruption of $200 million.",
    "source": "Reuters"
}

result = intercept_payload(payload)
print(result)
