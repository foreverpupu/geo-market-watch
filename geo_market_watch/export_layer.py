"""
Geo Market Watch v6.4 — Export Layer

Handles export of dashboard and performance data to JSON and CSV.
"""

import json
import csv
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _sanitize_for_csv(value) -> str:
    """Sanitize value for CSV export (replace newlines with spaces, convert to string)."""
    if value is None:
        return ""
    text = str(value)
    return text.replace('\n', ' ').replace('\r', ' ')


def build_idea_performance_view(conn: sqlite3.Connection, limit: int = 100) -> List[Dict]:
    """
    Build comprehensive idea performance view.
    
    Args:
        conn: Database connection
        limit: Maximum number of records
    
    Returns:
        List of performance records with idea details
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            t.trade_idea_id,
            t.company_name,
            t.ticker,
            t.direction,
            t.conviction,
            t.analyst_status,
            p.tracking_status,
            p.entry_price,
            p.entry_time,
            p.close_price,
            p.close_time,
            p.return_pct,
            p.benchmark_return_pct,
            p.alpha_spread_pct,
            p.outcome,
            p.holding_period_days,
            p.notes,
            t.created_at as idea_created_at,
            p.updated_at as performance_updated_at
        FROM trade_ideas t
        LEFT JOIN trade_idea_performance p ON t.trade_idea_id = p.trade_idea_id
        WHERE p.trade_idea_id IS NOT NULL
        ORDER BY 
            CASE p.tracking_status
                WHEN 'tracking' THEN 1
                WHEN 'closed' THEN 2
                ELSE 3
            END,
            p.updated_at DESC
        LIMIT ?
        """,
        (limit,)
    )
    
    return [dict(row) for row in cursor.fetchall()]


def build_performance_summary_view(conn: sqlite3.Connection) -> Dict:
    """
    Build performance summary statistics.
    
    Args:
        conn: Database connection
    
    Returns:
        Dictionary with summary statistics
    """
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
    
    return summary


def build_closed_idea_performance_view(conn: sqlite3.Connection, limit: int = 100) -> List[Dict]:
    """
    Build view of closed ideas with performance.
    
    Args:
        conn: Database connection
        limit: Maximum number of records
    
    Returns:
        List of closed performance records
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            t.trade_idea_id,
            t.company_name,
            t.ticker,
            t.direction,
            t.conviction,
            p.entry_price,
            p.entry_time,
            p.close_price,
            p.close_time,
            p.return_pct,
            p.benchmark_return_pct,
            p.alpha_spread_pct,
            p.outcome,
            p.holding_period_days,
            p.notes
        FROM trade_ideas t
        JOIN trade_idea_performance p ON t.trade_idea_id = p.trade_idea_id
        WHERE p.tracking_status = 'closed'
        ORDER BY p.close_time DESC
        LIMIT ?
        """,
        (limit,)
    )
    
    return [dict(row) for row in cursor.fetchall()]


def export_to_json(data: Dict or List, output_path: str) -> bool:
    """
    Export data to JSON file.
    
    Args:
        data: Data to export
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return True
    except Exception as e:
        print(f"Error exporting JSON: {e}")
        return False


def export_to_csv(data: List[Dict], output_path: str) -> bool:
    """
    Export data to CSV file.
    
    Args:
        data: List of dictionaries to export
        output_path: Output file path
    
    Returns:
        True if successful
    """
    if not data:
        print("No data to export")
        return False
    
    try:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Get fieldnames from first record
        fieldnames = list(data[0].keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in data:
                # Sanitize all values for CSV
                sanitized_row = {k: _sanitize_for_csv(v) for k, v in row.items()}
                writer.writerow(sanitized_row)
        
        return True
    except Exception as e:
        print(f"Error exporting CSV: {e}")
        return False


def export_dashboard_data(
    db_path: str,
    output_dir: str,
    timestamp: Optional[str] = None
) -> Dict[str, bool]:
    """
    Export all dashboard data to files.
    
    Args:
        db_path: Path to database
        output_dir: Directory for output files
        timestamp: Optional timestamp string for filenames
    
    Returns:
        Dictionary with export status for each file
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    conn = get_db_connection(db_path)
    
    results = {}
    
    # Export idea performance
    perf_data = build_idea_performance_view(conn)
    results['idea_performance_json'] = export_to_json(
        perf_data, 
        output_path / f"idea_performance_{timestamp}.json"
    )
    results['idea_performance_csv'] = export_to_csv(
        perf_data,
        output_path / f"idea_performance_{timestamp}.csv"
    )
    
    # Export latest (symlink/copy without timestamp)
    results['idea_performance_latest_json'] = export_to_json(
        perf_data,
        output_path / "idea_performance_latest.json"
    )
    results['idea_performance_latest_csv'] = export_to_csv(
        perf_data,
        output_path / "idea_performance_latest.csv"
    )
    
    # Export performance summary
    summary = build_performance_summary_view(conn)
    results['performance_summary'] = export_to_json(
        summary,
        output_path / "idea_performance_summary.json"
    )
    
    # Export closed ideas
    closed_data = build_closed_idea_performance_view(conn)
    results['closed_ideas_json'] = export_to_json(
        closed_data,
        output_path / f"closed_ideas_{timestamp}.json"
    )
    
    conn.close()
    
    return results


if __name__ == "__main__":
    print("Geo Market Watch v6.4 — Export Layer")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  • build_idea_performance_view()")
    print("  • build_performance_summary_view()")
    print("  • build_closed_idea_performance_view()")
    print("  • export_to_json()")
    print("  • export_to_csv()")
    print("  • export_dashboard_data()")
