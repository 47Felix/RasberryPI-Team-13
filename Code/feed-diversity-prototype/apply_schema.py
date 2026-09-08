"""One-off helper to apply supabase/migrations/*.sql via the Supabase
Management API.

Direct Postgres connections (port 5432) aren't reachable from this sandbox's
network, so this goes over HTTPS instead. Needs a Supabase *personal access
token* (Dashboard -> account menu -> Access Tokens), separate from the
project's publishable/secret API keys - set it as SUPABASE_MANAGEMENT_TOKEN.
Revoke the token again afterwards if you'd rather not leave it lying around.

Every migration file is idempotent (`if not exists`/`if exists` guards), so
re-running this after a new file was added just re-applies the earlier ones
as no-ops.

Usage: SUPABASE_MANAGEMENT_TOKEN=... python apply_schema.py [file.sql ...]
(with no arguments, applies every supabase/migrations/*.sql in order)
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_REF = "oblighpdvoefwkkyttja"
MIGRATIONS_DIR = Path(__file__).parent / "supabase" / "migrations"


def apply_file(token: str, path: Path) -> bool:
    query = path.read_text(encoding="utf-8")
    response = requests.post(
        f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"query": query},
        timeout=15,
    )
    if response.ok:
        print(f"{path.name}: applied.")
        return True
    print(f"{path.name}: failed ({response.status_code}): {response.text}", file=sys.stderr)
    return False


def main() -> None:
    token = os.environ.get("SUPABASE_MANAGEMENT_TOKEN")
    if not token:
        print("SUPABASE_MANAGEMENT_TOKEN not set, see module docstring.", file=sys.stderr)
        sys.exit(1)

    files = [Path(arg) for arg in sys.argv[1:]] or sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not all(apply_file(token, path) for path in files):
        sys.exit(1)


if __name__ == "__main__":
    main()
