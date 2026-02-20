#!/usr/bin/env python3
"""
blog_post_writer.py
A small utility that reads a partially populated blog post template and
uses OpenAI to generate a data-driven final draft. It reads CSV statistics from
a data directory and fills the template using the OPENAI_API_KEY env var.
"""

import os
import json
import glob
import csv
import math
import re
from typing import Dict, Any


api_key = os.environ.get("OPENAI_API_KEY")

# Optional: use pandas for nicer numeric stats if available
HAS_PANDAS = False
PANDAS_IMPORTED = False
try:
    import pandas as pd  # type: ignore
    import numpy as np  # type: ignore
    HAS_PANDAS = True
    PANDAS_IMPORTED = True
except Exception:
    HAS_PANDAS = False

# Import OpenAI; fall back gracefully if not installed
try:
    from openai import OpenAI
    
    client = OpenAI()  # type: ignore
except Exception:
    openai = None  # type: ignore


def read_template(template_path: str) -> str:
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def compute_stats_with_csv(data_dir: str) -> Dict[str, Dict[str, Any]]:
    """Compute basic statistics for numeric values in CSVs under data_dir.
    Returns dict: column -> {mean, std, min, max, count}
    Works with or without pandas installed.
    """
    if HAS_PANDAS:
        try:
            dfs = []
            for path in glob.glob(data_dir.rstrip('/') + '/*.csv'):
                try:
                    df = pd.read_csv(path)
                except Exception:
                    continue
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    continue
                dfs.append(df[numeric_cols].copy())
            if not dfs:
                return {}
            all_num = pd.concat(dfs, ignore_index=True)
            stats_out: Dict[str, Dict[str, Any]] = {}
            for col in all_num.columns:
                ser = all_num[col].astype('float64')
                mean = float(ser.mean())
                std = float(ser.std(ddof=1)) if len(ser) > 1 else 0.0
                mn = float(ser.min())
                mx = float(ser.max())
                count = int(ser.count())
                stats_out[col] = {"mean": mean, "std": std, "min": mn, "max": mx, "count": count}
            return stats_out
        except Exception:
            pass

    stats: Dict[str, Dict[str, Any]] = {}
    for path in glob.glob(data_dir.rstrip('/') + '/*.csv'):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                except StopIteration:
                    continue
                for row in reader:
                    for i, val in enumerate(row):
                        col = header[i] if i < len(header) else f"col_{i}"
                        try:
                            v = float(val)
                        except Exception:
                            continue
                        if col not in stats:
                            stats[col] = {"count": 0, "sum": 0.0, "sum_sq": 0.0, "min": None, "max": None}
                        s = stats[col]
                        s["count"] += 1
                        s["sum"] += v
                        s["sum_sq"] += v * v
                        if s["min"] is None or v < s["min"]:
                            s["min"] = v
                        if s["max"] is None or v > s["max"]:
                            s["max"] = v
        except Exception:
            continue
    final: Dict[str, Dict[str, Any]] = {}
    for col, s in stats.items():
        cnt = s["count"]
        if cnt == 0:
            continue
        mean = s["sum"] / cnt
        if cnt > 1:
            var = (s["sum_sq"] - (s["sum"] * s["sum"]) / cnt) / (cnt - 1)
            std = math.sqrt(var) if var > 0 else 0.0
        else:
            std = 0.0
        final[col] = {"mean": mean, "std": std, "min": s["min"], "max": s["max"], "count": cnt}
    return final


def _extract_content(resp) -> str:
    print("here")
    """Robustly extract the generated text content from various OpenAI response shapes."""
    try:
        # New-style OpenAI API response
        if hasattr(resp, 'choices') and isinstance(resp.choices, list) and len(resp.choices) > 0:
            first = resp.choices[0]
            msg = getattr(first, 'message', None)
            if isinstance(msg, dict):
                c = msg.get('content')
                if isinstance(c, str):
                    return c
            if hasattr(first, 'content'):
                c = getattr(first, 'content')
                if isinstance(c, str):
                    return c
            if hasattr(first, 'text'):
                t = getattr(first, 'text')
                if isinstance(t, str):
                    return t
        if isinstance(resp, dict):
            choices = resp.choices
            if isinstance(choices, list) and len(choices) > 0:
                c0 = choices[0]
                if isinstance(c0, dict):
                    if 'text' in c0:
                        return c0['text']
                    if 'message' in c0 and isinstance(c0['message'], dict):
                        return c0['message'].get('content', '')
    except Exception:
        pass
    return ""


def extract_placeholders(template_text: str) -> list[str]:
    """Extract placeholders of the form {{PLACEHOLDER}} from the template.
    Returns a list of unique placeholders in uppercase.
    """
    try:
        placeholders = re.findall(r"\{\{([A-Z0-9_]+)\}\}", template_text)
        # Unique while preserving order
        seen = set()
        uniq: list[str] = []
        for p in placeholders:
            up = p.upper()
            if up not in seen:
                seen.add(up)
                uniq.append(up)
        return uniq
    except Exception:
        return []


def _normalize_placeholder(ph: str) -> str:
    return ph.upper().strip()


def _fill_value_for_placeholder(ph: str, stats: Dict[str, Any]) -> Any:
    # Direct lookup by placeholder name
    if ph in stats:
        s = stats[ph]
        return s.get("mean", s.get("value"))
    # Try to match a column name by normalization
    for col, s in stats.items():
        if _normalize_placeholder(col) == ph:
            return s.get("mean", s.get("value"))
    return None


def _format_value(v: Any) -> str:
    if isinstance(v, (int, float)):
        try:
            return f"{float(v):.2f}"
        except Exception:
            return str(v)
    return str(v)


def _fill_values_from_stats(placeholders: list[str], stats: Dict[str, Any]) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for ph in placeholders:
        val = _fill_value_for_placeholder(ph, stats)
        if val is not None:
            values[ph] = _format_value(val)
    return values


def _replace_placeholders(text: str, replacements: Dict[str, str]) -> str:
    for ph, val in replacements.items():
        text = text.replace("{{" + ph + "}}", val)
    return text


def generate_post_via_openai(template_text: str, stats: Dict[str, Any], model: str = "gpt-4") -> str:
    if OpenAI is None:
        raise RuntimeError("OpenAI package is not installed. Install openai to use this script.")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    prompt = (
        "You are an experienced technical writer. Fill in the provided blog post template with data-driven insights using the supplied statistics. "
        "Preserve Markdown structure and headings. Fill only the placeholders that indicate missing data and leave the rest intact."
        f"\n\nTemplate:\n{template_text}\n\nStatistics (derived from CSVs in the data directory):\n{json.dumps(stats, indent=2)}\n"
        "If a placeholder refers to a specific value (e.g., AVERAGE_RESTING_HR), replace it with the actual value and provide a brief, human-friendly sentence there."
        "When in doubt, provide a short explanation and move on to the next item."
    )

    messages = [
        {"role": "system", "content": "You are an excellent, concise blog post writer who can transform data into engaging narrative."},
        {"role": "user", "content": prompt},
    ]

    try:
        # Use the public API call for chat-based completions
        resp = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
        generated = _extract_content(resp)
    except Exception:
        # Fallback to a simpler prompt if the first attempt fails
        fallback_prompt = (
            f"Template:\n{template_text}\n\nStatistics:\n{json.dumps(stats, indent=2)}\n\nProvide a completed markdown post."
        )
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "You are a concise blog post writer."},
            {"role": "user", "content": fallback_prompt},
        ], temperature=0.2)
        generated = _extract_content(resp)

    if not generated:
        return ""

    # Post-process: populate placeholders with stat-derived values where possible
    placeholders = extract_placeholders(template_text)
    if placeholders:
        filled_values = _fill_values_from_stats(placeholders, stats)
        generated = _replace_placeholders(generated, filled_values)

    return generated


def write_generated_post(template_path: str, content: str) -> str:
    base_dir = os.path.dirname(template_path)
    output_path = os.path.join(base_dir, 'generated_post.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path


def main():
    template_path = "/Users/kelvinnicholson/Workspace/kelvinism/content/posts/2025-q4-health-review/index.md"
    data_dir = "/Users/kelvinnicholson/Workspace/kelvinism/content/posts/2025-q4-health-review/data"
    template_text = read_template(template_path)
    stats = compute_stats_with_csv(data_dir)
    try:
        generated = generate_post_via_openai(template_text, stats, model="gpt-4")
    except Exception as e:
        print(e)
        generated = generate_post_via_openai(template_text, stats, model="gpt-3.5-turbo")

    if not generated:
        raise RuntimeError("Failed to generate blog post content from OpenAI.")
    output_path = write_generated_post(template_path, generated)
    print(f"Generated blog post saved to: {output_path}")


if __name__ == '__main__':
    main()
