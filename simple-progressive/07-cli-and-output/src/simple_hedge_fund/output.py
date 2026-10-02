"""Turn a snapshot and its analyst decisions into a readable terminal report.

This file only builds strings — it never prints and never fetches data. The
CLI decides *when* to print; this file decides *what it looks like*.
"""

from __future__ import annotations

from simple_hedge_fund.models import AnalystDecision, StockSnapshot


# --- added in lesson 07 ---
def render_analysis(
    snapshot: StockSnapshot,
    decisions: list[AnalystDecision],
    *,
    show_explanation: bool,
) -> str:
    """Format one ticker's snapshot and every analyst's call as plain text."""
    lines: list[str] = []
    lines.append(f"Ticker: {snapshot.ticker} | {snapshot.company_name}")
    lines.append("-" * 72)
    lines.append(f"Price: {_format_currency(snapshot.current_price)}")
    lines.append(f"Sector: {snapshot.sector or 'Unknown'}")
    lines.append(
        "Key metrics: "
        f"ROE {_format_percent(snapshot.return_on_equity)}, "
        f"Profit margin {_format_percent(snapshot.profit_margin)}, "
        f"Debt/Equity {_format_number(snapshot.debt_to_equity)}, "
        f"Trailing PE {_format_number(snapshot.trailing_pe)}, "
        f"Revenue growth {_format_percent(snapshot.revenue_growth)}, "
        f"Earnings growth {_format_percent(snapshot.earnings_growth)}"
    )

    for decision in decisions:
        lines.append(f"{decision.analyst}: {decision.signal.upper()} | score {decision.score}/100")
        if show_explanation:
            for point in decision.key_points:
                lines.append(f"  - {point}")

    return "\n".join(lines)


def _format_currency(value: float | None) -> str:
    """Format a price, or show a placeholder when it's missing."""
    if value is None:
        return "n/a"
    return f"${value:,.2f}"


def _format_percent(value: float | None) -> str:
    """Format a fraction-style value (0.18) as a percentage (18.0%)."""
    if value is None:
        return "n/a"
    return f"{value:.1%}"


def _format_number(value: float | None) -> str:
    """Format a plain number, or show a placeholder when it's missing."""
    if value is None:
        return "n/a"
    return f"{value:.2f}"
