# 책 대조 범위와 출처

제공된 책 사진 15장 277~299쪽(IMG_0936~IMG_0958)과 사용자 메모를 대조했다. 단일 서버 → 객체 저장소·API·메타데이터 분리 → 충돌·블록 처리·일관성·데이터 모델 → 업로드·다운로드·알림 → 보관·장애의 흐름으로 재구성했다. 문장과 그림은 복습을 위한 자체 설명이다.

서버 최신 버전의 일관성과 오프라인 단말 반영을 구분했다. “NoSQL은 ACID 미지원”, “메모리 캐시는 최종 일관성”이라는 일괄 단정은 제품과 프로토콜의 조건으로 보완했다. 객체 저장소의 지역 내 보장과 비동기 지역 복제를 구분하고, 여러 블록·DB의 버전 공개·조건부 확정·캐시 경쟁·단말 커서·참조 회수는 보충 설명으로 넣었다.

- [S3 저장 클래스](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html): 다중 AZ·단일 AZ 등 저장 범위의 차이.
- [S3 복제](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html): 지역 내·지역 간 객체 복제의 비동기 특성.
- [S3 일관성 모델](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel): 객체 읽기 일관성과 단일 키 원자성의 범위.
- [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html): 명시적 버전 보관과 삭제·덮어쓰기 복구.
- [DynamoDB 트랜잭션](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html): NoSQL 제품의 ACID 지원 사례다. 모든 제품·배포 범위에 일반화하지 않는다.
- [Dropbox Streaming File Synchronization](https://dropbox.tech/infrastructure/streaming-file-synchronization): 2014년 공개 사례의 블록 목록·네임스페이스·변경 저널·단말별 진행 위치를 참고했다. 당시 최적화나 수치를 현재 제품의 보장으로 사용하지 않았다.
- [Google Drive 변경 조회](https://developers.google.com/workspace/drive/api/guides/manage-changes): 공개 API의 변경 목록·페이지 토큰 사례이며 내부 구현 전체를 뜻하지 않는다.
- [10장 알림 시스템](../10-notification/README.md): 아웃박스·재시도·알림의 복구 경계.
- [12장 채팅](../12-chat/README.md): 다중 단말의 안전한 동기화 위치와 연결 복구.
- [stack-diagram](https://stacks.caru.moe/): 기존 장과 같은 그림 구성 방식과 아이콘 표현을 참고했다.

용량·QPS는 책의 추가 가정에 따른 추정이다. 500PB는 할당량 합계이며 실제 물리 사용량이 아니다. A·B·C 블록, v7·v8 버전, 단말 커서는 설명용 모델이다. 예시 검증은 실제 클라우드·DB의 장애 복구나 성능 벤치마크를 대신하지 않는다.
