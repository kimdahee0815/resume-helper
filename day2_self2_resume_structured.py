from pydantic import BaseModel, Field


class ResumeDraftInput(BaseModel):
    selected_style: str = Field(..., description="Day 2에서 고른 스타일")
    original_text: str = Field(..., description="개인정보를 제거한 원문")
    rewritten_text: str = Field(..., description="선택 스타일의 재작성 결과")
    observation: list[str] = Field(default_factory=list)


draft = ResumeDraftInput(
    selected_style="TODO",
    original_text="TODO",
    rewritten_text="TODO",
    observation=["TODO"],
)

print(draft.model_dump())
