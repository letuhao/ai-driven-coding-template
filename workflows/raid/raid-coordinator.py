#!/usr/bin/env python3
"""raid-coordinator.py - generic RAID Coordinator helper (project-agnostic).

The heart of the /raid autonomous loop: pick the next ready cycle from the cycle
log (PENDING + all dependencies DONE), and mark a cycle DONE when its sub-agent
returns. Paths come from `.raid/active-task.{yaml,json}` (per-branch) or defaults,
so the same engine drives any project's RAID task. Zero-dependency (stdlib; PyYAML
only if you use a .yaml active-task file).

Usage:
  raid-coordinator.py next-cycle             # JSON {cycle, title, brief_path, deps_satisfied} or {idle:true}
  raid-coordinator.py done-cycle <N> <sha>   # mark cycle N DONE in the cycle log

Cycle log format (markdown table, one row per cycle):
  | N | Title | STATUS | ... |    where STATUS in PENDING|DONE|BLOCKED
Brief dependencies (in each cycle brief): a "## Dependencies" section listing
cycle numbers (e.g. "C3, C7" or "3 7").

SSOT for the loop: ai/rules/task-workflow.md  ·  command: ai/agents/claude-code/commands/raid.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

DEFAULTS = {
    "cycle_log": "docs/raid/CYCLE_LOG.md",
    "briefs_dir": "docs/raid/cycle_briefs",
    "audit": "docs/audit/AUDIT_LOG.jsonl",
}


def load_active_task() -> dict:
    """Read `.raid/active-task.{json,yaml}` for paths; fall back to defaults so the
    coordinator works zero-config. Only the `paths`-relevant keys are used here."""
    cfg = dict(DEFAULTS)
    for name in (".raid/active-task.json", ".raid/active-task.yaml", ".raid/active-task.yml"):
        p = Path(name)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if name.endswith(".json"):
            data = json.loads(text)
        else:
            try:
                import yaml  # type: ignore
            except ImportError:
                print(f"WARN: {name} found but PyYAML not installed; using default paths.",
                      file=sys.stderr)
                data = {}
            else:
                data = yaml.safe_load(text) or {}
        for k in DEFAULTS:
            if data.get(k):
                cfg[k] = data[k]
        break
    return cfg


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def audit(cfg: dict, event: str, **fields) -> None:
    ap = Path(cfg["audit"])
    ap.parent.mkdir(parents=True, exist_ok=True)
    with ap.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now_iso(), "event": event, **fields}) + "\n")


def parse_cycle_log(cfg: dict) -> list[dict]:
    """Parse the cycle-log markdown table -> [{num, title, status}]."""
    p = Path(cfg["cycle_log"])
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*(\w+)\s*\|", line.strip())
        if m:
            num, title, status = m.groups()
            rows.append({"num": int(num), "title": title.strip(), "status": status.strip().upper()})
    return rows


def find_brief(cfg: dict, n: int) -> Path | None:
    d = Path(cfg["briefs_dir"])
    for pat in (f"{n:02d}_*.md", f"{n}_*.md", f"*{n}*.md"):
        matches = sorted(d.glob(pat))
        if matches:
            return matches[0]
    return None


def extract_deps(brief: Path) -> list[int]:
    """Cycle numbers under a '## Dependencies' section of the brief."""
    if not brief or not brief.exists():
        return []
    deps, in_deps = [], False
    for line in brief.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.lower().startswith("## dependencies"):
            in_deps = True
            continue
        if in_deps and s.startswith("##"):
            break
        if in_deps:
            for m in re.finditer(r"\bC?(\d+)\b", s):
                deps.append(int(m.group(1)))
    return sorted(set(deps))


def cmd_next_cycle(cfg: dict) -> int:
    rows = parse_cycle_log(cfg)
    if not rows:
        print(json.dumps({"idle": True, "reason": "cycle log empty or unparseable"}, indent=2))
        return 0
    done = {r["num"] for r in rows if r["status"] == "DONE"}
    for r in sorted((r for r in rows if r["status"] == "PENDING"), key=lambda x: x["num"]):
        brief = find_brief(cfg, r["num"])
        if not brief:
            continue
        unmet = [d for d in extract_deps(brief) if d not in done]
        if not unmet:
            result = {
                "cycle": r["num"], "title": r["title"],
                "brief_path": str(brief), "deps_satisfied": True,
            }
            print(json.dumps(result, indent=2))
            audit(cfg, "coordinator_next_cycle", cycle=r["num"])
            return 0
    print(json.dumps({"idle": True, "reason": "no pending cycle with satisfied deps"}, indent=2))
    audit(cfg, "coordinator_idle")
    return 0


def cmd_done_cycle(cfg: dict, n: int, sha: str) -> int:
    p = Path(cfg["cycle_log"])
    if not p.exists():
        print(f"ERROR: cycle log missing: {p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8")
    new = re.sub(rf"(\|\s*{n}\s*\|[^|]+\|\s*)PENDING(\s*\|)", r"\1DONE\2", text, count=1)
    if new != text:
        p.write_text(new, encoding="utf-8")
    else:
        print(f"WARN: no PENDING row for cycle {n} (already DONE?)", file=sys.stderr)
    audit(cfg, "coordinator_done_cycle", cycle=n, sha=sha)
    print(f"OK: cycle {n} marked DONE (sha={sha[:8]})")
    return 0


def main(argv) -> int:
    p = argparse.ArgumentParser(description="Generic RAID Coordinator helper.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next-cycle")
    pd = sub.add_parser("done-cycle")
    pd.add_argument("cycle", type=int)
    pd.add_argument("sha")
    args = p.parse_args(argv)
    cfg = load_active_task()
    if args.cmd == "next-cycle":
        return cmd_next_cycle(cfg)
    if args.cmd == "done-cycle":
        return cmd_done_cycle(cfg, args.cycle, args.sha)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
