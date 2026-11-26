# frontend-code-workflow

기존 프론트엔드 코드베이스에서 기능을 계획하고 구현하고 검증하는 Codex 스킬입니다.

코드를 바로 작성하기보다 사용자에게 보이는 결과와 관련 UI 상태를 먼저 확인합니다. 변경 위험에 따라 절차의 강도를 조절하며, 저장소에 이미 있는 테스트와 도구를 우선합니다.

## 주요 원칙

- 작은 스타일 변경에는 무거운 문서를 요구하지 않습니다.
- 상태가 있는 기능은 사용자 시나리오와 수용 기준을 먼저 합의합니다.
- 코드 검사와 실제 브라우저 검증을 구분합니다.
- 반응형, 키보드, 접근성, 다크 모드는 변경과 관련 있을 때 확인합니다.
- 새 라이브러리나 범위 확장은 설명과 승인 없이 추가하지 않습니다.
- 커밋, 푸시, PR, 배포는 사용자가 요청한 경우에만 수행합니다.

## 설치

Codex에게 다음과 같이 요청할 수 있습니다.

```text
https://github.com/khj0426/fronend-code-workflow/tree/main/skills/frontend-workflow
에서 frontend-workflow 스킬을 설치해줘.
```

수동 설치 시 `skills/frontend-workflow`를 Codex의 개인 skills 디렉터리에 복사합니다.

```text
~/.codex/skills/frontend-workflow/
```

## 사용

명시적으로 호출하려면 프롬프트에 스킬 이름을 적습니다.

```text
$frontend-workflow 검색 결과 필터를 URL과 동기화해줘.
```

```text
$frontend-workflow 이 회원가입 폼의 중복 제출 버그를 고쳐줘.
```

자동 스킬 선택이 활성화된 환경에서는 일반적인 프론트엔드 변경 요청에도 선택될 수 있습니다.

## 작업 흐름

```text
코드베이스 조사
→ 변경 위험 분류
→ 사용자 시나리오와 UI 상태 확인
→ 필요한 경우 설계 승인
→ 작은 수직 단위 구현
→ 타입·테스트·브라우저·접근성 검증
→ 최종 diff 리뷰와 결과 보고
```

스킬은 변경을 `small`, `standard`, `high-risk`로 분류합니다. 작은 변경에는 최소 절차를 적용하고, 공용 컴포넌트·라우팅·인증·데이터 계약처럼 영향 범위가 넓은 변경에는 설계와 회귀 검증을 강화합니다.

## 구조

```text
skills/frontend-workflow/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── specification.md
    ├── implementation.md
    ├── verification.md
    └── review.md
```

- `SKILL.md`: 작업 분류와 전체 흐름
- `specification.md`: 사용자 시나리오, UI 상태, 수용 기준
- `implementation.md`: 수직 단위 구현과 위험 상승 기준
- `verification.md`: 변경 유형별 코드·브라우저 검증
- `review.md`: 요구사항, 회귀, 복잡성 최종 점검

## 현재 범위

첫 버전은 하나의 워크플로 스킬만 제공합니다. 별도 리뷰 에이전트, 회고 스킬, CI 검사 스크립트는 실제 사용에서 반복되는 필요가 확인되면 추가합니다.
