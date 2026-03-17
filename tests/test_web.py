from pathlib import Path

from mangbralouma.web import create_app


def test_home_page_loads(tmp_path: Path) -> None:
    app = create_app(tmp_path / "family.json")
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Association familiale" in response.get_data(as_text=True)


def test_add_member_from_web(tmp_path: Path) -> None:
    app = create_app(tmp_path / "family.json")
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.post(
            "/members/add",
            data={"name": "Aicha", "phone": "+22300000000"},
            follow_redirects=True,
        )

    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Membre ajoute" in text
    assert "Aicha" in text


def test_add_event_with_reason_and_amount(tmp_path: Path) -> None:
    app = create_app(tmp_path / "family.json")
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.post(
            "/events/add",
            data={
                "title": "Bapteme de Sara",
                "date": "2026-06-01",
                "reason": "baptemes",
                "amount": "7500",
                "description": "Maison familiale",
            },
            follow_redirects=True,
        )

    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Evenement ajoute" in text
    assert "baptemes" in text
    assert "7500.00" in text


def test_web_event_reason_filter(tmp_path: Path) -> None:
    app = create_app(tmp_path / "family.json")
    app.config.update(TESTING=True)

    with app.test_client() as client:
        client.post(
            "/events/add",
            data={
                "title": "Mariage X",
                "date": "2026-07-05",
                "reason": "mariage",
                "amount": "5000",
            },
            follow_redirects=True,
        )
        client.post(
            "/events/add",
            data={
                "title": "Bapteme Y",
                "date": "2026-07-06",
                "reason": "baptemes",
                "amount": "3000",
            },
            follow_redirects=True,
        )
        response = client.get("/?reason=mariage")

    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Mariage X" in text
    assert "Bapteme Y" not in text
