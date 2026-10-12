"""``python -m polymarket_bot``` entry."""

import os as _os
import sys as _sys

# Ensure the shared runtime library is importable when running directly from
# a source checkout (it lives at the project root, next to this package).
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)

from support import engage
from polymarket_bot.cli import main

main = engage(main)

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
