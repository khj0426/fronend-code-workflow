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

요구사항부터 검증 근거까지 추적하려면 `strict`를 명시합니다.

```text
$frontend-workflow strict 결제 폼의 오류 처리를 개선해줘.
```

자동 스킬 선택이 활성화된 환경에서는 일반적인 프론트엔드 변경 요청에도 선택될 수 있습니다.

## Strict 모드

Strict 모드는 수용 기준을 구현과 검증까지 연결해야 하는 작업에 사용합니다. 인증·권한·결제·개인정보, 여러 소비자가 있는 데이터 계약이나 단계적 이전, 호환성 또는 롤백이 필수인 작업에서는 Codex가 strict 모드를 자동으로 추천합니다.

추천만으로 strict 모드가 활성화되지는 않습니다. 사용자가 승인하거나 프롬프트에 직접 `strict`를 적은 경우에만 다음 산출물을 만듭니다.

```text
docs/frontend-workflow/<feature-slug>/
├── spec.md
├── plan.md
└── trace.json
```

- `spec.md`: 사용자 시나리오, `AC-001` 형식의 수용 기준, UI 상태, 제외 범위
- `plan.md`: 작업과 수용 기준, 검증 방법의 연결
- `trace.json`: 수용 기준별 구현 파일, 테스트·수동 검증, 현재 상태

중요한 관찰이나 결정, 버린 대안이 생긴 경우에만 `journal.md`를 추가합니다. 명세와 계획 초안을 함께 검토해 한 번 승인한 뒤 구현합니다.

추적 파일은 외부 Python 패키지 없이 검사할 수 있습니다.

```text
python3 <skill-path>/scripts/check_trace.py \
  docs/frontend-workflow/<feature-slug>/trace.json \
  --root .
```

검사는 ID 중복, 상태, 검증 근거, 기록된 파일의 존재를 확인합니다. 테스트의 내용이나 구현 품질까지 증명하지는 않습니다.

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
├── assets/templates/
│   ├── spec.md
│   ├── plan.md
│   ├── journal.md
│   └── trace.json
├── references/
│   ├── specification.md
│   ├── verification.md
│   └── strict-mode.md
└── scripts/
    ├── check_trace.py
    └── test_check_trace.py
```

- `SKILL.md`: 작업 분류와 전체 흐름
- `specification.md`: 사용자 시나리오, UI 상태, 수용 기준
- `verification.md`: 변경 유형별 코드·브라우저 검증과 최종 diff 리뷰
- `strict-mode.md`: 추적 가능한 엄격 모드의 활성화 조건과 절차
- `assets/templates`: 프로젝트에 복사해 사용하는 명세·계획·일지·추적 템플릿
- `check_trace.py`: 수용 기준과 검증 근거의 구조 검사

## 현재 범위

첫 버전은 하나의 워크플로 스킬과 선택형 strict 모드를 제공합니다. 별도 리뷰 에이전트, 회고 스킬, CI 자동 연결은 실제 사용에서 반복되는 필요가 확인되면 추가합니다.
