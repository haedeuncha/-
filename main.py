import asyncio

import flet as ft

from src.classroom_control.model import ClassroomState


BACKGROUND = "#081426"
TEXT = "#F4F7FF"
MUTED = "#B6C4E2"


async def main(page: ft.Page):
    state = ClassroomState()
    page.title = "오늘의 수업 관제소"
    page.bgcolor = BACKGROUND
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {"NotoSansKR": "NotoSansCJK-Regular.ttc"}
    page.theme = ft.Theme(font_family="NotoSansKR")

    # 점수처럼 짧고 크게 보이는 글자는 운영체제 기본 글꼴로 돌아가는 경우가 있어,
    # 번들에 넣은 한글 글꼴을 각 텍스트에 명시한다.
    korean_font = "NotoSansKR"
    title = ft.Text("오늘의 수업 관제소", size=32, weight=ft.FontWeight.BOLD, color=TEXT, font_family=korean_font)
    status = ft.Text(size=20, weight=ft.FontWeight.BOLD, font_family=korean_font)
    timer = ft.Text("00:00", size=32, weight=ft.FontWeight.BOLD, color=TEXT, font_family=korean_font)
    score_text = ft.Text(
        size=44,
        weight=ft.FontWeight.BOLD,
        color=TEXT,
        font_family=korean_font,
        font_family_fallback=["Noto Sans CJK KR", "sans-serif"],
    )
    message = ft.Text(size=23, weight=ft.FontWeight.BOLD)
    recommendation = ft.Text(size=17, color=MUTED)
    encouragement = ft.Text(size=16, italic=True, color="#E8D7FF")
    score_label = ft.Text(size=16, color=MUTED)
    gauge = ft.ProgressRing(value=0.5, width=150, height=150, stroke_width=12, stroke_cap=ft.StrokeCap.ROUND, track_gap=6, year_2023=False)
    progress_fill = ft.Container(width=125, height=8, border_radius=4, bgcolor="#8B8CFF", animate=ft.Animation(380, ft.AnimationCurve.EASE_OUT_CUBIC))
    progress_track = ft.Container(content=progress_fill, width=250, height=8, border_radius=4, bgcolor="#24344F")
    card = ft.Container(border_radius=20, padding=18, bgcolor="#18233A")
    sliders: dict[str, ft.Slider] = {}
    care_title = ft.Text(size=23, weight=ft.FontWeight.BOLD, color=TEXT)
    care_summary = ft.Text(size=17, color=MUTED)
    care_steps = ft.Column(spacing=4)
    care_result = ft.Text(size=16, color="#49E7B1")

    def slider(label: str, field: str, value: int):
        control = ft.Slider(min=0, max=100, divisions=20, value=value, label="{value}%", on_change=update_state(field))
        sliders[field] = control
        return ft.Column(
            controls=[
                ft.Text(label, size=18, color=TEXT, weight=ft.FontWeight.BOLD),
                control,
            ],
            spacing=2,
        )

    def refresh():
        theme = state.theme
        score = state.survival_score
        page.bgcolor = theme.surface
        status.value = "● 수업 진행 중" if state.running else "● 대기 중"
        status.color = theme.accent
        timer.value = state.elapsed_label
        score_text.value = f"{score}점"
        score_label.value = f"생존 게이지 · {theme.name} 모드"
        message.value = theme.message
        message.color = theme.accent
        recommendation.value = state.recommendation
        encouragement.value = state.encouragement
        gauge.value = score / 100
        gauge.color = theme.accent
        gauge.bgcolor = "#24344F"
        progress_fill.width = max(8, score * 2.5)
        progress_fill.bgcolor = theme.accent
        card.bgcolor = "#101D35"
        plan = state.recommended_care
        care_title.value = plan.title
        care_summary.value = plan.summary
        care_steps.controls = [ft.Text(f"{index + 1}. {step}", size=17, color=TEXT) for index, step in enumerate(plan.steps)]
        for field, control in sliders.items():
            control.value = getattr(state, field)
        page.update()

    def update_state(field: str):
        def handler(event):
            setattr(state, field, int(float(event.control.value)))
            refresh()

        return handler

    async def tick():
        while state.running:
            timer.value = state.elapsed_label
            timer.update()
            await asyncio.sleep(1)

    async def start_class(_event):
        if state.start():
            refresh()
            page.run_task(tick)

    def stop_class(_event):
        state.stop()
        refresh()

    def apply_preset(name: str):
        def handler(_event):
            state.apply_preset(name)
            refresh()

        return handler

    def next_encouragement(_event):
        state.next_encouragement()
        refresh()

    def complete_care(_event):
        plan = state.recommended_care
        state.complete_care(plan.key)
        care_result.value = plan.completion
        refresh()

    start_button = ft.Button("수업 시작", on_click=start_class)
    stop_button = ft.Button("수업 중지", on_click=stop_class)

    card.content = ft.Column(
        controls=[
            ft.Row([ft.Column([status, ft.Text("수업 경과 시간", color=MUTED), timer]), ft.Row([start_button, stop_button])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#2A3A59"),
            ft.Row(
                [
                    ft.Container(content=ft.Stack([ft.Container(content=score_text, alignment=ft.Alignment.CENTER), gauge]), width=170, height=170),
                    ft.Column(
                        [
                            score_label,
                            message,
                            recommendation,
                            progress_track,
                            ft.Container(content=encouragement, bgcolor="#182640", border_radius=10, padding=10),
                            ft.Button("다른 응원 받기", on_click=next_encouragement),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=10,
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.ListView(
                controls=[
                    title,
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("오늘 컨디션을 확인하고 필요한 케어를 바로 받아요", size=16, color=MUTED),
                                ft.Text("LIVE CHECK", size=16, color="#49E7B1", weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor="#101D35",
                        border_radius=12,
                        padding=12,
                    ),
                    card,
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("빠른 컨디션 설정", size=20, color=TEXT, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    [
                                        ft.Button("집중 모드", on_click=apply_preset("focus")),
                                        ft.Button("졸림 모드", on_click=apply_preset("sleepy")),
                                        ft.Button("간식 모드", on_click=apply_preset("hungry")),
                                        ft.Button("초기화", on_click=apply_preset("reset")),
                                    ],
                                    spacing=6,
                                    wrap=True,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor="#101D35",
                        border_radius=16,
                        padding=14,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row([ft.Text("수업 케어 모드", size=20, color="#49E7B1", weight=ft.FontWeight.BOLD), ft.Text("지금 가장 필요한 도움", size=16, color=MUTED)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                care_title,
                                care_summary,
                                care_steps,
                                ft.Row([ft.Button("케어 완료했어", on_click=complete_care), care_result], wrap=True, spacing=10),
                            ],
                            spacing=8,
                        ),
                        bgcolor="#182640",
                        border_radius=20,
                        padding=18,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("컨디션 패널", size=23, weight=ft.FontWeight.BOLD, color=TEXT),
                                ft.Row(
                                    [
                                        ft.Column([slider("졸림", "sleepiness", state.sleepiness), slider("집중", "focus", state.focus)], expand=True),
                                        ft.Column([slider("이해도", "understanding", state.understanding), slider("배고픔", "hunger", state.hunger)], expand=True),
                                    ],
                                    spacing=28,
                                ),
                            ]
                        ),
                        bgcolor="#101D35",
                        border_radius=20,
                        padding=18,
                    ),
                ],
                spacing=12,
                padding=18,
                expand=True,
            )
        )
    )
    refresh()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
