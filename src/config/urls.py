"""
URL registry for HDFC Mutual Fund scheme pages on Groww.

Contains all 19 curated source URLs used by the data ingestion pipeline.
Each entry maps a human-readable scheme name to its Groww URL.
"""

from typing import Optional

# ── Scheme URL Registry ──────────────────────────────────────────────────────
# Format: { "Scheme Name": "Groww URL" }
# These are the ONLY data sources the assistant may use (no third-party blogs).

SCHEME_URLS: dict[str, str] = {
    "HDFC Silver ETF FoF Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-silver-etf-fof-direct-growth"
    ),
    "HDFC Mid Cap Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
    ),
    "HDFC Flexi Cap Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
    ),
    "HDFC Small Cap Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
    ),
    "HDFC Defence Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-defence-fund-direct-growth"
    ),
    "HDFC Gold ETF Fund Of Fund Direct Plan Growth": (
        "https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth"
    ),
    "HDFC Nifty 50 Index Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-nifty-50-index-fund-direct-growth"
    ),
    "HDFC Balanced Advantage Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
    ),
    "HDFC Pharma And Healthcare Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-pharma-and-healthcare-fund-direct-growth"
    ),
    "HDFC Multi Cap Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-multi-cap-fund-direct-growth"
    ),
    "HDFC Short Term Opportunities Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-short-term-opportunities-fund-direct-growth"
    ),
    "HDFC Focused Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth"
    ),
    "HDFC BSE Sensex Index Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-bse-sensex-index-fund-direct-growth"
    ),
    "HDFC Nifty Next 50 Index Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-nifty-next-50-index-fund-direct-growth"
    ),
    "HDFC Large And Mid Cap Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-large-and-mid-cap-fund-direct-growth"
    ),
    "HDFC Liquid Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-liquid-fund-direct-growth"
    ),
    "HDFC Infrastructure Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-infrastructure-fund-direct-growth"
    ),
    "HDFC Nifty Top 20 Equal Weight Index Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-nifty-top-20-equal-weight-index-fund-direct-growth"
    ),
    "HDFC Ultra Short Term Fund Direct Growth": (
        "https://groww.in/mutual-funds/hdfc-ultra-short-term-fund-direct-growth"
    ),
}


def get_all_urls() -> list[str]:
    """Return a flat list of all scheme URLs."""
    return list(SCHEME_URLS.values())


def get_all_schemes() -> list[dict[str, str]]:
    """Return a list of dicts with scheme name and URL."""
    return [
        {"scheme_name": name, "url": url}
        for name, url in SCHEME_URLS.items()
    ]


def get_scheme_name_by_url(url: str) -> Optional[str]:
    """Look up the scheme name for a given URL. Returns None if not found."""
    for name, scheme_url in SCHEME_URLS.items():
        if scheme_url == url:
            return name
    return None


# Total number of schemes in the registry
TOTAL_SCHEMES: int = len(SCHEME_URLS)
