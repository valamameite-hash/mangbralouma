from mangbralouma.main import main


def test_main(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert "Projet mangbralouma initialise." in captured.out
