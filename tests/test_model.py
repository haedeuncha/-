from src.classroom_control.model import ClassroomState


def test_survival_score_uses_all_four_conditions():
    state = ClassroomState(sleepiness=20, focus=80, understanding=60, hunger=40)

    assert state.survival_score == 70


def test_score_bands_have_the_expected_messages():
    assert ClassroomState(sleepiness=0, focus=100, understanding=100, hunger=0).theme.message == "완전 몰입 중!"
    assert ClassroomState().theme.message == "잘 버티는 중!"
    assert ClassroomState(sleepiness=100, focus=20, understanding=20, hunger=100).theme.message == "긴급 휴식 권장!"


def test_start_and_stop_track_elapsed_time():
    state = ClassroomState()

    assert state.start() is True
    assert state.start() is False
    assert state.stop() is True
    assert state.stop() is False


def test_quick_presets_change_the_classroom_state():
    state = ClassroomState()

    state.apply_preset("focus")
    assert state.survival_score >= 80

    state.apply_preset("hungry")
    assert state.hunger == 90


def test_encouragement_can_change_without_changing_the_score():
    state = ClassroomState()
    first_message = state.encouragement

    state.next_encouragement()

    assert state.encouragement != first_message
    assert state.survival_score == 50


def test_recommended_care_targets_the_largest_need():
    state = ClassroomState(sleepiness=90, focus=80, understanding=80, hunger=20)

    assert state.recommended_care.key == "sleepiness"

    state.complete_care("sleepiness")
    assert state.sleepiness == 75
    assert state.focus == 90


def test_hunger_care_reduces_hunger():
    state = ClassroomState(hunger=90)

    state.complete_care("hunger")

    assert state.hunger == 65
