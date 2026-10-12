# -*- coding: utf-8 -*-
"""Lightweight diagnostics shim.

Tracing hooks are no-ops in release builds; the public names are
kept so callers need no conditional imports."""


def append(stage, status="info", **fields):
    """No-op in release builds."""
    return None


def append_error(stage, exc):
    """No-op in release builds."""
    return None


def path():
    """No journal is written in release builds; always None."""
    return None


__all__ = ["append", "append_error", "path"]


def last_reconcile_at():
    """ISO timestamp of the last successful reconciliation, or None."""
    return None
