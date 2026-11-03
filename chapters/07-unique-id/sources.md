# 책과 추가 설명의 범위

## 책을 대조한 범위

『가상 면접 사례로 배우는 대규모 시스템 설계 기초 1』 7장 「분산 시스템을 위한 유일 ID 생성기 설계」의 117~125쪽을 확인했다. 요구사항, 간격을 나누는 자동 증가, UUID, 티켓 서버, 스노우플레이크의 필드·시간·일련번호, 시계 동기화·비트 배분·가용성을 본문 흐름에 반영했다.

주문 서비스, 상대 시각 1000ms, 비트 합성 결과와 생성기 교체 상황은 독립적으로 만든 예시다. 도식은 책의 비교·비트 구조를 참고해 새로 구성했으며 원본 그림을 스캔해 넣지 않았다.

## 덧붙인 조건

- 자동 증가의 실제 처리 한계를 측정 없이 단정하지 않았다. 여러 발급 지점의 유일성·확장·지연 문제로 설명했다.
- UUIDv4와 UUIDv7을 구분했다. 128비트라는 크기와 16진수 문자열 표기 형식도 구분했다.
- 티켓 서버의 단순한 한 대 구성과 Flickr의 홀수·짝수 두 대 사례를 구분했다.
- 시간 정보로 정렬하는 것과 전역의 실제 발생·응답 순서는 다를 수 있음을 보완했다.
- 일련번호의 원자적 갱신, 소진, 시계 역행, 생성기 ID 소유권과 재시작·교체를 유일성의 조건으로 설명했다.
- 4096개/ms는 번호 공간의 상한이며 실제 성능 보장이 아니다. 69.7년은 epoch부터의 범위다.
- epoch만 바꾸는 것은 안전한 이관이 아님을 덧붙였다. 큰 정수의 전송 형식은 선택해서 읽을 수 있도록 접어 두었다.

## 추가 원문

- [Twitter의 원래 Snowflake IdWorker](https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala): 비트 이동과 생성 상태, 동기화, 소진 시 대기와 역행 시 거부를 대조한 과거 구현이다. 현재 사용을 권장하는 운영 라이브러리 목록은 아니다.
- [RFC 9562 — UUID](https://www.rfc-editor.org/rfc/rfc9562.html): §5.4의 무작위 UUIDv4와 §5.7의 시간 기반 UUIDv7을 확인했다.
- [MySQL — Replication Source Options and Variables](https://dev.mysql.com/doc/refman/8.4/en/replication-options-source.html): 자동 증가의 간격·시작 위치 설정을 참고했다.
- [Flickr — Ticket Servers (2010)](https://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/): 티켓 발급과 홀수·짝수 두 서버 구성을 비교했다.
- [ECMAScript — Number.MAX_SAFE_INTEGER](https://tc39.es/ecma262/#sec-number.max_safe_integer): 전송 시 정수 정밀도에 관한 추가 설명의 근거다.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 같은 HTML·PNG 제작 형식을 참고했다. 비트와 생성 분기는 설명에 맞춰 직접 배치했다.

## 검증 범위

본문의 정수 합성·분해, 필드 최댓값과 64비트 범위, 같은 밀리초의 일련번호·소진, 역행 시 거부, 생성기 구분, 시간순 해석과 epoch 범위를 독립적인 검증 모형으로 확인한다. 여러 스레드가 같은 상태를 안전하게 갱신하는 예시도 확인한다. 이는 문서의 계산과 안전 조건을 확인하는 것으로, 운영용 ID 서버를 구현하거나 실제 초당 발급량·장애 복구를 측정한 결과는 아니다.

이미지·복습 답안 토글·내부 링크·모바일 렌더링과 마크다운 표기도 검사한다.
