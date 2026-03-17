from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_message(name: str | None = None, uppercase: bool = False) -> str:
    target = name.strip() if name else "mangbralouma"
    message = f"Projet {target} initialise."
    return message.upper() if uppercase else message


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mangbralouma",
        description="Point d'entree du projet mangbralouma.",
    )
    parser.add_argument(
        "--name",
        help="Nom du projet ou du contexte a afficher.",
    )
    parser.add_argument(
        "--upper",
        action="store_true",
        help="Affiche le message en majuscules.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    print(build_message(name=args.name, uppercase=args.upper))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
