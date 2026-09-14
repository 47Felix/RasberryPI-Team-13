"""One-off script: adds 100 more posts across the same 12 topics as
seed_demo_accounts.py's SEED_POSTS, on top of the 50 from seed_more_posts.py,
to grow the dataset further without touching any existing seed post or
requiring an admin Supabase Auth account.

Posted under a fictional byline (db.ensure_author(), the same "legacy"
mechanism as the original static dataset in supabase/migrations/0001_init.sql)
instead of a real user_id - so this only needs SUPABASE_URL/
SUPABASE_SECRET_KEY in the environment/.env, no account credentials. The
byline here is deliberately distinct from seed_more_posts.py's "Community
Desk" so a run of this script is easy to tell apart in the feed.

Usage:

    python3 seed_more_posts_v2.py

Safe to re-run in the sense that it won't create duplicate authors (upsert on
handle), but posts themselves ARE duplicated on a second run (no dedup key on
content) - only run once per environment.

Same per-topic pro/contra axis as SEED_POSTS in seed_demo_accounts.py (see
that file's docstring and supabase/migrations/0008_topic_stance_labels.sql
for the exact "pro means X, contra means Y" phrasing per topic). Every
proposal here is a fresh subject not already covered by SEED_POSTS or
seed_more_posts.py. Content is intentionally civil and states each side
fairly - this is a filter-bubble demo, not a place to model inflammatory
posting. political_label is the author's self-placement and does not always
line up with the pro/contra side, on purpose (cross-cutting cases keep the
diversity ranking honest).
"""

import sys

import db
from ranking import Post

BYLINE = {"name": "Policy Roundtable", "handle": "@policyroundtable", "avatar": "\U0001f4dd"}

MORE_POSTS = [
    # --- climate (pro = more climate protection, faster / contra = more weight on cost) ---
    Post("", "Back green hydrogen for heavy industry", "Targeted support for hydrogen in steel and chemicals cuts emissions in sectors that can't easily electrify.", "climate", "pro", "left"),
    Post("", "Build out grid-scale battery storage now", "Large storage projects let the grid absorb more wind and solar instead of curtailing it.", "climate", "pro", "center"),
    Post("", "Set an end date for new gas boiler sales", "A clear cut-off gives installers and households time to plan the switch to cleaner heating.", "climate", "pro", "left"),
    Post("", "Climate targets shouldn't outrun the grid", "Pushing electrification faster than transmission lines can be built risks blackouts and backlash.", "climate", "contra", "right"),
    Post("", "Reforest public land at scale", "Planting on state-owned land is a low-cost carbon sink that also helps with heat and flooding.", "climate", "pro", "center"),
    Post("", "Carbon border tariffs land on consumers", "A border levy on imports raises shelf prices for households while shielding domestic industry.", "climate", "contra", "right"),
    Post("", "Require methane leak monitoring at landfills and farms", "Cheap sensors and repair rules cut a potent greenhouse gas with a fast payback.", "climate", "pro", "left"),
    Post("", "Renewable levies fall hardest on low-income bills", "Funding the transition through a flat surcharge on power bills takes a bigger bite out of small incomes.", "climate", "contra", "left"),
    Post("", "Fast-track onshore wind along motorway corridors", "Land beside highways is already noisy and developed, so siting turbines there speeds approvals with little added impact.", "climate", "pro", "right"),
    # --- transport (pro = priority for bikes/transit/rail / contra = priority for cars/status quo) ---
    Post("", "Make public transit free for under-18s", "Free travel for young people builds the transit habit early and eases family budgets.", "transport", "pro", "left"),
    Post("", "Rural areas need better roads, not more rail", "Where trains will never run, resurfacing and safer junctions do more for daily mobility.", "transport", "contra", "right"),
    Post("", "Extend tram networks in mid-size cities", "Trams move far more people per lane than cars and are reliable in traffic once tracks are laid.", "transport", "pro", "center"),
    Post("", "Cargo-bike grants won't move real freight volumes", "Subsidising cargo bikes is a nice gesture but barely dents the tonnage that moves by van and lorry.", "transport", "contra", "left"),
    Post("", "Put park-and-ride hubs at every suburban station", "Secure parking at the edge of town lets people drive the first mile and take the train the rest.", "transport", "pro", "center"),
    Post("", "Removing downtown parking hurts local shops", "Small retailers lose walk-in customers when nearby parking disappears faster than transit improves.", "transport", "contra", "right"),
    Post("", "Ban overnight lorry transit on residential streets", "Routing heavy trucks away from homes at night cuts noise and danger with signage alone.", "transport", "pro", "left"),
    Post("", "Electrify the remaining diesel rail lines", "Overhead wires or battery trains on branch lines cut emissions and running costs over time.", "transport", "pro", "right"),
    Post("", "Bike-lane pilots keep going permanent without review", "Temporary lanes are often made permanent before anyone measures the effect on buses and deliveries.", "transport", "contra", "center"),
    # --- economy (pro = more redistribution/worker protection / contra = priority for business/market) ---
    Post("", "Put a right to disconnect into law", "A clear rule that after-hours messages can wait protects rest time without banning flexibility.", "economy", "pro", "left"),
    Post("", "A four-day week mandate would raise unit costs", "Forcing shorter weeks at the same pay pushes up the cost of every hour worked, especially in services.", "economy", "contra", "right"),
    Post("", "Extend sector-wide collective agreements", "Declaring negotiated deals binding for a whole sector stops undercutting on pay and conditions.", "economy", "pro", "left"),
    Post("", "Higher inheritance tax drives family firms abroad", "Steep transfer taxes can force heirs to sell or relocate a business that took decades to build.", "economy", "contra", "right"),
    Post("", "Set up a public investment bank for regional industry", "Patient state-backed lending helps smaller regions keep manufacturing that private capital overlooks.", "economy", "pro", "center"),
    Post("", "Supply-chain due-diligence law overloads mid-size exporters", "Tracing every supplier is manageable for multinationals but a heavy fixed cost for smaller firms.", "economy", "contra", "right"),
    Post("", "Require profit-sharing at listed companies", "A modest employee profit share spreads the gains of a good year to the people who produced them.", "economy", "pro", "left"),
    Post("", "Speed up insolvency so viable firms survive", "A faster restructuring process saves jobs by keeping fundamentally sound companies out of liquidation.", "economy", "contra", "center"),
    Post("", "Cap executive-to-median pay ratios for public contracts", "Firms bidding for taxpayer money should keep top pay within a set multiple of their own median wage.", "economy", "pro", "left"),
    # --- digital (pro = civil rights/privacy first / contra = fewer rules or more investigative power) ---
    Post("", "Write a right to encrypted messaging into law", "A statutory guarantee stops the on-again, off-again debate over weakening private communication.", "digital", "pro", "left"),
    Post("", "Platform liability rules push startups out", "Broad duties to police user content are survivable for big platforms and fatal for small ones.", "digital", "contra", "right"),
    Post("", "Mandate data portability between social networks", "Letting people take their contacts and posts elsewhere makes switching real and competition possible.", "digital", "pro", "center"),
    Post("", "Police need lawful access to device backups", "With a warrant, investigators should be able to reach cloud backups in serious crime cases.", "digital", "contra", "right"),
    Post("", "Ban biometric mass surveillance in public spaces", "Live face scanning of crowds treats everyone as a suspect and chills ordinary public life.", "digital", "pro", "left"),
    Post("", "A single digital ID wallet is one big target", "Concentrating every credential in one app creates a single point of failure for fraud and outages.", "digital", "contra", "left"),
    Post("", "Require public-interest audits of large platform algorithms", "Independent auditors checking ranking systems for well-documented harms adds accountability without dictating design.", "digital", "pro", "center"),
    Post("", "Longer data retention helps solve serious crime", "Keeping connection records for a defined period gives investigators a trail in cases that surface late.", "digital", "contra", "right"),
    Post("", "Publish municipal data as open data by default", "Timetables, budgets and permits released in machine-readable form let anyone build useful local tools.", "digital", "pro", "right"),
    # --- education (pro = redistribution/longer shared schooling / contra = achievement and tracking) ---
    Post("", "Cut class sizes in the highest-need schools first", "Smaller groups give teachers time for the students who are furthest behind.", "education", "pro", "left"),
    Post("", "Merit scholarships keep top students striving", "Rewarding excellence directly gives able students from any background a reason to push further.", "education", "contra", "right"),
    Post("", "Guarantee a pre-school place for every child", "Universal early-years education narrows gaps before they harden in the first school year.", "education", "pro", "center"),
    Post("", "A rigid national curriculum crowds out regional strengths", "One centrally fixed syllabus leaves no room for local industry links or languages.", "education", "contra", "right"),
    Post("", "Offer free tutoring to students falling behind", "Targeted small-group catch-up sessions cost little next to the price of repeated years.", "education", "pro", "left"),
    Post("", "Banning grade repetition just moves the problem on", "Passing students who haven't mastered the material leaves gaps that compound later.", "education", "contra", "right"),
    Post("", "Pay a salary premium for teaching in disadvantaged districts", "A clear pay bump helps schools that struggle most to attract and keep experienced staff.", "education", "pro", "center"),
    Post("", "Scrapping selective schools removes a ladder for gifted low-income kids", "For some able students from poorer families, an academically selective school is the fastest route up.", "education", "contra", "left"),
    # --- health (pro = solidarity/more state control / contra = competition and personal contribution) ---
    Post("", "Manufacture essential generic drugs publicly", "A public production line for a short list of critical generics ends recurring shortages of cheap medicines.", "health", "pro", "left"),
    Post("", "Small co-pays curb unnecessary visits", "A token fee per appointment nudges people to think twice without blocking anyone who is genuinely ill.", "health", "contra", "right"),
    Post("", "Set a national waiting-time guarantee for surgery", "If the public system can't treat within the limit, it funds care elsewhere at no cost to the patient.", "health", "pro", "center"),
    Post("", "Central price negotiation delays new drug launches", "Manufacturers often launch later in markets where a single buyer sets a hard price early.", "health", "contra", "right"),
    Post("", "Fund mental-health care inside primary practices", "An on-site counsellor at the GP catches problems early and avoids long specialist queues.", "health", "pro", "left"),
    Post("", "A sugar tax is a regressive nanny-state measure", "Levies on sweet drinks take a larger share of low incomes and treat adults as unable to choose.", "health", "contra", "right"),
    Post("", "Guarantee a same-week GP appointment", "A binding access standard, backed by funding, is what makes primary care usable when you need it.", "health", "pro", "center"),
    Post("", "Lump-sum hospital budgets reward inefficiency", "Paying a fixed block grant regardless of activity gives no reason to shorten waits or improve throughput.", "health", "contra", "right"),
    # --- migration (pro = more open/admission/inclusion / contra = tighter limits and controls) ---
    Post("", "Grant permanent status after five settled years", "A clear path to secure residence rewards people who have worked, paid in and put down roots.", "migration", "pro", "left"),
    Post("", "Hold benefits until status is decided", "Support should follow a positive decision, not run for the length of an open procedure.", "migration", "contra", "right"),
    Post("", "Create regional work visas for labour-short sectors", "Letting regions sponsor visas for care, farming or trades fills real vacancies where they exist.", "migration", "pro", "center"),
    Post("", "Family reunification needs an income threshold", "Sponsors should show they can house and support arriving relatives without immediate public help.", "migration", "contra", "right"),
    Post("", "Give long-term residents a local vote", "People who have lived and paid taxes in a town for years should have a say in how it's run.", "migration", "pro", "left"),
    Post("", "Safe-country lists speed up fair rejections", "Fast-tracking claims from demonstrably safe states frees capacity for those in real danger.", "migration", "contra", "right"),
    Post("", "Put an integration mentor in every municipality", "A named contact who helps with school, work and paperwork shortens the path to standing on your own.", "migration", "pro", "center"),
    Post("", "Replace cash benefits with in-kind support", "Housing, meal and travel provision covers real needs while reducing the pull of cash transfers.", "migration", "contra", "right"),
    # --- housing (pro = more rent regulation/social housing / contra = fewer rules, focus on new construction) ---
    Post("", "Give non-profit developers first pick of public land", "Selling or leasing state land to cost-rent builders locks in affordability for the long term.", "housing", "pro", "left"),
    Post("", "Density bonuses build more homes than subsidies", "Letting developers add floors in exchange for some affordable units delivers supply at low public cost.", "housing", "contra", "right"),
    Post("", "Cap short-term holiday rentals in tight markets", "A limit on nights per year returns whole flats to people who actually live and work in the city.", "housing", "pro", "center"),
    Post("", "Rent controls shrink the rental supply over time", "When returns are capped, owners sell to occupiers or hold units empty, leaving fewer to rent.", "housing", "contra", "right"),
    Post("", "Set up a public fund to buy rental blocks from investors", "A revolving fund that acquires and holds apartment buildings keeps sitting tenants housed and rents stable.", "housing", "pro", "left"),
    Post("", "Faster rezoning does more than rent caps", "The binding constraint is how long it takes to get permission to build, not the level of rents.", "housing", "contra", "right"),
    Post("", "Tax flats left empty for a year or more", "A vacancy levy makes hoarding housing as an asset costly and nudges units back onto the market.", "housing", "pro", "left"),
    Post("", "Drop parking minimums to cut build costs", "Not forcing a parking space per flat lowers the price of each home and frees land for housing.", "housing", "contra", "center"),
    # --- security (pro = more presence/police powers / contra = prevention and civil liberties first) ---
    Post("", "Keep permanent CCTV at major transport hubs", "Cameras at a handful of busy, well-defined sites help both deterrence and after-the-fact investigation.", "security", "pro", "right"),
    Post("", "Youth clubs cut crime more than extra patrols", "Somewhere to go in the evening does more to keep teenagers out of trouble than another squad car.", "security", "contra", "left"),
    Post("", "Fund more financial investigators for organised crime", "Following the money seizes proceeds and dismantles networks that street patrols never reach.", "security", "pro", "center"),
    Post("", "Facial recognition misidentifies too often to deploy", "Error rates, worse for some groups, mean live matching stops the wrong people as a matter of routine.", "security", "contra", "left"),
    Post("", "Pilot predictive policing in high-crime districts", "Directing patrols by recent incident patterns puts limited officers where the next call is likeliest.", "security", "pro", "right"),
    Post("", "Stop-and-search quotas erode community trust", "Targets for stops push officers toward volume over cause and sour relations in the areas hit hardest.", "security", "contra", "left"),
    Post("", "Run faster court proceedings for repeat offenders", "Swift, certain hearings for people cycling through the system do more than longer sentences years later.", "security", "pro", "center"),
    Post("", "Expanding DNA databases invites function creep", "Samples taken for one purpose tend to end up searched for others once the database exists.", "security", "contra", "left"),
    # --- welfare (pro = higher/more reliable benefits / contra = personal responsibility and incentives) ---
    Post("", "Pay a child allowance regardless of parental income", "A universal payment per child is simple, reaches everyone entitled and carries no stigma.", "welfare", "pro", "left"),
    Post("", "Benefit caps keep work paying more than welfare", "An overall ceiling on payments preserves the gap that makes taking a job worthwhile.", "welfare", "contra", "right"),
    Post("", "Pay housing benefit straight to tenants, quickly", "Fast, direct payment prevents arrears building up while a slow claim is processed.", "welfare", "pro", "center"),
    Post("", "Time limits on jobless benefits speed re-entry to work", "A defined support window concentrates job search and stops long-term detachment from the labour market.", "welfare", "contra", "right"),
    Post("", "Lift the state pension floor above the poverty line", "Nobody who paid in over a full working life should retire into hardship.", "welfare", "pro", "left"),
    Post("", "Means-test pensions to target money where it's needed", "Tapering the state pension for people with large private incomes frees funds for those who rely on it.", "welfare", "contra", "right"),
    Post("", "Scrap sanctions for missed appointments", "Docking someone's rent money for a late bus deepens crisis without improving their job prospects.", "welfare", "pro", "left"),
    Post("", "A participation income asks something back for support", "Light obligations like training or community work keep the deal reciprocal and public backing intact.", "welfare", "contra", "right"),
    # --- europe (pro = more shared EU authority / contra = more national control) ---
    Post("", "Use joint EU borrowing for cross-border energy grids", "Shared debt for interconnectors spreads the cost of infrastructure that benefits the whole bloc.", "europe", "pro", "left"),
    Post("", "Fiscal rules must stay in national hands", "Parliaments answerable to their own voters should keep the final say over tax and spending.", "europe", "contra", "right"),
    Post("", "Enforce an EU-wide corporate minimum tax", "A common floor, actually policed, stops member states competing to host paper headquarters.", "europe", "pro", "center"),
    Post("", "Majority voting on foreign policy sidelines small states", "Dropping the veto lets large members set a common line that smaller countries can't check.", "europe", "contra", "right"),
    Post("", "Give a common EU asylum agency binding decisions", "One agency applying the same rules everywhere ends the lottery of where a claim is lodged.", "europe", "pro", "left"),
    Post("", "Brussels shouldn't set national health standards", "How hospitals are run and funded is bound up with national budgets and should stay a domestic call.", "europe", "contra", "right"),
    Post("", "Write a single EU rulebook for AI and data", "One set of rules across the market is simpler for firms than 27 variants and easier to enforce.", "europe", "pro", "center"),
    Post("", "A pan-EU electoral list weakens local accountability", "MEPs elected from a continent-wide slate answer to a party machine, not a place voters can name.", "europe", "contra", "right"),
    # --- foreign_policy (pro = diplomacy/civilian means first / contra = deterrence and defense first) ---
    Post("", "Fund conflict-mediation and civilian observer missions", "Trained mediators and monitors on the ground can keep a ceasefire holding long enough for talks.", "foreign_policy", "pro", "left"),
    Post("", "Meet the defence spending pledge without delay", "Commitments made to allies only mean something if the budget follows on the agreed timetable.", "foreign_policy", "contra", "right"),
    Post("", "Provide climate-adaptation finance to vulnerable states", "Helping exposed countries build defences against drought and floods heads off later crises and displacement.", "foreign_policy", "pro", "center"),
    Post("", "Arms to partners under attack are a duty", "A country defending itself against invasion has a right to the means to do so, promptly.", "foreign_policy", "contra", "right"),
    Post("", "Rejoin and strengthen multilateral arms-control treaties", "Verified limits on weapons are cheaper and safer than an open-ended build-up on every side.", "foreign_policy", "pro", "left"),
    Post("", "Sanctions need military backing to be credible", "Economic pressure works only when the other side believes there is a harder response behind it.", "foreign_policy", "contra", "right"),
    Post("", "Expand cultural and academic exchange programmes", "Long-running exchanges build the personal ties that keep channels open even when relations cool.", "foreign_policy", "pro", "center"),
    Post("", "Energy security means stockpiles and alliances, not talks", "Reliable supply comes from diversified contracts and reserves, not from dialogue with unreliable suppliers.", "foreign_policy", "contra", "right"),
]


def main() -> None:
    if not db.is_configured():
        print("SUPABASE_URL/SUPABASE_SECRET_KEY are missing - please set .env before running this script.", file=sys.stderr)
        sys.exit(1)

    author_id = db.ensure_author(BYLINE["name"], BYLINE["handle"], BYLINE["avatar"])
    if author_id is None:
        print(f"Could not create/find the '{BYLINE['name']}' byline - aborting.", file=sys.stderr)
        sys.exit(1)

    inserted = 0
    for post in MORE_POSTS:
        if db.insert_post(post.title, post.text, post.topic, post.perspective, None, post.political_label, author_id):
            inserted += 1
        else:
            print(f"Failed to insert: {post.title!r}", file=sys.stderr)

    print(f"{inserted}/{len(MORE_POSTS)} posts created under '{BYLINE['name']}'.")


if __name__ == "__main__":
    main()
