# 책과 추가 설명의 범위

사용자가 제공한 4장 메모와 책의 인쇄 p.51–74를 바탕으로 흐름을 재구성했다. 본문은 원문 전사가 아니며 그림도 새로 그린 학습용 설명이다. 숫자와 상품 API 예시는 원리를 따라가기 위한 가정이다.

| 책의 흐름 | 인쇄 쪽수 | 이 문서의 연결 |
| --- | --- | --- |
| 목적·요구사항·제한 위치 | 51–56 | 본문 §1–2 |
| 토큰 버킷·누출 버킷 | 56–60 | 본문 §3–4, 질문 01 |
| 고정·이동 윈도 | 60–65 | 본문 §5–8 |
| 공유 상태·규칙·거부 응답·아키텍처 | 65–69 | 본문 §9–11 |
| 경쟁 조건·공유 판정·성능·모니터링 | 69–73 | 본문 §10·12–13, 질문 02 |
| 재시도 등 추가 고려사항 | 74 | 본문 §13, 질문 03 |

## 메모를 읽을 때 구분한 내용

- 토큰 버킷의 버스트는 남은 권한의 즉시 사용이다. 보충·검사·차감의 동시성은 따로 보장한다.
- Shopify의 leaky bucket 설명을 모든 API의 실제 FIFO 대기 구현으로 일반화하지 않는다.
- 이동 윈도 로그는 책의 ‘추가 후 검사’와 이 노트의 ‘허용 요청만 기록’ 변형을 구분한다.
- 이동 윈도 카운터의 계산값은 6.5이며 책의 내림 설명과 현재 요청을 포함하는 판정 규칙을 구분한다.
- Redis의 공유·명령별 원자성·판정 전체의 원자성·장애 후 내구성을 각각 구분한다.
- HTTP의 `Retry-After`, 서비스별 `X-RateLimit-*` 예시, 접수와 완료의 의미를 구분한다.
- 에지의 낮은 지연과 전역 한도의 정확성을 동시에 당연히 얻는다고 설명하지 않는다.

## 공식 자료 — 2026-11-03 확인

- [Redis Lua 실행](https://redis.io/docs/latest/develop/programmability/eval-intro/): 스크립트 실행의 원자성과 실행 중 대기.
- [Redis INCR](https://redis.io/docs/latest/commands/incr/): 카운터 증가와 조건부 만료 설정의 경쟁 사례.
- [Redis ZADD](https://redis.io/docs/latest/commands/zadd/): 고유 멤버와 점수 갱신의 의미.
- [Redis 트랜잭션](https://redis.io/docs/latest/develop/using-commands/transactions/): 명령 실행·오류·롤백의 구분.
- [Redis Cluster 사양](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/): 여러 키와 해시 슬롯, 권위 있는 노드로의 라우팅.
- [Redis 복제](https://redis.io/docs/latest/operate/oss_and_stack/management/replication/): 비동기 복제와 장애 전환 관련 한계.
- [Shopify API limits](https://shopify.dev/docs/api/usage/limits): API별 제한과 leaky bucket 설명.
- [HTTP 429 — RFC 6585 §4](https://www.rfc-editor.org/rfc/rfc6585.html#section-4): 제한 응답과 Retry-After.
- [AWS 멱등 API와 재시도](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/): 요청 식별과 중복 업무 처리 방지.
- [AWS 타임아웃·백오프·지터](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): 실패 시 재시도의 시간·부하 관리.
- [RabbitMQ 확인 응답](https://www.rabbitmq.com/docs/confirms): 발행 접수 확인과 소비 확인의 구분.

fail-open·로컬 비상 예산·다중 지역 예산과 중간 통신 실패의 업무 예시는 이 노트의 추가 설계 설명이다. 실제 정책은 보호할 자원과 실패 시 허용할 손실을 정한 뒤 선택한다.

## 검증과 한계

버킷·윈도 경계·이동 로그·가중 카운터의 숫자 예시를 계산으로 확인했다. Lua 예제는 로컬 모의 Redis와 Lua 실행 환경에서 100개 동시 판정 중 한도 7개만 허용하는지, 만료와 저장 상태가 맞는지 확인했다. 실제 Redis 클러스터의 부하·통신 단절·복제 장애를 시험했다는 뜻은 아니다. 코드는 판정 원리를 위한 학습용이다.

그림은 [stack-diagram](https://github.com/caru-ini/stack-diagram) 템플릿과 Lucide 아이콘을 사용했다. 알고리즘의 시간 그림은 별도 표시가 없는 한 개념적 배치이며 실제 요청 분포를 측정한 자료가 아니다.
