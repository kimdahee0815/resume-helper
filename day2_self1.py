from pathlib import Path

source = Path("resume_helper.py")
backup = Path("resume_helper_day1_backup.py")

if source.exists():
    print("resume_helper.py 확인 완료")
else:
    print("resume_helper.py를 먼저 찾아요")

if source.exists() and not backup.exists():
    backup.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"백업 완료 => {backup}")
else:
    print("백업 파일이 이미 존재합니다.")