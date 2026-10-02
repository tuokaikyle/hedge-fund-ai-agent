"""Render the final analysis into a readable terminal report."""

from __future__ import annotations

from simple_hedge_fund.models import RunResult


def render_report(result: RunResult, *, show_reasoning: bool) -> str:
    """Convert structured analysis results into plain text for the CLI."""
    lines: list[str] = []
    lines.append("Simple Hedge Fund")
    lines.append("=" * 17)
    lines.append(f"Provider: {result.provider}")
    lines.append(f"Model: {result.model}")
    lines.append(f"LLM status: {result.llm_status}")

    for analysis in result.analyses:
        snapshot = analysis.snapshot
        lines.append("")
        lines.append(f"Ticker: {snapshot.ticker} | {snapshot.company_name}")
        lines.append("-" * 72)
        lines.append(f"Price: {_format_currency(snapshot.current_price)}")
        lines.append(f"Sector: {snapshot.sector or 'Unknown'}")
        lines.append(
            "Key metrics: "
            f"ROE {_format_percent(snapshot.return_on_equity)}, "
            f"Profit margin {_format_percent(snapshot.profit_margin)}, "
            f"Operating margin {_format_percent(snapshot.operating_margin)}, "
            f"Debt/Equity {_format_number(snapshot.debt_to_equity)}, "
            f"Revenue growth {_format_percent(snapshot.revenue_growth)}, "
            f"Earnings growth {_format_percent(snapshot.earnings_growth)}"
        )

        for decision in analysis.analyst_decisions:
            lines.append(
                f"{decision.analyst}: {decision.signal.upper()} "
                f"| confidence {decision.confidence}% | score {decision.score}/100 "
                f"| {'LLM' if decision.used_llm else 'heuristic'}"
            )
            if show_reasoning:
                lines.append(f"  Reasoning: {decision.reasoning}")
                if decision.key_points:
                    lines.append(f"  Key points: {'; '.join(decision.key_points)}")

        final = analysis.final_recommendation
        lines.append(f"Final recommendation: {final.signal.upper()} | confidence {final.confidence}%")
        lines.append(f"Summary: {final.summary}")

        if show_reasoning and snapshot.recent_headlines:
            lines.append(f"Headline sample: {' | '.join(snapshot.recent_headlines)}")

    return "\n".join(lines)


def _format_currency(value: float | None) -> str:
    """Format a currency value or show a placeholder when missing."""
    if value is None:
        return "n/a"
    return f"${value:,.2f}"


def _format_percent(value: float | None) -> str:
    """Format a percentage value or show a placeholder when missing."""
    if value is None:
        return "n/a"
    return f"{value:.1%}"


def _format_number(value: float | None) -> str:
    """Format a generic numeric value or show a placeholder when missing."""
    if value is None:
        return "n/a"
    return f"{value:.2f}"