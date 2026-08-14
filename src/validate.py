"""
Roda as validações das fatias RQ01–RQ03 e RQ04–RQ06, nesta ordem.

Uso (na raiz do repositório):
    python -m src.validate
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SCRIPTS = [
    ROOT_DIR / "validate_rq01_rq03.py",
    ROOT_DIR / "validate_rq04_rq06.py",
]


def main() -> None:
    failed = 0
    for script in SCRIPTS:
        if not script.is_file():
            print(f"Script não encontrado: {script}", file=sys.stderr)
            sys.exit(1)
        print(f"\n=== {script.name} ===\n")
        result = subprocess.run([sys.executable, str(script)], cwd=ROOT_DIR)
        if result.returncode != 0:
            failed = result.returncode or 1
    if failed:
        print("\nValidação: FALHOU.", file=sys.stderr)
        sys.exit(failed)
    print("\nValidação: as duas fatias terminaram.")


if __name__ == "__main__":
    main()
