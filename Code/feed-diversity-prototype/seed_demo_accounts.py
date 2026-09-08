"""One-off script: creates a handful of demo accounts plus one admin account
and a lopsided like history, so a live demo can immediately show
ranking.dominant_perspective()/dominant_political_label() pulling the
standard feed toward whichever side an account has been liking.

Requires SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY and SUPABASE_SECRET_KEY in
the environment/.env (same variables db.py already uses) - refuses to run
without them rather than doing anything with placeholder values. The actual
email/password pairs used here are also read from the environment (see
DEMO_ACCOUNTS below) so no credentials end up in this file or in git.

Usage (once .env has SUPABASE_* and the DEMO_ACCOUNT_* variables below set):

    python3 seed_demo_accounts.py

Safe to re-run: sign_up() on an already-registered email just fails and this
script logs in instead, so accounts aren't duplicated. Posts/likes ARE
duplicated on a second run though (no dedup key on content) - only run once
per environment, or clean up manually via the Supabase dashboard first.

See README.md ("Beispiel-Accounts fuer den Standard-Algorithmus") and the
vault note ObsidianGehirn/06 Zugangsdaten/Feed-Diversity-Beispielaccounts.md
(name/Zweck ohne Zugangsdaten) for context.
"""

import os
import sys

import db
from ranking import Post

# Each entry: (env var prefix, display name, topic/perspective/political_label
# the account should consistently like). Deliberately one-sided per account
# so the bias is obvious within a handful of likes - this is a demo dataset,
# not meant to look like realistic organic behaviour.
DEMO_ACCOUNTS = [
    {"prefix": "DEMO_ACCOUNT_A", "display_name": "Nora Bergmann", "like_perspective": "contra", "like_political_label": "links"},
    {"prefix": "DEMO_ACCOUNT_B", "display_name": "Jonas Kessler", "like_perspective": "pro", "like_political_label": "rechts"},
    {"prefix": "DEMO_ACCOUNT_C", "display_name": "Lea Vogt", "like_perspective": "contra", "like_political_label": "links"},
    {"prefix": "DEMO_ACCOUNT_D", "display_name": "Tarek Aydin", "like_perspective": "pro", "like_political_label": "rechts"},
]
ADMIN_ACCOUNT = {"prefix": "DEMO_ADMIN", "display_name": "Team 13 Admin"}

# A handful of seed posts covering both perspectives/political labels per
# topic, so each demo account has enough same-leaning content to like.
# Posted under the admin account so the demo accounts' own like histories
# stay clean/interpretable.
SEED_POSTS = [
    Post("", "Windkraft-Ausbau beschleunigen", "Der Ausbau von Windkraft ist zentral fuer die Energiewende und muss beschleunigt werden.", "klima", "pro", "rechts"),
    Post("", "Windkraft belastet Anwohner", "Windkraftanlagen veraendern die Landschaft, die Kosten fuer den Ausbau sind zu hoch.", "klima", "contra", "links"),
    Post("", "Tempolimit jetzt einfuehren", "Ein Tempolimit auf Autobahnen senkt CO2-Ausstoss und Unfallzahlen spuerbar.", "verkehr", "pro", "links"),
    Post("", "Tempolimit bremst Mobilitaet aus", "Ein generelles Tempolimit bringt wenig, schraenkt aber individuelle Mobilitaet unnoetig ein.", "verkehr", "contra", "rechts"),
    Post("", "Mindestlohn deutlich anheben", "Ein hoeherer Mindestlohn staerkt die Kaufkraft und wirkt gegen Armut.", "wirtschaft", "pro", "links"),
    Post("", "Mindestlohn gefaehrdet Arbeitsplaetze", "Ein zu hoher Mindestlohn ueberfordert kleine Betriebe und kostet Arbeitsplaetze.", "wirtschaft", "contra", "rechts"),
    Post("", "Digitale Buergerrechte staerken", "Datenschutz und digitale Selbstbestimmung muessen gegenueber Konzernen gestaerkt werden.", "digital", "pro", "links"),
    Post("", "Weniger Regulierung fuer Tech-Standort", "Zu strenge Digitalregulierung schadet dem Innovationsstandort und der Wettbewerbsfaehigkeit.", "digital", "contra", "rechts"),
]


def _require_env(prefix: str) -> tuple[str, str]:
    email = os.environ.get(f"{prefix}_EMAIL")
    password = os.environ.get(f"{prefix}_PASSWORD")
    if not email or not password:
        print(f"Fehlt: {prefix}_EMAIL/{prefix}_PASSWORD in der Umgebung/.env - breche ab.", file=sys.stderr)
        sys.exit(1)
    return email, password


def _ensure_account(email: str, password: str, display_name: str) -> str:
    user = db.sign_up(email, password)
    if user is None:
        user = db.sign_in(email, password)
    if user is None:
        print(f"Konnte Account fuer {display_name} ({email}) weder anlegen noch einloggen.", file=sys.stderr)
        sys.exit(1)
    if db.fetch_profile(user["id"]) is None:
        db.create_unique_profile(user["id"], display_name)
    return user["id"]


def main() -> None:
    if not db.is_configured() or not db.auth_configured():
        print(
            "SUPABASE_URL/SUPABASE_SECRET_KEY/SUPABASE_PUBLISHABLE_KEY fehlen - "
            "bitte .env setzen, bevor dieses Skript laeuft. Keine Dummy-Werte moeglich.",
            file=sys.stderr,
        )
        sys.exit(1)

    admin_email, admin_password = _require_env(ADMIN_ACCOUNT["prefix"])
    admin_id = _ensure_account(admin_email, admin_password, ADMIN_ACCOUNT["display_name"])
    print(f"Admin-Account bereit: {ADMIN_ACCOUNT['display_name']}")

    for post in SEED_POSTS:
        db.insert_post(post.title, post.text, post.topic, post.perspective, admin_id, post.political_label)
    print(f"{len(SEED_POSTS)} Seed-Posts unter dem Admin-Account angelegt.")

    all_posts = db.fetch_posts()
    if not all_posts:
        print("Konnte die gerade angelegten Posts nicht wieder auslesen - Abbruch.", file=sys.stderr)
        sys.exit(1)

    for account in DEMO_ACCOUNTS:
        email, password = _require_env(account["prefix"])
        user_id = _ensure_account(email, password, account["display_name"])

        matching = [
            row["post"]
            for row in all_posts
            if row["post"].perspective == account["like_perspective"]
            and row["post"].political_label == account["like_political_label"]
        ]
        for post in matching:
            db.toggle_like(post.id, user_id)
        print(
            f"{account['display_name']}: {len(matching)} Posts geliked "
            f"({account['like_perspective']}/{account['like_political_label']})."
        )

    print(
        "\nFertig. Zum Vorfuehren: mit einem der Demo-Accounts einloggen und den "
        "Standard-Feed oeffnen - er sollte klar in Richtung der jeweiligen "
        "Like-Historie verzerrt sein."
    )


if __name__ == "__main__":
    main()
