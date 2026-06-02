from pydantic import BaseModel, Field
from enum import Enum
import json

class ResumeAnalysis(BaseModel):
    growth: str = Field(
        ...,
        description="성장 과정에서 겪은 경험과 그 경험이 직무 역량으로 이어지는 흐름을 서술해요. "
                    "질문: 성장 과정이 직무와 연결되나요?"
    )
    motivation: str = Field(
        ...,
        description="지원 동기가 단순한 희망이 아니라 회사와 직무의 특성과 연결되는지를 서술해요. "
                    "질문: 지원 동기가 회사·직무와 연결되나요?"
    )
    aspiration: str = Field(
        ...,
        description="포부가 '열심히 하겠습니다' 수준이 아니라 실제 행동 단위로 표현되는지를 서술해요. "
                    "질문: 입사 후 포부가 행동 단위로 보이나요?"
    )
    experience: str = Field(
        ...,
        description="상황(S)·과제(T)·행동(A)·결과(R) 흐름으로 직무 경험을 서술해요. "
                    "질문: STAR 구조로 설명할 경험이 있나요?"
    )
    success_failure: str = Field(
        ...,
        description="성공·실패의 결과뿐 아니라 그 경험에서 얻은 배움과 변화를 서술해요. "
                    "질문: 성공·실패에서 배운 점이 드러나나요?"
    )


def build_sample_payload() -> dict[str, str]:
    return {
        "growth": (
            "처음에는 프론트엔드만 담당했지만, 백엔드 담당자가 빠지면서 "
            "스스로 Spring Boot를 독학해 API를 완성한 경험이 "
            "백엔드 개발자로 방향을 잡는 계기가 됐습니다."
        ),
        "motivation": (
            "귀사의 JD에서 '대용량 트래픽 처리'와 '쿼리 최적화'를 강조한 부분이 "
            "제가 N+1 문제를 직접 해결한 경험과 연결돼 지원하게 됐습니다."
        ),
        "aspiration": (
            "입사 후 6개월 안에 서비스 내 느린 API 3건을 선정해 "
            "쿼리 실행 계획을 분석하고 응답 속도를 30% 이상 개선하겠습니다."
        ),
        "experience": (
            "팀 프로젝트에서 API 응답이 1.2초로 느려 사용자 불만이 생겼습니다(S). "
            "응답 지연 원인을 파악하고 성능을 개선하는 것이 과제였습니다(T). "
            "쿼리 로그와 실행 계획을 분석해 N+1 문제를 발견하고 "
            "JPA fetchJoin을 적용했습니다(A). "
            "배포 후 응답 속도가 0.3초로 단축됐습니다(R)."
        ),
        "success_failure": (
            "초기 설계 단계에서 인덱스를 추가하지 않아 데이터가 늘어날수록 "
            "조회 속도가 급격히 떨어지는 실패를 경험했습니다. "
            "이후 ERD 설계 단계부터 조회 패턴을 먼저 정의하는 습관을 갖게 됐습니다."
        ),
    }


def validate_payload() -> None:
    payload = build_sample_payload()

    # dict => ResumeAnalysis 모델로 검증
    analysis = ResumeAnalysis.model_validate(payload)
    print("=== 검증 통과 ===")
    print(analysis.model_dump())

    # JSON 스키마 전체 출력
    print("\n=== JSON 스키마 ===")
    print(json.dumps(ResumeAnalysis.model_json_schema(), ensure_ascii=False, indent=2))

class DefectType(str, Enum):
    abstract_expression = "추상표현"      # growth, aspiration - "열심히", "최선을"
    missing_metric      = "정량부재"      # experience, success_failure - 수치,기간,규모 없음
    keyword_mismatch    = "키워드미스매치" # motivation, experience - JD 키워드와 연결 안 됨
    self_promotion      = "자기자랑"      # experience, success_failure - 팀·결과보다 자기 과시
    inconsistency       = "일관성결여"    # 전체 필드 - 앞뒤 방향이 어긋남
    generic_template    = "공통템플릿"    # motivation, aspiration - 어느 회사에나 쓸 수 있는 문장

if __name__ == "__main__":
    payload = build_sample_payload()

    validate_payload()

    # schema의 properties 키만 출력
    schema = ResumeAnalysis.model_json_schema()
    print("\n=== 필드 목록 (properties 키) ===")
    for field_name in schema["properties"]:
        print(f"  - {field_name}")
        
