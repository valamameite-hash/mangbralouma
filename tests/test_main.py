from mangbralouma.main import build_message, main


def test_build_message_default() -> None:
    assert build_message() == "Projet mangbralouma initialise."


def test_build_message_with_name() -> None:
    assert build_message(name="demo") == "Projet demo initialise."


def test_main_with_cli_args(capsys) -> None:
    exit_code = main(["--name", "demo", "--upper"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "PROJET DEMO INITIALISE." in captured.out
