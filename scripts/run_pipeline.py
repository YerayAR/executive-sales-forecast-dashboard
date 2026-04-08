from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


def run(script_name: str) -> None:
    subprocess.run([sys.executable, str(SCRIPTS_DIR / script_name)], check=True)


def main() -> None:
    run("generate_sample_data.py")
    run("build_warehouse.py")
    run("train_forecast.py")


if __name__ == "__main__":
    main()
