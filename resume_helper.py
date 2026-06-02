import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from styles import STYLE_PRESETS, list_style_names


RESUME_SYSTEM_PROMPT = """
"당신은 한국 채용 시장 전문 자기소개서 첨삭 코치입니다.\n"
            "아래 기준으로 입력된 자소서를 분석하고 한국어로 피드백을 제공합니다.\n\n"
            "1. 서술 프레임: STAR(상황→과제→행동→결과), PREP(주장→근거→예시→재주장), "
            "CAR(맥락→행동→결과) 중 적합한 방식을 적용해 개선안을 제시합니다.\n"
            "2. NCS 역량 기반 분석: 의사소통, 문제해결, 자원관리, 대인관계, "
            "정보활용, 기술 역량이 드러나는지 확인합니다.\n"
            "3. 6대 결함 탐지:\n"
            "   - 추상적 표현 (열심히, 최선을, 노력했습니다)\n"
            "   - 정량 지표 부재 (수치·기간·규모 없음)\n"
            "   - 직무 키워드 미스매치 (JD와 무관한 경험)\n"
            "   - 자기 자랑 단방향 (기여·협업 관점 없음)\n"
            "   - 일관성 결여 (문항 간 스토리 충돌)\n"
            "   - 공통 템플릿 표현 (지원동기 없이 성장 포부만 나열)\n"
"""


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

def chat_loop():
    print("자소서 도우미를 시작합니다. /help로 도움말, /quit으로 종료합니다.")
    client = make_openai_client()
    while True:
        user_input = input("자소서 입력 > ")

        command = user_input.strip()

        if command == "/help":
            help_text = """
                [사용 방법]
                - 자기소개서 문단을 그대로 붙여 넣으면 AI가 첨삭 제안을 드립니다.
                - /sample : 예시 자소서로 테스트합니다.
                - /quit   : 프로그램을 종료합니다.

                [주의]
                - 이름, 학교명, 생년월일 등 개인정보는 입력 전에 삭제하세요.
                - 공개 저장소(GitHub 등)에 실제 자소서를 올리지 마세요.
            """
            print(help_text)
            continue
        
        elif command == "/quit":
            print("종료합니다.")
            break
        
        elif command.startswith("/style"):
            current_style = handle_style_command(user_input=user_input)
            RESUME_SYSTEM_PROMPT = STYLE_PRESETS[current_style]["system"]

        elif not command:
            print("텍스트를 입력해 주세요. 도움말은 /help")
            continue

        else:
            messages=[
                {"role":"system", "content":RESUME_SYSTEM_PROMPT},
                {"role":"user", "content":user_input}
            ]

            response = client.chat.completions.create(
                model="gpt-5.4-nano",
                max_completion_tokens=1000,
                messages=messages
            )

            answer = response.choices[0].message.content
            print(answer)

current_style_key = "간결형"

# def handle_style_command(user_input: str) -> str:
#     parts = user_input.split(maxsplit=1)

#     if len(parts) < 2:
#         print("사용 가능한 스타일: ", list_style_names())
#         return current_style_key

#     style_key = parts[1].strip()

#     if style_key in STYLE_PRESETS:
#         print("현재 스타일: ", style_key)
#         return style_key
    
#     print("가능한 스타일은 다음과 같습니다: ", list_style_names())
#     return current_style_key

def handle_style_command(user_input: str) -> None:
    parts = user_input.split(maxsplit=1)
    if len(parts) < 2:
        print("사용 가능한 스타일:", ", ".join(STYLE_PRESETS.keys()))
        return

    style_key = parts[1]
    if style_key in STYLE_PRESETS:
        print("현재 스타일: ", style_key)
        RESUME_SYSTEM_PROMPT = STYLE_PRESETS[style_key]["system"]
    else:
        print(f"알 수 없는 스타일. 가능: {', '.join(STYLE_PRESETS.keys())}")

def main() -> None:
    settings = load_settings()
    print("OpenAI key ready:", settings["openai_key_exists"])
    print("Claude key ready:", settings["anthropic_key_exists"])
    sample_text = get_sample_resume()
    # provider = input("사용할 제공사(openai/claude)를 입력하세요: ").strip().lower()

    # if provider == "openai":
    #     result = ask_openai_once(sample_text)
    # elif provider == "claude":
    #     result = ask_claude_once(sample_text)
    # else:
    #     print("openai 또는 claude 중 하나를 입력해요.")
    #     return

    # print("[자소서 도우미 첫 응답]")
    # print(result[:1000])
    chat_loop()

if __name__ == "__main__":
    main()

