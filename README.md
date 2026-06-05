## 실행 명령

- `uv run python resume_helper.py`

### 필요한 환경변수

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `MODEL_OPENAI` (기본값: gpt-5.4-nano)
- `MODEL_CLAUDE` (기본값: claude-haiku-4-5-20251001)

### 오늘 추가한 자유 기능

- 명령 이름: `/blind`
- 사용 방법 1줄: 자소서 본문을 붙여넣으면 블라인드 채용 위험 표현(학교/나이/사진 등)을 자동 탐지한다.
- 실행 예시 1줄: `/blind` 입력 → "블라인드 채용 위험 표현 후보: - 학교 - 사진 등등" 출력

### 최종 검증 결과

- 선택한 검증 항목 3개: STAR 구조 충족 여부 / 정량 근거 포함 여부 / NCS 직무 키워드 밀도
- 개선 권고 1개: "열심히", "최선을" 같은 추상 표현을 수치 기반 결과로 교체 필요
- 남은 수정 후보: /style 명령이 전역 변수를 실제로 반영하는지 재확인 필요

### 다음 시간에 넘길 것

- README에 넣을 기능 목록: /help, /style, /blind, check_resume_ai_filter
- GitHub push 전 개인정보 점검 여부: 자소서 원문 .gitignore 또는 sample_text 더미 텍스트로 교체 확인 필요
