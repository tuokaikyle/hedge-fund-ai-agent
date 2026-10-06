"""Measure how much of an agent's expected data was returned."""


def data_completeness(*values: float | None) -> int:
    return round(100 * sum(value is not None for value in values) / len(values))
