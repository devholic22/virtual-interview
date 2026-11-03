"""Assemble each chapter into its README without separate reading pages."""
from pathlib import Path
import posixpath
import re
import sys

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


PARTS_FOUR = [
    ("core-concepts", "요청을 제한하는 흐름 따라 읽기", "concepts.md"),
    ("q1", "질문 01 · 토큰 버킷의 버스트와 동시성", "questions/01-token-bucket.md"),
    ("q2", "질문 02 · Lua와 정렬 집합의 원자적 판정", "questions/02-atomic-redis.md"),
    ("q3", "질문 03 · 중간 통신 실패와 재시도", "questions/03-network-failures.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


PARTS_FIVE = [
    ("core-concepts", "서버 변경에서 해시 링과 가상 노드까지", "concepts.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


PARTS_SIX = [
    ("core-concepts", "단일 서버에서 복제·일관성·복구까지", "concepts.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


PARTS_SEVEN = [
    ("core-concepts", "후보 비교에서 스노우플레이크와 운영 조건까지", "concepts.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


PARTS_EIGHT = [
    ("core-concepts", "생성과 리다이렉션의 흐름 따라 읽기", "concepts.md"),
    ("q1", "질문 01 · 블룸 필터로 DB를 얼마나 대신할 수 있을까?", "questions/01-bloom-filter.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


PARTS_NINE = [
    ("core-concepts", "발견·수집·재수집의 흐름 따라 읽기", "concepts.md"),
    ("q1", "질문 01 · 호스트 수와 논리 큐·작업자 수", "questions/01-host-queues.md"),
    ("q2", "질문 02 · 블룸 필터가 반복 등장하는 이유", "questions/02-bloom-filter.md"),
    ("q3", "질문 03 · 안정 해시의 공통 목적", "questions/03-consistent-hashing.md"),
    ("review", "스스로 답하기 · 답안 토글", "review.md"),
    ("sources", "책과 추가 설명의 범위", "sources.md"),
]


def build(chapter, parts, intro=None):
    anchors = {str((chapter / path).resolve()): anchor for anchor, _, path in parts}
    anchors[str((chapter / "README.md").resolve())] = "contents"
    pieces = [
        '<a id="top"></a>\n\n# 1장. 사용자 수에 따른 규모 확장성\n\n'
        "작은 상품 판매 서비스가 커진다고 가정한다. 서버 한 대에서 시작해, "
        "문제가 생길 때마다 구성을 하나씩 바꾸며 이유와 동작을 따라간다. "
        "책 1장의 흐름을 바탕으로 재구성한 학습 노트다.\n\n"
        "앞부분은 요청이 어떤 경로로 처리되는지 이해하는 본문이다. "
        "그 뒤의 질문별 심화는 그 구성에서 더 궁금해지는 이유와 실패 사례를 다룬다. "
        "설명·그림·복습 답안은 이 README 안에서 함께 볼 수 있다.\n\n"
        '<a id="contents"></a>\n\n## 목차\n\n'
        + "\n".join(f"- [{label}](#{anchor})" for anchor, label, _ in parts)
        + "\n\n---\n"
    ]
    if intro is not None:
        pieces[0] = intro + "\n".join(f"- [{label}](#{anchor})" for anchor, label, _ in parts) + "\n\n---\n"
    for anchor, _, relative in parts:
        source = chapter / relative
        text = source.read_text(encoding="utf-8")

        def link(match):
            image, label, url = match.groups()
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) or url.startswith("#"):
                return match.group(0)
            target = (source.parent / url.split("#")[0]).resolve()
            dest = "#" + anchors[str(target)] if str(target) in anchors else posixpath.relpath(str(target), str(chapter))
            if str(target) not in anchors and "#" in url:
                dest += "#" + url.split("#", 1)[1]
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
    (chapter / "README.md").write_text("\n".join(pieces), encoding="utf-8")
    print(f"Built {chapter.relative_to(ROOT)}/README.md")


def main():
    targets = sys.argv[1:] or ["1", "4", "5", "6", "7", "8", "9"]
    if any(value not in {"1", "4", "5", "6", "7", "8", "9"} for value in targets):
        raise SystemExit("Usage: python3 scripts/build_chapter.py [1|4|5|6|7|8|9 ...]")
    if "1" in targets:
        build(CHAPTER, PARTS)
    if "4" in targets:
        intro = (
            '<a id="top"></a>\n\n# 4장. 처리율 제한 장치의 설계\n\n'
            "상품 API에 요청이 몰리는 상황에서 출발해, 어디서 무엇을 세고 언제 허용할지 따라간다. "
            "사용자가 제공한 메모와 책 4장의 흐름을 바탕으로 정리한 학습 노트다.\n\n"
            "기본 알고리즘 뒤에는 토큰 차감의 동시성, Redis의 원자적 판정, "
            "게이트웨이·큐 중간의 통신 실패를 따로 살펴본다. 설명·그림·복습 답안을 이 문서에서 함께 읽는다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/04-rate-limiter", PARTS_FOUR, intro)

    if "5" in targets:
        intro = (
            '<a id="top"></a>\n\n# 5장. 안정 해시 설계\n\n'
            "상품 캐시 서버 한 대가 빠졌는데 정상 서버의 키까지 목적지가 바뀌는 상황에서 출발한다. "
            "해시 링으로 변경 범위를 줄이고, 가상 노드로 분포의 편차를 완화하는 과정을 따라간다.\n\n"
            "기본 개념·그림·복습 답안을 이 문서에서 함께 읽는다. "
            "책 5장과 제공된 메모를 바탕으로 재구성했으며 추가 설명의 범위는 마지막에 구분한다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/05-consistent-hashing", PARTS_FIVE, intro)

    if "6" in targets:
        intro = (
            '<a id="top"></a>\n\n# 6장. 키-값 저장소 설계\n\n'
            "메모리 해시 테이블 한 대에서 출발해 데이터를 나누고 복제한 뒤, "
            "서로 다른 사본을 읽고 고치는 과정까지 따라간다. "
            "마지막에는 한 복제 노드 내부의 로그·메모리·파일 경로를 살펴본다.\n\n"
            "책 6장과 제공된 메모를 바탕으로 재구성했다. "
            "개념·그림·실제 답안이 든 복습 토글을 이 README에서 함께 읽는다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/06-key-value-store", PARTS_SIX, intro)

    if "7" in targets:
        intro = (
            '<a id="top"></a>\n\n# 7장. 분산 시스템을 위한 유일 ID 생성기 설계\n\n'
            "여러 주문 서버가 서로 겹치지 않는 ID를 만드는 문제에서 출발한다. "
            "후보들을 비교한 뒤 64비트의 역할을 나누고, 같은 밀리초·시계 이상·재시작 때도 "
            "유일성의 조건을 지키는 과정을 따라간다.\n\n"
            "책 7장과 제공된 메모를 바탕으로 재구성했다. "
            "개념·그림·복습 답안을 이 README에서 함께 읽는다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/07-unique-id", PARTS_SEVEN, intro)

    if "8" in targets:
        intro = (
            '<a id="top"></a>\n\n# 8장. URL 단축기 설계\n\n'
            "상품 페이지의 긴 주소를 등록해 짧은 링크를 만들고, "
            "그 링크를 누른 사용자를 원래 페이지로 보내는 과정을 따라간다. "
            "코드 생성·매핑 저장·캐시 조회를 설명한 뒤 블룸 필터의 활용과 한계를 살펴본다.\n\n"
            "책 8장과 제공된 메모를 바탕으로 재구성했다. "
            "개념·그림·심화 질문·복습 답안을 이 README에서 함께 읽는다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/08-url-shortener", PARTS_EIGHT, intro)

    if "9" in targets:
        intro = (
            '<a id="top"></a>\n\n# 9장. 웹 크롤러 설계\n\n'
            "검색용 페이지를 모으는 단순한 링크 탐색에서 출발해 "
            "우선순위·호스트 예절·실패 복구·재수집을 갖춘 흐름으로 확장한다. "
            "많은 논리 큐를 운영하는 방법과 블룸 필터·안정 해시의 공통 목적도 연결한다.\n\n"
            "책 9장과 제공된 메모를 바탕으로 재구성했다. "
            "개념·그림·심화 질문·복습 답안을 이 README에서 함께 읽는다.\n\n"
            '<a id="contents"></a>\n\n## 목차\n\n'
        )
        build(ROOT / "chapters/09-web-crawler", PARTS_NINE, intro)


if __name__ == "__main__":
    main()
