"""Turn a completed analysis into a readable terminal report."""

from textwrap import fill

from models import TickerAnalysis


# introduced in lesson 15
def render_report(analysis: TickerAnalysis) -> str:
    """Format existing results without changing scores or making model calls."""
    snapshot = analysis.snapshot
    lines = [
        "Hedge Fund Mini",
        "===============",
        f"Ticker: {snapshot.ticker} | {snapshot.company_name}",
        f"Sector: {snapshot.sector or 'n/a'}",
        f"Price: {_format_number(snapshot.current_price)}",
        "",
        "Snapshot metrics",
        f"  Trailing P/E: {_format_number(snapshot.trailing_pe)}",
        f"  Return on equity: {_format_percent(snapshot.return_on_equity)}",
        f"  Profit margin: {_format_percent(snapshot.profit_margin)}",
        f"  Operating margin: {_format_percent(snapshot.operating_margin)}",
        f"  Debt/equity: {_format_number(snapshot.debt_to_equity)}",
        f"  Revenue growth: {_format_percent(snapshot.revenue_growth)}",
        f"  Earnings growth: {_format_percent(snapshot.earnings_growth)}",
        "",
        "Agent decisions",
    ]
    for decision in analysis.analyst_decisions:
        lines.extend([
            f"  {decision.analyst}: {decision.signal.upper()} | score {decision.score}/100",
            f"  Data completeness: {decision.data_completeness}% | confidence: {decision.confidence}%",
            fill(f"Reasoning: {decision.reasoning}", width=88,
                 initial_indent="  ", subsequent_indent="    "),
            "",
        ])

    final = analysis.final_recommendation
    lines.extend([
        "Combined result",
        f"  Equal average: {final.plain_signal.upper()} | score {final.plain_score}/100",
        f"  Confidence-weighted average: {final.signal.upper()} | score {final.weighted_score}/100",
        f"  Final recommendation: {final.signal.upper()}",
        "",
        "Data completeness measures input coverage; confidence measures rule support.",
        "Neither is a measured probability of being correct.",
    ])
    return "\n".join(lines)


# introduced in lesson 15
def _format_number(value: float | None) -> str:
    return "n/a" if value is None else f"{value:,.2f}"


# introduced in lesson 15
def _format_percent(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"
