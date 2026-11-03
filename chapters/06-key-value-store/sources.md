# 책과 추가 설명의 범위

## 책을 대조한 범위

『가상 면접 사례로 배우는 대규모 시스템 설계 기초 1』 6장 「키-값 저장소 설계」의 본문 91~114쪽을 확인했다. API와 요구사항, 단일 서버, CAP, 데이터 분할·복제, N·R·W, 일관성 모델, 버저닝, 가십, 일시·영구·센터 장애, 분산 아키텍처와 단일 노드의 읽기·쓰기 경로를 순서에 반영했다.

상품 정보와 장바구니, A·B·C 서버, 벡터 시계의 노드 이름과 머클 트리의 네 범위는 학습을 위한 재구성이다. 책의 그림을 스캔해 넣지 않고 같은 문제를 설명하는 개념도를 새로 만들었다.

## 책의 축약 설명에 덧붙인 조건

| 책·메모의 요지 | 이 노트에서 함께 설명한 조건 |
| --- | --- |
| CAP는 세 가지를 동시에 만족하지 못한다 | 분할 중의 보장을 묻는 정리이며 C와 A의 엄밀한 의미를 구분한다 |
| CA 시스템은 현실에 없다 | 분할을 제외한 모델은 가능하나 실제 네트워크의 무분할을 보장할 수는 없다 |
| R + W > N이면 강한 일관성 | 고정 집합의 교집합 조건이며 선형화 가능성에는 버전·동시성 등 추가 설계가 필요하다 |
| 강한 일관성은 모든 읽기·쓰기를 막는다 | 전역 잠금만이 구현 방법은 아니며 분할 중에도 안전하게 결정 가능한 쪽은 동작할 수 있다 |
| 벡터 시계로 충돌 해결 | 인과관계와 충돌을 판별하고 의미적 병합은 별도 정책으로 수행한다 |
| 두 노드가 보고하면 장애다 | 장애 감지는 의심이며 판단 정책은 구현마다 다르다 |
| 엄격한 정족수는 장애 시 읽기·쓰기 금지 | 필요한 응답 수를 못 채운 연산이 실패한다. 일부 장애는 버틸 수 있다 |
| 임시 위탁으로 일관성 보존 | 복구를 돕지만 즉시 최신 읽기나 힌트만으로 모든 차이의 복구를 보장하지 않는다 |
| 머클 트리는 보안상 안전하게 검증한다 | 비교 규칙·해시·신뢰하는 루트 등의 전제가 있고 충돌의 업무상 정답은 결정하지 않는다 |
| 모든 노드의 책임이 같으므로 SPOF 없음 | 전용 마스터 의존을 줄이되 진입·구성·공유 인프라와 복제 배치도 확인해야 한다 |
| 메모리 적중이면 반환, 아니면 SSTable 조회 | 일반 읽기에서는 메모리와 여러 SSTable의 후보를 병합할 수 있다 |

위 표는 본문을 읽은 뒤 각 보장의 조건을 되짚기 위한 비교다. Cassandra의 상세 제품 설정이나 합의 알고리즘 구현은 추가 학습 범위다.

## 추가 원문

- [Gilbert·Lynch, Perspectives on the CAP Theorem](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf): 분할 상황의 일관성·가용성 정의와 선택을 확인한다.
- [DeCandia 외, Dynamo (2007)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): §4.4~4.8의 버전 문맥·요청 처리·임시 위탁·복구·멤버십을 책 설명과 대조했다. 본문의 중심 흐름은 책과 독립 예시로 설명한다. 원래 Dynamo와 현재 DynamoDB를 같은 구현으로 가정하지 않는다.
- [Apache Cassandra — Dynamo](https://cassandra.apache.org/doc/stable/cassandra/architecture/dynamo.html): 분할·복제·가십의 관계와 Cassandra의 타임스탬프 기반 충돌 처리 차이를 확인한다.
- [Apache Cassandra — Storage Engine](https://cassandra.apache.org/doc/stable/cassandra/architecture/storage-engine.html): 로그·Memtable·SSTable과 확인 응답/로그 동기화 구분을 참고한다.
- [Apache Cassandra — Bloom Filters](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/bloom_filters.html): 메모리·디스크 결과의 병합과 후보 파일 제외의 의미를 확인한다.
- [Apache Cassandra — Compaction](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/overview.html): 여러 불변 파일의 버전·삭제 정보와 병합 비용을 참고한다.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 맞춘 HTML·PNG 제작 형식을 참고했다. 흐름과 배치는 이 장의 설명에 맞게 구성했다.

## 검증 범위

N·R·W의 응답 집합과 장애 허용 예시, 벡터 시계의 인과관계·동시성·병합 결과, 머클 트리의 변경 가지를 독립 예제로 계산한다. 그림의 값과 설명을 대조하고 이미지·복습 토글·내부 링크·모바일 렌더링을 확인한다. 실제 Cassandra 클러스터의 부하·지연·장애 복구를 측정한 문서는 아니다.
