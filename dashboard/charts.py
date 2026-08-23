"""Meaningful Plotly visualizations for assessment results."""

from __future__ import annotations

import plotly.graph_objects as go


def risk_gauge(score: float, level: str) -> go.Figure:
    """Return a 0-10 risk gauge with the calculated risk level."""

    figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 10"},
        title={"text": f"{level} risk"},
        gauge={"axis": {"range": [0, 10]}, "bar": {"color": "#22d3ee"}, "steps": [
            {"range": [0, 3], "color": "#064e3b"},
            {"range": [3, 6], "color": "#854d0e"},
            {"range": [6, 8], "color": "#9a3412"},
            {"range": [8, 10], "color": "#7f1d1d"},
        ]},
    ))
    figure.update_layout(height=260, margin={"l": 20, "r": 20, "t": 70, "b": 10}, paper_bgcolor="rgba(0,0,0,0)")
    return figure
