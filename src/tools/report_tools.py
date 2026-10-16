from __future__ import annotations
import json
from typing import Any
import pandas as pd

from .registry import tool


@tool("aggregate")
def aggregate(
    df: pd.DataFrame,
    group_by: str,
    metrics: dict[str, str],
    **_: Any,
) -> pd.DataFrame:
    """
    Generic group-by aggregator.

    Args:
        df:        input DataFrame
        group_by:  column to group on (e.g. "workflow_id")
        metrics:   mapping of output_name -> aggregation expression
                   e.g. {"runs": "size",
                         "failures": "sum",
                         "avg_time": "mean"}

    The aggregation expression is applied to the column named the same
    as the output key unless the value is one of the pandas builtins
    ("size", "count", "sum", "mean", "min", "max").
    """
    grouped = df.groupby(group_by)

    out = pd.DataFrame(index=grouped.size().index)

    for name, expr in metrics.items():
        if expr == "size":
            out[name] = grouped.size()
        elif expr in {"count", "sum", "mean", "min", "max"}:
            # apply to a column with the same name as the output key
            if name in df.columns:
                out[name] = getattr(grouped[name], expr)()
            else:
                out[name] = getattr(grouped, expr)()
        else:
            # custom expression evaluated against the group frame
            out[name] = grouped.apply(lambda g: eval(expr, {"g": g}, {}))

    return out.reset_index()


@tool("compute_rate")
def compute_rate(
    df: pd.DataFrame,
    numerator_col: str,
    denominator_col: str,
    out_col: str = "rate",
    **_: Any,
) -> pd.DataFrame:
    """Add a `numerator / denominator` column (safe against div-by-zero)."""
    df = df.copy()
    df[out_col] = df[numerator_col] / df[denominator_col].replace(0, pd.NA)
    return df


@tool("flag_threshold")
def flag_threshold(
    df: pd.DataFrame,
    column: str,
    threshold: float,
    op: str = ">",
    **_: Any,
) -> pd.DataFrame:
    """Return only rows where df[column] <op> threshold."""
    ops = {
        ">":  lambda s: s > threshold,
        ">=": lambda s: s >= threshold,
        "<":  lambda s: s < threshold,
        "<=": lambda s: s <= threshold,
        "==": lambda s: s == threshold,
        "!=": lambda s: s != threshold,
    }
    if op not in ops:
        raise ValueError(f"Unsupported op: {op}")
    return df[ops[op](df[column])].reset_index(drop=True)


@tool("rank_by")
def rank_by(
    df: pd.DataFrame,
    column: str,
    ascending: bool = False,
    top_n: int | None = None,
    **_: Any,
) -> pd.DataFrame:
    """Sort by a column; optionally keep the top N rows."""
    out = df.sort_values(column, ascending=ascending)
    return out.head(top_n) if top_n else out


@tool("to_json")
def to_json(obj: Any, indent: int = 2, **_: Any) -> str:
    """Serialize DataFrames / dicts / lists to pretty JSON for the agent."""
    if isinstance(obj, pd.DataFrame):
        obj = obj.to_dict(orient="records")
    return json.dumps(obj, indent=indent, default=str)


@tool("summary_stats")
def summary_stats(df: pd.DataFrame, column: str, **_: Any) -> dict:
    """Basic descriptive stats for a numeric column."""
    s = pd.to_numeric(df[column], errors="coerce").dropna()
    return {
        "count": int(s.size),
        "mean":  float(s.mean())  if s.size else None,
        "median": float(s.median()) if s.size else None,
        "min":   float(s.min())   if s.size else None,
        "max":   float(s.max())   if s.size else None,
        "p95":   float(s.quantile(0.95)) if s.size else None,
    }