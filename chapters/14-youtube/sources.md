# 책 대조 범위와 출처

제공된 책 사진 14장 247~275쪽(IMG_0906~IMG_0934)과 사용자 메모를 대조했다. 요구사항·규모 추정 → 원본 업로드와 메타데이터 → 스트리밍 → 트랜스코딩·DAG·자원 관리 → 속도·보호·비용 → 오류·확장 순서로 재구성했다. 문장과 그림은 복습을 위한 자체 설명이다.

GOP·업로드 파트·재생 세그먼트의 차이, 큐와 입력 의존성, ready의 게시 조건, 멱등한 완료·삭제와의 경쟁, CDN과 지속 원본의 구분, 암호화와 권한, 직접 제공 비용의 조건은 보충 설명이다. 책의 과거 서비스 통계·클라우드 단가는 현재 값으로 인용하지 않았다.

- [S3 사전 서명 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html): 객체·동작·만료 범위와 반복 사용·덮어쓰기 조건.
- [S3 멀티파트 업로드](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html): 바이트 파트의 독립 업로드·실패 파트 재전송·완성과 정리.
- [S3 이벤트 알림](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html): 최소 한 번 전달과 중복 처리의 경계.
- [Apple HLS 개요](https://developer.apple.com/library/archive/referencelibrary/GettingStarted/AboutHTTPLiveStreaming/about/about.html): 보관 문서에서 변형·목록·세그먼트·적응형 재생의 기본 흐름을 참고했다. 오래된 코덱·세그먼트 길이 예시를 모든 현재 단말의 필수 설정으로 사용하지 않았다.
- [RFC 8216](https://www.rfc-editor.org/rfc/rfc8216.html): HLS 목록·미디어 세그먼트·클라이언트 동작을 설명하는 RFC다. 최신 제품별 지원 전체를 대신하는 자료는 아니다.
- [MediaConvert GOP 설명](https://docs.aws.amazon.com/mediaconvert/latest/ug/video-quality.html): 프레임 참조와 GOP·품질·호환성의 관계.
- [CloudFront 비공개 콘텐츠](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html): CDN 서명 접근과 원본 우회 방지.
- [10장 알림 시스템](../10-notification/README.md): 아웃박스·재시도·중복 처리 경계를 연결한다.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 같은 그림 구성 방식과 아이콘 표현을 참고했다.

비디오 크기·업로드 비율·시청 횟수·평균 비트레이트는 계산의 가정이다. 3.375PB와 7.5PB는 서로 다른 가정에 따른 전송량이며 실제 서비스 관측값이 아니다. 워크플로 예시 검증은 실제 클라우드 장애·코덱 호환성·성능 벤치마크를 대신하지 않는다.
