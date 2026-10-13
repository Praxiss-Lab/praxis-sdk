"""MkDocs hooks for the Praxis documentation site.

The site lives on the ``documentation`` branch. Links to repository files outside
``docs/`` (README, source code, examples) point to their location on ``main``.
"""

import posixpath
import re
from pathlib import Path


_LINK = re.compile(r"(\]\()([^)\s]+)(\))")
_ALERT = re.compile(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
_ADMONITION = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "info",
    "WARNING": "warning",
    "CAUTION": "danger",
}
_EXTERNAL = ("http://", "https://", "mailto:", "#", "/")


def _rewrite(
    target: str, page_dir: str, docs_dir: Path, repo_root: Path, base: str
) -> str:
    if target.startswith(_EXTERNAL):
        return target
    path, sep, fragment = target.partition("#")
    resolved = posixpath.normpath(posixpath.join(page_dir, path))
    if not resolved.startswith("../"):
        # Inside docs/: a directory README is served as that directory's index.
        if posixpath.basename(resolved) == "README.md":
            index = posixpath.join(posixpath.dirname(resolved), "index.md")
            if (docs_dir / index).exists():
                return posixpath.relpath(index, page_dir) + sep + fragment
        return target
    repo_path = posixpath.normpath(posixpath.join("docs", resolved))
    local = repo_root / repo_path
    # The documentation branch holds only the site, so infer directories from the path.
    is_dir = local.is_dir() if local.exists() else not posixpath.splitext(path)[1]
    kind = "tree" if is_dir else "blob"
    return f"{base}/{kind}/main/{repo_path}{sep}{fragment}"


def _convert_alerts(markdown: str) -> str:
    """Render GitHub ``> [!WARNING]`` alerts as Material admonitions."""
    out, lines, i = [], markdown.split("\n"), 0
    while i < len(lines):
        match = _ALERT.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        out.append(f"!!! {_ADMONITION[match.group(1)]}")
        out.append("")
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            body = lines[i][1:]
            out.append("    " + body[1:] if body.startswith(" ") else "    " + body)
            i += 1
        out.append("")
    return "\n".join(out)


def on_page_markdown(markdown, page, config, **_kwargs):
    docs_dir = Path(config["docs_dir"])
    repo_root = docs_dir.parent
    base = config["repo_url"].rstrip("/")
    page_dir = posixpath.dirname(page.file.src_uri)

    def replace(match):
        return (
            match.group(1)
            + _rewrite(match.group(2), page_dir, docs_dir, repo_root, base)
            + match.group(3)
        )

    out, in_fence = [], False
    for line in _convert_alerts(markdown).splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        out.append(line if in_fence else _LINK.sub(replace, line))
    return "".join(out)
