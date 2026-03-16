"""
Geo Market Watch v6.2 — Exposure Engine

Deterministic mapping from geopolitical events to sector and company exposures.
"""

import json
from typing import Any

# Deterministic sector mapping by event category
SECTOR_MAP = {
    "Maritime disruption": {
        "primary": ["tanker_shipping", "marine_insurance"],
        "secondary": ["crude_oil", "lng", "freight_logistics"],
        "direction": "long",
        "rationale": "Disruption increases shipping rates and risk premiums"
    },
    "Energy infrastructure risk": {
        "primary": ["defense", "energy_security"],
        "secondary": ["crude_oil", "refined_products", "cybersecurity"],
        "direction": "long",
        "rationale": "Infrastructure attacks drive defense spending and energy volatility"
    },
    "Fertilizer supply chain": {
        "primary": ["fertilizer", "agriculture_inputs"],
        "secondary": ["food_processing", "agriculture_machinery"],
        "direction": "long",
        "rationale": "Supply disruption drives input prices and food inflation"
    },
    "Conflict escalation": {
        "primary": ["defense", "energy_security"],
        "secondary": ["gold", "safe_haven_currencies", "cybersecurity"],
        "direction": "long",
        "rationale": "Military escalation drives defense and safe haven assets"
    },
    "Sanctions escalation": {
        "primary": ["energy_security", "commodity_trading"],
        "secondary": ["defense", "shipping"],
        "direction": "long",
        "rationale": "Sanctions create supply bottlenecks and trading opportunities"
    }
}


# Company universe by sector
COMPANY_UNIVERSE = {
    "tanker_shipping": [
        {"name": "Frontline", "ticker": "FRO", "exposure": "high"},
        {"name": "Euronav", "ticker": "EURN", "exposure": "high"},
        {"name": "Scorpio Tankers", "ticker": "STNG", "exposure": "high"}
    ],
    "energy": [
        {"name": "ExxonMobil", "ticker": "XOM", "exposure": "medium"},
        {"name": "Chevron", "ticker": "CVX", "exposure": "medium"},
        {"name": "Shell", "ticker": "SHEL", "exposure": "medium"},
        {"name": "TotalEnergies", "ticker": "TTE", "exposure": "medium"}
    ],
    "defense": [
        {"name": "Lockheed Martin", "ticker": "LMT", "exposure": "high"},
        {"name": "Raytheon", "ticker": "RTX", "exposure": "high"},
        {"name": "Northrop Grumman", "ticker": "NOC", "exposure": "high"}
    ],
    "fertilizer": [
        {"name": "Nutrien", "ticker": "NTR", "exposure": "high"},
        {"name": "Mosaic", "ticker": "MOS", "exposure": "high"},
        {"name": "CF Industries", "ticker": "CF", "exposure": "high"}
    ],
    "agriculture": [
        {"name": "Archer Daniels Midland", "ticker": "ADM", "exposure": "medium"},
        {"name": "Bunge", "ticker": "BG", "exposure": "medium"}
    ]
}


def get_sector_exposure(event: dict[str, Any]) -> dict[str, Any]:
    """
    Generate sector exposure for an event.
    
    Args:
        event: Event dict with category, region, score, etc.
        
    Returns:
        Sector exposure dict
    """
    category = event.get('category', 'Unknown')
    score = event.get('score', 0)
    
    # Get sector mapping for category
    mapping = SECTOR_MAP.get(category, {
        "primary": ["general_equities"],
        "secondary": [],
        "direction": "neutral",
        "rationale": "No specific mapping available"
    })
    
    # Adjust conviction based on score
    if score >= 8:
        conviction = "high"
    elif score >= 6:
        conviction = "medium-high"
    elif score >= 4:
        conviction = "medium"
    else:
        conviction = "low"
    
    return {
        "event_key": event.get('event_key'),
        "event_title": event.get('event_title'),
        "category": category,
        "primary_sectors": mapping["primary"],
        "secondary_sectors": mapping["secondary"],
        "direction": mapping["direction"],
        "conviction": conviction,
        "rationale": mapping["rationale"],
        "score": score
    }


def get_company_exposure(event: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Generate company exposure list for an event.
    
    Args:
        event: Event dict
        
    Returns:
        List of company exposure dicts
    """
    sector_exposure = get_sector_exposure(event)
    companies = []
    
    # Get companies from primary sectors
    for sector in sector_exposure["primary_sectors"]:
        sector_companies = COMPANY_UNIVERSE.get(sector, [])
        for company in sector_companies:
            companies.append({
                "event_key": event.get('event_key'),
                "event_title": event.get('event_title'),
                "company_name": company["name"],
                "ticker": company["ticker"],
                "sector": sector,
                "exposure_level": company["exposure"],
                "direction": sector_exposure["direction"],
                "conviction": sector_exposure["conviction"]
            })
    
    # Add select companies from secondary sectors (lower conviction)
    for sector in sector_exposure["secondary_sectors"]:
        sector_companies = COMPANY_UNIVERSE.get(sector, [])
        for company in sector_companies[:2]:  # Limit to top 2
            companies.append({
                "event_key": event.get('event_key'),
                "event_title": event.get('event_title'),
                "company_name": company["name"],
                "ticker": company["ticker"],
                "sector": sector,
                "exposure_level": "low",
                "direction": sector_exposure["direction"],
                "conviction": "low"  # Lower conviction for secondary
            })
    
    return companies


def generate_trade_idea(event: dict[str, Any], company: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a trade idea for an event-company pair.
    
    Args:
        event: Event dict
        company: Company exposure dict
        
    Returns:
        Trade idea dict
    """
    score = event.get('score', 0)
    
    # Determine idea type based on score and direction
    if score >= 7 and company["direction"] == "long":
        idea_type = "event_driven_long"
    elif score >= 5 and company["direction"] == "long":
        idea_type = "watchlist_with_upside"
    else:
        idea_type = "monitor_only"
    
    # Generate thesis
    thesis = f"{event.get('event_title')} creates {company['conviction']} conviction {company['direction']} opportunity in {company['company_name']} ({company['ticker']}) via {company['sector']} exposure."
    
    # Generate invalidation condition
    if idea_type == "event_driven_long":
        invalidation = f"Event de-escalates OR {company['company_name']} decouples from {event.get('category')} risk."
    else:
        invalidation = f"No material impact on {company['sector']} OR event resolves without market disruption."
    
    return {
        "event_key": event.get('event_key'),
        "event_title": event.get('event_title'),
        "company_name": company["company_name"],
        "ticker": company["ticker"],
        "sector": company["sector"],
        "direction": company["direction"],
        "conviction": company["conviction"],
        "idea_type": idea_type,
        "thesis": thesis,
        "invalidation_condition": invalidation,
        "status": "active",
        "score": score
    }


def build_sector_exposure_view(events: list[dict[str, Any]], limit: int = 100) -> list[dict[str, Any]]:
    """Build sector exposure view for multiple events."""
    exposures = []
    for event in events[:limit]:
        exposure = get_sector_exposure(event)
        exposures.append(exposure)
    return exposures


def build_company_exposure_view(events: list[dict[str, Any]], limit: int = 100) -> list[dict[str, Any]]:
    """Build company exposure view for multiple events."""
    companies = []
    for event in events[:limit]:
        event_companies = get_company_exposure(event)
        companies.extend(event_companies)
    return companies


def build_trade_idea_view(events: list[dict[str, Any]], limit: int = 100) -> list[dict[str, Any]]:
    """Build trade idea view for multiple events."""
    ideas = []
    for event in events[:limit]:
        companies = get_company_exposure(event)
        for company in companies:
            idea = generate_trade_idea(event, company)
            ideas.append(idea)
    return ideas


if __name__ == "__main__":
    # Example usage
    example_event = {
        "event_key": "test|maritime-disruption|test-event",
        "event_title": "Test Maritime Event",
        "category": "Maritime disruption",
        "score": 7
    }
    
    print("Sector Exposure:")
    print(json.dumps(get_sector_exposure(example_event), indent=2))
    
    print("\nCompany Exposures:")
    for company in get_company_exposure(example_event):
        print(f"  - {company['company_name']} ({company['ticker']}): {company['direction']} / {company['conviction']}")
    
    print("\nTrade Ideas:")
    for idea in build_trade_idea_view([example_event]):
        print(f"  - {idea['ticker']}: {idea['idea_type']} ({idea['conviction']})")
