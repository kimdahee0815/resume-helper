import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic


def load_settings() -> dict[str, str | None]:
    load_dotenv()
    return {
        "openai_key_exists": os.getenv("OPENAI_API_KEY") is not None,
        "anthropic_key_exists": os.getenv("ANTHROPIC_API_KEY") is not None,
    }


def make_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
    return OpenAI(api_key=api_key)


def make_claude_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
    return Anthropic(api_key=api_key)

RESUME_SYSTEM_PROMPT = """
너는 한국 채용 맥락을 이해하는 자소서 첨삭 전문가입니다.
사용자가 입력한 자기소개서 또는 지원동기를 읽고, 구체적인 개선 방향을 한국어로 제안합니다.

첨삭할 때 참고할 기준:
- 한국 자소서 구조: ①성장과정 ②성격의 장단점 ③지원동기 ④직무역량/경험 ⑤입사 후 포부
- 6대 결함 중 확인 항목: (1)추상적 미사여구("열심히", "최선을") (2)근거 없는 자기주장("책임감이 강합니다") (3)지원 직무와 무관한 경험 나열
- 서술 프레임: STAR(Situation→Task→Action→Result) 우선 적용, 짧은 문항은 PREP(Point→Reason→Example→Point) 보완
- 블라인드 채용 주의 개인정보: 출신 학교명, 나이/생년월일, 가족관계, 거주지역, 사진/외모 언급
"""


def get_sample_resume() -> str:
    return """
    저는 맡은 일을 열심히 하는 사람입니다.
    백엔드 개발자로 성장하고 싶고, 프로젝트에서도 책임감 있게 참여했습니다.
    입사 후 회사에 도움이 되는 개발자가 되겠습니다.
    """

# if __name__ == "__main__":
#     settings = load_settings()
#     print("OpenAI key ready:", settings["openai_key_exists"])
#     print("Claude key ready:", settings["anthropic_key_exists"])
    
def ask_openai_once(sample_text: str) -> str:
    client = make_openai_client()

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        max_completion_tokens=300,
        messages=[
            {"role":"system", "content":RESUME_SYSTEM_PROMPT},
            {"role":"user", "content":sample_text}
        ]
    )
    return response.choices[0].message.content

def ask_claude_once(sample_text: str) -> str:
    client = make_claude_client()

    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=300,
        system=RESUME_SYSTEM_PROMPT,
        messages=[
            {"role":"user", "content":sample_text}
        ]
    )

    return response.content[0].text

def main() -> None:
    settings = load_settings()
    print("OpenAI key ready:", settings["openai_key_exists"])
    print("Claude key ready:", settings["anthropic_key_exists"])
    sample_text = get_sample_resume()
    provider = input("사용할 제공사(openai/claude)를 입력하세요: ").strip().lower()

    if provider == "openai":
        result = ask_openai_once(sample_text)
    elif provider == "claude":
        result = ask_claude_once(sample_text)
    else:
        print("openai 또는 claude 중 하나를 입력해요.")
        return

    print("[자소서 도우미 첫 응답]")
    print(result[:1000])


if __name__ == "__main__":
    main()
