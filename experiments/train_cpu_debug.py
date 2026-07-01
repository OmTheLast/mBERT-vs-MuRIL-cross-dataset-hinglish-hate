#!/usr/bin/env python3
"""Small CPU/debug training entrypoint for smoke tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    command = [
        sys.executable,
        str(ROOT / "experiments" / "train_transformer.py"),
        "--batch-size",
        "4",
        "--epochs",
        "1",
        "--max-samples",
        "256",
        "--cleaning",
        "minimal",
        *sys.argv[1:],
    ]
    raise SystemExit(subprocess.call(command, cwd=ROOT))


if __name__ == "__main__":
    main()
