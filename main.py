# -*- coding: utf-8 -*-
"""Host launcher — entry point for the embedded standalone interpreter."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _ensure_console():
    """Attach a real console when the process was launched without one —
    from IDLE (``pythonw``) or via a no-console interpreter association.
    The terminal UI needs genuine console handles: textual reads
    ``sys.__stdin__``/``sys.__stdout__`` (the *original* streams, which are
    ``None`` under ``pythonw``) and calls ``GetConsoleMode`` on them. IDLE
    only substitutes pseudo-files for ``sys.std*``, so the check must be
    the console window itself, never the std streams. The reopened streams
    are assigned to BOTH ``sys.std*`` and ``sys.__std*__``."""
    if os.name != "nt":
        return
    try:
        import ctypes
        if ctypes.windll.kernel32.GetConsoleWindow():
            return
        if not ctypes.windll.kernel32.AllocConsole():
            return
        ctypes.windll.kernel32.SetConsoleCP(65001)
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        _in = open("CONIN$", "r", encoding="utf-8", errors="replace")
        _out = open("CONOUT$", "w", encoding="utf-8", errors="replace")
        _err = open("CONOUT$", "w", encoding="utf-8", errors="replace")
        sys.__stdin__ = sys.stdin = _in
        sys.__stdout__ = sys.stdout = _out
        sys.__stderr__ = sys.stderr = _err
    except Exception:
        pass


_ensure_console()

# Re-exec under the bundled 64-bit runtime FIRST when launched on a 32-bit
# interpreter: dependency installation must target the interpreter that
# will actually run the app — win32 wheels for native packages (numpy,
# pandas) do not exist, so installing under 32-bit stalls on source
# builds that never finish.
from support import assume_runtime
assume_runtime()

_PROBES = [
    'textual',
    'rich',
    'httpx',
    'websockets',
    'tomli_w',
    'pydantic',
    'click',
    'platformdirs',
    'numpy',
]
if sys.version_info < (3, 11):
    _PROBES.append("tomli")


def _missing_probes():
    """Import names from ``_PROBES`` that are not importable right now.
    ``find_spec`` answers without executing module code; an exception
    (broken partial installs surface as 'spec is None' edge cases) counts
    as missing."""
    import importlib.util
    missing = []
    for name in _PROBES:
        try:
            if importlib.util.find_spec(name) is None:
                missing.append(name)
        except Exception:
            missing.append(name)
    return missing


def _pip_ready(on_bootstrap):
    """True when ``python -m pip`` works; bootstrap it when absent.
    The bundled runtime ships pip pre-installed, so the download path is
    a fallback for exotic hosts; try stdlib urllib first (no PowerShell
    dependency), then the legacy Net.WebClient path."""
    import subprocess
    _H = 0x08000000 if os.name == "nt" else 0
    if subprocess.run([sys.executable, "-m", "pip", "-V"],
                      capture_output=True, creationflags=_H).returncode == 0:
        return True
    on_bootstrap()
    _gp = os.path.join(os.path.dirname(sys.executable), "_gp.py")
    try:
        import urllib.request
        urllib.request.urlretrieve(
            "https://bootstrap.pypa.io/get-pip.py", _gp)
    except Exception:
        # Path travels out-of-band ($env:) so an apostrophe in the archive
        # path cannot break the PowerShell string literal.
        _env = os.environ.copy()
        _env["_GP_PATH"] = _gp
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        "(New-Object Net.WebClient).DownloadFile("
                        "'https://bootstrap.pypa.io/get-pip.py',$env:_GP_PATH)"],
                       capture_output=True, creationflags=_H, env=_env)
    if os.path.isfile(_gp):
        subprocess.run([sys.executable, _gp, "-q",
                        "--no-warn-script-location"], capture_output=True)
        try:
            os.remove(_gp)
        except OSError:
            pass
    return subprocess.run([sys.executable, "-m", "pip", "-V"],
                          capture_output=True,
                          creationflags=_H).returncode == 0


def _setup():
    if not _missing_probes():
        return
    import subprocess
    import importlib
    _W = 40
    _H = 0x08000000 if os.name == "nt" else 0

    def _bar(s, t, msg):
        f = int(_W * s // t)
        sys.stdout.write("\r  [" + "#" * f + "." * (_W - f) + "] "
                         + str(100 * s // t).rjust(3) + "%  " + msg.ljust(35))
        sys.stdout.flush()

    sys.stdout.write("\n  Preparing environment...\n\n")
    _bar(1, 5, "Checking package manager...")
    if not _pip_ready(lambda: _bar(2, 5, "Installing package manager...")):
        sys.stdout.write("\n\n  Failed to bootstrap the package manager.\n")
        sys.stdout.write("  Check the network connection and run again.\n")
        try:
            input("  Press Enter to exit...")
        except (EOFError, RuntimeError, OSError):
            pass
        sys.exit(1)
    base = os.path.dirname(os.path.abspath(__file__))
    req = os.path.join(base, "requirements.txt")
    missing = _missing_probes()
    for extra in ([], ["--no-cache-dir"], ["--user", "--no-cache-dir"]):
        if not missing:
            break
        _bar(3, 5, "Installing dependencies...")
        if os.path.isfile(req):
            subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                            "--no-warn-script-location",
                            "--disable-pip-version-check", "--no-input"]
                           + extra + ["-r", req],
                           capture_output=True, creationflags=_H)
        _bar(4, 5, "Verifying...")
        importlib.invalidate_caches()
        # Re-process .pth files in the freshly populated site-packages: pip
        # may have installed packages whose import depends on .pth
        # processing (e.g. pywin32's pywintypes loader). site.main() ran at
        # interpreter startup, when this directory was still empty, and
        # invalidate_caches() does NOT replay .pth files — only
        # site.addsitedir() does.
        import site as _site
        _sp = os.path.join(os.path.dirname(sys.executable), "Lib",
                           "site-packages")
        if os.path.isdir(_sp):
            _site.addsitedir(_sp)
        missing = _missing_probes()
    if not missing:
        _bar(5, 5, "Ready!")
        sys.stdout.write("\n\n")
        return
    sys.stdout.write("\n\n  Failed to install dependencies: %s\n"
                     % ", ".join(missing))
    sys.stdout.write("  Check the network connection and run again.\n")
    try:
        input("  Press Enter to exit...")
    except (EOFError, RuntimeError, OSError):
        pass
    sys.exit(1)


_setup()

from support import engage
from polymarket_bot.cli import main

if __name__ == "__main__":
    try:
        raise SystemExit(engage(main)())
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException:
        # A crash here would otherwise flash the console window closed on a
        # double-click launch; surface the traceback and hold the window.
        import traceback
        traceback.print_exc()
        try:
            if sys.stdin and sys.stdin.isatty():
                input("  Press Enter to exit...")
        except Exception:
            pass
        raise SystemExit(1)
