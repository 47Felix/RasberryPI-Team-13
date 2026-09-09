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

SEED_POSTS below is ~100 posts across 12 topics. Each demo account only
likes at most MAX_LIKES_PER_TOPIC of the matching posts per topic (default
1), so its like history stays small and obviously one-sided even though the
overall dataset is large - the point of the demo is a readable bias, not a
realistic-looking activity log. The eight non-default topics need their
`categories` rows (supabase/migrations/0006_more_categories.sql) applied
first, otherwise db.insert_post() can't resolve the category_id.

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

# How many matching posts each demo account likes per topic. Kept at 1 so a
# demo account ends up with ~12 likes (one per topic), all leaning the same
# way - enough for dominant_perspective_by_topic()/dominant_political_label()
# to show a clear bias without the history looking like a wall of likes.
MAX_LIKES_PER_TOPIC = 1

# Seed posts covering both perspectives (pro/contra on the topic's central
# proposal) and all three political labels per topic, so every demo account
# finds enough same-leaning content to like on every topic. Posted under the
# admin account so the demo accounts' own like histories stay clean/
# interpretable. ~100 posts across 12 topics (the four defaults plus the
# eight from supabase/migrations/0006_more_categories.sql); each topic has at
# least one "contra/links" and one "pro/rechts" post so DEMO_ACCOUNTS below
# always has a target. Content is intentionally civil and states each side
# fairly - this is a filter-bubble demo, not a place to model inflammatory
# posting.
SEED_POSTS = [
    # --- klima -------------------------------------------------------------
    Post("", "Windkraft-Ausbau beschleunigen", "Der Ausbau von Windkraft ist zentral fuer die Energiewende und muss beschleunigt werden.", "klima", "pro", "rechts"),
    Post("", "Windkraft belastet Anwohner", "Windkraftanlagen veraendern die Landschaft, die Kosten fuer den Ausbau sind zu hoch.", "klima", "contra", "links"),
    Post("", "CO2-Preis konsequent erhoehen", "Ein verlaesslich steigender CO2-Preis lenkt Investitionen dauerhaft in klimafreundliche Technik.", "klima", "pro", "links"),
    Post("", "CO2-Preis trifft Pendler zu hart", "Ein steigender CO2-Preis belastet vor allem Menschen auf dem Land ohne Alternative zum Auto.", "klima", "contra", "rechts"),
    Post("", "Gebaeudesanierung gezielt foerdern", "Foerderprogramme fuer Waermedaemmung senken Emissionen und langfristig die Heizkosten.", "klima", "pro", "mitte"),
    Post("", "Sanierungspflicht ueberfordert Eigentuemer", "Kurzfristige Sanierungspflichten sind fuer viele Hausbesitzer finanziell nicht zu stemmen.", "klima", "contra", "mitte"),
    Post("", "Kohleausstieg vorziehen", "Ein frueherer Kohleausstieg ist machbar, wenn Speicher und Netze parallel ausgebaut werden.", "klima", "pro", "links"),
    Post("", "Kohleausstieg gefaehrdet Versorgungssicherheit", "Ein vorgezogener Ausstieg ohne gesicherte Reserve riskiert Engpaesse im Winter.", "klima", "contra", "rechts"),
    Post("", "Solarpflicht auf Neubauten", "Eine Solarpflicht bei Neubauten holt viel ungenutzte Dachflaeche in die Stromerzeugung.", "klima", "pro", "rechts"),
    # --- verkehr ---------------------------------------------------------
    Post("", "Tempolimit jetzt einfuehren", "Ein Tempolimit auf Autobahnen senkt CO2-Ausstoss und Unfallzahlen spuerbar.", "verkehr", "pro", "links"),
    Post("", "Tempolimit bremst Mobilitaet aus", "Ein generelles Tempolimit bringt wenig, schraenkt aber individuelle Mobilitaet unnoetig ein.", "verkehr", "contra", "rechts"),
    Post("", "Deutschlandticket dauerhaft guenstig halten", "Ein bezahlbares bundesweites Ticket bringt nachweislich mehr Menschen in Bus und Bahn.", "verkehr", "pro", "links"),
    Post("", "Ausbau vor Nulltarif im Nahverkehr", "Solange Strecken ueberlastet sind, sollte Geld in Kapazitaet statt in einen Nulltarif fliessen.", "verkehr", "contra", "links"),
    Post("", "Sichere Radwege baulich trennen", "Baulich getrennte Radwege erhoehen die Sicherheit und entlasten die Strassen in den Staedten.", "verkehr", "pro", "mitte"),
    Post("", "Autospuren nicht ersatzlos streichen", "Neue Radwege sollten entstehen, ohne bestehende Fahrspuren einfach wegzunehmen.", "verkehr", "contra", "mitte"),
    Post("", "Mehr Gueter auf die Schiene", "Mehr Gueterverkehr auf der Schiene senkt Laerm, Emissionen und Unfallzahlen.", "verkehr", "pro", "links"),
    Post("", "Lkw-Logistik bleibt unverzichtbar", "Die Schiene deckt die Flaeche nicht ab, fuer viele Betriebe bleibt der Lkw alternativlos.", "verkehr", "contra", "rechts"),
    Post("", "Nachtzuege wieder ausbauen", "Ein groesseres Nachtzugnetz macht klimafreundliche Reisen ueber lange Strecken attraktiv.", "verkehr", "pro", "rechts"),
    # --- wirtschaft ----------------------------------------------------
    Post("", "Mindestlohn deutlich anheben", "Ein hoeherer Mindestlohn staerkt die Kaufkraft und wirkt gegen Armut.", "wirtschaft", "pro", "links"),
    Post("", "Mindestlohn gefaehrdet Arbeitsplaetze", "Ein zu hoher Mindestlohn ueberfordert kleine Betriebe und kostet Arbeitsplaetze.", "wirtschaft", "contra", "rechts"),
    Post("", "Buerokratie fuer Betriebe abbauen", "Weniger Meldepflichten und schnellere Genehmigungen verschaffen kleinen Firmen Luft.", "wirtschaft", "pro", "rechts"),
    Post("", "Buerokratieabbau darf Schutz nicht kippen", "Vereinfachung ist gut, solange Umwelt- und Arbeitsschutz nicht als Buerokratie wegdefiniert werden.", "wirtschaft", "contra", "links"),
    Post("", "Fachkraeftezuwanderung erleichtern", "Schnellere Anerkennung auslaendischer Abschluesse hilft gegen den Arbeitskraeftemangel.", "wirtschaft", "pro", "mitte"),
    Post("", "Erst inlaendisches Potenzial heben", "Vor mehr Zuwanderung sollten Weiterbildung und Teilzeitkraefte staerker aktiviert werden.", "wirtschaft", "contra", "mitte"),
    Post("", "Uebergewinne staerker besteuern", "In Krisenzeiten koennen Abgaben auf Zufallsgewinne Entlastungen fuer alle gegenfinanzieren.", "wirtschaft", "pro", "links"),
    Post("", "Sondersteuern schrecken Investoren ab", "Kurzfristige Sondersteuern machen den Standort unberechenbar und bremsen Investitionen.", "wirtschaft", "contra", "rechts"),
    Post("", "Unternehmenssteuern senken", "Wettbewerbsfaehige Steuersaetze halten Wertschoepfung und Arbeitsplaetze im Land.", "wirtschaft", "pro", "rechts"),
    # --- digital ------------------------------------------------------
    Post("", "Digitale Buergerrechte staerken", "Datenschutz und digitale Selbstbestimmung muessen gegenueber Konzernen gestaerkt werden.", "digital", "pro", "links"),
    Post("", "Weniger Regulierung fuer Tech-Standort", "Zu strenge Digitalregulierung schadet dem Innovationsstandort und der Wettbewerbsfaehigkeit.", "digital", "contra", "rechts"),
    Post("", "Verwaltung endlich digitalisieren", "Ein zentraler Online-Zugang zu Amtsleistungen spart Buergern und Behoerden viel Zeit.", "digital", "pro", "mitte"),
    Post("", "Digitalpflicht darf niemanden ausschliessen", "Online-Angebote der Verwaltung brauchen weiter einen analogen Weg fuer alle ohne Zugang.", "digital", "contra", "mitte"),
    Post("", "Chatkontrolle stoppen", "Anlasslose Nachrichtenscans verletzen das Recht auf private Kommunikation.", "digital", "pro", "links"),
    Post("", "Ermittler brauchen digitale Befugnisse", "Bei schwerer Kriminalitaet muessen Behoerden auf verschluesselte Inhalte zugreifen koennen.", "digital", "contra", "rechts"),
    Post("", "Recht auf schnelles Internet verankern", "Ein gesetzlicher Anspruch auf Breitband bringt auch abgelegene Orte verlaesslich ans Netz.", "digital", "pro", "rechts"),
    Post("", "Open Source in der Verwaltung bevorzugen", "Offene Software macht den Staat unabhaengiger von einzelnen Konzernen.", "digital", "pro", "links"),
    Post("", "KI-Einsatz in Behoerden streng pruefen", "Automatisierte Entscheidungen in Aemtern brauchen Nachvollziehbarkeit und Widerspruchsrechte.", "digital", "contra", "links"),
    # --- bildung -----------------------------------------------------
    Post("", "Schulen nach Sozialindex finanzieren", "Ein Sozialindex lenkt Lehrkraefte und Mittel dorthin, wo der Bedarf am groessten ist.", "bildung", "pro", "links"),
    Post("", "Leistung an Schulen staerker belohnen", "Statt nur nach Sozialindex zu verteilen, sollten gute Ergebnisse gezielt gefoerdert werden.", "bildung", "contra", "rechts"),
    Post("", "Digitalpakt Schule verstetigen", "Geraete, Wartung und Fortbildung brauchen eine dauerhafte Finanzierung statt Einmalgeldern.", "bildung", "pro", "mitte"),
    Post("", "Technik ersetzt keine Lehrkraefte", "Vor neuer Ausstattung sollten Schulen genug Personal und ein tragfaehiges Konzept haben.", "bildung", "contra", "mitte"),
    Post("", "Laenger gemeinsam lernen", "Eine spaetere Aufteilung auf Schulformen gibt Kindern aus benachteiligten Familien mehr Chancen.", "bildung", "pro", "links"),
    Post("", "Gegliedertes Schulsystem erhalten", "Ein frueh gegliedertes System kann unterschiedliche Begabungen gezielter foerdern.", "bildung", "contra", "rechts"),
    Post("", "Bafoeg elternunabhaengiger machen", "Eine hoehere, planbare Foerderung senkt die Huerde fuers Studium unabhaengig vom Elternhaus.", "bildung", "pro", "rechts"),
    Post("", "Bafoeg-Reform darf Wohnkosten nicht ignorieren", "Pauschale Erhoehungen helfen wenig, wenn Mietkosten und Antragshuerden bleiben.", "bildung", "contra", "links"),
    # --- gesundheit ----------------------------------------------
    Post("", "Buergerversicherung einfuehren", "Eine Versicherung fuer alle verteilt die Beitragslast breiter und stabiler.", "gesundheit", "pro", "links"),
    Post("", "Private Krankenversicherung erhalten", "Der Wettbewerb zwischen den Systemen setzt Anreize fuer bessere Leistungen.", "gesundheit", "contra", "rechts"),
    Post("", "Pflegekraefte besser bezahlen", "Hoehere Loehne und verbindliche Personalschluessel halten Pflegekraefte im Beruf.", "gesundheit", "pro", "mitte"),
    Post("", "Beitragssaetze nicht weiter erhoehen", "Steigende Kassenbeitraege belasten Beschaeftigte und Betriebe zusaetzlich.", "gesundheit", "contra", "mitte"),
    Post("", "Krankenhaeuser flaechendeckend sichern", "Eine Grundversorgung in erreichbarer Naehe darf nicht dem Sparzwang geopfert werden.", "gesundheit", "pro", "links"),
    Post("", "Kleine Kliniken buendeln fuer mehr Qualitaet", "Spezialisierte Zentren erzielen bei schweren Eingriffen bessere Ergebnisse als viele Kleinhaeuser.", "gesundheit", "contra", "rechts"),
    Post("", "Landarztquote im Studium ausweiten", "Reservierte Studienplaetze mit Landarzt-Verpflichtung wirken gegen den Aerztemangel auf dem Land.", "gesundheit", "pro", "rechts"),
    Post("", "Quoten loesen den Aerztemangel nicht", "Ohne bessere Arbeitsbedingungen bleiben auch Quotenaerzte nicht in der Flaeche.", "gesundheit", "contra", "links"),
    # --- migration ---------------------------------------------
    Post("", "Sichere Fluchtwege schaffen", "Legale und geordnete Wege verringern gefaehrliche Ueberfahrten und das Geschaeft der Schlepper.", "migration", "pro", "links"),
    Post("", "Irregulaere Migration konsequent begrenzen", "Wer kein Bleiberecht hat, sollte zuegig und verlaesslich zurueckgefuehrt werden.", "migration", "contra", "rechts"),
    Post("", "Schnellere Asylverfahren mit fairer Beratung", "Kurze Verfahren schaffen Klarheit, wenn unabhaengige Beratung von Anfang an dabei ist.", "migration", "pro", "mitte"),
    Post("", "Verfahren beschleunigen ohne Rechtsschutz zu kuerzen", "Tempo darf nicht auf Kosten von Anhoerung und gerichtlicher Kontrolle gehen.", "migration", "contra", "mitte"),
    Post("", "Kommunen bei der Aufnahme besser finanzieren", "Planbare Zuschuesse fuer Unterkunft, Schule und Sprachkurse entlasten die Staedte vor Ort.", "migration", "pro", "links"),
    Post("", "Aufnahmekapazitaet hat Grenzen", "Integration gelingt nur, wenn Wohnraum, Kita- und Schulplaetze mitwachsen.", "migration", "contra", "rechts"),
    Post("", "Arbeitsmarktzugang frueher oeffnen", "Wer frueh arbeiten darf, wird schneller unabhaengig von Sozialleistungen.", "migration", "pro", "rechts"),
    Post("", "Integration braucht mehr als eine Arbeitserlaubnis", "Ohne Sprachkurse, Wohnung und Anerkennung von Abschluessen bleibt Teilhabe Stueckwerk.", "migration", "contra", "links"),
    # --- wohnen ---------------------------------------------
    Post("", "Mietpreisbremse verschaerfen", "Strengere Obergrenzen bei Neuvermietung bremsen die Verdraengung in angespannten Lagen.", "wohnen", "pro", "links"),
    Post("", "Mietregulierung bremst den Neubau", "Zu enge Mietregeln senken die Rendite und damit die Zahl neuer Wohnungen.", "wohnen", "contra", "rechts"),
    Post("", "Mehr sozialen Wohnungsbau foerdern", "Dauerhafte Foerderung und laengere Bindungsfristen sichern bezahlbare Wohnungen.", "wohnen", "pro", "mitte"),
    Post("", "Foerderung ohne Bauland verpufft", "Zuschuesse helfen wenig, solange Kommunen kein bezahlbares Bauland bereitstellen.", "wohnen", "contra", "mitte"),
    Post("", "Bodenspekulation staerker besteuern", "Eine Abgabe auf ungenutztes Bauland bringt Grundstuecke schneller in Nutzung.", "wohnen", "pro", "links"),
    Post("", "Neue Grundsteuer trifft am Ende Mieter", "Steigende Grundsteuern werden ueber die Nebenkosten weitergereicht.", "wohnen", "contra", "rechts"),
    Post("", "Bauvorschriften entschlacken", "Einheitliche, schlankere Bauordnungen senken Kosten und verkuerzen die Bauzeit.", "wohnen", "pro", "rechts"),
    Post("", "Standards senken geht auf Kosten der Qualitaet", "Beim Laerm-, Brand- und Waermeschutz zu sparen raecht sich ueber die Lebensdauer.", "wohnen", "contra", "links"),
    # --- sicherheit --------------------------------------
    Post("", "Sichtbare Polizeipraesenz erhoehen", "Mehr Streifen an belebten Orten beugt Straftaten vor und staerkt das Sicherheitsgefuehl.", "sicherheit", "pro", "rechts"),
    Post("", "Mehr Praevention statt mehr Kontrolle", "Jugend-, Sozial- und Suchtarbeit verhindern Kriminalitaet nachhaltiger als zusaetzliche Befugnisse.", "sicherheit", "contra", "links"),
    Post("", "Polizei besser ausstatten und fortbilden", "Moderne Ausruestung und mehr Training verbessern die Arbeit im Einsatz messbar.", "sicherheit", "pro", "mitte"),
    Post("", "Neue Befugnisse brauchen strenge Kontrolle", "Ausweitungen von Ueberwachung gehoeren an unabhaengige richterliche Aufsicht gebunden.", "sicherheit", "contra", "mitte"),
    Post("", "Videoueberwachung an Brennpunkten ausweiten", "Kameras an wenigen klar benannten Orten helfen bei Aufklaerung und Abschreckung.", "sicherheit", "pro", "rechts"),
    Post("", "Kameras verdraengen Kriminalitaet nur", "Ueberwachung verlagert Straftaten oft nur, statt sie zu verhindern.", "sicherheit", "contra", "links"),
    Post("", "Unabhaengige Polizei-Beschwerdestelle einrichten", "Eine externe Stelle fuer Beschwerden staerkt Vertrauen und entlastet die Polizei selbst.", "sicherheit", "pro", "links"),
    Post("", "Zusaetzliche Kontrollstellen ueberfordern die Justiz", "Neue Aufsichtsgremien binden Personal, das bei Gerichten und Polizei schon fehlt.", "sicherheit", "contra", "rechts"),
    # --- soziales ----------------------------------
    Post("", "Kindergrundsicherung ausbauen", "Eine gebuendelte, unbuerokratische Leistung erreicht mehr arme Kinder als der heutige Flickenteppich.", "soziales", "pro", "links"),
    Post("", "Sozialleistungen staerker an Gegenleistung binden", "Wer kann, sollte fuer Unterstuetzung zumutbare Mitwirkung zeigen.", "soziales", "contra", "rechts"),
    Post("", "Rente stabil halten ohne hoehere Beitraege", "Ein stabiles Rentenniveau laesst sich mit breiterer Finanzierung sichern.", "soziales", "pro", "mitte"),
    Post("", "Rentenniveau nicht dauerhaft per Steuer stuetzen", "Immer hoehere Zuschuesse aus dem Haushalt verdraengen andere Ausgaben.", "soziales", "contra", "mitte"),
    Post("", "Buergergeld-Saetze regelmaessig anpassen", "Die Regelsaetze muessen mit Miet- und Lebensmittelpreisen Schritt halten.", "soziales", "pro", "links"),
    Post("", "Buergergeld darf Arbeit nicht unattraktiv machen", "Der Abstand zwischen Lohn und Leistung muss spuerbar bleiben.", "soziales", "contra", "rechts"),
    Post("", "Aktivierende Vermittlung statt Sanktionen", "Passgenaue Qualifizierung bringt mehr Menschen dauerhaft in Arbeit als Leistungskuerzungen.", "soziales", "pro", "rechts"),
    Post("", "Ohne Mitwirkungspflichten fehlt der Hebel", "Foerderangebote wirken nur, wenn ihre Wahrnehmung auch verbindlich ist.", "soziales", "contra", "links"),
    # --- europa --------------------------
    Post("", "EU-Asylsystem solidarisch verteilen", "Ein fester Verteilmechanismus entlastet die Aussengrenzstaaten und macht Verfahren einheitlicher.", "europa", "pro", "links"),
    Post("", "Nationale Kontrolle ueber die Grenzen behalten", "Mitgliedstaaten muessen im Zweifel selbst ueber Zuzug und Kontrollen entscheiden koennen.", "europa", "contra", "rechts"),
    Post("", "EU-Buerokratie fuer Betriebe verschlanken", "Weniger Berichtspflichten aus Bruessel entlasten gerade kleine und mittlere Unternehmen.", "europa", "pro", "mitte"),
    Post("", "Binnenmarktregeln nicht aufweichen", "Gemeinsame Standards sind der Kern des Binnenmarkts und sollten nicht ausgehoehlt werden.", "europa", "contra", "mitte"),
    Post("", "Gemeinsame EU-Verteidigung ausbauen", "Gebuendelte Beschaffung und Kommandostrukturen sparen Geld und erhoehen die Wirksamkeit.", "europa", "pro", "links"),
    Post("", "Verteidigung bleibt nationale Aufgabe", "Ueber Einsaetze und Wehretat sollten weiter die Parlamente der Mitgliedstaaten entscheiden.", "europa", "contra", "rechts"),
    Post("", "EU-Erweiterung aktiv vorantreiben", "Eine glaubwuerdige Beitrittsperspektive stabilisiert die Nachbarschaft der Union.", "europa", "pro", "rechts"),
    Post("", "Erweiterung ohne Reform ueberfordert die EU", "Vor neuen Mitgliedern brauchen Entscheidungsregeln und Haushalt ein Update.", "europa", "contra", "links"),
    # --- aussenpolitik ----------
    Post("", "Entwicklungszusammenarbeit ausbauen", "Verlaessliche Mittel fuer Bildung, Gesundheit und Klimaanpassung wirken langfristig stabilisierend.", "aussenpolitik", "pro", "links"),
    Post("", "Entwicklungshilfe an klare Bedingungen knuepfen", "Zahlungen sollten an Reformfortschritte und Rueckuebernahme-Abkommen gekoppelt sein.", "aussenpolitik", "contra", "rechts"),
    Post("", "Verteidigungsausgaben verlaesslich planen", "Ein stetiger Aufwuchs statt Ruck-Zuck-Etats macht Beschaffung guenstiger und planbar.", "aussenpolitik", "pro", "mitte"),
    Post("", "Hoehere Wehretats brauchen klare Prioritaeten", "Mehr Geld hilft wenig ohne Reform von Beschaffung und Struktur.", "aussenpolitik", "contra", "mitte"),
    Post("", "Diplomatie vor militaerischen Optionen", "Vermittlung und zivile Krisenpraevention sollten den Vorrang vor Eskalation haben.", "aussenpolitik", "pro", "links"),
    Post("", "Glaubwuerdige Abschreckung sichert Frieden", "Nur wer verteidigungsfaehig ist, kann glaubwuerdig verhandeln.", "aussenpolitik", "contra", "rechts"),
    Post("", "Ruestungsexporte strenger kontrollieren", "Klare, nachpruefbare Kriterien verhindern Lieferungen in Krisen- und Kriegsgebiete.", "aussenpolitik", "pro", "rechts"),
    Post("", "Exportstopps treffen auch Partner", "Pauschale Ausfuhrverbote schwaechen die Zusammenarbeit mit verbuendeten Demokratien.", "aussenpolitik", "contra", "links"),
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

        per_topic: dict[str, int] = {}
        matching = []
        for row in all_posts:
            post = row["post"]
            if (
                post.perspective == account["like_perspective"]
                and post.political_label == account["like_political_label"]
                and per_topic.get(post.topic, 0) < MAX_LIKES_PER_TOPIC
            ):
                matching.append(post)
                per_topic[post.topic] = per_topic.get(post.topic, 0) + 1
        for post in matching:
            db.toggle_like(post.id, user_id)
        print(
            f"{account['display_name']}: {len(matching)} Posts geliked "
            f"({account['like_perspective']}/{account['like_political_label']}, "
            f"max {MAX_LIKES_PER_TOPIC} pro Thema)."
        )

    print(
        "\nFertig. Zum Vorfuehren: mit einem der Demo-Accounts einloggen und den "
        "Standard-Feed oeffnen - er sollte klar in Richtung der jeweiligen "
        "Like-Historie verzerrt sein."
    )


if __name__ == "__main__":
    main()
