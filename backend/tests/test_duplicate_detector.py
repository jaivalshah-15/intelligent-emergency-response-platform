from app.services.duplicate_detector import text_similarity


def test_similar_incident_text():
    score = text_similarity(
        "Large factory fire near Ahmedabad",
        "Factory fire near Ahmedabad area"
    )

    assert score > 0.6

def test_different_incident_text():
    score = text_similarity(
        "Factory fire in Ahmedabad",
        "Heavy flooding in Surat"
    )

    assert score < 0.6