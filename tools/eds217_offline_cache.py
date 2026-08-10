"""
Transparent local cache for URL-based pandas reads (EDS 217 authoring aid).

Course materials keep writing plain:

    pd.read_csv('https://example.org/data.csv')

This module wraps pandas.read_csv and pandas.read_excel so that a string
argument beginning with http:// or https:// is served from a local cache
directory when a copy exists, and downloaded (then cached) when it does not.
Nothing in the course materials changes, and nothing depends on whether you
currently have a network connection.

This is an INSTRUCTOR-SIDE tool. It is installed into the IPython startup
directory on one machine. Students never load it and see ordinary pandas.

Environment variables
---------------------
EDS217_CACHE_DIR      cache location (default: ~/.eds217-data-cache)
EDS217_CACHE_MODE     auto     cache first, download on miss (default)
                      refresh  always download, overwrite the cache
                      off      passthrough, no caching at all
EDS217_CACHE_VERBOSE  set to 1 to print a line per intercepted read
"""

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

__all__ = ["cache_dir", "index", "fetch", "status", "install"]

_UA = "Mozilla/5.0 (compatible; eds217-cache/1.0)"
_INDEX_NAME = "index.json"
_installed = False


def cache_dir() -> Path:
    d = Path(os.environ.get("EDS217_CACHE_DIR", Path.home() / ".eds217-data-cache"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _mode() -> str:
    return os.environ.get("EDS217_CACHE_MODE", "auto").strip().lower()


def _verbose() -> bool:
    return os.environ.get("EDS217_CACHE_VERBOSE", "").strip() in {"1", "true", "yes"}


def _say(msg: str) -> None:
    if _verbose():
        print(f"[eds217-cache] {msg}", file=sys.stderr)


def _index_path() -> Path:
    return cache_dir() / _INDEX_NAME


def index() -> dict:
    p = _index_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except (ValueError, OSError):
        return {}


def _write_index(idx: dict) -> None:
    tmp = _index_path().with_suffix(".json.tmp")
    tmp.write_text(json.dumps(idx, indent=2, sort_keys=True))
    tmp.replace(_index_path())


def _cache_path(url: str) -> Path:
    """Stable, human-readable filename. Extension preserved so pandas can
    still infer compression and format from the name."""
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    tail = url.split("?")[0].rstrip("/").split("/")[-1] or "data"
    suffix = "".join(Path(tail).suffixes[-2:]) or ".csv"
    stem = Path(tail).name[: len(Path(tail).name) - len(suffix)] or "data"
    stem = "".join(c if (c.isalnum() or c in "-_") else "_" for c in stem)[:48]
    return cache_dir() / f"{stem}-{digest}{suffix}"


def _download(url: str, dest: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = resp.read()
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(payload)
    tmp.replace(dest)
    idx = index()
    idx[url] = {"file": dest.name, "bytes": len(payload)}
    _write_index(idx)
    return dest


def fetch(url: str, force: bool = False) -> Path:
    """Return a local path for `url`, downloading it if needed."""
    dest = _cache_path(url)
    if dest.exists() and not force:
        return dest
    return _download(url, dest)


def _resolve(url: str) -> object:
    """Map a URL to a local path, or hand back the URL if we cannot."""
    mode = _mode()
    if mode == "off":
        return url

    dest = _cache_path(url)

    if mode == "refresh":
        try:
            _say(f"refresh {url}")
            return _download(url, dest)
        except Exception as exc:
            if dest.exists():
                _say(f"refresh failed ({exc}); using cached copy")
                return dest
            raise

    # mode == "auto": cache first
    if dest.exists():
        _say(f"cache hit  {url}")
        return dest

    try:
        _say(f"cache miss {url} (downloading)")
        return _download(url, dest)
    except Exception as exc:
        raise OSError(
            f"eds217-cache: no local copy of\n    {url}\n"
            f"and the download failed ({exc.__class__.__name__}: {exc}).\n"
            f"Cache directory: {cache_dir()}\n"
            f"Run `python tools/warm_cache.py` while online to populate it."
        ) from exc


def _wrap(func):
    def wrapper(filepath_or_buffer=None, *args, **kwargs):
        target = filepath_or_buffer
        if isinstance(target, str) and target[:8].lower().startswith(("http://", "https://")):
            target = _resolve(target)
        return func(target, *args, **kwargs)

    wrapper.__name__ = getattr(func, "__name__", "read")
    wrapper.__doc__ = getattr(func, "__doc__", None)
    wrapper.__wrapped__ = func
    wrapper._eds217_cached = True
    return wrapper


def install() -> bool:
    """Patch pandas readers. Safe to call more than once."""
    global _installed
    if _installed:
        return True
    try:
        import pandas as pd
    except ImportError:
        return False
    for name in ("read_csv", "read_excel"):
        func = getattr(pd, name, None)
        if func is not None and not getattr(func, "_eds217_cached", False):
            setattr(pd, name, _wrap(func))
    _installed = True
    return True


def status() -> str:
    idx = index()
    return (
        f"eds217 offline cache: mode={_mode()} "
        f"dir={cache_dir()} entries={len(idx)}"
    )
