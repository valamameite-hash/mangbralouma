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
    "export_id": 1,
}

EVENT_REASONS = (
    "funerailles",
    "mariage",
    "baptemes",
    "sacrifices",
    "autres",
)


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
    first_name: str,
    last_name: str,
    nickname: str | None,
    country: str | None,
    city: str | None,
    occupation: str | None,
    phone: str | None,
    email: str | None,
) -> tuple[int, str]:
    data = load_data(data_path)
    member_id = data["next_member_id"]
    first_name_clean = first_name.strip()
    last_name_clean = last_name.strip()
    full_name = f"{first_name_clean} {last_name_clean}".strip()
    data["members"].append(
        {
            "id": member_id,
            "first_name": first_name_clean,
            "last_name": last_name_clean,
            "nickname": nickname.strip() if nickname else None,
            "country": country.strip() if country else None,
            "city": city.strip() if city else None,
            "occupation": occupation.strip() if occupation else None,
            "name": full_name,
            "phone": phone.strip() if phone else None,
            "email": email.strip() if email else None,
        }
    )
    data["next_member_id"] = member_id + 1
    save_data(data_path, data)
    return 0, f"Membre ajoute: #{member_id} {full_name}"


def cmd_member_list(data_path: Path) -> tuple[int, str]:
    data = load_data(data_path)
    members = data["members"]
    if not members:
        return 0, "Aucun membre enregistre."
    lines = ["Membres:"]
    for member in members:
        first_name = member.get("first_name", "").strip()
        last_name = member.get("last_name", "").strip()
        display_name = (f"{first_name} {last_name}").strip()
        if not display_name:
            display_name = member.get("name", "Sans nom")

        lines.append(
            f"- #{member['id']} {display_name} "
            "(tel: "
            f"{member.get('phone') or '-'}, "
            "email: "
            f"{member.get('email') or '-'})"
        )
        lines.append(
            "  "
            f"sobriquet: {member.get('nickname') or '-'}, "
            f"residence: {member.get('city') or '-'}, "
            f"{member.get('country') or '-'}, "
            f"activite: {member.get('occupation') or '-'}"
        )
    return 0, "\n".join(lines)


def cmd_member_search(
    data_path: Path,
    query: str,
) -> tuple[int, str]:
    data = load_data(data_path)
    query_lower = query.lower().strip()
    found = []
    for member in data["members"]:
        if member.get("active", True) is False:
            continue
        full_name = (
            f"{member.get('first_name', '')} "
            f"{member.get('last_name', '')}"
        ).lower()
        nickname = (member.get("nickname") or "").lower()
        phone = (member.get("phone") or "").lower()
        email = (member.get("email") or "").lower()
        if (
            query_lower in full_name
            or query_lower in nickname
            or query_lower in phone
            or query_lower in email
        ):
            found.append(member)
    if not found:
        return 0, f"Aucun membre correspond a '{query}'."
    lines = [f"Resultats de recherche pour '{query}':"]
    for member in found:
        first_name = member.get("first_name", "").strip()
        last_name = member.get("last_name", "").strip()
        display_name = (f"{first_name} {last_name}").strip()
        lines.append(
            f"- #{member['id']} {display_name} "
            f"({member.get('phone') or '-'})"
        )
    return 0, "\n".join(lines)


def cmd_member_update(
    data_path: Path,
    member_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    nickname: str | None = None,
    country: str | None = None,
    city: str | None = None,
    occupation: str | None = None,
    phone: str | None = None,
    email: str | None = None,
) -> tuple[int, str]:
    data = load_data(data_path)
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"
    if first_name is not None:
        member["first_name"] = first_name.strip()
    if last_name is not None:
        member["last_name"] = last_name.strip()
    if nickname is not None:
        member["nickname"] = (
            nickname.strip() if nickname.strip() else None
        )
    if country is not None:
        member["country"] = (
            country.strip() if country.strip() else None
        )
    if city is not None:
        member["city"] = city.strip() if city.strip() else None
    if occupation is not None:
        member["occupation"] = (
            occupation.strip() if occupation.strip() else None
        )
    if phone is not None:
        member["phone"] = phone.strip() if phone.strip() else None
    if email is not None:
        member["email"] = email.strip() if email.strip() else None
    member["name"] = (
        f"{member.get('first_name', '')} "
        f"{member.get('last_name', '')}"
    ).strip()
    save_data(data_path, data)
    return 0, f"Membre #{member_id} mis a jour."


def cmd_member_delete(
    data_path: Path,
    member_id: int,
) -> tuple[int, str]:
    data = load_data(data_path)
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"
    data["members"] = [m for m in data["members"] if m["id"] != member_id]
    save_data(data_path, data)
    return 0, f"Membre #{member_id} supprime."


def cmd_member_deactivate(
    data_path: Path,
    member_id: int,
) -> tuple[int, str]:
    data = load_data(data_path)
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"
    member["active"] = False
    save_data(data_path, data)
    return 0, f"Membre #{member_id} archive."


def cmd_member_reactivate(
    data_path: Path,
    member_id: int,
) -> tuple[int, str]:
    data = load_data(data_path)
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"
    member["active"] = True
    save_data(data_path, data)
    return 0, f"Membre #{member_id} reacte."


def cmd_cotisation_report(
    data_path: Path,
    member_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> tuple[int, str]:
    data = load_data(data_path)
    cotisations = data["cotisations"]
    if member_id is not None:
        cotisations = [
            entry for entry in cotisations
            if entry["member_id"] == member_id
        ]
    if start_date:
        cotisations = [
            entry for entry in cotisations
            if entry["date"] >= start_date
        ]
    if end_date:
        cotisations = [
            entry for entry in cotisations
            if entry["date"] <= end_date
        ]
    if not cotisations:
        return 0, "Aucune cotisation trouve dans la periode."
    lines = ["Rapport des cotisations:"]
    total = 0.0
    for entry in cotisations:
        amount = float(entry["amount"])
        total += amount
        member = find_member(data, entry["member_id"])
        member_name = (
            f"{member.get('first_name', '')} "
            f"{member.get('last_name', '')}"
        ).strip() if member else f"#{entry['member_id']}"
        lines.append(
            f"- {entry['date']} {member_name} ({entry['member_id']}) "
            f"{amount:.2f} XOF"
        )
        if entry.get("note"):
            lines.append(f"  Note: {entry['note']}")
    lines.append(f"Total: {total:.2f} XOF")
    return 0, "\n".join(lines)


def cmd_event_add_attendee(
    data_path: Path,
    event_id: int,
    member_id: int,
) -> tuple[int, str]:
    data = load_data(data_path)
    event = None
    for evt in data["events"]:
        if evt["id"] == event_id:
            event = evt
            break
    if not event:
        return 1, f"Evenement introuvable: #{event_id}"
    member = find_member(data, member_id)
    if not member:
        return 1, f"Membre introuvable: #{member_id}"
    if "attendees" not in event:
        event["attendees"] = []
    if member_id not in event["attendees"]:
        event["attendees"].append(member_id)
        save_data(data_path, data)
        return (
            0,
            f"Membre #{member_id} ajoute a "
            f"l'evenement #{event_id}.",
        )
    return 0, f"Membre #{member_id} etait deja present."


def export_to_csv(
    data_path: Path,
    entity_type: str,
) -> tuple[int, str]:
    try:
        import csv
    except ImportError:
        return 1, "Module csv non disponible."
    data = load_data(data_path)
    export_path = data_path.parent / f"{entity_type}_export.csv"
    try:
        if entity_type == "members":
            with export_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "ID", "Prenom", "Nom", "Sobriquet",
                        "Pays", "Ville", "Activite",
                        "Telephone", "Email", "Actif",
                    ]
                )
                for member in data.get("members", []):
                    writer.writerow(
                        [
                            member.get("id"),
                            member.get("first_name", ""),
                            member.get("last_name", ""),
                            member.get("nickname", ""),
                            member.get("country", ""),
                            member.get("city", ""),
                            member.get("occupation", ""),
                            member.get("phone", ""),
                            member.get("email", ""),
                            member.get("active", True),
                        ]
                    )
        elif entity_type == "cotisations":
            with export_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "ID", "Member ID", "Montant",
                        "Date", "Note",
                    ]
                )
                for cot in data.get("cotisations", []):
                    writer.writerow(
                        [
                            cot.get("id"),
                            cot.get("member_id"),
                            cot.get("amount"),
                            cot.get("date"),
                            cot.get("note", ""),
                        ]
                    )
        elif entity_type == "events":
            with export_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "ID", "Titre", "Date", "Raison",
                        "Montant", "Description",
                    ]
                )
                for evt in data.get("events", []):
                    writer.writerow(
                        [
                            evt.get("id"),
                            evt.get("title"),
                            evt.get("date"),
                            evt.get("reason"),
                            evt.get("amount"),
                            evt.get("description", ""),
                        ]
                    )
        else:
            return 1, f"Type d'export non reconnu: {entity_type}"
        return (
            0,
            f"Export reussi: {export_path}",
        )
    except Exception as e:
        return 1, f"Erreur lors de l'export: {e}"


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
    reason: str,
    amount: float,
    description: str | None,
) -> tuple[int, str]:
    if amount < 0:
        return 1, "Le montant cotise ne peut pas etre negatif."
    if reason not in EVENT_REASONS:
        return 1, "Raison invalide pour la cotisation de l'evenement."

    data = load_data(data_path)
    event_id = data["next_event_id"]
    data["events"].append(
        {
            "id": event_id,
            "title": title.strip(),
            "date": event_date,
            "reason": reason,
            "amount": float(amount),
            "description": description.strip() if description else None,
        }
    )
    data["next_event_id"] = event_id + 1
    save_data(data_path, data)
    return (
        0,
        "Evenement ajoute: "
        f"#{event_id} {title.strip()} ({event_date}) "
        f"raison={reason} montant={amount:.2f}",
    )


def cmd_event_list(
    data_path: Path,
    reason: str | None = None,
) -> tuple[int, str]:
    data = load_data(data_path)
    events = data["events"]
    if reason:
        events = [event for event in events if event.get("reason") == reason]
    if not events:
        return 0, "Aucun evenement enregistre."
    lines = ["Evenements:"]
    for event in events:
        reason = event.get("reason", "autres")
        amount = float(event.get("amount", 0.0))
        text = f"- #{event['id']} {event['date']} {event['title']}"
        text += f" | raison: {reason} | montant: {amount:.2f}"
        if event.get("description"):
            text += f" - {event['description']}"
        lines.append(text)
    return 0, "\n".join(lines)


def cmd_summary(data_path: Path) -> tuple[int, str]:
    data = load_data(data_path)
    total = sum(entry["amount"] for entry in data["cotisations"])
    total_events = sum(
        float(event.get("amount", 0.0)) for event in data["events"]
    )
    lines = [
        "Resume:",
        f"- Membres: {len(data['members'])}",
        f"- Cotisations: {len(data['cotisations'])}",
        f"- Total cotisations: {total:.2f}",
        f"- Evenements: {len(data['events'])}",
        f"- Total cotise sur evenements: {total_events:.2f}",
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
    member_add.add_argument(
        "--first-name",
        required=True,
        help="Prenom du membre.",
    )
    member_add.add_argument(
        "--last-name",
        required=True,
        help="Nom de famille du membre.",
    )
    member_add.add_argument("--nickname", help="Sobriquet du membre.")
    member_add.add_argument(
        "--country",
        help="Pays de residence du membre.",
    )
    member_add.add_argument(
        "--city",
        help="Ville de residence du membre.",
    )
    member_add.add_argument(
        "--occupation",
        help="Activite professionnelle du membre.",
    )
    member_add.add_argument("--phone", help="Telephone du membre.")
    member_add.add_argument("--email", help="Email du membre.")
    member_sub.add_parser("list", help="Lister les membres.")
    member_search = member_sub.add_parser("search", help="Chercher un membre.")
    member_search.add_argument(
        "--query",
        required=True,
        help="Rechercher par nom, email ou telephone.",
    )
    member_update = member_sub.add_parser(
        "update",
        help="Mettre a jour un membre.",
    )
    member_update.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID du membre a mettre a jour.",
    )
    member_update.add_argument(
        "--first-name",
        help="Nouveau prenom.",
    )
    member_update.add_argument(
        "--last-name",
        help="Nouveau nom.",
    )
    member_update.add_argument(
        "--nickname",
        help="Nouveau sobriquet.",
    )
    member_update.add_argument(
        "--country",
        help="Nouveau pays.",
    )
    member_update.add_argument(
        "--city",
        help="Nouvelle ville.",
    )
    member_update.add_argument(
        "--occupation",
        help="Nouvelle activite.",
    )
    member_update.add_argument(
        "--phone",
        help="Nouveau telephone.",
    )
    member_update.add_argument(
        "--email",
        help="Nouveau email.",
    )
    member_delete = member_sub.add_parser(
        "delete",
        help="Supprimer un membre.",
    )
    member_delete.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID du membre a supprimer.",
    )
    member_deactivate = member_sub.add_parser(
        "deactivate",
        help="Desactiver un membre (archivage).",
    )
    member_deactivate.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID du membre a desactiver.",
    )
    member_reactivate = member_sub.add_parser(
        "reactivate",
        help="Reactiver un membre.",
    )
    member_reactivate.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID du membre a reactiver.",
    )

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
    cot_report = cot_sub.add_parser(
        "report",
        help="Generer un rapport de cotisations.",
    )
    cot_report.add_argument("--member-id", type=int, help="Filtrer par membre.")
    cot_report.add_argument(
        "--start-date",
        help="Date de debut (YYYY-MM-DD).",
    )
    cot_report.add_argument(
        "--end-date",
        help="Date de fin (YYYY-MM-DD).",
    )

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
    event_add.add_argument(
        "--reason",
        choices=EVENT_REASONS,
        default="autres",
        help="Raison: funerailles, mariage, baptemes, sacrifices, autres.",
    )
    event_add.add_argument(
        "--amount",
        type=float,
        required=True,
        help="Montant cotise pour l'evenement.",
    )
    event_add.add_argument("--description", help="Description optionnelle.")
    event_list = event_sub.add_parser("list", help="Lister les evenements.")
    event_list.add_argument(
        "--reason",
        choices=EVENT_REASONS,
        help="Filtrer la liste par raison.",
    )
    event_attendee = event_sub.add_parser(
        "add-attendee",
        help="Ajouter un participant a un evenement.",
    )
    event_attendee.add_argument(
        "--event-id",
        required=True,
        type=int,
        help="ID de l'evenement.",
    )
    event_attendee.add_argument(
        "--member-id",
        required=True,
        type=int,
        help="ID du membre participant.",
    )

    subparsers.add_parser("summary", help="Afficher un resume global.")

    export_parser = subparsers.add_parser(
        "export",
        help="Exporter les donnees.",
    )
    export_parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Format d'export.",
    )
    export_parser.add_argument(
        "--type",
        choices=["members", "cotisations", "events"],
        required=True,
        help="Type d'entite a exporter.",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    data_path = Path(args.data)

    if args.command == "init":
        code, message = cmd_init(data_path, force=args.force)
    elif args.command == "member" and args.member_command == "add":
        code, message = cmd_member_add(
            data_path,
            first_name=args.first_name,
            last_name=args.last_name,
            nickname=args.nickname,
            country=args.country,
            city=args.city,
            occupation=args.occupation,
            phone=args.phone,
            email=args.email,
        )
    elif args.command == "member" and args.member_command == "list":
        code, message = cmd_member_list(data_path)
    elif args.command == "member" and args.member_command == "search":
        code, message = cmd_member_search(data_path, query=args.query)
    elif args.command == "member" and args.member_command == "update":
        code, message = cmd_member_update(
            data_path,
            member_id=args.id,
            first_name=args.first_name,
            last_name=args.last_name,
            nickname=args.nickname,
            country=args.country,
            city=args.city,
            occupation=args.occupation,
            phone=args.phone,
            email=args.email,
        )
    elif args.command == "member" and args.member_command == "delete":
        code, message = cmd_member_delete(data_path, member_id=args.id)
    elif args.command == "member" and args.member_command == "deactivate":
        code, message = cmd_member_deactivate(
            data_path,
            member_id=args.id,
        )
    elif args.command == "member" and args.member_command == "reactivate":
        code, message = cmd_member_reactivate(
            data_path,
            member_id=args.id,
        )
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
    elif args.command == "cotisation" and args.cot_command == "report":
        code, message = cmd_cotisation_report(
            data_path,
            member_id=args.member_id,
            start_date=args.start_date,
            end_date=args.end_date,
        )
    elif args.command == "event" and args.event_command == "add":
        code, message = cmd_event_add(
            data_path,
            title=args.title,
            event_date=args.event_date,
            reason=args.reason,
            amount=args.amount,
            description=args.description,
        )
    elif args.command == "event" and args.event_command == "list":
        code, message = cmd_event_list(data_path, reason=args.reason)
    elif args.command == "event" and args.event_command == "add-attendee":
        code, message = cmd_event_add_attendee(
            data_path,
            event_id=args.event_id,
            member_id=args.member_id,
        )
    elif args.command == "summary":
        code, message = cmd_summary(data_path)
    elif args.command == "export":
        code, message = export_to_csv(data_path, entity_type=args.type)
    else:
        code, message = 1, "Commande non reconnue."

    print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
