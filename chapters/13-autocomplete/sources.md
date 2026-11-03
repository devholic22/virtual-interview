# 책 대조 범위와 출처

제공된 책 사진 13장 223–244쪽(IMG_0882–IMG_0903)과 사용자 메모를 대조했다. 요구사항·규모 추정 → 빈도 테이블 → 트라이·상위 목록 캐시 → 수집·집계·빌드 → 질의 서비스 → 갱신·삭제·샤딩 → 국가·다국어·실시간 확장의 흐름으로 재구성했다. 그림과 문장은 복습을 위한 자체 설명이다.

O(1)의 고정 상한 전제, 자동완성 조회와 검색 실행의 구분, 집계 재처리·표본 오차, 스냅샷 검증·버전 전환·롤백, 캐시 미스 집중, 응답 역전, 삭제 후 후보 보충, 샤드 top-k 병합 조건은 보충 설명이다. 샤딩의 26대 한계는 단순한 첫 글자 고정 배치의 조건으로 한정했다.

- [PostgreSQL 인덱스 문서](https://www.postgresql.org/docs/current/indexes-types.html): 접두어 LIKE 조건에 B-tree 인덱스를 사용할 수 있는 조건과 로캘 관련 제약을 확인했다. 접두어 조회와 빈도 정렬을 구분하는 데 사용했다.
- [Elasticsearch completion 설명](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/search-suggesters#completion-suggester): 조회를 빠르게 하기 위한 메모리 검색 구조와 빌드 비용의 제품 사례다. 본문의 단순 트라이와 동일한 구현으로 일반화하지 않는다.
- [Unicode 정규화 FAQ](https://unicode.org/faq/normalization.html): 같은 문자의 조합 표현을 일관되게 다루는 배경이다. 정규화와 맞춤법 자동수정을 구분한다.
- [1장 규모 확장](../01-scaling/README.md): 캐시·DB·샤딩·장애 경계를 연결한다.
- [11장 뉴스 피드](../11-news-feed/README.md): 미리 계산한 후보·현재 필터·분산 조회의 교환 관계를 연결한다.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 같은 그림 구성 방식과 아이콘 표현을 참고했다.

책의 24,000 평균 QPS·48,000 피크 QPS는 가정에 따른 근삿값이다. 하루 0.4GB는 문자열 중심의 단순 추정이며 실제 로그·트라이·복제 용량과 다르다. bag 등의 단어·빈도와 버전·샤드 배치는 설명용 예시다. 알고리즘 예시 검증은 제품 벤치마크나 실제 분산 장애 시험을 대신하지 않는다.
