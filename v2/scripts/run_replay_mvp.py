"""
Replay & Evaluation MVP Runner

演示回放和评估功能。
"""

from datetime import datetime, timedelta
from v2.config import DEFAULT_REPLAY_CONFIG
from v2.domain.models import Signal, PricePoint
from v2.domain.enums import SignalClass
from v2.repositories.price_repository import MockPriceRepository
from v2.services.replay_engine import run_signal_replay, run_batch_evaluation


def run_replay_demo():
    """运行回放演示。"""
    print("=" * 70)
    print("Geo Market Watch V2 - Replay & Evaluation MVP Demo")
    print("=" * 70)
    print()
    
    now = datetime(2024, 1, 15, 12, 0, 0)
    config = DEFAULT_REPLAY_CONFIG
    
    # 初始化价格存储
    price_repo = MockPriceRepository()
    
    # 场景 1: 航运中断信号（有市场反应）
    print("-" * 70)
    print("Scenario 1: Shipping Disruption Signal with Market Reaction")
    print("-" * 70)
    
    signal1 = Signal(
        signal_id="SIG_001",
        event_id="EVT_shipping_001",
        signal_class=SignalClass.HIGH_PRIORITY.value,
        rank_score=0.85,
        severity_score=0.70,
        market_relevance_score=0.80,
        novelty_score=0.75,
        confidence_score=0.68,
        breadth_score=0.60,
        urgency_score=0.90,
        watchlist_match_score=0.0,
        assigned_queue="triage",
        status="generated",
        summary_text="Red Sea shipping disruption",
        reasoning_trace="High priority shipping event",
        generated_at=now,
    )
    
    # 注入市场反应（航运 ETF 上涨 3%）
    price_repo.inject_market_move("BDRY", now, 60, 0.03)
    
    result1 = run_signal_replay(signal1, ["BDRY", "USO"], price_repo, config, now)
    
    print(f"Signal: {result1.signal_id}")
    print(f"Event: {result1.event_id}")
    print(f"Prompt Version: {result1.prompt_version}")
    print(f"Model Config: {result1.model_config_id}")
    print()
    print("Timeline:")
    print(f"  Signal generated at: {result1.timeline.signal_generated_at}")
    print(f"  Market reaction detected at: {result1.timeline.market_reaction_detected_at}")
    print(f"  Market move direction: {result1.timeline.market_move_direction}")
    print(f"  Market move magnitude: {result1.timeline.market_move_magnitude}")
    print()
    print("Usefulness Metrics:")
    print(f"  Usefulness Score: {result1.metrics.usefulness_score}")
    print(f"  Usefulness Rating: {result1.metrics.usefulness_rating}")
    print(f"  Lead Time (minutes): {result1.metrics.lead_time_minutes}")
    print(f"  Prediction Error: {result1.metrics.prediction_error}")
    print(f"  Is False Alarm: {result1.metrics.is_false_alarm}")
    print(f"  Volatility Spike Match: {result1.metrics.volatility_spike_match}")
    print(f"  Event Category: {result1.metrics.event_category}")
    print()
    
    # 场景 2: 误报信号（无市场反应）
    print("-" * 70)
    print("Scenario 2: False Alarm Signal (No Market Reaction)")
    print("-" * 70)
    
    signal2 = Signal(
        signal_id="SIG_002",
        event_id="EVT_labor_001",
        signal_class=SignalClass.LOW_SIGNAL.value,
        rank_score=0.35,
        severity_score=0.40,
        market_relevance_score=0.30,
        novelty_score=0.20,
        confidence_score=0.50,
        breadth_score=0.20,
        urgency_score=0.30,
        watchlist_match_score=0.0,
        assigned_queue="triage",
        status="generated",
        summary_text="Local labor strike",
        reasoning_trace="Low priority local event",
        generated_at=now,
    )
    
    # 不注入市场反应
    result2 = run_signal_replay(signal2, ["SPY"], price_repo, config, now)
    
    print(f"Signal: {result2.signal_id}")
    print(f"Usefulness Rating: {result2.metrics.usefulness_rating}")
    print(f"Is False Alarm: {result2.metrics.is_false_alarm}")
    print()
    
    # 场景 3: 批量评估
    print("-" * 70)
    print("Scenario 3: Batch Evaluation")
    print("-" * 70)
    
    signals = [signal1, signal2]
    symbol_mapping = {
        "SIG_001": ["BDRY", "USO"],
        "SIG_002": ["SPY"],
    }
    
    evaluation = run_batch_evaluation(signals, symbol_mapping, price_repo, config, now)
    
    print(f"Total Signals: {evaluation.total_signals}")
    print(f"High Usefulness: {evaluation.high_usefulness_count}")
    print(f"Medium Usefulness: {evaluation.medium_usefulness_count}")
    print(f"Low Usefulness: {evaluation.low_usefulness_count}")
    print(f"False Alarms: {evaluation.false_alarm_count}")
    print(f"Avg Lead Time (minutes): {evaluation.avg_lead_time_minutes:.1f}" if evaluation.avg_lead_time_minutes else "  Avg Lead Time: N/A")
    print(f"Avg Prediction Error: {evaluation.avg_prediction_error:.4f}" if evaluation.avg_prediction_error else "  Avg Prediction Error: N/A")
    print(f"Volatility Accuracy: {evaluation.volatility_accuracy:.2%}")
    print(f"Directionality Accuracy: {evaluation.directionality_accuracy:.2%}")
    print()
    
    # 场景 4: 波动率事件评估
    print("-" * 70)
    print("Scenario 4: Volatility Event (Military Exercise)")
    print("-" * 70)
    
    signal3 = Signal(
        signal_id="SIG_003",
        event_id="EVT_military_001",
        signal_class=SignalClass.HIGH_PRIORITY.value,
        rank_score=0.80,
        severity_score=0.85,
        market_relevance_score=0.70,
        novelty_score=0.60,
        confidence_score=0.75,
        breadth_score=0.50,
        urgency_score=0.80,
        watchlist_match_score=0.0,
        assigned_queue="triage",
        status="generated",
        summary_text="Military exercise near Taiwan",
        reasoning_trace="Volatility event",
        generated_at=now,
    )
    
    # 注入波动率增加
    # 先生成基础数据
    _ = price_repo.get_price_data("GLD", now - timedelta(hours=2), now + timedelta(hours=4))
    # 然后注入高波动
    for point in price_repo._data.get("GLD", []):
        if now <= point.timestamp <= now + timedelta(hours=2):
            point.volatility = point.volatility * 3.0 if point.volatility else 0.05
    
    result3 = run_signal_replay(signal3, ["GLD", "SPY"], price_repo, config, now)
    
    print(f"Signal: {result3.signal_id}")
    print(f"Event Category: {result3.metrics.event_category}")
    print(f"Volatility Spike Match: {result3.metrics.volatility_spike_match}")
    print(f"Usefulness Rating: {result3.metrics.usefulness_rating}")
    print()
    
    # 最终摘要
    print("=" * 70)
    print("Final Summary")
    print("=" * 70)
    print("\nReplay system features demonstrated:")
    print("  ✓ Event timeline reconstruction")
    print("  ✓ Lead time calculation (T_market_move - T_signal_generated)")
    print("  ✓ Signal usefulness scoring")
    print("  ✓ False alarm detection")
    print("  ✓ Volatility spike matching")
    print("  ✓ Event category classification (directionality vs volatility)")
    print("  ✓ Batch evaluation with aggregate metrics")
    print("  ✓ Logic versioning (prompt_version, model_config_id)")


if __name__ == "__main__":
    run_replay_demo()
