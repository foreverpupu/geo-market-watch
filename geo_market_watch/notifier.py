"""
Geo Market Watch v5.5 — Notifier

Generates human-readable notifications for monitoring and handoff events.
"""

from typing import Any


def render_monitor_notification(event: dict[str, Any]) -> str:
    """
    Generate notification for monitor events (band = monitor, no trigger).
    
    Args:
        event: Event dict with score, band, and metadata
        
    Returns:
        Markdown-formatted notification string
    """
    lines = [
        "# Geo Market Watch Alert",
        "",
        "**Status:** Monitoring",
        "",
        f"**Event:** {event.get('event_title', 'Unknown')}",
        "",
        f"**Region:** {event.get('region', 'Unknown')}",
        "",
        f"**Category:** {event.get('category', 'Unclassified')}",
        "",
        f"**Score:** {event.get('score', 'N/A')}",
        "",
        f"**Band:** {event.get('band', 'unknown')}",
        "",
        "**Trigger Full Analysis:** no",
        "",
        f"**Summary:** {event.get('summary', 'No summary provided.')}",
        "",
        "**Next Action:** Continue monitoring. Recheck in 24 hours.",
        ""
    ]
    
    return "\n".join(lines)


def render_full_analysis_notification(event: dict[str, Any]) -> str:
    """
    Generate notification for full analysis handoff events.
    
    Args:
        event: Event dict with score, band, trigger info, and metadata
        
    Returns:
        Markdown-formatted notification string
    """
    reasons = event.get('trigger_reasons', [])
    reasons_text = "\n".join([f"- {r}" for r in reasons]) if reasons else "- score_threshold"
    
    lines = [
        "# Geo Market Watch Alert",
        "",
        "**Status:** Escalate to Full Analysis",
        "",
        f"**Event:** {event.get('event_title', 'Unknown')}",
        "",
        f"**Region:** {event.get('region', 'Unknown')}",
        "",
        f"**Category:** {event.get('category', 'Unclassified')}",
        "",
        f"**Score:** {event.get('score', 'N/A')}",
        "",
        f"**Band:** {event.get('band', 'unknown')}",
        "",
        "**Trigger Full Analysis:** yes",
        "",
        "**Reasons:**",
        reasons_text,
        "",
        f"**Summary:** {event.get('summary', 'No summary provided.')}",
        "",
        "**Next Action:** Send this event into Full Analysis Mode.",
        ""
    ]
    
    return "\n".join(lines)


def render_notification(event: dict[str, Any]) -> str:
    """
    Generate appropriate notification based on event trigger status.
    
    Args:
        event: Event dict with trigger_full_analysis field
        
    Returns:
        Markdown-formatted notification string
    """
    trigger = event.get('trigger_full_analysis', False)
    
    if trigger:
        return render_full_analysis_notification(event)
    else:
        return render_monitor_notification(event)


def write_notification(event: dict[str, Any], output_dir: str) -> str:
    """
    Write notification to file.
    
    Args:
        event: Event dict
        output_dir: Directory to write file
        
    Returns:
        Path to written file
    """
    import os
    
    event_key = event.get('event_key', 'unknown')
    trigger = event.get('trigger_full_analysis', False)
    band = event.get('band', 'unknown')
    
    # Determine filename
    if trigger:
        filename = f"full_analysis_{event_key}.md"
    else:
        filename = f"monitor_{band}_{event_key}.md"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Write file
    filepath = os.path.join(output_dir, filename)
    content = render_notification(event)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


if __name__ == "__main__":
    # Example usage
    monitor_event = {
        "event_key": "abc123",
        "event_title": "Red Sea shipping disruption",
        "region": "Middle East",
        "category": "Maritime disruption",
        "score": 5,
        "band": "monitor",
        "trigger_full_analysis": False,
        "summary": "Major container lines reroute vessels due to security risks in the Red Sea."
    }
    
    full_analysis_event = {
        "event_key": "def456",
        "event_title": "Russia expands oil export restrictions",
        "region": "Russia / Global Energy",
        "category": "Sanctions / policy change",
        "score": 7,
        "band": "full_analysis",
        "trigger_full_analysis": True,
        "trigger_reasons": ["score_threshold", "major_sanctions_escalation"],
        "summary": "Russia expands restrictions affecting energy exports."
    }
    
    print("=" * 60)
    print("MONITOR NOTIFICATION")
    print("=" * 60)
    print(render_notification(monitor_event))
    print()
    
    print("=" * 60)
    print("FULL ANALYSIS NOTIFICATION")
    print("=" * 60)
    print(render_notification(full_analysis_event))
