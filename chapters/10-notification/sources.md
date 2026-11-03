# 책 대조 범위와 출처

제공된 책 사진 10장 165~181쪽(IMG_0823~IMG_0839)과 사용자 메모를 대조했다. 채널·연락처 등록·단일 서버의 한계·채널별 큐와 작업자·안정성·템플릿·설정·제한·재시도·모니터링의 순서를 바탕으로 재구성했다. 문장과 그림은 복습을 위한 자체 설명이며 책 그림의 복제본이 아니다.

일일 전송량은 책의 시간 단위를 따른다. 아웃박스·결과 미확인·멱등성 범위·콜백 순서·재시도 예산·작업자 증설 판단은 실패 경계를 이해하기 위한 보충 설명이다. “소실되면 안 된다”는 목표는 내구성 있게 접수한 처리 의무와 실제 단말 수신을 구분했다. “앱 키·시크릿으로 보안”은 신뢰할 수 있는 서버의 전송 자격 증명과 API 권한 검사로 구체화했다.

- [APNs 전송 요청](https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns): 요청과 최선형 전달 특성.
- [APNs 앱 등록](https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns): 앱·단말별 토큰과 서버 등록.
- [FCM 서버 환경](https://firebase.google.com/docs/cloud-messaging/server-environment): 신뢰할 수 있는 발신 서버와 자격 증명.
- [FCM 대규모 전송](https://firebase.google.com/docs/cloud-messaging/scale-fcm): 혼잡 제어·429·백오프와 재시도 분산.
- [Twilio 메시지 상태](https://www.twilio.com/docs/messaging/api/message-resource#message-status-values): 접수·전송·배달 결과 구분.
- [RabbitMQ 확인 방식](https://www.rabbitmq.com/docs/confirms): 발행 확인과 소비 확인의 경계.
- [AWS 트랜잭션 아웃박스](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html): DB와 메시지 발행의 이중 쓰기 문제.
- [You Cannot Have Exactly-Once Delivery](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)와 [후속 글](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery-redux/): 전달과 처리 효과의 보장 범위를 구분하여 읽는다.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 동일하게 그림의 구성 방식과 아이콘 표현을 참고했다.

평균 처리량·적체 해소 수치는 설명용 계산이다. 특정 업체의 현재 계약 한도나 실측 성능을 뜻하지 않는다. 실제 설계에서는 채널·계정·지역별 한도와 제공되는 배달 확인 기능을 별도로 확인해야 한다.
