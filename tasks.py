"""Convert local YAML task definitions to HUD Task objects for syncing.

Usage:
    hud sync tasks <your-taskset-name> tasks.py
    hud sync tasks <your-taskset-name> tasks.py --dry-run
"""

import glob
import os

import yaml
from hud.eval.task import Task

TASKS_DIR = os.path.join(os.path.dirname(__file__), "tasks")
DEFAULT_ENV = "liveweb-samples-env"
# Optional per-task args, passed through as-is (the login task uses these).
PASSTHROUGH_ARGS = ("credential_profile", "use_visual_grading")


def _load_yaml_tasks() -> list[Task]:
    yaml_files = sorted(glob.glob(os.path.join(TASKS_DIR, "*.yaml")))
    result: list[Task] = []
    seen_slugs: set[str] = set()

    for path in yaml_files:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        raw_tasks = data.get("tasks", []) if isinstance(data, dict) else data or []

        for t in raw_tasks:
            slug = t["name"]
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            rubric_items = [
                {"requirement": item.get("r", ""), "weight": item.get("w", 1)}
                for item in t.get("rubric", [])
            ]

            args: dict = {"prompt": t["prompt"], "url": t["url"]}
            if rubric_items:
                args["rubric_items"] = rubric_items
            for key in PASSTHROUGH_ARGS:
                if key in t:
                    args[key] = t[key]

            result.append(Task(
                env=t.get("env", DEFAULT_ENV),
                id="web-research",
                slug=slug,
                args=args,
            ))

    return result


tasks = _load_yaml_tasks()
