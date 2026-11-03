# 책 대조 범위와 출처

제공된 책 사진 12장 197–220쪽(IMG_0855–IMG_0878)과 사용자 메모를 대조했다. 요구사항 → 폴링·롱 폴링·WebSocket → 구성과 저장소 → 메시지 모델·서비스 탐색 → 1:1·다중 단말·그룹 흐름 → 접속 상태 → 장애와 확장 순서로 재구성했다. 그림과 문장은 복습을 위한 자체 설명이다.

5,000만은 책의 DAU이며 동시 연결 수가 아니다. HTTP 지속 연결·롱 폴링의 연결 재사용, ZooKeeper의 역할, SQL·NoSQL 선택 조건을 보완했다. 스노우플레이크와 엄격한 순서의 차이, 최대 관측 ID와 안전한 커서의 차이, 내구성 접수·후속 발행·중복 제거, 단말별 접속 상태와 늦은 종료 이벤트는 실패 경계를 설명하기 위한 추가 내용이다.

책이 인용한 과거의 Facebook·WhatsApp 메시지량은 현재 트래픽 수치로 재사용하지 않았다. Discord 등의 제품 사례도 아래 자료가 공개된 당시의 설계를 설명하며 모든 채팅 서비스의 필수 구성으로 일반화하지 않았다.

- [RFC 9112 지속 연결](https://www.rfc-editor.org/rfc/rfc9112.html#name-persistence): HTTP/1.1의 기본 연결 재사용과 요청·응답 경계.
- [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html): WebSocket 핸드셰이크·양방향 프레임·Ping/Pong 등의 프로토콜 경계.
- [ZooKeeper 프로그래머 가이드](https://zookeeper.apache.org/doc/r3.8.5/zookeeperProgrammers.html): 세션·임시 노드·서비스 등록에 활용할 조정 기능.
- [Discord 메시지 저장 사례](https://discord.com/blog/how-discord-stores-trillions-of-messages): 2023년 공개. 채널·시간 구간 파티션과 핫 파티션 등 저장·운영의 교환 관계.
- [Discord 검색 인덱스 사례](https://discord.com/blog/how-discord-indexes-trillions-of-messages): 2025년 공개. 이력 저장과 별개인 메시지 검색 인덱스 경로.
- [7장 유일 ID 생성기](../07-unique-id/README.md): 스노우플레이크 ID의 구성과 시계·유일성 조건.
- [10장 알림 시스템](../10-notification/README.md): 아웃박스·재시도·중복 효과의 경계.
- [11장 뉴스 피드](../11-news-feed/README.md): 수신자별 팬아웃과 읽기 비용의 교환 관계.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 같은 그림 구성 방식과 아이콘 표현을 참고했다.

연결당 메모리·그룹 팬아웃 수는 가정에 따른 계산이다. 실제 장비 처리량이나 업체의 현재 한도를 측정한 값은 아니다. 동기화 예시는 프로토콜의 조건을 설명하기 위한 모델이며 실제 분산 저장소의 장애·복제 보장을 검증한 구현은 아니다.
