#!/usr/bin/env python3
"""Normalize job keys and summarize a Markdown application ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


STATUSES = {
    "unapplied": "☐ 未投递",
    "applied": "✅ 已投递",
    "assessment": "📝 笔试中",
    "interview_pending": "📅 待面试",
    "interviewing": "💬 面试中",
    "offer": "🎉 已 offer",
    "closed": "❌ 流程终止",
}


def normalize_part(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return "".join(char for char in value if char.isalnum())


def normalize_key(company: str, role: str) -> str:
    return f"{normalize_part(company)}|{normalize_part(role)}"


def parse_rows(markdown: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in markdown.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        if cells[0] == "公司" or all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def summarize(path: Path) -> dict[str, int]:
    rows = parse_rows(path.read_text(encoding="utf-8"))
    counts = {key: 0 for key in STATUSES}
    counts["total"] = len(rows)
    counts["s_unapplied"] = 0
    counts["unknown_status"] = 0

    for cells in rows:
        rating = cells[5].upper()
        status = cells[7]
        matched = False
        for key, label in STATUSES.items():
            if label in status:
                counts[key] += 1
                matched = True
                break
        if not matched:
            counts["unknown_status"] += 1
        if rating == "S" and STATUSES["unapplied"] in status:
            counts["s_unapplied"] += 1
    return counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    normalize = subparsers.add_parser("normalize", help="Print a permanent dedupe key")
    normalize.add_argument("company")
    normalize.add_argument("role")

    stats = subparsers.add_parser("stats", help="Summarize a Markdown job ledger")
    stats.add_argument("ledger", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "normalize":
        key = normalize_key(args.company, args.role)
        if key == "|":
            print("company and role cannot both be empty", file=sys.stderr)
            return 2
        print(key)
        return 0
    if not args.ledger.is_file():
        print(f"ledger not found: {args.ledger}", file=sys.stderr)
        return 2
    print(json.dumps(summarize(args.ledger), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
