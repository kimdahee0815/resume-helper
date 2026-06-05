# 나만의 자소서 도우미

## 프로젝트 목적

- 추상적 표현·정량 지표 부재·직무 키워드 미스매치 등 6대 결함 패턴을 탐지하고,
  간결형·스토리형·직무맞춤형·성과수치형·PREP형 5가지 스타일로 맞춤 첨삭을 제공한다.
- STAR / PREP 프레임을 기반으로 자소서 문항을 구조적으로 재작성하고,
  블라인드 채용 위험 표현까지 자동으로 점검한다.

## 실행 환경

- Python: 3.11 이상 권장
- 실행 도구: uv
- 주요 패키지:

  - openai>=2.29.0
  - anthropic>=0.104.0
  - openai-agents>=0.17.3
  - python-dotenv
  - pydantic

## 실행 방법

```powershell
uv run python resume_helper.py
```

## 필요한 설정

- `.env` 파일에 아래 키를 넣는다.

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MODEL_OPENAI=gpt-5.4-nano   
MODEL_CLAUDE=claude-haiku-4-5-20251001 
```

## 예시 입출력

### 입력 예시

```text
지원 직무: 백엔드 개발자
문항: 문제 해결 경험을 서술하세요.
초안: 저는 API 성능 개선 경험을 통해 문제 해결 역량을 기르고 노력했습니다.
```

### 명령 흐름

```text
/style 성과수치형
/analyze 자소서본문: 위 초안, NCS/JD 키워드(쉼표 구분): REST API, 성능 최적화, JPA
```

### 출력 예시

```text
요약: STAR 구조 중 Result 단계에 수치 없음 - 응답속도 개선폭 추가 필요
발견한 결함: 정량 지표 부재 / 추상적 표현("노력했습니다")
개선 방향: "API 응답속도를 1.2초→0.3초로 단축(JPA fetchJoin 적용)"으로 Result 보강
다음 행동: /style PREP형으로 전환 후 지원동기 문항에 같은 경험 연결
```

## 제출 기록

- 저장소 공개 범위: Public
- 마지막 commit 메시지: Finalize resume helper submission
- push 시각: 2026.06.05 5:28pm
- push 결과: 성공
- 로컬 제출 대체 사유: 해당 없음
- 민감 파일 점검: **`.env`**, 자소서 원문, 실행 로그가 commit에 포함되지 않음

## 5일 회고

- Day 1: 대화 루프 구조(while + input)와 system 프롬프트 분리가 유지보수의 핵심임을 배움.
- Day 2: **`/style`** 전환으로 전역 변수를 함수 안에서 바꿀 때 **`global`** 선언이 필요하다는 걸 배움.
- Day 3: **`ResumeAnalysis`** Pydantic 모델로 결함, 점수, 키워드를 구조화하면 저장과 재사용이 쉬워진다는 걸 배움.
- Day 4: Triage 에이전트가 입력을 분류해 전문 에이전트로 넘기는 흐름이 단일 프롬프트보다 정확도가 높다는 걸 배움.
- Day 5: README, **`.gitignore`**, final_check.py로 제출 전 민감 정보 누출을 막는 루틴이 습관이 되어야 한다는 걸 배움.

## 남은 위험

- API 키 누출 위험: `.env`를 `.gitignore`에 추가하고 코드에 키를 직접 쓰지 않는 방식으로 막음.
- 토큰 비용 폭주: `max_completion_tokens`를 항상 명시하고, 대화 히스토리를 누적하지 않는 단발성 호출 구조를 유지함.
- raw error 노출 방지: try/except로 API 오류를 잡아 사용자에게는 "일시적 오류가 발생했어요. 다시 시도해주세요."만 출력할 계획임.

## 9주차 TODO

- Streamlit 전환 후보 함수: **`check_resume_ai_filter`**, **`check_blind_risks`**, **`analyze_resume`**, **`handle_style_command`**
- 화면 구성 후보:
- 입력칸: 자소서 본문 텍스트 영역, 직무 키워드 입력칸
- 결과 영역: 결함 목록, 개선 권고, 블라인드 위험 표현
- 실행 버튼: 점검 시작, 스타일 전환 드롭다운
