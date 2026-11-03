# 그림 원본과 재생성

각 장 README의 그림은 [stack-diagram](https://stack-diagram.com/)의 템플릿·아이콘 타일·격자 배경을 바탕으로 만든다. JSON에서 구성 요소·관계·논리적 역할 그룹을 정의하고, 자체 완결 HTML에서 밝은 PNG와 어두운 PNG를 생성한다. 출력은 각 장의 `assets`에 두고, 공통 지식용 그림은 `fundamentals/assets`에 둔다.

연결선은 장애물이 없는 직선이나 간단한 직각 경로를 우선한다. 불필요한 바깥 우회와 짧은 계단 모양 꺾임을 피하고, 라벨을 놓을 공간도 남긴다. 복잡한 구성에서는 역할별 층과 탑다운 배치를 이용한다.

구성도는 실제 컴포넌트 사이의 연결을 표시한다. 그룹은 설명을 위한 논리적 역할 경계이며, 책에 없는 VPC·배포 제품·복제 보장을 의미하지 않는다. 해시 링·비트 배치·시간 창·버전 충돌·시퀀스 등은 원리를 설명하는 별도 구조로 유지한다. 같은 서버에서 일어나는 준비·확정을 서로 다른 서버처럼 표현하지 않는다.

```sh
uv run scripts/redraw_diagrams.py --render
uv run scripts/redraw_diagrams.py drive-upload cache-aside --render
uv run scripts/redraw_diagrams.py fund-resource-waits fund-query-index --render
uv run scripts/check_diagrams.py
uv run scripts/check_markdown.py
```

PNG는 HTML을 Chromium에서 렌더링해 만든다. `--render`는 실제 글꼴의 너비로 라벨 위치를 조정한 뒤 HTML과 PNG를 함께 저장한다. 라벨은 단어 단위로 줄바꿈하며, 연결선 가까이에 배치하고 다른 화살표·아이콘·라벨과 겹치지 않는지 확인한다. `check_diagrams.py`는 렌더링된 HTML을 검사한다. 자동 검사와 별도로 PNG를 열어 흐름·의미·가독성을 검토한다.

원본은 `mode: topology`의 컴포넌트·관계 데이터 또는 `mode: structure`의 SVG/HTML 구조로 구분한다. `layout`은 구성도별 배치와 그룹 경계를 지정한다. `diagram_label_layout.js`는 브라우저의 실제 글자 경계를 이용해 라벨을 해당 연결선에 붙인다.

아이콘은 추상 역할에 Lucide를 사용한다. Redis·APNs·FCM처럼 제품이 명시된 경우에는 svgl에서 받은 Redis·Apple·Firebase의 원본 마크를 사용하며, 일반 캐시나 저장소에 임의의 제품을 붙이지 않는다. 로고의 권리는 각 소유자에게 있다. 템플릿과 내장 글꼴의 라이선스는 `licenses`에 보관한다.
