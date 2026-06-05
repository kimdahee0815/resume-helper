import subprocess
from pathlib import Path


def check_resume_not_in_git_history() -> bool:
    """자소서 원문이 Git 추적 대상에 들어갔는지 점검하는 함수예요."""
    result = subprocess.run(
        ["git", "log", "--all", "--", "*.txt"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print("⚠️  .txt 파일이 Git 히스토리에 있어요. 확인이 필요해요.")
        return False
    print("✅ 자소서 원문이 Git 히스토리에 없어요.")
    return True


def check_required_files() -> bool:
    """제출 필수 파일이 있는지 확인하는 함수예요."""
    required = ["README.md", ".gitignore", "resume_helper.py", "resume_agents.py"]
    missing = [f for f in required if not Path(f).exists()]
    if missing:
        print(f"⚠️  누락된 파일: {', '.join(missing)}")
        return False
    print("✅ 필수 파일이 모두 있어요.")
    return True


if __name__ == "__main__":
    check_required_files()
    check_resume_not_in_git_history()