"""Estimate how strongly the lesson's rules support their final signal."""


def decision_confidence(score: int, completeness: int) -> int:
    if score >= 70:
        distance = score - 70
    elif score < 45:
        distance = 45 - score
    else:
        distance = min(score - 45, 70 - score)

    return min(completeness, 50 + distance)
