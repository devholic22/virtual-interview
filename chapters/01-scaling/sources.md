# 범위와 근거

## 책 대조 범위

제공된 『가상 면접 사례로 배우는 대규모 시스템 설계 기초』 1장 이미지의 인쇄 p.1–30을 기준으로 주제 누락을 확인했다. 원문 이미지나 장 전체 전사는 저장소에 넣지 않았다. 본문은 독립적인 학습 설명이며 세부 설계 제안은 책의 주장과 구분한다.

| 책의 주제 | 인쇄 쪽수 | 저장소에서 읽을 곳 |
| --- | --- | --- |
| 단일 서버, DNS, 요청 흐름 | 1–3 | 핵심 개념 §1 |
| DB와 DB 선택 | 4–5 | 핵심 개념 §2, 질문 01 |
| 수직·수평 확장 | 5–6 | 핵심 개념 §3 |
| 로드 밸런서 | 6–7 | 핵심 개념 §4, 질문 04 |
| 데이터베이스 다중화 | 7–10 | 핵심 개념 §5, 질문 02·03 |
| 캐시 계층과 고려사항 | 11–13 | 핵심 개념 §6, 질문 05 |
| CDN과 고려사항 | 13–17 | 핵심 개념 §7 |
| 무상태 웹 계층 | 17–20 | 핵심 개념 §8 |
| 데이터 센터 | 20–22 | 핵심 개념 §9 |
| 메시지 큐 | 22–23 | 핵심 개념 §10, 질문 02 |
| 로그·메트릭·자동화 | 23–25 | 핵심 개념 §11 |
| DB 수직 확장·샤딩 | 25–28 | 핵심 개념 §12, 질문 01 |
| 확장 구성과 핵심 원칙 | 29–30 | 핵심 개념 §13 |

개념과 추가 학습은 장별 README 한 문서에 모았다. 현재 완성 범위는 **1장**이며 다른 장의 요약 완료를 뜻하지 않는다.

## 외부 자료 — 2026-11-02 확인

- [Scaling Memcache at Facebook — USENIX 논문](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf): 2013년 사례. §2의 look-aside와 삭제, §3.2.1의 lease, §4.1의 로그 기반 무효화, §5의 다중 지역·marker·일관성 모델. 현재의 모든 Meta 시스템에 일반화하지 않는다.
- [Cache made consistent — Meta, 2022](https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/): 캐시 채움·무효화 경쟁, 버전 정보 퇴거, 운영상 일관성 관측.
- [Transactional outbox — AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html): 이중 쓰기, 이벤트 의도와 업무 데이터의 DB 트랜잭션, 중복·순서, CDC.
- [Redis key eviction](https://redis.io/docs/latest/develop/reference/eviction/): 메모리 한도와 퇴거 정책. FIFO를 Redis 제공 정책이라고 서술한 것이 아니다.
- [HTTP caching — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching): 공유·개인 캐시, 헤더, 재검증.
- [CloudFront expiration](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html): TTL, 재검증, 조기 퇴거와 제품별 정책.
- [CloudFront invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html): 무효화와 버전 파일의 차이.
- [CloudFront cache key](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html): 요청의 구분 정보와 적중률.
- [PostgreSQL replication](https://www.postgresql.org/docs/current/warm-standby.html): 동기·비동기·계단식 복제.
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html): 조건부 갱신과 동시 실행.
- [DynamoDB latency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TroubleshootingLatency.html): 단건 작업 지연과 실제 요청 지연의 구분.
- [DynamoDB partitions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html): 자동 파티션 관리.
- [DynamoDB partition keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html): 키·부하 분산.
- [NGINX load balancing](https://nginx.org/en/docs/http/load_balancing.html): 알고리즘과 활성 연결.
- [Kafka design](https://kafka.apache.org/41/design/design/): 파티션·소비·전달과 순서 관련 설명.

## 그림

책의 관계를 참고해 새로 배치한 설명용 개념도다. 원본 도판의 복제나 실제 서비스 배포도는 아니다. [stack-diagram](https://github.com/caru-ini/stack-diagram) 템플릿과 Lucide 아이콘으로 만들었다. DB 읽기를 파란 점선으로 표시한 범례와 순서도의 세로 점선은 각 그림의 설명 규칙이다. 점선이 비동기라는 뜻은 아니다.

Outbox·CDC·버전·TTL의 조합, 재고 처리 예시와 장애 시험 항목은 이 저장소의 추가 학습·설계 제안이다. 이를 모두 Facebook 논문의 구현으로 소개하지 않는다.
