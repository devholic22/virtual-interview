"""Assemble chapter 1 into its README without requiring separate reading pages."""
from pathlib import Path
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/01-scaling"
PARTS = [
    ("core-concepts", "서비스가 커지는 흐름 따라 읽기", "concepts.md"),
    ("q1", "질문 01 · NoSQL", "questions/01-nosql.md"),
    ("q2", "질문 02 · 쓰기 폭주", "questions/02-write-bursts.md"),
    ("q3", "질문 03 · 읽기 복제본", "questions/03-read-replicas.md"),
    ("q4", "질문 04 · 부하 분산", "questions/04-load-balancing.md"),
    ("q5", "질문 05 · DB와 캐시 일관성", "questions/05-cache-consistency.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책 대조 범위와 출처", "sources.md"),
]


def main():
    anchors = {str((CHAPTER / path).resolve()): anchor for anchor, _, path in PARTS}
    anchors[str((CHAPTER / "README.md").resolve())] = "contents"
    pieces = [
        '<a id="top"></a>\n\n# 1장. 사용자 수에 따른 규모 확장성\n\n'
        "작은 상품 판매 서비스가 커진다고 가정한다. 서버 한 대에서 시작해, "
        "문제가 생길 때마다 구성을 하나씩 바꾸며 이유와 동작을 따라간다. "
        "책 1장의 흐름을 바탕으로 재구성한 학습 노트다.\n\n"
        "앞부분은 요청이 어떤 경로로 처리되는지 이해하는 본문이다. "
        "그 뒤의 질문별 심화는 그 구성에서 더 궁금해지는 이유와 실패 사례를 다룬다. "
        "설명·그림·복습 답안은 이 README 안에서 함께 볼 수 있다.\n\n"
        '<a id="contents"></a>\n\n## 목차\n\n'
        + "\n".join(f"- [{label}](#{anchor})" for anchor, label, _ in PARTS)
        + "\n\n---\n"
    ]
    for anchor, _, relative in PARTS:
        source = CHAPTER / relative
        text = source.read_text(encoding="utf-8")

        def link(match):
            image, label, url = match.groups()
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) or url.startswith("#"):
                return match.group(0)
            target = (source.parent / url.split("#")[0]).resolve()
            dest = "#" + anchors[str(target)] if str(target) in anchors else posixpath.relpath(str(target), str(CHAPTER))
            return f"{image}[{label}]({dest})"

        text = re.sub(r"(!?)\[([^\]]*)\]\(([^)]+)\)", link, text)
        lines = []
        fenced = False
        for line in text.splitlines():
            if line.startswith("```"):
                fenced = not fenced
            if not fenced and re.match(r"#{1,5} ", line):
                line = "#" + line
            lines.append(line)
        pieces.append(
            f'\n<a id="{anchor}"></a>\n\n'
            + "\n".join(lines).strip()
            + "\n\n[목차로 돌아가기](#contents)\n\n---\n"
        )
    (CHAPTER / "README.md").write_text("\n".join(pieces), encoding="utf-8")
    print("Built chapters/01-scaling/README.md")


if __name__ == "__main__":
    main()
