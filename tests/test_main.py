from pathlib import Path

from mangbralouma.main import main


def test_init_and_member_listing(capsys, tmp_path: Path) -> None:
    data_file = tmp_path / "family.json"

    assert main(["--data", str(data_file), "init"]) == 0
    assert (
        main([
            "--data",
            str(data_file),
            "member",
            "add",
            "--name",
            "Aicha",
        ])
        == 0
    )
    assert main(["--data", str(data_file), "member", "list"]) == 0

    output = capsys.readouterr().out
    assert "Membre ajoute" in output
    assert "Aicha" in output


def test_cotisation_requires_existing_member(capsys, tmp_path: Path) -> None:
    data_file = tmp_path / "family.json"

    assert main(["--data", str(data_file), "init"]) == 0
    exit_code = main(
        [
            "--data",
            str(data_file),
            "cotisation",
            "add",
            "--member-id",
            "999",
            "--amount",
            "1200",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Membre introuvable" in output


def test_summary_with_cotisation_and_event(capsys, tmp_path: Path) -> None:
    data_file = tmp_path / "family.json"

    assert main(["--data", str(data_file), "init"]) == 0
    assert (
        main([
            "--data",
            str(data_file),
            "member",
            "add",
            "--name",
            "Mariam",
        ])
        == 0
    )
    assert main(
        [
            "--data",
            str(data_file),
            "cotisation",
            "add",
            "--member-id",
            "1",
            "--amount",
            "2500",
            "--date",
            "2026-03-17",
        ]
    ) == 0
    assert main(
        [
            "--data",
            str(data_file),
            "event",
            "add",
            "--title",
            "Reunion familiale",
            "--date",
            "2026-04-05",
        ]
    ) == 0
    assert main(["--data", str(data_file), "summary"]) == 0

    output = capsys.readouterr().out
    assert "Membres: 1" in output
    assert "Cotisations: 1" in output
    assert "Total cotisations: 2500.00" in output
    assert "Evenements: 1" in output
