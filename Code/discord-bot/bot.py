"""
Discord-Bot, der Claude Code pro Discord-User mit dessen eigenem
CLAUDE_CONFIG_DIR (= eigenes Abo/Login) ansteuert.
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
ALLOWED_CHANNEL_ID = int(os.environ["ALLOWED_CHANNEL_ID"])
MAIN_REPO_PATH = os.environ.get("REPO_PATH", os.path.expanduser("~/RasberryPI-Team-13"))
WORKTREES_BASE = Path(os.path.expanduser("~/repos/worktrees"))
SESSIONS_BASE = Path(os.path.expanduser("~/sessions"))
USERS_FILE = Path(__file__).parent / "users.json"
CLAUDE_TIMEOUT_SECONDS = 300
AUTO_RESET_AFTER_MESSAGES = 25  # Session wird danach automatisch neu gestartet, kein !register noetig


def ensure_worktree(name: str) -> str:
    """Jeder Discord-User bekommt eine eigene Git-Worktree statt sich das
    Arbeitsverzeichnis mit allen anderen Sessions (inkl. Vault-Sync-Cron) zu
    teilen. Gemeinsame Historie/Objekte, aber unabhaengige Branches/Dateien -
    verhindert, dass parallele Sessions sich gegenseitig Branches wegschalten
    oder Dateien in den Weg legen (siehe Claude Discord Bot Setup.md)."""
    worktree_path = WORKTREES_BASE / name
    if not worktree_path.exists():
        WORKTREES_BASE.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=MAIN_REPO_PATH, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(worktree_path), "origin/main"],
            cwd=MAIN_REPO_PATH, check=True, capture_output=True,
        )
    return str(worktree_path)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def load_users() -> dict:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}


def save_users(users: dict) -> None:
    USERS_FILE.write_text(json.dumps(users, indent=2, ensure_ascii=False))


async def run_claude(config_dir: str, worktree_path: str, message: str, session_id):
    cmd = ["claude", "-p", message, "--output-format", "json", "--dangerously-skip-permissions"]
    if session_id:
        cmd += ["--resume", session_id]

    env = os.environ.copy()
    env["CLAUDE_CONFIG_DIR"] = config_dir

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=worktree_path,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=CLAUDE_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        proc.kill()
        return ("Timeout: Claude hat zu lange gebraucht.", session_id)

    if proc.returncode != 0:
        # stderr ist bei der Claude-Code-CLI oft leer, weil Fehler
        # (z.B. abgelaufene OAuth-Session, ungueltige --resume-Session-ID,
        # kaputter Worktree) bei --output-format json haeufig als JSON auf
        # stdout statt auf stderr landen. Ohne Fallback zeigte der Bot dann
        # nur "Fehler von Claude:" mit leerem Codeblock an.
        detail = stderr.decode().strip() or stdout.decode().strip()
        if not detail:
            detail = f"(keine Ausgabe von Claude, nur Exit-Code {proc.returncode})"
        return (f"Fehler von Claude:\n```\n{detail[:1500]}\n```", session_id)

    try:
        data = json.loads(stdout.decode())
    except json.JSONDecodeError:
        return (stdout.decode()[:1900], session_id)

    answer = data.get("result") or data.get("response") or str(data)
    new_session_id = data.get("session_id", session_id)
    return (answer, new_session_id)


def chunk_message(text: str, limit: int = 1900):
    for i in range(0, len(text), limit):
        yield text[i : i + limit]


def bump_and_maybe_reset(user_entry: dict) -> bool:
    """Zaehlt eine Nachricht mit. Gibt True zurueck, wenn die Session ab
    jetzt zurueckgesetzt wird (naechste Nachricht laeuft ohne --resume,
    also faktisch ein "Clear") - Registrierung/Worktree bleiben unberuehrt,
    niemand muss sich deswegen neu per !register anmelden."""
    user_entry["message_count"] = user_entry.get("message_count", 0) + 1
    if user_entry["message_count"] >= AUTO_RESET_AFTER_MESSAGES:
        user_entry["message_count"] = 0
        return True
    return False


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")


@bot.command(name="myid")
async def myid(ctx: commands.Context):
    await ctx.send(f"Deine Discord-User-ID: `{ctx.author.id}`")


@bot.command(name="register")
async def register(ctx: commands.Context, name: str):
    safe_name = "".join(c for c in name if c.isalnum() or c in "-_").lower()
    if not safe_name:
        await ctx.send("Ungueltiger Name. Nur Buchstaben/Zahlen/-/_ erlaubt.")
        return

    config_dir = SESSIONS_BASE / safe_name
    config_dir.mkdir(parents=True, exist_ok=True)
    worktree_path = ensure_worktree(safe_name)

    users = load_users()
    users[str(ctx.author.id)] = {
        "name": safe_name,
        "config_dir": str(config_dir),
        "worktree": worktree_path,
        "session_id": None,
        "message_count": 0,
    }
    save_users(users)

    await ctx.send(
        f"Registriert als `{safe_name}` (eigene Worktree unter `{worktree_path}` angelegt).\n"
        f"Jetzt noch per SSH auf der VM einmalig ausfuehren:\n"
        f"```\nCLAUDE_CONFIG_DIR={config_dir} claude login\n```"
    )


@bot.command(name="clear")
async def clear(ctx: commands.Context):
    users = load_users()
    user_entry = users.get(str(ctx.author.id))
    if not user_entry:
        await ctx.send("Du bist noch nicht registriert. Schreib `!register <deinname>`.")
        return
    user_entry["session_id"] = None
    user_entry["message_count"] = 0
    users[str(ctx.author.id)] = user_entry
    save_users(users)
    await ctx.send(
        "Kontext geleert - naechste Nachricht startet eine frische Claude-Session. "
        "Registrierung bleibt bestehen, kein erneutes !register noetig."
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    if message.content.startswith("!"):
        return
    if message.channel.id != ALLOWED_CHANNEL_ID and getattr(message.channel, "parent_id", None) != ALLOWED_CHANNEL_ID:
        return

    users = load_users()
    user_entry = users.get(str(message.author.id))
    if not user_entry:
        await message.reply(
            "Du bist noch nicht registriert. Schreib `!register <deinname>` und folge der Anleitung."
        )
        return

    worktree_path = user_entry.get("worktree") or ensure_worktree(user_entry["name"])

    async with message.channel.typing():
        answer, new_session_id = await run_claude(
            config_dir=user_entry["config_dir"],
            worktree_path=worktree_path,
            message=message.content,
            session_id=user_entry.get("session_id"),
        )

    if new_session_id != user_entry.get("session_id"):
        user_entry["session_id"] = new_session_id

    reset_now = bump_and_maybe_reset(user_entry)
    if reset_now:
        user_entry["session_id"] = None

    users[str(message.author.id)] = user_entry
    save_users(users)

    for chunk in chunk_message(answer):
        await message.reply(chunk)

    if reset_now:
        await message.channel.send(
            "_Kontext automatisch aufgeraeumt (neue Session, keine erneute Registrierung noetig)._"
        )


if __name__ == "__main__":
    SESSIONS_BASE.mkdir(parents=True, exist_ok=True)
    bot.run(DISCORD_BOT_TOKEN)
