#!/usr/bin/env python3
"""new-project.py - assemble a new project from a recipe.

Reads a recipe, copies the catalog pieces it references into an output directory,
then substitutes {{ variable }} placeholders in file CONTENTS and in file/dir NAMES
(scaffolder-fill, per ADR-003). Author-time <...> blanks are left untouched. One-shot
scaffolder (ADR-004): it does not track or update the generated project afterwards.

Zero-dependency (stdlib). Recipes are JSON (canonical) or YAML (if PyYAML installed).

Usage:
  new-project.py --list
  new-project.py --recipe <name> --name <project> --out <dir> [--var key=value ...]

A recipe (recipes/<name>/recipe.{json,yaml}):
  {
    "name": "go-minimal",
    "description": "...",
    "variables": { "project_name": {"required": true}, "go_module": {"required": true} },
    "pieces": [ { "src": "templates/languages/go", "dest": "." } ]
  }
Each piece copies a collection path (file or dir) to <out>/<dest>. The template
usually has dest ".". --name sets project_name; --var overrides any variable.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Collection root = parent of this script's directory (scripts/..).
ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
VAR_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


def die(msg: str) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_recipe(name: str) -> dict:
    base = RECIPES / name
    for fn in (f"{name}.json", "recipe.json", f"{name}.yaml", "recipe.yaml", "recipe.yml"):
        p = base / fn if (base / fn).exists() else RECIPES / fn
        if p.exists():
            text = p.read_text(encoding="utf-8")
            if p.suffix == ".json":
                import json
                return json.loads(text)
            try:
                import yaml  # type: ignore
            except ImportError:
                die(f"{p.name} is YAML but PyYAML is not installed. Install pyyaml or "
                    f"provide a recipe.json.")
            return yaml.safe_load(text) or {}
    die(f"recipe '{name}' not found under {RECIPES}")


def list_recipes() -> int:
    if not RECIPES.exists():
        print("(no recipes/ directory)")
        return 0
    found = sorted({p.parent.name for p in RECIPES.glob("*/recipe.*")}
                   | {p.stem for p in RECIPES.glob("*.json")})
    if not found:
        print("(no recipes found)")
        return 0
    print("Available recipes:")
    for n in found:
        try:
            r = load_recipe(n)
            print(f"  {n:28s} {r.get('description', '')}  [{r.get('maturity', 'n/a')}]")
        except SystemExit:
            print(f"  {n}")
    return 0


def resolve_vars(recipe: dict, name: str | None, overrides: dict) -> dict:
    spec = recipe.get("variables", {}) or {}
    values: dict = {}
    for var, meta in spec.items():
        meta = meta or {}
        if "default" in meta:
            values[var] = str(meta["default"])
    if name is not None:
        values["project_name"] = name
    values.update(overrides)
    missing = [v for v, m in spec.items()
               if (m or {}).get("required") and not values.get(v)]
    if missing:
        die(f"missing required variable(s): {', '.join(missing)} "
            f"(pass via --name and/or --var key=value)")
    return values


def substitute(text: str, values: dict) -> str:
    return VAR_RE.sub(lambda m: values.get(m.group(1), m.group(0)), text)


def copy_piece(src_rel: str, dest_rel: str, out: Path) -> None:
    src = ROOT / src_rel
    if not src.exists():
        die(f"piece source not found in collection: {src_rel}")
    dest = out / dest_rel
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for item in src.rglob("*"):
            rel = item.relative_to(src)
            target = dest / rel
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def render_tree(out: Path, values: dict) -> int:
    """Substitute {{ var }} in contents, then rename paths containing {{ var }}.
    Returns the number of files whose contents changed."""
    changed = 0
    # 1. contents (skip binary: undecodable files are left as-is)
    for f in out.rglob("*"):
        if f.is_file():
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                continue
            new = substitute(text, values)
            if new != text:
                f.write_text(new, encoding="utf-8")
                changed += 1
    # 2. names (deepest first so child renames don't invalidate parent paths)
    for p in sorted(out.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if VAR_RE.search(p.name):
            new_name = substitute(p.name, values)
            if new_name != p.name:
                p.rename(p.with_name(new_name))
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble a new project from a recipe.")
    ap.add_argument("--list", action="store_true", help="list available recipes")
    ap.add_argument("--recipe", help="recipe name")
    ap.add_argument("--name", help="project name (sets {{project_name}})")
    ap.add_argument("--out", help="output directory (must not exist or be empty)")
    ap.add_argument("--var", action="append", default=[], metavar="KEY=VALUE",
                    help="set/override a variable (repeatable)")
    args = ap.parse_args()

    if args.list or not args.recipe:
        return list_recipes()

    overrides = {}
    for kv in args.var:
        if "=" not in kv:
            die(f"--var must be KEY=VALUE, got '{kv}'")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = v
    if not args.out:
        die("--out <dir> is required")
    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        die(f"--out '{out}' exists and is not empty")

    recipe = load_recipe(args.recipe)
    values = resolve_vars(recipe, args.name, overrides)
    pieces = recipe.get("pieces", [])
    if not pieces:
        die(f"recipe '{args.recipe}' has no `pieces`")

    out.mkdir(parents=True, exist_ok=True)
    for piece in pieces:
        copy_piece(piece["src"], piece.get("dest", "."), out)
    changed = render_tree(out, values)

    print(f"OK: created {out} from recipe '{args.recipe}'")
    print(f"  variables: {', '.join(f'{k}={v}' for k, v in values.items())}")
    print(f"  pieces: {len(pieces)} · files rendered: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
