"""Estimate how strongly the lesson's rules support their final signal."""

from models import Signal


def decision_confidence(score: int, signal: Signal, completeness: int) -> int:
    if signal == "buy":
        distance = score - 70
    elif signal == "sell":
        distance = 45 - score
    elif score >= 70:
        # A price or debt rule blocked a buy despite a high score.
        distance = 0
    else:
        distance = min(score - 45, 70 - score)

    return min(completeness, 50 + distance)
