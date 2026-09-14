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

See README.md ("Example accounts for the standard algorithm") and the vault
note ObsidianGehirn/06 Zugangsdaten/Feed-Diversity-Beispielaccounts.md
(name/purpose without credentials) for context.
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
    {"prefix": "DEMO_ACCOUNT_A", "display_name": "Nora Bergmann", "like_perspective": "contra", "like_political_label": "left"},
    {"prefix": "DEMO_ACCOUNT_B", "display_name": "Jonas Kessler", "like_perspective": "pro", "like_political_label": "right"},
    {"prefix": "DEMO_ACCOUNT_C", "display_name": "Lea Vogt", "like_perspective": "contra", "like_political_label": "left"},
    {"prefix": "DEMO_ACCOUNT_D", "display_name": "Tarek Aydin", "like_perspective": "pro", "like_political_label": "right"},
]
ADMIN_ACCOUNT = {"prefix": "DEMO_ADMIN", "display_name": "Team 13 Admin"}

# How many matching posts each demo account likes per topic. Kept at 1 so a
# demo account ends up with ~12 likes (one per topic), all leaning the same
# way - enough for dominant_perspective_by_topic()/dominant_political_label()
# to show a clear bias without the history looking like a wall of likes.
MAX_LIKES_PER_TOPIC = 1

# Seed posts covering both perspectives and all three political labels per
# topic, so every demo account finds enough same-leaning content to like on
# every topic. Posted under the admin account so the demo accounts' own like
# histories stay clean/interpretable. ~100 posts across 12 topics (the four
# defaults plus the eight from supabase/migrations/0006_more_categories.sql);
# each topic has at least one "contra/left" and one "pro/right" post so
# DEMO_ACCOUNTS below always has a target.
#
# `perspective` is a consistent axis *per topic*, not just "pro/contra the
# post's own headline": within a topic, every "pro" post leans the same way
# (roughly: more ambition / more protection / more openness), every "contra"
# post the other way (more weight on cost, the market or the status quo).
# app.TOPIC_STANCES spells that direction out per topic ("climate pro" =
# "more climate protection, faster"), and the feed/dashboard show that
# phrase instead of a bare "pro"/"contra". Keep new posts on the same axis
# as the rest of their topic. Content is intentionally civil and states each
# side fairly - this is a filter-bubble demo, not a place to model
# inflammatory posting.
SEED_POSTS = [
    # --- climate -------------------------------------------------------------
    Post("", "Speed up wind power expansion", "Expanding wind power is central to the energy transition and needs to move faster.", "climate", "pro", "right"),
    Post("", "Wind turbines burden residents", "Wind turbines change the landscape, and the cost of expansion is too high.", "climate", "contra", "left"),
    Post("", "Raise the carbon price steadily", "A reliably rising carbon price steers investment toward climate-friendly technology for the long term.", "climate", "pro", "left"),
    Post("", "Carbon pricing hits commuters too hard", "A rising carbon price mainly burdens people in rural areas who have no alternative to the car.", "climate", "contra", "right"),
    Post("", "Fund building renovation properly", "Subsidy programs for insulation cut emissions and heating costs in the long run.", "climate", "pro", "center"),
    Post("", "Renovation mandates overwhelm owners", "Short-notice renovation mandates are financially out of reach for many homeowners.", "climate", "contra", "center"),
    Post("", "Bring the coal phase-out forward", "An earlier coal phase-out is feasible if storage and grids are expanded in parallel.", "climate", "pro", "left"),
    Post("", "Coal phase-out risks supply security", "An accelerated phase-out without a secured reserve risks shortages in winter.", "climate", "contra", "right"),
    Post("", "Require solar panels on new builds", "A solar mandate for new buildings puts a lot of unused roof space to work generating power.", "climate", "pro", "right"),
    # --- transport ---------------------------------------------------------
    Post("", "Introduce a speed limit now", "A speed limit on highways noticeably cuts CO2 emissions and accident numbers.", "transport", "pro", "left"),
    Post("", "A speed limit holds mobility back", "A blanket speed limit achieves little but needlessly restricts individual mobility.", "transport", "contra", "right"),
    Post("", "Keep the nationwide transit ticket cheap", "An affordable nationwide ticket demonstrably gets more people onto buses and trains.", "transport", "pro", "left"),
    Post("", "Expansion before free fares", "As long as routes are overcrowded, money should go into capacity rather than free fares.", "transport", "contra", "left"),
    Post("", "Physically separate bike lanes", "Physically separated bike lanes improve safety and take pressure off city streets.", "transport", "pro", "center"),
    Post("", "Don't just remove car lanes", "New bike lanes should be built without simply removing existing traffic lanes.", "transport", "contra", "center"),
    Post("", "Shift more freight onto rail", "More freight on rail cuts noise, emissions and accident numbers.", "transport", "pro", "left"),
    Post("", "Truck logistics remains essential", "Rail doesn't cover every area, so for many businesses trucks remain the only option.", "transport", "contra", "right"),
    Post("", "Expand night trains again", "A bigger night-train network makes climate-friendly long-distance travel appealing.", "transport", "pro", "right"),
    # --- economy ----------------------------------------------------
    Post("", "Raise the minimum wage significantly", "A higher minimum wage strengthens purchasing power and helps fight poverty.", "economy", "pro", "left"),
    Post("", "Minimum wage hikes threaten jobs", "A minimum wage set too high overwhelms small businesses and costs jobs.", "economy", "contra", "right"),
    Post("", "Cut red tape for businesses", "Fewer reporting requirements and faster permits give small companies room to breathe.", "economy", "contra", "right"),
    Post("", "Cutting red tape must not gut protections", "Environmental and worker protections must not be redefined away as red tape.", "economy", "pro", "left"),
    Post("", "Immigration must not undercut wages", "New entrants to the labor market must not undermine wages and collective-bargaining standards.", "economy", "contra", "left"),
    Post("", "Tap domestic potential first", "Rather than relying on more immigration, training and better work incentives should come first.", "economy", "pro", "right"),
    Post("", "Tax windfall profits more heavily", "In times of crisis, levies on windfall profits can help fund relief for everyone.", "economy", "pro", "left"),
    Post("", "Special taxes scare off investors", "Short-notice special taxes make the country unpredictable and slow investment.", "economy", "contra", "right"),
    Post("", "Cut corporate taxes", "Lower corporate taxes mainly benefit businesses and capital.", "economy", "contra", "right"),
    # --- digital ------------------------------------------------------
    Post("", "Strengthen digital civil rights", "Privacy and digital self-determination need to be strengthened against corporations.", "digital", "pro", "left"),
    Post("", "Less regulation for the tech sector", "Overly strict digital regulation harms the innovation ecosystem and competitiveness.", "digital", "contra", "right"),
    Post("", "Finally digitize public administration", "A single online access point for government services saves citizens and agencies a lot of time.", "digital", "pro", "center"),
    Post("", "Mandatory digital services can't exclude anyone", "Online government services still need an offline path for everyone without access.", "digital", "contra", "center"),
    Post("", "Stop chat control", "Scanning private messages without cause violates the right to private communication.", "digital", "pro", "left"),
    Post("", "Investigators need digital powers", "For serious crimes, authorities need to be able to access encrypted content.", "digital", "contra", "right"),
    Post("", "Enshrine a right to fast internet", "A legal right to broadband reliably connects even remote areas.", "digital", "pro", "right"),
    Post("", "Favor open source in government", "Open software makes the state less dependent on individual corporations.", "digital", "pro", "left"),
    Post("", "Scrutinize AI use in government closely", "Automated decisions by public agencies need transparency and a right to appeal.", "digital", "contra", "left"),
    # --- education -----------------------------------------------------
    Post("", "Fund schools by a social index", "A social index directs teachers and funding to where the need is greatest.", "education", "pro", "left"),
    Post("", "Reward achievement at school more", "Instead of distributing funds solely by social index, strong results should be rewarded directly.", "education", "contra", "right"),
    Post("", "Make the school digital pact permanent", "Devices, maintenance and training need ongoing funding instead of one-off payments.", "education", "pro", "center"),
    Post("", "Technology doesn't replace teachers", "Before new equipment, schools need enough staff and a workable plan.", "education", "contra", "center"),
    Post("", "Keep students together longer", "Splitting students into school tracks later gives children from disadvantaged families a better chance.", "education", "pro", "left"),
    Post("", "Keep the tracked school system", "An early-tracked system can support different aptitudes more specifically.", "education", "contra", "right"),
    Post("", "Make student aid less dependent on parents", "Higher, more predictable aid lowers the barrier to studying regardless of family background.", "education", "pro", "right"),
    Post("", "Student aid reform can't ignore housing costs", "Flat-rate increases help little if rent costs and red tape in applying stay the same.", "education", "contra", "left"),
    # --- health ----------------------------------------------
    Post("", "Introduce a universal health insurance", "One insurance system for everyone spreads the cost of contributions more broadly and stably.", "health", "pro", "left"),
    Post("", "Keep private health insurance", "Competition between systems creates incentives for better care.", "health", "contra", "right"),
    Post("", "Pay care workers better", "Higher wages and binding staffing ratios keep care workers in the profession.", "health", "pro", "center"),
    Post("", "Stop raising contribution rates", "Rising health-insurance contributions place an extra burden on workers and employers.", "health", "contra", "center"),
    Post("", "Guarantee hospitals across the country", "Basic care within reach must not be sacrificed to budget cuts.", "health", "pro", "left"),
    Post("", "Consolidate small clinics for quality", "Specialized centers get better outcomes on serious procedures than many small hospitals.", "health", "contra", "right"),
    Post("", "Expand the rural-doctor quota in medical school", "Reserved study places tied to a rural-service commitment help counter the shortage of doctors in the countryside.", "health", "pro", "right"),
    Post("", "Quotas won't fix the doctor shortage", "Without better working conditions, even quota doctors won't stay in rural areas.", "health", "contra", "left"),
    # --- migration ---------------------------------------------
    Post("", "Create safe escape routes", "Legal, orderly pathways reduce dangerous crossings and the smugglers' business.", "migration", "pro", "left"),
    Post("", "Consistently limit irregular migration", "Those without a right to stay should be returned promptly and reliably.", "migration", "contra", "right"),
    Post("", "Faster asylum procedures with fair counseling", "Short procedures create clarity as long as independent counseling is there from the start.", "migration", "pro", "center"),
    Post("", "Speed up procedures without cutting legal protection", "Speed must not come at the expense of hearings and judicial review.", "migration", "contra", "center"),
    Post("", "Fund municipalities better for reception", "Predictable funding for housing, schools and language courses relieves local towns and cities.", "migration", "pro", "left"),
    Post("", "Reception capacity has limits", "Integration only works if housing, daycare and school places grow along with it.", "migration", "contra", "right"),
    Post("", "Open labor-market access sooner", "Those allowed to work early become independent of welfare benefits faster.", "migration", "pro", "right"),
    Post("", "Integration needs more than a work permit", "Without language courses, housing and recognized qualifications, participation stays patchy.", "migration", "contra", "left"),
    # --- housing ---------------------------------------------
    Post("", "Tighten the rent cap", "Stricter caps on new leases slow displacement in tight housing markets.", "housing", "pro", "left"),
    Post("", "Rent regulation slows new construction", "Overly tight rent rules lower returns and, with them, the number of new units built.", "housing", "contra", "right"),
    Post("", "Fund more social housing", "Ongoing subsidies and longer affordability terms secure affordable housing.", "housing", "pro", "right"),
    Post("", "Subsidies fizzle out without building land", "Grants help little as long as municipalities don't provide affordable building land.", "housing", "contra", "center"),
    Post("", "Tax land speculation more heavily", "A levy on unused building land brings plots into use faster.", "housing", "pro", "left"),
    Post("", "The new property tax ends up hitting tenants", "Rising property taxes get passed on through utility bills.", "housing", "contra", "right"),
    Post("", "Streamline building codes instead of adding rules", "Leaner building codes and fewer requirements are meant to cut costs - regulation takes a back seat.", "housing", "contra", "right"),
    Post("", "Lowering standards costs quality later", "Skimping on noise, fire and thermal protection catches up with a building over its lifetime.", "housing", "contra", "left"),
    # --- security --------------------------------------
    Post("", "Increase visible police presence", "More patrols in busy areas prevent crime and strengthen the sense of safety.", "security", "pro", "right"),
    Post("", "More prevention instead of more control", "Youth, social and addiction services prevent crime more sustainably than extra police powers.", "security", "contra", "left"),
    Post("", "Equip and train police better", "Modern equipment and more training measurably improve work in the field.", "security", "pro", "center"),
    Post("", "New powers need strict oversight", "Any expansion of surveillance should be tied to independent judicial oversight.", "security", "contra", "center"),
    Post("", "Expand video surveillance at hotspots", "Cameras at a few clearly defined locations help with solving crimes and deterrence.", "security", "pro", "right"),
    Post("", "Cameras just displace crime", "Surveillance often just shifts crime elsewhere instead of preventing it.", "security", "contra", "left"),
    Post("", "Set up an independent police complaints office", "Instead of more powers, what's needed is external oversight: an independent complaints office builds trust.", "security", "contra", "left"),
    Post("", "Extra oversight bodies overburden the justice system", "New oversight bodies tie up staff that courts and police are already short of.", "security", "contra", "right"),
    # --- welfare ----------------------------------
    Post("", "Expand the basic child benefit", "One bundled, low-bureaucracy benefit reaches more children in poverty than today's patchwork of programs.", "welfare", "pro", "left"),
    Post("", "Tie welfare benefits more to reciprocity", "Those who are able should show reasonable engagement in exchange for support.", "welfare", "contra", "right"),
    Post("", "Keep pensions stable without raising contributions", "A stable pension level can be secured with a broader funding base.", "welfare", "pro", "center"),
    Post("", "Don't prop up pensions with tax money indefinitely", "Ever-higher subsidies from the budget crowd out other spending.", "welfare", "contra", "center"),
    Post("", "Adjust basic income rates regularly", "Standard rates need to keep pace with rent and food prices.", "welfare", "pro", "left"),
    Post("", "Basic income must not make work unattractive", "The gap between wages and benefits needs to stay noticeable.", "welfare", "contra", "right"),
    Post("", "Active job placement instead of sanctions", "Tailored qualification programs get more people into lasting work than benefit cuts do.", "welfare", "pro", "right"),
    Post("", "Without participation requirements, there's no lever", "Support programs only work if taking part in them is actually binding.", "welfare", "contra", "left"),
    # --- europe --------------------------
    Post("", "Distribute the EU asylum system fairly", "A fixed distribution mechanism relieves border states and makes procedures more consistent.", "europe", "pro", "left"),
    Post("", "Keep national control over borders", "Member states must be able to decide on entry and controls themselves when in doubt.", "europe", "contra", "right"),
    Post("", "Streamline EU red tape for businesses", "Fewer reporting requirements from Brussels especially relieve small and medium businesses.", "europe", "pro", "center"),
    Post("", "Don't water down single-market rules", "Common standards are the core of the single market and shouldn't be hollowed out.", "europe", "contra", "center"),
    Post("", "Build up joint EU defense", "Pooled procurement and command structures save money and increase effectiveness.", "europe", "pro", "left"),
    Post("", "Defense stays a national matter", "Member states' own parliaments should keep deciding on deployments and defense budgets.", "europe", "contra", "right"),
    Post("", "Actively push EU enlargement", "A credible path to membership stabilizes the Union's neighborhood.", "europe", "pro", "right"),
    Post("", "Enlargement without reform overwhelms the EU", "Before new members join, decision-making rules and the budget need an update.", "europe", "contra", "left"),
    # --- foreign_policy ----------
    Post("", "Expand development cooperation", "Reliable funding for education, health and climate adaptation has a stabilizing effect in the long run.", "foreign_policy", "pro", "left"),
    Post("", "Tie development aid to clear conditions", "Payments should be linked to reform progress and readmission agreements.", "foreign_policy", "contra", "right"),
    Post("", "Increase defense spending reliably", "A steady increase in the defense budget takes priority so procurement can be planned.", "foreign_policy", "contra", "center"),
    Post("", "Higher defense budgets need clear priorities", "More money helps little without reforming procurement and structure.", "foreign_policy", "contra", "center"),
    Post("", "Diplomacy before military options", "Mediation and civilian crisis prevention should take priority over escalation.", "foreign_policy", "pro", "left"),
    Post("", "Credible deterrence secures peace", "Only those capable of defending themselves can negotiate credibly.", "foreign_policy", "contra", "right"),
    Post("", "Control arms exports more strictly", "Clear, verifiable criteria prevent shipments to crisis and war zones.", "foreign_policy", "pro", "right"),
    Post("", "Export bans also hit partners", "Blanket export bans weaken cooperation with allied democracies.", "foreign_policy", "contra", "left"),
]


def _require_env(prefix: str) -> tuple[str, str]:
    email = os.environ.get(f"{prefix}_EMAIL")
    password = os.environ.get(f"{prefix}_PASSWORD")
    if not email or not password:
        print(f"Missing: {prefix}_EMAIL/{prefix}_PASSWORD in the environment/.env - aborting.", file=sys.stderr)
        sys.exit(1)
    return email, password


def _ensure_account(email: str, password: str, display_name: str) -> str:
    user = db.sign_up(email, password)
    if user is None:
        user = db.sign_in(email, password)
    if user is None:
        print(f"Could not create or log in to account for {display_name} ({email}).", file=sys.stderr)
        sys.exit(1)
    if db.fetch_profile(user["id"]) is None:
        db.create_unique_profile(user["id"], display_name)
    return user["id"]


def main() -> None:
    if not db.is_configured() or not db.auth_configured():
        print(
            "SUPABASE_URL/SUPABASE_SECRET_KEY/SUPABASE_PUBLISHABLE_KEY are missing - "
            "please set .env before running this script. No placeholder values allowed.",
            file=sys.stderr,
        )
        sys.exit(1)

    admin_email, admin_password = _require_env(ADMIN_ACCOUNT["prefix"])
    admin_id = _ensure_account(admin_email, admin_password, ADMIN_ACCOUNT["display_name"])
    print(f"Admin account ready: {ADMIN_ACCOUNT['display_name']}")

    for post in SEED_POSTS:
        db.insert_post(post.title, post.text, post.topic, post.perspective, admin_id, post.political_label)
    print(f"{len(SEED_POSTS)} seed posts created under the admin account.")

    all_posts = db.fetch_posts()
    if not all_posts:
        print("Could not read back the posts that were just created - aborting.", file=sys.stderr)
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
            f"{account['display_name']}: liked {len(matching)} posts "
            f"({account['like_perspective']}/{account['like_political_label']}, "
            f"max {MAX_LIKES_PER_TOPIC} per topic)."
        )

    print(
        "\nDone. To demo: log in with one of the demo accounts and open the "
        "standard feed - it should be clearly skewed toward that account's "
        "like history."
    )


if __name__ == "__main__":
    main()
