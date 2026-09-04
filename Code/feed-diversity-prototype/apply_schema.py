"""One-off helper to create the `posts` table via the Supabase Management API.

Direct Postgres connections (port 5432) aren't reachable from this sandbox's
network, so this goes over HTTPS instead. Needs a Supabase *personal access
token* (Dashboard -> account menu -> Access Tokens), separate from the
project's publishable/secret API keys - set it as SUPABASE_MANAGEMENT_TOKEN.
Revoke the token again afterwards if you'd rather not leave it lying around.

Usage: SUPABASE_MANAGEMENT_TOKEN=... python apply_schema.py
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_REF = "oblighpdvoefwkkyttja"
SCHEMA_FILE = Path(__file__).parent / "supabase" / "migrations" / "0001_init.sql"


def main() -> None:
    token = os.environ.get("SUPABASE_MANAGEMENT_TOKEN")
    if not token:
        print("SUPABASE_MANAGEMENT_TOKEN not set, see module docstring.", file=sys.stderr)
        sys.exit(1)

    query = SCHEMA_FILE.read_text(encoding="utf-8")
    response = requests.post(
        f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"query": query},
        timeout=15,
    )
    if response.ok:
        print("Schema applied.")
    else:
        print(f"Failed ({response.status_code}): {response.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
