# Classroom Care Center | 오늘의 수업 관제소

수업 중인 나의 컨디션을 부드럽게 살피고, 지금 필요한 작은 도움을 건네는 Flet 앱입니다. 졸리면 바람을 쐬러 가라고 알려 주고, 배고프면 간식 루틴을, 집중이 흐트러지면 5분 집중 루틴을 제안합니다.

## 이런 기능이 있어요

- `졸림`, `집중`, `이해도`, `배고픔`을 슬라이더로 기록
- 네 가지 상태를 계산한 **생존 점수**와 컬러 게이지
- 수업 시작·중지 타이머
- 졸림·집중·간식 빠른 설정 버튼
- 현재 가장 필요한 수업 케어 루틴과 완료 처리
- 힘나는 응원 문구 바꾸기

## 폴더 구조

```text
Flet Calc/
├── main.py                 # 앱을 실행하는 파일
├── src/classroom_control/  # 점수·케어 루틴 계산 코드
├── tests/                  # 자동 테스트
├── assets/                 # 한글 글꼴 등 앱 자산
├── SPEC.md                 # 기능 명세
├── IMP-PLAN.md             # 구현 계획
└── README.md               # 이 사용 설명서
```

## 실행 방법 (Antigravity IDE + WSL)

Antigravity IDE에서 `Terminal` 메뉴를 열고 아래 명령을 **한 줄씩** 실행합니다.

```bash
wsl -d AIO
cd "/mnt/c/vibe/Flet Calc"
uv run flet run main.py
```

브라우저 또는 앱 창이 열리면 성공입니다. 실행을 멈출 때는 터미널에서 `Ctrl + C`를 누릅니다.

## 사용하는 법

1. `수업 시작`을 눌러 수업 시간을 기록합니다.
2. 슬라이더를 움직여 지금 컨디션을 솔직하게 표시합니다.
3. 상단 게이지와 메시지로 오늘의 생존 상태를 확인합니다.
4. **수업 케어 모드**의 작은 루틴을 해 보고 `케어 완료했어`를 누릅니다.
5. 응원이 필요하면 `다른 응원 받기`를 눌러 기분을 환기합니다.

## 테스트하기

앱 폴더에서 다음 명령을 실행합니다.

```bash
uv run pytest -q
```

## 다른 사람에게 전달하기

다른 사람이 WSL, Python, `uv` 없이 실행하게 하려면 Windows용 `.exe` 앱으로 빌드합니다. 이 작업은 **Windows PowerShell**에서 실행하며, 처음 한 번은 Visual Studio의 `Desktop development with C++` 구성 요소가 필요합니다.

```powershell
cd "C:\vibe\Flet Calc"
uv run flet build windows
```

완료되면 `build\windows` 안의 앱 폴더를 통째로 압축해 전달합니다. 받는 사람은 압축을 풀고 앱 실행 파일을 더블클릭하면 됩니다.

> 현재 Windows PowerShell에는 `uv`가 설치되어 있지 않습니다. 개발 중에는 위 WSL 실행 방법을 쓰고, 배포할 때만 Windows 빌드 환경을 준비하면 됩니다.

## GitHub에 백업하기

이 프로젝트는 GitHub 저장소에 올려 두면 컴퓨터가 바뀌어도 안전하고, 다른 사람과 코드도 공유할 수 있습니다.

### 처음 한 번: GitHub 로그인

WSL 터미널에서 아래 명령을 실행합니다.

```bash
gh auth login
```

화면의 선택지는 다음처럼 고릅니다.

1. `GitHub.com`
2. `HTTPS`
3. `Login with a web browser`

브라우저가 열리면 GitHub 계정으로 로그인하고 권한을 허용합니다. **비밀번호나 개인 토큰을 코드나 채팅에 적지 않습니다.**

### 변경사항 올리기

로그인 후 앱 폴더에서 다음을 실행합니다.

```bash
cd "/mnt/c/vibe/Flet Calc"
git add .
git commit -m "feat: describe your change"
git push
```

예를 들어 버튼 디자인을 고쳤다면 커밋 메시지는 `feat: improve care buttons`처럼, 무엇을 바꿨는지 짧게 적으면 됩니다.
