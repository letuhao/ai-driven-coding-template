#!/usr/bin/env python3
"""workflow-gate.py - generic, config-driven enforcement of the Task Workflow.

Project-agnostic: the engine is identical across projects. Everything
project-specific lives in `workflow.config.json` (or `.yaml` if PyYAML is
installed) - see workflow.config.example.json. It also runs **zero-config**
with the defaults below.

Zero-dependency: stdlib only. No assumption about the project's own language.

Usage:
  workflow-gate.py size <XS|S|M|L|XL> <files> <logic> <side_effects> [context_pct]
  workflow-gate.py phase <name>
  workflow-gate.py complete <name> "<evidence>"
  workflow-gate.py check <name>
  workflow-gate.py skip <name> "<reason>"
  workflow-gate.py status
  workflow-gate.py pre-commit
  workflow-gate.py reset
  workflow-gate.py amaw-enable [task-slug]
  workflow-gate.py slices <manifest.yaml|.json>     # /warp gate (needs the warp validator)

SSOT for the model: ai/rules/task-workflow.md
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(".workflow-state.json")

PHASES = [
    "clarify", "design", "review-design", "plan", "build",
    "verify", "review-code", "qc", "post-review", "session",
    "commit", "retro",
]
SIZES = ["XS", "S", "M", "L", "XL"]
SKIPPABLE = {"XS": {"clarify", "plan"}, "S": {"plan"}}

# Phases whose completion the pre-commit hook requires.
COMMIT_GATES = [
    ("verify", "Phase 6 VERIFY not done - run tests and record evidence"),
    ("post-review", "Phase 9 POST-REVIEW not done - present changes to the human"),
    ("session", "Phase 10 SESSION not done - update the handoff"),
]

DEFAULT_CONFIG = {
    "module_globs": ["services/*", "packages/*", "apps/*"],
    "paths": {"audit": "docs/audit/AUDIT_LOG.jsonl"},
    "verify": {
        "cross_module_smoke": True,
        "smoke_tokens": ["live smoke", "live-smoke", "live infra unavailable"],
    },
    # Optional, pluggable. null ⇒ no-op (the engine never depends on them).
    "integrations": {"lessons_store_cmd": None, "guardrails_cmd": None},
}

INITIAL_STATE = {
    "task": "", "size": None,
    "size_counts": {"files": 0, "logic": 0, "side_effects": 0},
    "current_phase": None, "current_phase_index": -1,
    "phases_completed": [], "phases_skipped": [],
    "verify_evidence": None, "started_at": None, "last_transition": None,
    "amaw_enabled": False, "amaw_enabled_at": None,
}


# ── config ───────────────────────────────────────────────────────────

def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in (override or {}).items():
        out[k] = _deep_merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def load_config() -> dict:
    """Load workflow.config.{json,yaml} from repo root if present; else defaults.

    JSON is canonical (zero-dependency). YAML is accepted only when PyYAML is
    importable - otherwise a .yaml config errors with clear guidance rather than
    silently ignoring the operator's settings.
    """
    for name in ("workflow.config.json", "workflow.config.yaml", "workflow.config.yml"):
        p = Path(name)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if name.endswith(".json"):
            user = json.loads(text)
        else:
            try:
                import yaml  # type: ignore
            except ImportError:
                fail(f"{name} found but PyYAML is not installed. Install pyyaml, or use "
                     f"workflow.config.json (same keys).")
            user = yaml.safe_load(text) or {}
        return _deep_merge(DEFAULT_CONFIG, user)
    return dict(DEFAULT_CONFIG)


# ── state ────────────────────────────────────────────────────────────

def load_state() -> dict:
    if not STATE_FILE.exists():
        save_state(dict(INITIAL_STATE))
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        # A corrupt/empty state file must not make every gate command (incl. the
        # pre-commit hook) die with a traceback. Reset and warn loudly.
        print(f"WARN: {STATE_FILE} unreadable/corrupt ({exc}); resetting.", file=sys.stderr)
        fresh = dict(INITIAL_STATE)
        save_state(fresh)
        return fresh


def save_state(state: dict) -> None:
    # Atomic write: serialize to a per-process temp, then atomic rename, so the
    # state file always holds a complete old-or-new state on a process crash.
    tmp = STATE_FILE.with_name(f"{STATE_FILE.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        tmp.replace(STATE_FILE)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def completed_phases(state: dict) -> set:
    return {p["phase"] for p in state.get("phases_completed", [])}


def fail(msg: str) -> None:
    print(f"BLOCKED: {msg}", file=sys.stderr)
    sys.exit(1)


def _now() -> str:
    return datetime.now().isoformat()


def _normalize_slug(raw) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(raw).lower()).strip("-")[:64].strip("-")
    return slug or "unnamed-task"


# ── pluggable integrations (no-op when unconfigured) ─────────────────

def _log_audit(cfg: dict, event: dict) -> None:
    audit = Path(cfg["paths"]["audit"])
    audit.parent.mkdir(parents=True, exist_ok=True)
    with audit.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _record_lesson(cfg: dict, title: str, content: str, tags: list) -> None:
    """Best-effort: shell out to the configured lessons store. Never raises,
    never blocks - the state machine stays deterministic regardless of any
    external store's availability. No-op when `lessons_store_cmd` is null."""
    cmd = cfg["integrations"].get("lessons_store_cmd")
    if not cmd:
        return
    try:
        subprocess.run(
            shlex.split(cmd) + ["--title", title, "--content", content, "--tags", ",".join(tags)],
            capture_output=True, text=True, timeout=75,
        )
    except (subprocess.SubprocessError, OSError) as e:
        print(f"WARN: lessons-store bridge skipped ({e})", file=sys.stderr)


def _modules_in_diff(cfg: dict) -> set:
    """Distinct module ids touched in the working diff, per configured globs.
    Generalizes the source's hardcoded services/<name>/ detection."""
    try:
        r = subprocess.run(["git", "diff", "--name-only", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            return set()
        files = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    except (subprocess.SubprocessError, OSError, FileNotFoundError):
        return set()
    patterns = []
    for g in cfg.get("module_globs", []):
        prefix = g[:-1] if g.endswith("*") else g.rstrip("/") + "/"
        patterns.append(re.compile(r"^" + re.escape(prefix) + r"([^/]+)/"))
    mods = set()
    for path in files:
        for pat in patterns:
            m = pat.match(path)
            if m:
                mods.add(m.group(0))
    return mods


def _check_live_smoke(cfg: dict, evidence: str) -> None:
    """Soft WARN (never blocks) when a cross-module change's VERIFY evidence
    lacks a live-smoke token. Mock-only coverage hides cross-module contract bugs."""
    if not cfg["verify"].get("cross_module_smoke", True):
        return
    mods = _modules_in_diff(cfg)
    if len(mods) < 2:
        return
    ev = evidence.lower()
    if any(t.lower() in ev for t in cfg["verify"].get("smoke_tokens", [])):
        return
    print(f"WARN: VERIFY evidence does not acknowledge a live cross-module smoke for a\n"
          f"      change touching {len(mods)} modules. Mock-only coverage hides cross-module\n"
          f"      contract bugs. Include ONE smoke token in your evidence, or an explicit\n"
          f"      deferral / 'live infra unavailable: <reason>'. (Soft warning - phase IS complete.)",
          file=sys.stderr)


# ── sizing ───────────────────────────────────────────────────────────

def _expected_size(files: int, logic: int, side_effects: int):
    if logic <= 1:   base = 0
    elif logic <= 3: base = 1
    elif logic <= 6: base = 2
    elif logic <= 12: base = 3
    else:            base = 4
    if files >= 6 and logic >= files:   # genuine depth across breadth → +1 tier
        base = min(4, base + 1)
    floor = 0
    if side_effects >= 1: floor = max(floor, 1)
    if side_effects >= 2: floor = max(floor, 2)
    return SIZES[max(base, floor)], floor


# ── commands ─────────────────────────────────────────────────────────

def cmd_size(cfg, args):
    if len(args) < 4:
        fail("Usage: size <XS|S|M|L|XL> <files> <logic> <side_effects> [context_pct]")
    size = args[0].upper()
    if size not in SIZES:
        fail(f"Invalid size '{size}'.")
    files, logic, se = int(args[1]), int(args[2]), int(args[3])
    context_pct = int(args[4]) if len(args) > 4 else None
    expected, floor = _expected_size(files, logic, se)
    if SIZES.index(size) < floor:
        fail(f"Cannot undersize below the RISK floor: {se} side effect(s) require at least "
             f"{SIZES[floor]} (breadth can be discounted; risk cannot).")
    state = load_state()
    state["size"] = size
    state["size_counts"] = {"files": files, "logic": logic, "side_effects": se}
    if context_pct is not None:
        state["context_pct"] = context_pct
    save_state(state)
    skips = SKIPPABLE.get(size, set())
    print(f"OK: classified {size} (files={files}, logic={logic}, side_effects={se})")
    if SIZES.index(size) < SIZES.index(expected):
        print(f"  NOTE: complexity suggests ~{expected}; sized down to {size} (breadth-discounted - OK).")
    print(f"  Allowed skips: {', '.join(sorted(skips)) or '(none)'}")
    if context_pct is not None and context_pct >= 80:
        print(f"  BUDGET: context {context_pct}% - checkpoint/commit at the next risk boundary.")


def cmd_phase(cfg, args):
    if not args:
        fail("Usage: phase <name>")
    phase = args[0].lower()
    if phase not in PHASES:
        fail(f"Unknown phase '{phase}'. Valid: {', '.join(PHASES)}")
    idx = PHASES.index(phase)
    state = load_state()
    size = state.get("size")
    if size is None:
        fail("Task size not classified. Run: size <XS|S|M|L|XL> <files> <logic> <side_effects>")
    current_idx = state.get("current_phase_index", -1) or -1
    skippable = SKIPPABLE.get(size, set())
    done = completed_phases(state)
    for i in range(current_idx + 1, idx):
        p = PHASES[i]
        if p in done or p in skippable:
            continue
        frm = f"'{PHASES[current_idx]}'" if current_idx >= 0 else "(start)"
        fail(f"Phase '{p}' not completed and not auto-skippable for '{size}'. "
             f"Cannot jump from {frm} to '{phase}'.")
    state["current_phase"] = phase
    state["current_phase_index"] = idx
    state["last_transition"] = _now()
    state.setdefault("started_at", _now())
    save_state(state)
    print(f"OK: entered '{phase}' ({idx + 1}/{len(PHASES)})")


def cmd_complete(cfg, args):
    if len(args) < 2:
        fail("Usage: complete <phase> \"<evidence>\"")
    phase, evidence = args[0].lower(), args[1]
    state = load_state()
    completed = [p for p in state.get("phases_completed", []) if p["phase"] != phase]
    ts = _now()
    completed.append({"phase": phase, "completed_at": ts, "evidence": evidence})
    state["phases_completed"] = completed
    if phase == "verify":
        state["verify_evidence"] = evidence
    save_state(state)
    print(f"OK: phase '{phase}' complete")
    if phase == "verify":
        _check_live_smoke(cfg, evidence)
    if state.get("amaw_enabled"):
        slug = _normalize_slug(state.get("task") or "unnamed-task")
        _log_audit(cfg, {"ts": ts, "task": slug, "phase": phase, "agent": "main",
                         "action": "phase_complete", "evidence": evidence})
        if phase == "retro":
            _record_lesson(cfg, f"Sprint complete: {slug}",
                           f"Phase: retro\nCompleted: {ts}\nEvidence: {evidence}",
                           ["workflow", "sprint", slug])


def cmd_check(cfg, args):
    if not args:
        fail("Usage: check <phase>")
    phase = args[0].lower()
    if phase in completed_phases(load_state()):
        print(f"OK: '{phase}' is completed")
    else:
        print(f"NOT COMPLETED: '{phase}'")
        sys.exit(1)


def cmd_skip(cfg, args):
    if len(args) < 2:
        fail("Usage: skip <phase> \"<reason>\"")
    phase, reason = args[0].lower(), args[1]
    state = load_state()
    state.setdefault("phases_skipped", []).append(
        {"phase": phase, "reason": reason, "skipped_at": _now()})
    completed = [p for p in state.get("phases_completed", []) if p["phase"] != phase]
    completed.append({"phase": phase, "completed_at": _now(), "evidence": f"SKIPPED: {reason}"})
    state["phases_completed"] = completed
    save_state(state)
    print(f"OK: phase '{phase}' skipped (reason: {reason})")


def cmd_amaw_enable(cfg, args):
    state = load_state()
    if state.get("amaw_enabled"):
        print(f"OK: AMAW already enabled for '{state.get('task') or '(unnamed)'}' (no-op)")
        return
    state["amaw_enabled"] = True
    state["amaw_enabled_at"] = _now()
    if args:
        state["task"] = _normalize_slug(args[0])
    save_state(state)
    print(f"OK: AMAW enabled for '{state.get('task') or '(unnamed)'}' (audit → {cfg['paths']['audit']})")


def cmd_pre_commit(cfg, args):
    if not STATE_FILE.exists():
        print("WARNING: no workflow state found. Proceeding without enforcement.")
        sys.exit(0)
    done = completed_phases(load_state())
    for phase, msg in COMMIT_GATES:
        if phase not in done:
            print(f"\n{'=' * 50}\n  COMMIT BLOCKED: {msg}\n{'=' * 50}")
            print(f"\n  Fix: workflow-gate.py complete {phase} \"<evidence>\"")
            print(f"  Or:  workflow-gate.py skip {phase} \"<reason>\"\n")
            sys.exit(1)
    print("OK: pre-commit passed (verify + post-review + session complete)")
    sys.exit(0)


def cmd_status(cfg, args):
    state = load_state()
    done = completed_phases(state)
    skipped = {p["phase"] for p in state.get("phases_skipped", [])}
    current = state.get("current_phase")
    counts = state.get("size_counts", {})
    print(f"Task: {state.get('task') or '(unnamed)'}")
    print(f"Size: {state.get('size', 'NOT SET')} (files={counts.get('files', 0)}, "
          f"logic={counts.get('logic', 0)}, side_effects={counts.get('side_effects', 0)})")
    print(f"AMAW: {'ENABLED' if state.get('amaw_enabled') else 'disabled (default)'}")
    print(f"Current phase: {current or 'none'}\n")
    for p in PHASES:
        marker = "[S]" if p in skipped else "[x]" if p in done else "[>]" if p == current else "[ ]"
        print(f"  {marker} {p}")


def cmd_reset(cfg, args):
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    swept = 0
    for stale in (STATE_FILE.parent if str(STATE_FILE.parent) else Path(".")).glob(f"{STATE_FILE.name}.*.tmp"):
        stale.unlink(missing_ok=True)
        swept += 1
    print("OK: workflow state reset." + (f" (swept {swept} tmp)" if swept else ""))


def cmd_slices(cfg, args):
    """/warp independence gate - propagates the slice-manifest validator's exit
    code (0 clean / 1 BLOCK). Requires the warp validator alongside this engine."""
    if not args:
        fail("Usage: slices <manifest.yaml|.json>")
    script = Path(__file__).resolve().parent.parent.parent / "warp" / "slice-manifest-validate.py"
    if not script.exists():
        fail(f"slice-manifest validator not found: {script} (port the warp scripts first).")
    sys.exit(subprocess.run([sys.executable, str(script), *args]).returncode)


COMMANDS = {
    "size": cmd_size, "phase": cmd_phase, "complete": cmd_complete, "check": cmd_check,
    "skip": cmd_skip, "pre-commit": cmd_pre_commit, "status": cmd_status, "reset": cmd_reset,
    "amaw-enable": cmd_amaw_enable, "slices": cmd_slices,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: workflow-gate.py {" + "|".join(COMMANDS) + "} [args]")
        print("Model: ai/rules/task-workflow.md   Config: workflow.config.json (optional)")
        sys.exit(1)
    COMMANDS[sys.argv[1]](load_config(), sys.argv[2:])


if __name__ == "__main__":
    main()
