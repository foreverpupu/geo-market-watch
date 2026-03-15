"""
Replay Engine

Step 5 orchestrator，统一执行回放和评估。
"""

import uuid
from datetime import datetime
from v2.config import ReplayConfig, DEFAULT_REPLAY_CONFIG
from v2.domain.models import Signal, ReplayResult, EvaluationResult
from v2.repositories.price_repository import PriceRepository, MockPriceRepository
from v2.services.replay_core import build_event_timeline, calculate_lead_time
from v2.services.signal_usefulness import evaluate_signal_usefulness


def _generate_replay_id() -> str:
    """生成回放 ID。"""
    return f"REPLAY_{uuid.uuid4().hex[:12].upper()}"


def run_signal_replay(
    signal: Signal,
    symbols: list[str],
    price_repository: PriceRepository | None = None,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
    now: datetime | None = None,
) -> ReplayResult:
    """
    执行信号回放。
    
    流程：
    1. 构建事件时间线
    2. 计算领先时间
    3. 评估信号效用度
    4. 生成回放结果
    
    Args:
        signal: 信号
        symbols: 相关资产代码
        price_repository: 价格数据存储（可选）
        config: 配置
        now: 当前时间
        
    Returns:
        ReplayResult
    """
    if now is None:
        now = datetime.now()
    
    if price_repository is None:
        price_repository = MockPriceRepository()
    
    # Step 1: 构建事件时间线
    timeline = build_event_timeline(signal, symbols, price_repository, config, now)
    
    # Step 2: 计算领先时间
    lead_time = calculate_lead_time(signal, timeline, config)
    
    # Step 3: 评估信号效用度
    metrics = evaluate_signal_usefulness(signal, timeline, lead_time, config)
    
    # Step 4: 生成回放结果
    return ReplayResult(
        replay_id=_generate_replay_id(),
        signal_id=signal.signal_id if hasattr(signal, 'signal_id') else "unknown",
        event_id=signal.event_id if hasattr(signal, 'event_id') else "unknown",
        prompt_version=config.prompt_version,
        model_config_id=config.model_config_id,
        timeline=timeline,
        metrics=metrics,
        generated_at=now,
    )


def run_batch_evaluation(
    signals: list[Signal],
    symbol_mapping: dict[str, list[str]],  # signal_id -> symbols
    price_repository: PriceRepository | None = None,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
    now: datetime | None = None,
) -> EvaluationResult:
    """
    批量评估多个信号。
    
    Args:
        signals: 信号列表
        symbol_mapping: 信号到资产的映射
        price_repository: 价格数据存储（可选）
        config: 配置
        now: 当前时间
        
    Returns:
        EvaluationResult
    """
    if now is None:
        now = datetime.now()
    
    if price_repository is None:
        price_repository = MockPriceRepository()
    
    results = []
    for signal in signals:
        symbols = symbol_mapping.get(signal.signal_id, ["SPY"])
        replay = run_signal_replay(signal, symbols, price_repository, config, now)
        results.append(replay)
    
    # 计算汇总指标
    total = len(results)
    high_count = sum(1 for r in results if r.metrics.usefulness_rating == "high")
    medium_count = sum(1 for r in results if r.metrics.usefulness_rating == "medium")
    low_count = sum(1 for r in results if r.metrics.usefulness_rating == "low")
    false_alarm_count = sum(1 for r in results if r.metrics.is_false_alarm)
    
    # 平均领先时间
    lead_times = [r.metrics.lead_time_minutes for r in results if r.metrics.lead_time_minutes is not None]
    avg_lead_time = sum(lead_times) / len(lead_times) if lead_times else None
    
    # 平均预测误差
    errors = [r.metrics.prediction_error for r in results if r.metrics.prediction_error is not None]
    avg_error = sum(errors) / len(errors) if errors else None
    
    # 波动率准确率
    volatility_signals = [r for r in results if r.metrics.event_category == "volatility"]
    volatility_correct = sum(1 for r in volatility_signals if r.metrics.volatility_spike_match)
    volatility_accuracy = volatility_correct / len(volatility_signals) if volatility_signals else 0.0
    
    # 方向性准确率
    directionality_signals = [r for r in results if r.metrics.event_category == "directionality"]
    directionality_correct = sum(1 for r in directionality_signals if not r.metrics.is_false_alarm)
    directionality_accuracy = directionality_correct / len(directionality_signals) if directionality_signals else 0.0
    
    return EvaluationResult(
        total_signals=total,
        high_usefulness_count=high_count,
        medium_usefulness_count=medium_count,
        low_usefulness_count=low_count,
        false_alarm_count=false_alarm_count,
        avg_lead_time_minutes=avg_lead_time,
        avg_prediction_error=avg_error,
        volatility_accuracy=round(volatility_accuracy, 4),
        directionality_accuracy=round(directionality_accuracy, 4),
    )
