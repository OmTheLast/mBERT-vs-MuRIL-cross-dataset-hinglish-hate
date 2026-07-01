#!/usr/bin/env python3
"""Mac Apple Silicon training entrypoint.

This wrapper enables MPS fallback and uses conservative defaults that are safer on
Mac laptops/desktops than CUDA-oriented settings.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    command = [
        sys.executable,
        str(ROOT / "experiments" / "train_transformer.py"),
        "--batch-size",
        "8",
        "--cleaning",
        "minimal",
        *sys.argv[1:],
    ]
    raise SystemExit(subprocess.call(command, cwd=ROOT, env=os.environ.copy()))


if __name__ == "__main__":
    main()
