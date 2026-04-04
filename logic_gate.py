import re
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    filename='Guard_Trace.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_intercept(reason, payload):
    """
    将拦截原因和相关信息记录到 Guard_Trace.log 文件中
    """
    logging.info(f"Intercepted: {reason}, Payload: {payload}")

def normalize_number(number):
    """
    将不同的数字单位（M, K, 百万, percent等）标准化为数字，支持逗号分隔的数字
    """
    number = number.lower().replace(',', '')  # 移除千位分隔符
    if 'percent' in number:
        return float(number.replace('percent', '').strip())
    elif '%' in number:
        return float(number.replace('%', '').strip())
    elif 'billion' in number:
        return float(number.replace('billion', '').strip()) * 1e9
    elif 'million' in number:
        return float(number.replace('million', '').strip()) * 1e6
    elif 'thousand' in number:
        return float(number.replace('thousand', '').strip()) * 1e3
    elif 'b' in number:
        return float(number.replace('b', '').strip()) * 1e9  # B -> 十亿
    elif 'm' in number:
        return float(number.replace('m', '').strip()) * 1e6  # M -> 百万
    elif 'k' in number:
        return float(number.replace('k', '').strip()) * 1e3  # K -> 千
    else:
        try:
            return float(number)
        except ValueError:
            return None

def check_number_in_context(number, context, source):
    """
    校验数字语义匹配，且source出现在context中
    """
    normalized_target = normalize_number(number)
    if normalized_target is None:
        return False

    # 匹配context中的数字：支持逗号分隔、小数、各类单位、percent
    context_numbers = re.findall(
        r'\$?\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:[KkMmBb%]|thousand|million|billion|percent))?',
        context,
        re.IGNORECASE
    )
    
    number_matched = False
    for ctx_num in context_numbers:
        normalized_ctx = normalize_number(ctx_num.replace('$', ''))
        if normalized_ctx == normalized_target:
            number_matched = True
            break
    
    # 必须同时满足数字匹配 + source匹配
    if not number_matched:
        return False
    return source.lower() in context.lower()

def intercept_payload(payload):
    """
    熔断逻辑：数字或来源不匹配时拦截，仅拦截时写日志
    """
    # 校验USD字段
    if 'USD' in payload:
        if not check_number_in_context(payload['USD'], payload['context'], payload['source']):
            log_intercept("USD number or source mismatch", payload)
            return {"status": "intercepted", "reason": "USD number or source mismatch"}
    
    # 校验percentage字段
    if 'percentage' in payload:
        if not check_number_in_context(payload['percentage'], payload['context'], payload['source']):
            log_intercept("Percentage number or source mismatch", payload)
            return {"status": "intercepted", "reason": "Percentage number or source mismatch"}
    
    return {"status": "valid"}