from video_notes.profiles import get_profile


def test_known_profile():
    assert "Review Questions" in get_profile("course")


def test_unknown_profile_falls_back_to_general():
    assert get_profile("missing") == get_profile("general")
