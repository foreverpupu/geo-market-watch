"""
Geo Market Watch v6.4 — Performance Engine

Tracks paper trading performance for approved trade ideas.
"""

import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List
from pathlib import Path
import sys

# Import lifecycle engine for event recording
try:
    from .lifecycle_engine import record_lifecycle_event
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent))
    from lifecycle_engine import record_lifecycle_event


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _parse_iso_time(time_str: str) -> datetime:
    """Parse ISO format time string to datetime."""
    # Handle various ISO formats
    time_str = time_str.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(time_str)
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")


def _validate_prices(entry_price: float, close_price: Optional[float] = None) -> Tuple[bool, str]:
    """Validate price values."""
    if entry_price <= 0:
        return False, "Entry price must be positive"
    if close_price is not None and close_price <= 0:
        return False, "Close price must be positive"
    return True, ""


def _validate_times(entry_time: str, close_time: Optional[str] = None) -> Tuple[bool, str]:
    """Validate time values."""
    try:
        entry_dt = _parse_iso_time(entry_time)
    except ValueError as e:
        return False, f"Invalid entry time: {e}"
    
    if close_time:
        try:
            close_dt = _parse_iso_time(close_time)
        except ValueError as e:
            return False, f"Invalid close time: {e}"
        
        if close_dt < entry_dt:
            return False, "Close time must not be earlier than entry time"
    
    return True, ""


def _calculate_holding_days(entry_time: str, close_time: str) -> int:
    """Calculate holding period in whole days."""
    entry_dt = _parse_iso_time(entry_time)
    close_dt = _parse_iso_time(close_time)
    delta = close_dt - entry_dt
    return max(0, delta.days)


def _calculate_return(direction: str, entry_price: float, close_price: float) -> float:
    """Calculate return percentage based on direction."""
    if direction == 'short':
        return ((entry_price - close_price) / entry_price) * 100
    else:  # long or monitor (treat as long for calculation)
        return ((close_price - entry_price) / entry_price) * 100


def _classify_outcome(return_pct: float) -> str:
    """
    Classify trade outcome based on return.
    
    Classification buckets:
    - strong_positive: > 10%
    - positive: > 5% to 10%
    - flat: -5% to 5%
    - negative: -10% to -5%
    - strong_negative: < -10%
    """
    if return_pct > 10:
        return 'strong_positive'
    elif return_pct > 5:
        return 'positive'
    elif return_pct < -10:
        return 'strong_negative'
    elif return_pct < -5:
        return 'negative'
    else:
        return 'flat'


def _is_approved_for_tracking(db_path: str, trade_idea_id: str) -> Tuple[bool, str, Optional[Dict]]:
    """Check if trade idea is approved for tracking."""
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT trade_idea_id, direction, analyst_status, approval_status
            FROM trade_ideas
            WHERE trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}", None
        
        idea = dict(row)
        
        # Check approval status
        if idea['analyst_status'] != 'approved' and idea['approval_status'] != 'approved':
            return False, f"Trade idea not approved for tracking (status: {idea['analyst_status']})", idea
        
        return True, "", idea
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}", None


def start_tracking(
    db_path: str,
    trade_idea_id: str,
    entry_price: float,
    entry_time: str,
    notes: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Start tracking performance for an approved trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        entry_price: Entry price (must be positive)
        entry_time: Entry timestamp (ISO format)
        notes: Optional tracking notes
    
    Returns:
        Tuple of (success, message_or_error)
    """
    # Validate approval status
    is_approved, error, idea = _is_approved_for_tracking(db_path, trade_idea_id)
    if not is_approved:
        return False, error
    
    # Validate prices
    valid, error = _validate_prices(entry_price)
    if not valid:
        return False, error
    
    # Validate times
    valid, error = _validate_times(entry_time)
    if not valid:
        return False, error
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Check if performance record already exists
        cursor.execute(
            "SELECT performance_id, tracking_status FROM trade_idea_performance WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        existing = cursor.fetchone()
        
        now = datetime.now(timezone.utc).isoformat()
        
        if existing:
            # Update existing record only if not already tracking
            if existing['tracking_status'] == 'tracking':
                conn.close()
                return False, "Tracking already active for this idea. Use update_price_reference to modify entry."
            
            cursor.execute(
                """
                UPDATE trade_idea_performance
                SET tracking_status = 'tracking',
                    entry_price = ?,
                    entry_time = ?,
                    notes = COALESCE(?, notes),
                    updated_at = ?
                WHERE trade_idea_id = ?
                """,
                (entry_price, entry_time, notes, now, trade_idea_id)
            )
        else:
            # Create new performance record
            performance_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO trade_idea_performance (
                    performance_id, trade_idea_id, tracking_status,
                    entry_price, entry_time, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (performance_id, trade_idea_id, 'tracking', entry_price, entry_time, notes, now, now)
            )
        
        conn.commit()
        conn.close()
        
        # Record lifecycle event
        lifecycle_reason = f"Entry price: {entry_price}, Time: {entry_time}"
        if notes:
            lifecycle_reason += f" - {notes}"
        record_lifecycle_event(db_path, trade_idea_id, "tracking_started", lifecycle_reason)
        
        return True, f"Tracking started for {trade_idea_id} at {entry_price}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def close_tracking(
    db_path: str,
    trade_idea_id: str,
    close_price: float,
    close_time: str,
    notes: Optional[str] = None
) -> Tuple[bool, str, Optional[Dict]]:
    """
    Close tracking for a trade idea and compute performance.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        close_price: Close price (must be positive)
        close_time: Close timestamp (ISO format)
        notes: Optional close notes
    
    Returns:
        Tuple of (success, message, performance_dict)
    """
    # Validate close price
    if close_price <= 0:
        return False, "Close price must be positive", None
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Get current tracking record
        cursor.execute(
            """
            SELECT p.*, t.direction
            FROM trade_idea_performance p
            JOIN trade_ideas t ON p.trade_idea_id = t.trade_idea_id
            WHERE p.trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "No tracking record found. Start tracking first.", None
        
        perf = dict(row)
        
        if perf['tracking_status'] != 'tracking':
            conn.close()
            return False, f"Tracking not active (status: {perf['tracking_status']})", None
        
        if not perf['entry_price'] or not perf['entry_time']:
            conn.close()
            return False, "Missing entry reference", None
        
        # Validate times
        valid, error = _validate_times(perf['entry_time'], close_time)
        if not valid:
            conn.close()
            return False, error, None
        
        # Calculate performance
        direction = perf.get('direction', 'long')
        return_pct = _calculate_return(direction, perf['entry_price'], close_price)
        holding_days = _calculate_holding_days(perf['entry_time'], close_time)
        outcome = _classify_outcome(return_pct)
        
        # Calculate alpha spread if benchmark exists
        alpha_spread = None
        if perf.get('benchmark_return_pct') is not None:
            alpha_spread = return_pct - perf['benchmark_return_pct']
        
        now = datetime.now(timezone.utc).isoformat()
        
        # Update performance record
        cursor.execute(
            """
            UPDATE trade_idea_performance
            SET tracking_status = 'closed',
                close_price = ?,
                close_time = ?,
                return_pct = ?,
                alpha_spread_pct = ?,
                outcome = ?,
                holding_period_days = ?,
                notes = COALESCE(?, notes),
                updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (close_price, close_time, return_pct, alpha_spread, outcome, 
             holding_days, notes, now, trade_idea_id)
        )
        
        conn.commit()
        conn.close()
        
        # Record lifecycle event
        lifecycle_reason = f"Close price: {close_price}, Return: {return_pct:.2f}%, Outcome: {outcome}"
        if notes:
            lifecycle_reason += f" - {notes}"
        record_lifecycle_event(db_path, trade_idea_id, "tracking_closed", lifecycle_reason)
        
        result = {
            'trade_idea_id': trade_idea_id,
            'return_pct': return_pct,
            'outcome': outcome,
            'holding_period_days': holding_days,
            'entry_price': perf['entry_price'],
            'close_price': close_price
        }
        
        return True, f"Tracking closed. Return: {return_pct:.2f}% ({outcome})", result
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}", None


def update_benchmark_return(
    db_path: str,
    trade_idea_id: str,
    benchmark_return_pct: float
) -> Tuple[bool, str]:
    """
    Update benchmark return for a tracked idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        benchmark_return_pct: Benchmark return percentage
    
    Returns:
        Tuple of (success, message)
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Check if record exists
        cursor.execute(
            "SELECT return_pct FROM trade_idea_performance WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "No tracking record found"
        
        # Calculate alpha spread if we have return
        alpha_spread = None
        if row['return_pct'] is not None:
            alpha_spread = row['return_pct'] - benchmark_return_pct
        
        now = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            """
            UPDATE trade_idea_performance
            SET benchmark_return_pct = ?,
                alpha_spread_pct = ?,
                updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (benchmark_return_pct, alpha_spread, now, trade_idea_id)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Benchmark return updated: {benchmark_return_pct:.2f}%"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def recompute_performance(db_path: str, trade_idea_id: str) -> Optional[Dict]:
    """
    Recompute performance metrics for a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
    
    Returns:
        Performance dict or None if not found
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT p.*, t.direction
            FROM trade_idea_performance p
            JOIN trade_ideas t ON p.trade_idea_id = t.trade_idea_id
            WHERE p.trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        perf = dict(row)
        
        # Only recompute if we have both entry and close
        if perf.get('entry_price') and perf.get('close_price') and perf.get('entry_time') and perf.get('close_time'):
            direction = perf.get('direction', 'long')
            return_pct = _calculate_return(direction, perf['entry_price'], perf['close_price'])
            holding_days = _calculate_holding_days(perf['entry_time'], perf['close_time'])
            outcome = _classify_outcome(return_pct)
            
            alpha_spread = None
            if perf.get('benchmark_return_pct') is not None:
                alpha_spread = return_pct - perf['benchmark_return_pct']
            
            now = datetime.now(timezone.utc).isoformat()
            
            cursor.execute(
                """
                UPDATE trade_idea_performance
                SET return_pct = ?,
                    alpha_spread_pct = ?,
                    outcome = ?,
                    holding_period_days = ?,
                    updated_at = ?
                WHERE trade_idea_id = ?
                """,
                (return_pct, alpha_spread, outcome, holding_days, now, trade_idea_id)
            )
            
            conn.commit()
            
            perf['return_pct'] = return_pct
            perf['alpha_spread_pct'] = alpha_spread
            perf['outcome'] = outcome
            perf['holding_period_days'] = holding_days
        
        conn.close()
        return perf
    
    except sqlite3.Error as e:
        return None


def recompute_recent_performance(db_path: str, limit: int = 50) -> Dict:
    """
    Recompute performance for recent trade ideas.
    
    Args:
        db_path: Path to the SQLite database
        limit: Maximum number of ideas to recompute
    
    Returns:
        Summary dict with counts
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT p.trade_idea_id
            FROM trade_idea_performance p
            ORDER BY p.updated_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        updated = 0
        failed = 0
        
        for row in rows:
            result = recompute_performance(db_path, row['trade_idea_id'])
            if result:
                updated += 1
            else:
                failed += 1
        
        return {
            'total': len(rows),
            'updated': updated,
            'failed': failed
        }
    
    except sqlite3.Error as e:
        return {'error': str(e)}


def get_performance_record(db_path: str, trade_idea_id: str) -> Optional[Dict]:
    """
    Get performance record for a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
    
    Returns:
        Performance dict or None if not found
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT p.*, t.company_name, t.ticker, t.direction
            FROM trade_idea_performance p
            JOIN trade_ideas t ON p.trade_idea_id = t.trade_idea_id
            WHERE p.trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    except sqlite3.Error as e:
        return None


def list_tracked_ideas(
    db_path: str,
    status_filter: Optional[str] = None
) -> List[Dict]:
    """
    List tracked trade ideas with performance summary.
    
    Args:
        db_path: Path to the SQLite database
        status_filter: Optional filter by tracking_status
    
    Returns:
        List of tracked ideas with performance
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                t.company_name, t.ticker, t.direction,
                p.tracking_status, p.entry_price, p.close_price,
                p.return_pct, p.outcome, p.holding_period_days,
                p.trade_idea_id
            FROM trade_idea_performance p
            JOIN trade_ideas t ON p.trade_idea_id = t.trade_idea_id
        """
        
        if status_filter:
            query += " WHERE p.tracking_status = ? ORDER BY p.updated_at DESC"
            cursor.execute(query, (status_filter,))
        else:
            query += """ ORDER BY
                CASE p.tracking_status
                    WHEN 'tracking' THEN 1
                    WHEN 'closed' THEN 2
                    ELSE 3
                END,
                p.updated_at DESC"""
            cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


if __name__ == "__main__":
    print("Geo Market Watch v6.4 — Performance Engine")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  • start_tracking()")
    print("  • close_tracking()")
    print("  • update_benchmark_return()")
    print("  • recompute_performance()")
    print("  • recompute_recent_performance()")
    print("  • get_performance_record()")
    print("  • list_tracked_ideas()")
