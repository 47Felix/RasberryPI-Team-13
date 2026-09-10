"""One-off script: adds 50 more posts across the same 12 topics as
seed_demo_accounts.py's SEED_POSTS, to grow the dataset without touching the
existing ~100 seed posts or requiring an admin Supabase Auth account.

Posted under a fictional byline (db.ensure_author(), the same "legacy"
mechanism as the original static dataset in supabase/migrations/0001_init.sql)
instead of a real user_id - so this only needs SUPABASE_URL/
SUPABASE_SECRET_KEY in the environment/.env, no account credentials.

Usage:

    python3 seed_more_posts.py

Safe to re-run in the sense that it won't create duplicate authors (upsert on
handle), but posts themselves ARE duplicated on a second run (no dedup key on
content) - only run once per environment.

Same per-topic pro/contra axis as SEED_POSTS in seed_demo_accounts.py (see
that file's docstring and supabase/migrations/0008_topic_stance_labels.sql
for the exact "pro means X, contra means Y" phrasing per topic). Content is
intentionally civil and states each side fairly - this is a filter-bubble
demo, not a place to model inflammatory posting.
"""

import sys

import db
from ranking import Post

BYLINE = {"name": "Community Desk", "handle": "@communitydesk", "avatar": "\U0001f4f0"}

MORE_POSTS = [
    # --- climate (pro = more climate protection, faster / contra = more weight on cost) ---
    Post("", "Phase out fossil fuel subsidies", "Ending subsidies for coal, oil and gas frees up public funds for the renewable transition and removes an unfair cost advantage.", "climate", "pro", "left"),
    Post("", "Heat-pump mandates cost families too much upfront", "Requiring heat pumps in every renovation adds costs many households can't absorb without more support first.", "climate", "contra", "right"),
    Post("", "Fund community solar projects", "Grants for shared solar installations let renters and low-income households benefit from clean energy too.", "climate", "pro", "center"),
    Post("", "Carbon offsets let big polluters off the hook", "Relying on offset credits lets large emitters avoid actually cutting their own emissions.", "climate", "contra", "left"),
    Post("", "Speed up nuclear plant approvals", "Faster licensing for next-generation reactors adds reliable, low-carbon power to the grid sooner.", "climate", "pro", "right"),
    # --- transport (pro = priority for bikes/transit/rail / contra = priority for cars/status quo) ---
    Post("", "Make city-center bus lanes permanent", "Dedicated bus lanes keep public transit reliable even during rush-hour congestion.", "transport", "pro", "left"),
    Post("", "Congestion pricing punishes commuters", "Charging drivers to enter city centers mainly hurts people who have no realistic transit alternative.", "transport", "contra", "right"),
    Post("", "Standardize e-scooter parking zones", "Clear parking rules for shared scooters reduce sidewalk clutter without banning the service outright.", "transport", "pro", "center"),
    Post("", "Ride-hailing apps undercut public transit funding", "Cheap ride-hailing pulls riders and revenue away from buses and trains that serve everyone.", "transport", "contra", "left"),
    # --- economy (pro = more redistribution/worker protection / contra = priority for business/market) ---
    Post("", "Guarantee equal-pay audits for large employers", "Mandatory pay audits make wage gaps visible and give workers a real basis to demand fairness.", "economy", "pro", "left"),
    Post("", "Mandatory audits burden small employers too", "Even small businesses would face compliance costs meant for large corporations.", "economy", "contra", "right"),
    Post("", "Simplify small-business tax filing", "A simplified flat filing option saves small business owners time without cutting their tax bill unfairly.", "economy", "pro", "center"),
    Post("", "Trade deals need enforceable labor protections", "Agreements without real labor standards let companies shift production to avoid worker protections.", "economy", "contra", "left"),
    # --- digital (pro = civil rights/privacy first / contra = fewer rules or more investigative power) ---
    Post("", "Ban targeted political ads based on personal data", "Restricting microtargeted political ads limits manipulation based on personal profiling.", "digital", "pro", "left"),
    Post("", "Ad restrictions hurt small campaigns most", "Limiting targeted ads mainly hurts under-funded campaigns that rely on cheap, precise outreach.", "digital", "contra", "right"),
    Post("", "Require plain-language privacy notices", "Clear, short privacy summaries help people actually understand what they're agreeing to.", "digital", "pro", "center"),
    Post("", "Age-verification laws risk more data collection", "Requiring ID checks to access platforms creates new databases of sensitive personal information.", "digital", "contra", "left"),
    Post("", "Cut licensing barriers for small tech startups", "Fewer bureaucratic hurdles let small software companies compete with established platforms.", "digital", "pro", "right"),
    # --- education (pro = redistribution/longer shared schooling / contra = achievement and tracking) ---
    Post("", "Provide free school meals for all students", "Universal free meals remove stigma and make sure no child studies hungry.", "education", "pro", "left"),
    Post("", "Free meals for all is a poor use of limited funds", "Means-tested meal programs reach families who actually need help without spending on those who don't.", "education", "contra", "right"),
    Post("", "Expand vocational training partnerships with local businesses", "Direct partnerships give students real work experience alongside their studies.", "education", "pro", "center"),
    Post("", "Standardized testing narrows what schools teach", "Heavy emphasis on test scores pushes schools to teach to the test instead of broader skills.", "education", "contra", "left"),
    # --- health (pro = solidarity/more state control / contra = competition and personal contribution) ---
    Post("", "Cap out-of-pocket costs for chronic medication", "A firm yearly cap protects patients with long-term conditions from unpredictable costs.", "health", "pro", "left"),
    Post("", "Price caps discourage new drug development", "Capping prices too aggressively reduces the incentive to invest in new treatments.", "health", "contra", "right"),
    Post("", "Expand telehealth access in rural areas", "Remote consultations bring specialist care to areas without nearby clinics.", "health", "pro", "center"),
    Post("", "Telehealth can't replace in-person care for everyone", "Virtual visits work well for some cases but risk missing issues that need hands-on examination.", "health", "contra", "left"),
    # --- migration (pro = more open/admission/inclusion / contra = tighter limits and controls) ---
    Post("", "Recognize foreign qualifications faster", "Speeding up credential recognition lets skilled migrants work in their trained profession sooner.", "migration", "pro", "left"),
    Post("", "Faster recognition without proper checks risks quality", "Skipping thorough verification steps could let unqualified applicants through in high-stakes fields.", "migration", "contra", "right"),
    Post("", "Fund language courses starting on arrival", "Early language support improves integration outcomes and reduces long-term costs.", "migration", "pro", "center"),
    Post("", "Language requirements shouldn't gate basic services", "Requiring fluency before accessing healthcare or housing support punishes people for still learning.", "migration", "contra", "left"),
    # --- housing (pro = more rent regulation/social housing / contra = fewer rules, focus on new construction) ---
    Post("", "Give tenants first right to buy their building", "A right of first refusal lets tenants organize and buy their building before it's sold to investors.", "housing", "pro", "left"),
    Post("", "Right-to-buy rules discourage property investment", "Limiting a landlord's ability to sell freely makes investing in rental housing less attractive.", "housing", "contra", "right"),
    Post("", "Streamline permits for accessory dwelling units", "Faster approval for small backyard units adds affordable housing without large new developments.", "housing", "pro", "center"),
    Post("", "Accessory units alone won't fix the housing shortage", "Small individual units are no substitute for large-scale public housing investment.", "housing", "contra", "left"),
    # --- security (pro = more presence/police powers / contra = prevention and civil liberties first) ---
    Post("", "Increase funding for forensic labs", "Faster case processing depends on labs having the staff and equipment to keep up with demand.", "security", "pro", "right"),
    Post("", "More forensic funding shouldn't mean more surveillance", "Investment in solving crimes must not come bundled with expanded data collection powers.", "security", "contra", "left"),
    Post("", "Require body cameras for all patrol officers", "Consistent body-camera use protects both officers and the public with a clear record of encounters.", "security", "pro", "center"),
    Post("", "Body-camera programs are expensive to maintain", "Storage, review and maintenance costs for footage strain smaller department budgets.", "security", "contra", "right"),
    # --- welfare (pro = higher/more reliable benefits / contra = personal responsibility and incentives) ---
    Post("", "Automatically enroll eligible families in benefits", "Automatic enrollment ensures families actually receive support they qualify for instead of missing it due to paperwork.", "welfare", "pro", "left"),
    Post("", "Automatic enrollment risks paying ineligible people", "Skipping active verification increases the risk of benefits going to people who don't qualify.", "welfare", "contra", "right"),
    Post("", "Index benefit rates to actual regional living costs", "Adjusting support levels by region reflects that the cost of living varies significantly.", "welfare", "pro", "center"),
    Post("", "Regional indexing could shortchange people in cheaper areas", "Lower payments in lower-cost regions can still leave people without enough to live decently.", "welfare", "contra", "left"),
    # --- europe (pro = more shared EU authority / contra = more national control) ---
    Post("", "Create a joint EU minimum-wage framework", "A coordinated wage floor across member states reduces a race to the bottom on labor costs.", "europe", "pro", "left"),
    Post("", "Wage policy should stay a national decision", "Cost of living varies too much across the EU for one common wage floor to make sense.", "europe", "contra", "right"),
    Post("", "Simplify cross-border recognition of professional degrees", "Faster mutual recognition lets professionals work across the EU without duplicate certification.", "europe", "pro", "center"),
    Post("", "Harmonizing degree standards could lower quality floors", "Aligning standards across very different education systems risks settling for the lowest common denominator.", "europe", "contra", "left"),
    # --- foreign_policy (pro = diplomacy/civilian means first / contra = deterrence and defense first) ---
    Post("", "Expand humanitarian visa programs", "Dedicated visa pathways for people fleeing crises save lives without waiting on lengthy asylum processes.", "foreign_policy", "pro", "left"),
    Post("", "Humanitarian visas need stricter vetting", "Fast-tracked entry programs still need thorough security screening before approval.", "foreign_policy", "contra", "right"),
    Post("", "Increase funding for international peacekeeping missions", "Well-funded peacekeeping missions help prevent conflicts from escalating into larger regional wars.", "foreign_policy", "pro", "center"),
    Post("", "Peacekeeping missions shouldn't prop up unstable governments", "Long-term missions can end up supporting governments that don't serve their own people's interests.", "foreign_policy", "contra", "left"),
]


def main() -> None:
    if not db.is_configured():
        print("SUPABASE_URL/SUPABASE_SECRET_KEY are missing - please set .env before running this script.", file=sys.stderr)
        sys.exit(1)

    author_id = db.ensure_author(BYLINE["name"], BYLINE["handle"], BYLINE["avatar"])
    if author_id is None:
        print("Could not create/find the 'Community Desk' byline - aborting.", file=sys.stderr)
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
