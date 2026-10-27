from __future__ import annotations

from dataclasses import dataclass
import time


@dataclass(frozen=True)
class Theme:
    name: str
    message: str
    emoji: str
    accent: str
    surface: str


@dataclass(frozen=True)
class CarePlan:
    key: str
    title: str
    summary: str
    steps: tuple[str, ...]
    completion: str


THEMES = (
    Theme("몰입", "완전 몰입 중!", "🔥", "#49E7B1", "#123E3D"),
    Theme("안정", "잘 버티는 중!", "🙂", "#8B8CFF", "#252554"),
    Theme("충전", "충전이 필요해요!", "☕", "#FFB84D", "#4D351A"),
    Theme("휴식", "긴급 휴식 권장!", "🛟", "#FF6B6B", "#4A2028"),
)

ENCOURAGEMENTS = (
    "모르는 건 뒤처진 게 아니라, 배우고 있다는 증거야.",
    "작은 한 칸을 채운 것도 오늘의 멋진 진전이야.",
    "지금의 해든이는 충분히 잘하고 있어. 한 숨만 고르자.",
    "완벽보다 중요한 건 다시 화면을 켜는 용기야.",
    "한 번의 집중이 쌓이면, 나중엔 진짜 내 실력이 돼.",
    "오늘 버틴 시간도 분명히 해든이 편이 되어 줄 거야.",
    "천천히 가도 괜찮아. 멈추지 않은 네가 이미 대단해.",
    "작은 질문 하나가 큰 이해의 시작이 될 수 있어.",
)

CARE_PLANS = {
    "sleepiness": CarePlan(
        "sleepiness",
        "잠 깨기 1분 루틴",
        "잠깐 밖에 나가 바람을 쐬고, 몸을 가볍게 깨운 뒤 돌아와요.",
        ("물 한 모금 마시기", "복도나 창가에 나가 1분 바람 쐬기", "어깨를 천천히 5번 돌리기"),
        "좋아! 몸이 조금 깨어났어. 다음 한 가지를 가볍게 시작해 보자.",
    ),
    "hunger": CarePlan(
        "hunger",
        "간식 에너지 충전",
        "배고프면 집중력이 먼저 줄어들 수 있어요.",
        ("물 또는 우유 한 잔 챙기기", "바나나·견과류·작은 빵 중 하나 고르기", "먹은 뒤 3분만 쉬기"),
        "든든해졌어! 이제 작은 실습 하나만 다시 열어 보자.",
    ),
    "focus": CarePlan(
        "focus",
        "집중 리셋 5분",
        "해야 할 일을 작게 만들면 시작이 쉬워져요.",
        ("지금 할 일 하나만 정하기", "알림과 다른 탭 하나 닫기", "5분 동안 그 일만 하기"),
        "잘했어! 5분을 시작한 순간 이미 집중 모드야.",
    ),
    "understanding": CarePlan(
        "understanding",
        "개념 정리 한 장",
        "모르는 부분을 작게 쪼개면 이해가 훨씬 편해져요.",
        ("모르는 단어 하나 적기", "예시 하나 찾기", "내 말로 한 줄 다시 설명하기"),
        "좋아! 한 줄로 설명할 수 있으면 이미 내 것이 되고 있어.",
    ),
}


@dataclass
class ClassroomState:
    sleepiness: int = 50
    focus: int = 50
    understanding: int = 50
    hunger: int = 50
    running: bool = False
    _started_at: float | None = None
    _elapsed_seconds: int = 0
    encouragement_index: int = 0

    @property
    def survival_score(self) -> int:
        values = (self.focus, self.understanding, 100 - self.sleepiness, 100 - self.hunger)
        return round(sum(values) / len(values))

    @property
    def theme(self) -> Theme:
        score = self.survival_score
        if score >= 80:
            return THEMES[0]
        if score >= 50:
            return THEMES[1]
        if score >= 30:
            return THEMES[2]
        return THEMES[3]

    @property
    def elapsed_seconds(self) -> int:
        if self.running and self._started_at is not None:
            return int(time.monotonic() - self._started_at)
        return self._elapsed_seconds

    @property
    def elapsed_label(self) -> str:
        minutes, seconds = divmod(self.elapsed_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def recommendation(self) -> str:
        if self.survival_score >= 80:
            return "지금 흐름 좋아! 어려운 실습 하나를 바로 끝내 보자."
        if self.survival_score >= 50:
            return "괜찮아. 다음 25분만 한 가지 작업에 집중해 보자."
        if self.survival_score >= 30:
            return "물 한 모금, 스트레칭 30초 뒤에 다시 출발하자."
        return "잠깐 멈춰도 괜찮아. 쉬고 나서 작은 일 하나만 해 보자."

    @property
    def recommended_care(self) -> CarePlan:
        needs = {
            "sleepiness": self.sleepiness,
            "hunger": self.hunger,
            "focus": 100 - self.focus,
            "understanding": 100 - self.understanding,
        }
        return CARE_PLANS[max(needs, key=needs.get)]

    def complete_care(self, key: str) -> None:
        if key == "sleepiness":
            self.sleepiness = max(0, self.sleepiness - 15)
            self.focus = min(100, self.focus + 10)
        elif key == "hunger":
            self.hunger = max(0, self.hunger - 25)
        elif key == "focus":
            self.focus = min(100, self.focus + 15)
        elif key == "understanding":
            self.understanding = min(100, self.understanding + 15)

    @property
    def encouragement(self) -> str:
        return ENCOURAGEMENTS[self.encouragement_index % len(ENCOURAGEMENTS)]

    def next_encouragement(self) -> None:
        self.encouragement_index += 1

    def apply_preset(self, name: str) -> None:
        presets = {
            "focus": (15, 90, 85, 20),
            "sleepy": (85, 35, 45, 35),
            "hungry": (25, 55, 60, 90),
            "reset": (50, 50, 50, 50),
        }
        self.sleepiness, self.focus, self.understanding, self.hunger = presets[name]

    def start(self) -> bool:
        if self.running:
            return False
        self.running = True
        self._started_at = time.monotonic() - self._elapsed_seconds
        return True

    def stop(self) -> bool:
        if not self.running:
            return False
        self._elapsed_seconds = self.elapsed_seconds
        self._started_at = None
        self.running = False
        return True
