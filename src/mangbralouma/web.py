from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from .main import (
    cmd_cotisation_add,
    cmd_event_add,
    cmd_member_add,
    load_data,
)


def create_app(data_path: Path | None = None) -> Flask:
    app = Flask(__name__)
    app.config["DATA_PATH"] = Path(data_path or ".mangbralouma_data.json")

    @app.get("/")
    def index():
        storage = Path(app.config["DATA_PATH"])
        data = load_data(storage)
        total_cotisations = sum(item["amount"] for item in data["cotisations"])
        return render_template(
            "index.html",
            data=data,
            total_cotisations=total_cotisations,
            today=date.today().isoformat(),
            message=request.args.get("message"),
            error=request.args.get("error"),
        )

    @app.post("/members/add")
    def add_member():
        storage = Path(app.config["DATA_PATH"])
        name = (request.form.get("name") or "").strip()
        phone = (request.form.get("phone") or "").strip() or None
        email = (request.form.get("email") or "").strip() or None
        if not name:
            return redirect(
                url_for("index", error="Le nom du membre est requis.")
            )

        code, msg = cmd_member_add(
            storage,
            name=name,
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
        description = (request.form.get("description") or "").strip() or None

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
            description=description,
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
