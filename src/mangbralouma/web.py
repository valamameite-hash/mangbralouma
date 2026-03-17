from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from .main import (
    EVENT_REASONS,
    cmd_cotisation_add,
    cmd_event_add,
    cmd_member_add,
    cmd_member_update,
    cmd_member_delete,
    cmd_member_search,
    cmd_member_deactivate,
    cmd_cotisation_report,
    cmd_event_add_attendee,
    export_to_csv,
    load_data,
    find_member,
)


def create_app(data_path: Path | None = None) -> Flask:
    app = Flask(__name__)
    app.config["DATA_PATH"] = Path(data_path or ".mangbralouma_data.json")

    @app.get("/")
    def index():
        storage = Path(app.config["DATA_PATH"])
        data = load_data(storage)
        selected_reason = (request.args.get("reason") or "").strip().lower()
        filtered_events = data["events"]
        if selected_reason:
            filtered_events = [
                event
                for event in data["events"]
                if event.get("reason") == selected_reason
            ]

        view_data = dict(data)
        view_data["events"] = filtered_events
        total_cotisations = sum(item["amount"] for item in data["cotisations"])
        total_event_cotisations = sum(
            float(item.get("amount", 0.0)) for item in filtered_events
        )
        return render_template(
            "index.html",
            data=view_data,
            total_cotisations=total_cotisations,
            total_event_cotisations=total_event_cotisations,
            today=date.today().isoformat(),
            event_reasons=EVENT_REASONS,
            selected_reason=selected_reason,
            message=request.args.get("message"),
            error=request.args.get("error"),
        )

    @app.post("/members/add")
    def add_member():
        storage = Path(app.config["DATA_PATH"])
        first_name = (request.form.get("first_name") or "").strip()
        last_name = (request.form.get("last_name") or "").strip()
        nickname = (request.form.get("nickname") or "").strip() or None
        country = (request.form.get("country") or "").strip() or None
        city = (request.form.get("city") or "").strip() or None
        occupation = (request.form.get("occupation") or "").strip() or None
        phone = (request.form.get("phone") or "").strip() or None
        email = (request.form.get("email") or "").strip() or None
        if not first_name or not last_name:
            return redirect(
                url_for(
                    "index",
                    error="Le prenom et le nom du membre sont requis.",
                )
            )

        code, msg = cmd_member_add(
            storage,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            country=country,
            city=city,
            occupation=occupation,
            phone=phone,
            email=email,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.post("/cotisations/add")
    def add_cotisation():
        storage = Path(app.config["DATA_PATH"])

        try:
            member_id = int(request.form.get("member_id", ""))
            amount = float(request.form.get("amount", ""))
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="member_id et amount doivent etre valides.",
                )
            )

        payment_date = (
            request.form.get("date") or date.today().isoformat()
        ).strip()
        note = (request.form.get("note") or "").strip() or None
        code, msg = cmd_cotisation_add(
            storage,
            member_id=member_id,
            amount=amount,
            payment_date=payment_date,
            note=note,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.post("/events/add")
    def add_event():
        storage = Path(app.config["DATA_PATH"])
        title = (request.form.get("title") or "").strip()
        event_date = (request.form.get("date") or "").strip()
        reason = (request.form.get("reason") or "autres").strip().lower()
        amount_raw = (request.form.get("amount") or "").strip()
        description = (request.form.get("description") or "").strip() or None

        try:
            amount = float(amount_raw)
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="Le montant de l'evenement est invalide.",
                )
            )

        if not title or not event_date:
            return redirect(
                url_for(
                    "index",
                    error="Le titre et la date de l'evenement sont requis.",
                )
            )

        code, msg = cmd_event_add(
            storage,
            title=title,
            event_date=event_date,
            reason=reason,
            amount=amount,
            description=description,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.post("/members/update")
    def update_member():
        storage = Path(app.config["DATA_PATH"])
        try:
            member_id = int(request.form.get("id", ""))
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="ID du membre invalide.",
                )
            )
        first_name = (request.form.get("first_name") or "").strip() or None
        last_name = (request.form.get("last_name") or "").strip() or None
        nickname = (request.form.get("nickname") or "").strip() or None
        country = (request.form.get("country") or "").strip() or None
        city = (request.form.get("city") or "").strip() or None
        occupation = (
            (request.form.get("occupation") or "").strip() or None
        )
        phone = (request.form.get("phone") or "").strip() or None
        email = (request.form.get("email") or "").strip() or None
        code, msg = cmd_member_update(
            storage,
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            country=country,
            city=city,
            occupation=occupation,
            phone=phone,
            email=email,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.post("/members/delete")
    def delete_member():
        storage = Path(app.config["DATA_PATH"])
        try:
            member_id = int(request.form.get("id", ""))
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="ID du membre invalide.",
                )
            )
        code, msg = cmd_member_delete(storage, member_id=member_id)
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.post("/members/deactivate")
    def deactivate_member():
        storage = Path(app.config["DATA_PATH"])
        try:
            member_id = int(request.form.get("id", ""))
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="ID du membre invalide.",
                )
            )
        code, msg = cmd_member_deactivate(
            storage,
            member_id=member_id,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    @app.get("/members/search")
    def search_members():
        storage = Path(app.config["DATA_PATH"])
        data = load_data(storage)
        query = (request.args.get("q") or "").strip()
        results = []
        if query:
            query_lower = query.lower()
            for member in data.get("members", []):
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
                    results.append(member)
        return render_template(
            "index.html",
            data=data,
            search_results=results,
            search_query=query,
            total_cotisations=sum(
                item["amount"] for item in data.get("cotisations", [])
            ),
            today=date.today().isoformat(),
            event_reasons=EVENT_REASONS,
        )

    @app.get("/export/<entity_type>")
    def export_data(entity_type: str):
        storage = Path(app.config["DATA_PATH"])
        code, msg = export_to_csv(storage, entity_type=entity_type)
        if code == 0:
            return redirect(
                url_for("index", message=msg)
            )
        return redirect(url_for("index", error=msg))

    @app.post("/events/add-attendee")
    def add_attendee():
        storage = Path(app.config["DATA_PATH"])
        try:
            event_id = int(request.form.get("event_id", ""))
            member_id = int(request.form.get("member_id", ""))
        except ValueError:
            return redirect(
                url_for(
                    "index",
                    error="IDs invalides.",
                )
            )
        code, msg = cmd_event_add_attendee(
            storage,
            event_id=event_id,
            member_id=member_id,
        )
        key = "message" if code == 0 else "error"
        return redirect(url_for("index", **{key: msg}))

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mangbralouma-web",
        description="Serveur web local pour la gestion familiale.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000, type=int)
    parser.add_argument("--data", default=".mangbralouma_data.json")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    app = create_app(Path(args.data))
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    run()
