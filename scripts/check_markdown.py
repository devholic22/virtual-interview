# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py==4.0.0"]
# ///
"""Fail when Markdown emphasis markers remain visible in rendered prose.

Run: uv run scripts/check_markdown.py
Code blocks and inline code are excluded by the CommonMark parser.
"""
from pathlib import Path
import sys

from markdown_it import MarkdownIt


def visible_markers(source: str):
    parser = MarkdownIt("commonmark")
    for block in parser.parse(source):
        if block.type != "inline":
            continue
        for token in block.children or []:
            if token.type == "text" and ("**" in token.content or "__" in token.content):
                yield (block.map[0] + 1 if block.map else 1), token.content.strip()


def main() -> int:
    # Guard the specific Korean punctuation regression and code exceptions.
    assert list(visible_markers("**샤드 키(파티션 키)**는 기준이다."))
    assert not list(visible_markers("**샤드 키**(파티션 키)는 기준이다."))
    assert not list(visible_markers("`**literal**`\n\n```\n**literal\n```"))
    root = Path(__file__).resolve().parents[1]
    errors = []
    paths = [path for path in sorted(root.rglob("*.md")) if ".git" not in path.parts]
    for path in paths:
        for line, text in visible_markers(path.read_text(encoding="utf-8")):
            errors.append(f"{path.relative_to(root)}:{line}: {text[:180]}")
    if errors:
        print("FAIL: emphasis markers remain visible in Markdown prose.")
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(paths)} Markdown files; no visible emphasis markers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
