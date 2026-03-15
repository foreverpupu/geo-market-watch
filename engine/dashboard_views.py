"""
Geo Market Watch v6.4 — Dashboard Views

Provides filtered views and JSON snapshots for dashboard display.
Includes performance tracking views.
"""

import sqlite3
import json
from typing import List, Dict, Optional
from pathlib import Path

from .lifecycle_engine import get_active_ideas, get_ideas_by_status


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_approved_trade_ideas(db_path: str) -> List[Dict]:
    """
    Get all approved trade ideas, sorted by conviction and recency.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of approved trade ideas
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.analyst_status, t.approval_status, t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.analyst_status = 'approved'
            ORDER BY 
                CASE t.conviction
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                    ELSE 4
                END,
                t.created_at DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


def get_pending_trade_ideas(db_path: str) -> List[Dict]:
    """
    Get all pending review trade ideas, sorted by conviction and recency.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of pending trade ideas
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.analyst_status, t.approval_status, t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.analyst_status = 'pending_review'
            ORDER BY 
                CASE t.conviction
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                    ELSE 4
                END,
                t.created_at DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


def get_invalidated_trade_ideas(db_path: str) -> List[Dict]:
    """
    Get all invalidated trade ideas, sorted by recency.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of invalidated trade ideas
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.analyst_status, t.approval_status, t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.analyst_status = 'invalidated'
            ORDER BY t.updated_at DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


def get_dashboard_snapshot(db_path: str) -> Dict:
    """
    Get a complete dashboard snapshot with all key views.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        Dictionary with all dashboard views
    """
    return {
        "active_trade_ideas": get_active_ideas(db_path),
        "approved_trade_ideas": get_approved_trade_ideas(db_path),
        "pending_review": get_pending_trade_ideas(db_path),
        "invalidated_ideas": get_invalidated_trade_ideas(db_path),
        "tracked_ideas": get_tracked_ideas(db_path),
        "closed_ideas": get_closed_ideas(db_path),
        "performance_summary": get_performance_summary(db_path),
        "idea_performance": get_tracked_ideas(db_path)
    }


def export_dashboard_snapshot(db_path: str, output_path: str) -> bool:
    """
    Export dashboard snapshot to JSON file.
    
    Args:
        db_path: Path to the SQLite database
        output_path: Path to write JSON file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        snapshot = get_dashboard_snapshot(db_path)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error exporting snapshot: {e}")
        return False


def get_idea_summary(db_path: str, trade_idea_id: str) -> Optional[Dict]:
    """
    Get a summary of a single trade idea with review and lifecycle info.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
    
    Returns:
        Dictionary with idea summary or None if not found
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Get idea details
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.invalidation_condition, t.analyst_status, t.approval_status,
                t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        idea = dict(row)
        
        # Get reviews
        cursor.execute(
            """
            SELECT reviewer, review_decision, confidence, review_notes, created_at
            FROM idea_reviews
            WHERE trade_idea_id = ?
            ORDER BY created_at DESC
            """,
            (trade_idea_id,)
        )
        idea["reviews"] = [dict(r) for r in cursor.fetchall()]
        
        # Get lifecycle events
        cursor.execute(
            """
            SELECT event_type, event_reason, created_at
            FROM idea_lifecycle
            WHERE trade_idea_id = ?
            ORDER BY created_at ASC
            """,
            (trade_idea_id,)
        )
        idea["lifecycle_events"] = [dict(r) for r in cursor.fetchall()]
        
        # Get performance if exists
        cursor.execute(
            """
            SELECT tracking_status, entry_price, close_price, return_pct,
                   benchmark_return_pct, alpha_spread_pct, outcome, holding_period_days
            FROM trade_idea_performance
            WHERE trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        perf_row = cursor.fetchone()
        if perf_row:
            idea["performance"] = dict(perf_row)
        
        conn.close()
        return idea
    
    except sqlite3.Error as e:
        return None


def get_performance_summary(db_path: str) -> Dict:
    """
    Get performance summary statistics.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        Dictionary with performance statistics
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Overall counts
        cursor.execute(
            """
            SELECT 
                COUNT(*) as tracked_count,
                COUNT(CASE WHEN tracking_status = 'closed' THEN 1 END) as closed_count,
                COUNT(CASE WHEN return_pct > 0 THEN 1 END) as positive_count,
                COUNT(CASE WHEN return_pct < 0 THEN 1 END) as negative_count,
                COUNT(CASE WHEN return_pct = 0 THEN 1 END) as zero_count,
                AVG(return_pct) as average_return_pct,
                AVG(alpha_spread_pct) as average_alpha_spread_pct
            FROM trade_idea_performance
            WHERE tracking_status = 'closed'
            """
        )
        
        row = cursor.fetchone()
        summary = {
            "tracked_count": cursor.execute("SELECT COUNT(*) FROM trade_idea_performance").fetchone()[0],
            "closed_count": row['closed_count'] or 0,
            "positive_count": row['positive_count'] or 0,
            "negative_count": row['negative_count'] or 0,
            "zero_count": row['zero_count'] or 0,
            "average_return_pct": round(row['average_return_pct'], 2) if row['average_return_pct'] else 0.0,
            "average_alpha_spread_pct": round(row['average_alpha_spread_pct'], 2) if row['average_alpha_spread_pct'] else None
        }
        
        # Outcome distribution
        cursor.execute(
            """
            SELECT outcome, COUNT(*) as count
            FROM trade_idea_performance
            WHERE outcome IS NOT NULL
            GROUP BY outcome
            """
        )
        summary["outcome_distribution"] = {row['outcome']: row['count'] for row in cursor.fetchall()}
        
        # Direction breakdown
        cursor.execute(
            """
            SELECT 
                t.direction,
                COUNT(*) as count,
                AVG(p.return_pct) as avg_return
            FROM trade_idea_performance p
            JOIN trade_ideas t ON p.trade_idea_id = t.trade_idea_id
            WHERE p.return_pct IS NOT NULL
            GROUP BY t.direction
            """
        )
        summary["by_direction"] = [
            {"direction": row['direction'], "count": row['count'], "avg_return": round(row['avg_return'], 2) if row['avg_return'] else 0}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return summary
    
    except sqlite3.Error as e:
        return {"error": str(e)}


def get_tracked_ideas(db_path: str) -> List[Dict]:
    """
    Get all tracked ideas with performance data.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of tracked ideas
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id,
                t.company_name,
                t.ticker,
                t.direction,
                p.tracking_status,
                p.entry_price,
                p.close_price,
                p.return_pct,
                p.outcome,
                p.holding_period_days
            FROM trade_ideas t
            JOIN trade_idea_performance p ON t.trade_idea_id = p.trade_idea_id
            ORDER BY 
                CASE p.tracking_status
                    WHEN 'tracking' THEN 1
                    WHEN 'closed' THEN 2
                    ELSE 3
                END,
                p.updated_at DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


def get_closed_ideas(db_path: str) -> List[Dict]:
    """
    Get all closed tracked ideas.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of closed ideas with performance
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id,
                t.company_name,
                t.ticker,
                t.direction,
                p.entry_price,
                p.close_price,
                p.return_pct,
                p.benchmark_return_pct,
                p.alpha_spread_pct,
                p.outcome,
                p.holding_period_days
            FROM trade_ideas t
            JOIN trade_idea_performance p ON t.trade_idea_id = p.trade_idea_id
            WHERE p.tracking_status = 'closed'
            ORDER BY p.close_time DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error as e:
        return []


if __name__ == "__main__":
    print("Geo Market Watch v6.4 — Dashboard Views")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  • get_approved_trade_ideas()")
    print("  • get_pending_trade_ideas()")
    print("  • get_invalidated_trade_ideas()")
    print("  • get_dashboard_snapshot()")
    print("  • export_dashboard_snapshot()")
    print("  • get_idea_summary()")
    print("  • get_performance_summary()")
