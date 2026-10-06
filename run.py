"""Run one lesson with the root project's shared Python environment."""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Hedge Fund Mini lesson")
    parser.add_argument("--lesson", type=int, required=True, help="Lesson number, such as 1 or 2")
    parser.add_argument("--ticker", required=True, help="Ticker to use for the lesson")
    args = parser.parse_args()

    matches = sorted(path for path in ROOT.glob(f"{args.lesson:02d}-*") if path.is_dir())
    if len(matches) != 1:
        parser.error(f"Expected one directory for lesson {args.lesson}; found {len(matches)}")

    lesson_dir = matches[0]
    lesson_file = lesson_dir / "lesson.py"
    if not lesson_file.is_file():
        parser.error(f"No lesson entrypoint found in {lesson_dir.name}")

    # Put the selected lesson first so imports resolve to its own files.
    sys.path.insert(0, str(lesson_dir))
    lesson = runpy.run_path(str(lesson_file))
    lesson["run"](ticker=args.ticker)


if __name__ == "__main__":
    main()
