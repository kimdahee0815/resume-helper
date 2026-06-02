from pydantic import BaseModel, Field


class ResumeDraftInput(BaseModel):
    selected_style: str = Field(..., description="Day 2에서 고른 스타일")
    original_text: str = Field(..., description="개인정보를 제거한 원문")
    rewritten_text: str = Field(..., description="선택 스타일의 재작성 결과")
    observation: list[str] = Field(default_factory=list)


draft = ResumeDraftInput(
    selected_style="스토리형",
    original_text=(
        "팀 프로젝트에서 API 응답 속도가 느려 사용자 불만이 생겼습니다. "
        "원인을 분석한 결과 N+1 쿼리 문제를 발견했고, JPA fetchJoin으로 개선했습니다. "
        "배포 후 응답 속도가 1.2초에서 0.3초로 줄었고, 팀 내 코드 리뷰 문화도 함께 정착시켰습니다."
    ),
    rewritten_text=(
        "팀 프로젝트를 진행하던 중 일부 API의 응답 속도가 느려 사용자 불만이 발생하는 상황이 있었습니다. "
        "사용자 경험을 개선하기 위해 응답 지연의 원인을 파악하고 성능을 개선하는 것이 주요 과제였습니다.\n\n"
        "저는 쿼리 로그와 실행 계획을 분석하며 문제를 추적했고, 그 과정에서 N+1 쿼리 문제가 발생하고 있음을 발견했습니다. "
        "이후 JPA의 fetchJoin을 적용해 불필요한 추가 조회를 제거하고 데이터 조회 방식을 최적화했습니다. "
        "또한 같은 문제가 반복되지 않도록 코드 리뷰 과정에서 성능 관점의 검토 항목을 제안하고 공유했습니다.\n\n"
        "그 결과 API 응답 속도를 1.2초에서 0.3초로 단축할 수 있었으며, 사용자 불만을 줄이는 데 기여했습니다. "
        "또한 성능 이슈를 함께 점검하는 코드 리뷰 문화가 팀 내에 정착하는 계기가 되었고, "
        "이를 통해 기술적 문제 해결뿐 아니라 협업 프로세스 개선의 중요성도 배울 수 있었습니다."
    ),
    observation=[
        "구조: STAR 4단계가 단락별로 명확히 분리됨. S→T→A→R 순서로 자연스럽게 전개",
        "결함: S/T 단락이 2문장으로 다소 길고 완곡 표현이 긴장감을 낮춤. R 단락 교훈 문장이 추상적",
        "키워드: N+1 쿼리, JPA fetchJoin, 쿼리 로그, 실행 계획, 응답 속도, 코드 리뷰, 성능 최적화",
        "STAR 매핑: S→API 응답 지연·사용자 불만 / T→원인 파악·성능 개선 / A→로그 분석·fetchJoin 적용·리뷰 항목 제안 / R→1.2초→0.3초(75% 단축)·코드 리뷰 문화 정착",
        "재작성 후보: R 단락 마지막 문장 '기술적 문제 해결뿐 아니라 협업 프로세스 개선의 중요성도 배울 수 있었습니다' → Day 3 JSON 분석 대상",
    ],
)

print(draft.model_dump())