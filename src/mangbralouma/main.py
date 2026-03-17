from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from collections.abc import Sequence


DEFAULT_DATA = {
    "next_member_id": 1,
    "next_cotisation_id": 1,
    "next_event_id": 1,
    "members": [],
    "cotisations": [],
    "events": [],
}


def load_data(data_path: Path) -> dict:
    if not data_path.exists():
        return dict(DEFAULT_DATA)
    with data_path.open("r", encoding="utf-8") as file:
        raw = json.load(file)
    data = dict(DEFAULT_DATA)
    data.update(raw)
    return data


def save_data(data_path: Path, data: dict) -> None:
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with data_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def cmd_init(data_path: Path, force: bool) -> tuple[int, str]:
    if data_path.exists() and not force:
        return 0, f"Base deja presente: {data_path}"
    save_data(data_path, dict(DEFAULT_DATA))
    return 0, f"Base creee: {data_path}"


def cmd_member_add(
    data_path: Path,
    name: str,
    phone: str | None,
    email: str | None,
) -> tuple[int, str]:
    data = load_data(data_path)
    member_id = data["next_member_id"]
    data["members"].append(
        {
            "id": member_id,
            "name": name.strip(),
            "phone": phone.strip() if phone else None,
            "email": email.strip() if email else None,
        }
    )
    data["next_member_id"] = member_id + 1
    save_data(data_path, data)
    return 0, f"Membre ajoute: #{member_id} {name.strip()}"


def cmd_member_list(data_path: Path) -> tuple[int, str]:
    data = load_data(data_path)
    members = data["members"]
    if not members:
        return 0, "Aucun membre enregistre."
    lines = ["Membres:"]
    for member in members:
        lines.append(
            f"- #{member['id']} {member['name']} "
            "(tel: "
            f"{member.get('phone') or '-'}, "
            "email: "
            f"{member.get('email') or '-'})"
        )
    return 0, "\n".join(lines)


def find_member(data: dict, member_id: int) -> dict | None:
    for member in data["members"]:
        if member["id"] == member_id:
            return member
    return None


def cmd_cotisation_add(
    data_path: Path,
    member_id: int,
    amount: float,
    payment_date: str,
    note: str | None,
) -> tuple[int, str]:
    if amount <= 0:
        return 1, "Le montant doit etre strictement positif."
    data = load_data(data_path)
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"

    cotisation_id = data["next_cotisation_id"]
    data["cotisations"].append(
        {
            "id": cotisation_id,
            "member_id": member_id,
            "amount": float(amount),
            "date": payment_date,
            "note": note.strip() if note else None,
        }
    )
    data["next_cotisation_id"] = cotisation_id + 1
    save_data(data_path, data)
    return (
        0,
        "Cotisation ajoutee: "
        f"#{cotisation_id} membre #{member_id} montant {amount:.2f}",
    )


def cmd_cotisation_list(
    data_path: Path,
    member_id: int | None,
) -> tuple[int, str]:
    data = load_data(data_path)
    cotisations = data["cotisations"]
    if member_id is not None:
        cotisations = [
            entry for entry in cotisations if entry["member_id"] == member_id
        ]
    if not cotisations:
        return 0, "Aucune cotisation enregistree."

    lines = ["Cotisations:"]
    for entry in cotisations:
        lines.append(
            f"- #{entry['id']} membre #{entry['member_id']} "
            f"{entry['amount']:.2f} le {entry['date']}"
            + (f" note: {entry['note']}" if entry.get("note") else "")
        )
    return 0, "\n".join(lines)


def cmd_event_add(
    data_path: Path,
    title: str,
    event_date: str,
    description: str | None,
) -> tuple[int, str]:
    data = load_data(data_path)
    event_id = data["next_event_id"]
    data["events"].append(
        {
            "id": event_id,
            "title": title.strip(),
            "date": event_date,
            "description": description.strip() if description else None,
        }
    )
    data["next_event_id"] = event_id + 1
    save_data(data_path, data)
    return 0, f"Evenement ajoute: #{event_id} {title.strip()} ({event_date})"


def cmd_event_list(data_path: Path) -> tuple[int, str]:
    data = load_data(data_path)
    events = data["events"]
    if not events:
        return 0, "Aucun evenement enregistre."
    lines = ["Evenements:"]
    for event in events:
        text = f"- #{event['id']} {event['date']} {event['title']}"
        if event.get("description"):
            text += f" - {event['description']}"
        lines.append(text)
    return 0, "\n".join(lines)


def cmd_summary(data_path: Path) -> tuple[int, str]:
    data = load_data(data_path)
    total = sum(entry["amount"] for entry in data["cotisations"])
    lines = [
        "Resume:",
        f"- Membres: {len(data['members'])}",
        f"- Cotisations: {len(data['cotisations'])}",
        f"- Total cotisations: {total:.2f}",
        f"- Evenements: {len(data['events'])}",
    ]
    return 0, "\n".join(lines)


def parse_iso_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Format de date attendu: YYYY-MM-DD"
        ) from exc
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mangbralouma",
        description=(
            "Gestion de la grande famille: membres, "
            "cotisations et evenements."
        ),
    )
    parser.add_argument(
        "--data",
        default=".mangbralouma_data.json",
        help="Chemin vers le fichier JSON de stockage.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init",
        help="Initialiser la base de donnees locale.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Reinitialiser la base meme si elle existe.",
    )

    member_parser = subparsers.add_parser(
        "member",
        help="Gestion des membres.",
    )
    member_sub = member_parser.add_subparsers(
        dest="member_command",
        required=True,
    )
    member_add = member_sub.add_parser("add", help="Ajouter un membre.")
    member_add.add_argument("--name", required=True, help="Nom du membre.")
    member_add.add_argument("--phone", help="Telephone du membre.")
    member_add.add_argument("--email", help="Email du membre.")
    member_sub.add_parser("list", help="Lister les membres.")

    cot_parser = subparsers.add_parser(
        "cotisation",
        help="Gestion des cotisations.",
    )
    cot_sub = cot_parser.add_subparsers(dest="cot_command", required=True)
    cot_add = cot_sub.add_parser("add", help="Ajouter une cotisation.")
    cot_add.add_argument(
        "--member-id",
        required=True,
        type=int,
        help="Identifiant du membre.",
    )
    cot_add.add_argument(
        "--amount",
        required=True,
        type=float,
        help="Montant de la cotisation.",
    )
    cot_add.add_argument(
        "--date",
        dest="payment_date",
        type=parse_iso_date,
        default=date.today().isoformat(),
        help="Date de paiement au format YYYY-MM-DD.",
    )
    cot_add.add_argument("--note", help="Note optionnelle.")
    cot_list = cot_sub.add_parser("list", help="Lister les cotisations.")
    cot_list.add_argument("--member-id", type=int, help="Filtrer par membre.")

    event_parser = subparsers.add_parser(
        "event",
        help="Gestion des evenements.",
    )
    event_sub = event_parser.add_subparsers(
        dest="event_command",
        required=True,
    )
    event_add = event_sub.add_parser("add", help="Ajouter un evenement.")
    event_add.add_argument(
        "--title",
        required=True,
        help="Titre de l'evenement.",
    )
    event_add.add_argument(
        "--date",
        dest="event_date",
        required=True,
        type=parse_iso_date,
    )
    event_add.add_argument("--description", help="Description optionnelle.")
    event_sub.add_parser("list", help="Lister les evenements.")

    subparsers.add_parser("summary", help="Afficher un resume global.")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    data_path = Path(args.data)

    if args.command == "init":
        code, message = cmd_init(data_path, force=args.force)
    elif args.command == "member" and args.member_command == "add":
        code, message = cmd_member_add(
            data_path,
            name=args.name,
            phone=args.phone,
            email=args.email,
        )
    elif args.command == "member" and args.member_command == "list":
        code, message = cmd_member_list(data_path)
    elif args.command == "cotisation" and args.cot_command == "add":
        code, message = cmd_cotisation_add(
            data_path,
            member_id=args.member_id,
            amount=args.amount,
            payment_date=args.payment_date,
            note=args.note,
        )
    elif args.command == "cotisation" and args.cot_command == "list":
        code, message = cmd_cotisation_list(
            data_path,
            member_id=args.member_id,
        )
    elif args.command == "event" and args.event_command == "add":
        code, message = cmd_event_add(
            data_path,
            title=args.title,
            event_date=args.event_date,
            description=args.description,
        )
    elif args.command == "event" and args.event_command == "list":
        code, message = cmd_event_list(data_path)
    elif args.command == "summary":
        code, message = cmd_summary(data_path)
    else:
        code, message = 1, "Commande non reconnue."

    print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
