# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py==4.2.0"]
# ///
"""Reject exposed emphasis markers and unintended GitHub strikethrough.

Run: uv run scripts/check_markdown.py
GitHub accepts both single and double tilde delimiters. Code and link
destinations retain their literal syntax; table cells are parsed separately.
"""
from pathlib import Path
import re
import sys

from markdown_it import MarkdownIt


HTML_STRIKE = re.compile(r"</?(?:s|del|strike)\b|text-decoration\s*:\s*[^;\"']*line-through", re.I)


def visible_markers(source: str):
    parser = MarkdownIt("commonmark", {"strikethrough_single_tilde": True})
    parser.enable(["strikethrough", "table"])
    for block in parser.parse(source):
        line = block.map[0] + 1 if block.map else 1
        if block.type == "html_block" and HTML_STRIKE.search(block.content):
            yield line, "HTML 취소선: " + block.content.strip()
        if block.type != "inline":
            continue
        for token in block.children or []:
            if token.type == "s_open":
                yield line, "취소선으로 렌더링됨: " + block.content.strip()
            elif token.type == "text" and any(marker in token.content for marker in ("**", "__", "~~")):
                yield line, "서식 기호가 노출됨: " + token.content.strip()
            elif token.type == "html_inline" and HTML_STRIKE.search(token.content):
                yield line, "HTML 취소선: " + token.content.strip()


def main() -> int:
    # Real regressions: Korean punctuation, GitHub's single tilde, table cells,
    # inline-code boundaries, and HTML strike tags. Literal code/URLs stay valid.
    assert list(visible_markers("**샤드 키(파티션 키)**는 기준이다."))
    assert not list(visible_markers("**샤드 키**(파티션 키)는 기준이다."))
    assert list(visible_markers("0~9, a~z, A~Z 순서다."))
    assert list(visible_markers("0~31과 0~4095를 사용한다."))
    assert list(visible_markers("~~취소~~"))
    assert list(visible_markers("`a`~`z`와 `A`~`Z`다."))
    assert list(visible_markers("| 범위 |\n| --- |\n| 0~9, a~z |"))
    assert not list(visible_markers("| 비트 | 범위 |\n| --- | --- |\n| 5 | 0~31 |\n| 12 | 0~4095 |"))
    assert not list(visible_markers("0–9, a–z, A–Z 순서다."))
    assert not list(visible_markers(r"\~물결표\~"))
    assert not list(visible_markers("[자료](https://example.com/~name/)"))
    assert not list(visible_markers("`**literal**` `0~9` `~~literal~~` `<del>literal</del>`\n\n```\n**literal\n~literal~\n```"))
    assert not list(visible_markers("~~~text\n~literal~\n~~~"))
    assert list(visible_markers("<del>취소</del>"))
    assert list(visible_markers("<span style='text-decoration: line-through'>취소</span>"))
    root = Path(__file__).resolve().parents[1]
    errors = []
    paths = [path for path in sorted(root.rglob("*.md")) if ".git" not in path.parts]
    for path in paths:
        for line, text in visible_markers(path.read_text(encoding="utf-8")):
            errors.append(f"{path.relative_to(root)}:{line}: {text[:180]}")
    if errors:
        print("FAIL: exposed Markdown markers or unintended strikethrough.")
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(paths)} Markdown files; no exposed emphasis markers or unintended strikethrough (GitHub single/double tilde rules).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
