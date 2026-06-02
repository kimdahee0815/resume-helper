from pathlib import Path
from pydantic import BaseModel, Field

def run_cli() -> None:
    print("자소서 도우미입니다. /analyze 를 입력해요.")
    command = input("명령: ").strip()

    if command == "/analyze":
        resume_text = input("자소서 원문: ").strip()
        keyword_text = input("NCS/JD 키워드(쉼표 구분): ").strip()

        # 분석 실행
        analysis = analyze_resume(resume_text=resume_text, raw_keywords=keyword_text)

        # 결과 출력
        print(f"\n분석 점수: {analysis.score}")
        print(f"결함 수: {len(analysis.defects)}")
        print(f"결함 목록: {analysis.defects}")
        print(f"키워드 매칭: {analysis.keyword_match}")
        print(f"블라인드 위반: {analysis.blind_violations}")

        # JSON 저장
        save_analysis(analysis)

    else:
        print("지원하는 명령: /analyze")

def detect_flaws(resume_text: str, required_keywords: list[str]) -> list[str]:
    defects: list[str] = []
    sentences = [part.strip() for part in resume_text.split(".")]

    # STAR/PREP 프레임 미준수
    star_hints = ["상황", "과제", "행동", "결과", "근거", "이유"]
    if sum(1 for hint in star_hints if hint in resume_text) < 2:
        defects.append("STAR/PREP 프레임 미준수")

    # NCS 키워드 누락
    if any(kw not in resume_text for kw in required_keywords):
        defects.append("NCS 키워드 누락")

    # 블라인드 채용 위반
    blind_hints = ["대학교", "대학원", "출신", "나이", "남성", "여성", "지방"]
    if any(hint in resume_text for hint in blind_hints):
        defects.append("블라인드 채용 위반")

    # 공백 문장
    if any(s == "" for s in resume_text.splitlines()):
        defects.append("공백 문장")

    # 일반화 표현
    vague_hints = ["최선을", "열심히", "좋은", "노력했습니다", "열정적으로", "성실하게"]
    if any(hint in resume_text for hint in vague_hints):
        defects.append("일반화 표현")

    # 수동태 남발
    passive_hints = ["되었습니다", "됐습니다", "하게 되었", "지게 되었"]
    if sum(resume_text.count(hint) for hint in passive_hints) >= 2:
        defects.append("수동태 남발")

    return defects


def normalize_keywords(raw_keywords: str) -> list[str]:
    # 쉼표로 나누고, 앞뒤 공백 제거, 빈 값 제거
    return [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]

def match_keywords(resume_text: str, required_keywords: list[str]) -> dict[str, object]:
    matched = [kw for kw in required_keywords if kw in resume_text]
    missing = [kw for kw in required_keywords if kw not in resume_text]
    score = round(len(matched) / len(required_keywords) * 100, 1) if required_keywords else 0.0

    return {
        "required": required_keywords,
        "matched": matched,
        "missing": missing,
        "score": score,
    }
    
def detect_blind_violations(resume_text: str) -> list[str]:
    violations: list[str] = []

    risky_patterns = [
        # 학교명·학력 직접 노출
        ("대학교",      "학교명 또는 학력 직접 노출"),
        ("대학원",      "학교명 또는 학력 직접 노출"),
        ("졸업",        "학교명 또는 학력 직접 노출"),
        # 나이·연령 표현
        ("나이",        "나이 또는 연령 표현"),
        ("살입니다",    "나이 또는 연령 표현"),
        ("년생",        "나이 또는 연령 표현"),
        # 성별 표현
        ("남성",        "성별 직접 표현"),
        ("여성",        "성별 직접 표현"),
        ("남자",        "성별 직접 표현"),
        ("여자",        "성별 직접 표현"),
        # 지역·출신 표현
        ("출신",        "지역 출신 표현"),
        ("고향",        "지역 출신 표현"),
        ("지방",        "지역 출신 표현"),
    ]

    seen = set()  # 같은 레이블이 중복 추가되지 않도록
    for pattern, label in risky_patterns:
        if pattern in resume_text and label not in seen:
            violations.append(label)
            seen.add(label)

    return violations

class ResumeAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    defects: list[str]
    keyword_match: dict[str, object]
    blind_violations: list[str]
    revised_text: str


def analyze_resume(resume_text: str, raw_keywords: str) -> ResumeAnalysis:
    # 1. 키워드 정규화
    keywords = normalize_keywords(raw_keywords)

    # 2. 키워드 매칭
    keyword_match = match_keywords(resume_text, keywords)

    # 3. 블라인드 채용 위반 탐지
    blind_violations = detect_blind_violations(resume_text)

    # 4. 결함 탐지
    defects = detect_flaws(resume_text, keywords)

    # 5. 점수 계산
    # keyword_match score 70% + 결함 감점 10%씩, 최저 0점
    base_score = keyword_match["score"] * 0.7
    deduction = len(defects) * 10
    score = max(0, round(base_score + 30 - deduction))  # 나머지 30점은 기본 점수

    # 6. 개선 텍스트 — 결함 목록을 힌트로 붙여 반환
    if defects:
        revised_text = resume_text + f"\n\n[개선 필요 항목: {', '.join(defects)}]"
    else:
        revised_text = resume_text + "\n\n[결함 없음]"

    payload: dict[str, object] = {
        "score": min(score, 100),
        "defects": defects,
        "keyword_match": keyword_match,
        "blind_violations": blind_violations,
        "revised_text": revised_text,
    }
    return ResumeAnalysis.model_validate(payload)


def save_analysis(analysis: ResumeAnalysis, output_path: str = "analyze_result.json") -> None:
    path = Path(output_path)
    path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")
    print(f"저장 위치: {path}")
    print(f"분석 점수: {analysis.score}")
    print(f"결함 수: {len(analysis.defects)}")

if __name__ == "__main__":
    run_cli()