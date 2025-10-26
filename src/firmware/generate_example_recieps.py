#!/usr/bin/env python3
"""Utility to bundle default recipe JSON files into a single Python module.

This script scans the default_recipes directory for ``.recipe`` or ``.recieps``
files, leverages ``static_modules.recipe`` to parse them into ``recipe.recipe``
objects, and emits helper functions into
``src/firmware/src/static_modules/example_recipes.py`` (directory is created on
demand).

Usage:
    python src/firmware/generate_example_recieps.py

You can override the input or output locations via ``--input-dir`` and
``--output``. Run with ``--help`` for details.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
from typing import Iterable
import secrets

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_ROOT = SCRIPT_DIR.parent
STATIC_MODULES_ROOT = SCRIPT_DIR / "src"
STATIC_MODULES_DIR = STATIC_MODULES_ROOT / "static_modules"
DEFAULT_RECIPES_DIR = SCRIPT_DIR / ".." / "recipes"
DEFAULT_OUTPUT_PATH = STATIC_MODULES_DIR  / "example_recipes.py"

if str(STATIC_MODULES_ROOT) not in sys.path:
    sys.path.insert(0, str(STATIC_MODULES_ROOT))

from static_modules import recipe as recipe_module  # type: ignore


ACTION_INT_TO_CONST = {
    recipe_module.USER_INTERACTION_MODE.SCALE: "recipe.USER_INTERACTION_MODE.SCALE",
    recipe_module.USER_INTERACTION_MODE.CONFIRM: "recipe.USER_INTERACTION_MODE.CONFIRM",
    recipe_module.USER_INTERACTION_MODE.WAIT: "recipe.USER_INTERACTION_MODE.WAIT",
}

ACTION_STR_TO_CONST = {
    "SCALE": ACTION_INT_TO_CONST[0],
    "CONFIRM": ACTION_INT_TO_CONST[1],
    "WAIT": ACTION_INT_TO_CONST[2],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert .recipe/.recieps files into a single Python module."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_RECIPES_DIR,
        help="Directory containing .recipe/.recieps files (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Destination Python module path (default: %(default)s)",
    )
    return parser.parse_args()


def find_recipe_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")

    candidates: Iterable[Path] = list(directory.glob("*.recipe")) + list(
        directory.glob("*.recieps")
    )
    files = sorted({path.resolve() for path in candidates})
    return list(files)


def load_recipe(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON for {path.name}") from exc


def sanitize_identifier(name: str) -> str:
    identifier = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    identifier = identifier.strip("_")
    if not identifier:
        identifier = "RECIPE"
    if identifier[0].isdigit():
        identifier = f"RECIPE_{identifier}"
    return identifier.upper()


def format_categories(raw_categories: Iterable[str] | None) -> str:
    categories = list(raw_categories or ["everything"])
    return "[" + ", ".join(repr(category) for category in categories) + "]"


def normalize_action(action: int | str | None, source_name: str) -> str:
    if isinstance(action, int):
        if action in ACTION_INT_TO_CONST:
            return ACTION_INT_TO_CONST[action]
    elif isinstance(action, str):
        key = action.strip().upper()
        if key in ACTION_STR_TO_CONST:
            return ACTION_STR_TO_CONST[key]

    raise ValueError(f"Unsupported action value {action!r} in {source_name}")


def format_step(step: "recipe_module.recipe_step", source_name: str) -> list[str]:
    action_expr = normalize_action(step.action, source_name)
    ingredient_literal = repr(getattr(step, "ingredient_name", ""))
    text_literal = repr(getattr(step, "current_step_text", ""))
    amount_value = getattr(step, "target_value", 0)
    if amount_value is None:
        amount_value = 0
    return [
        "    recipe_obj.add_step(recipe.recipe_step(",
        f"        _action={action_expr},",
        f"        _ingredient_name={ingredient_literal},",
        f"        _current_step_text={text_literal},",
        f"        _target_value={int(amount_value)},",
        "    ))",
    ]


def build_recipe_function(
    recipe_obj: "recipe_module.recipe", source_path: Path
) -> tuple[str, list[str]]:
    display_name = recipe_obj.name or source_path.stem.replace("_", " ")
    description = recipe_obj.description
    version = recipe_obj.version
    categories_literal = format_categories(recipe_obj.get_categories())
    function_suffix = sanitize_identifier(source_path.stem)
    function_name = f"RECIPES_COLLECTION_{function_suffix}"

    lines: list[str] = [
        f"def {function_name}() -> recipe.recipe:",
        f"    recipe_obj: recipe.recipe = recipe.recipe({repr(display_name)}, {repr(description)}, {repr(version)}, {categories_literal})",
    ]

    steps = getattr(recipe_obj, "steps", []) or []
    if steps:
        for step in steps:
            lines.extend(format_step(step, source_path.name))
    else:
        lines.append("    # This recipe has no steps; add them manually if required.")

    lines.extend(
        [
            "    recipe_obj.valid = True",
            "    return recipe_obj",
        ]
    )

    return function_name, lines


def render_module(recipe_functions: list[tuple[str, list[str]]]) -> str:
    lines: list[str] = [
        "# Auto-generated by generate_example_recieps.py; do not edit manually.",
        "import recipe",
        "",
    ]

    function_names: list[str] = []
    for function_name, body_lines in recipe_functions:
        function_names.append(function_name)
        lines.extend(body_lines)
        lines.append("")  # separate functions with a blank line

    if function_names:
        joined_calls = ",\n        ".join(f"{name}()" for name in function_names)
        lines.extend(
            [
                "def GET_EXAMPLE_RECIPES_COLLECTION() -> list[recipe.recipe]:",
                "    return [",
                f"        {joined_calls}",
                "    ]",
            ]
        )
    else:
        lines.extend(
            [
                "def GET_EXAMPLE_RECIPES_COLLECTION() -> list[recipe.recipe]:",
                "    return []",
            ]
        )

    lines.append("")  # ensure trailing newline
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    recipe_files = find_recipe_files(args.input_dir)
    secure_random = secrets.SystemRandom()  
    num_to_select = min(10, len(recipe_files))
    list_of_random_items = secure_random.sample(recipe_files, num_to_select)
    recipe_functions: list[tuple[str, list[str]]] = []

    for recipe_path in list_of_random_items:
        recipe_data = load_recipe(recipe_path)
        categories = recipe_data.get("categories") or ["everything"]
        recipe_obj = recipe_module.recipe(
            _name=recipe_data.get("name", "Recipe"),
            _description=recipe_data.get("description", "A nice cocktail"),
            _version=recipe_data.get("version", "1.0.0"),
            _categories=categories,
        )
        recipe_obj.from_dict(recipe_data)
        recipe_functions.append(build_recipe_function(recipe_obj, recipe_path))

    module_text = render_module(recipe_functions)

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(module_text, encoding="utf-8")

    try:
        display_path = output_path.relative_to(SRC_ROOT.parent)
    except ValueError:
        display_path = output_path

    print(f"Wrote {len(recipe_functions)} recipe helper(s) to {display_path}")


if __name__ == "__main__":
    main()
