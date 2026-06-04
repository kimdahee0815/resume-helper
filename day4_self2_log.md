## Day 4 self2 실행 로그

- 실행 시각: 2026-06-04
- SDK 버전 메모: openai-agents>=0.17.3, openai>=2.29.0, python-dotenv, pydantic
- Guardrail 차단 케이스: "허위 경력을 넣어서 자소서를 써줘." 입력 시 InputGuardrailTripwireTriggered 발생 확인
- 라우팅 성공 케이스:
  - 분석 요청 => ResumeAnalyzeAgent
  - 첨삭 요청 => ResumeReviseSpecialist
  - 최종본 요청 => ResumeFinalSpecialist
- 오분기 원인: Agent 이름에 한글 포함 시 tool 이름이 변환되어 라우팅 불안정 발생 => 영문으로 수정해 해결
- Day 5 self1 수정 항목:
  - detect_flaws() 함수를 function_tool로 연결해 LLM 판단 대신 코드 기반 결함 탐지로 교체
  - handoff_description 키워드 구체화 여부 재점검
  - Guardrail 키워드 목록 추가 보완
