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
