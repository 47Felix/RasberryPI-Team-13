# Feed Diversity Prototype (DTEW Case 3)

Small test environment for the core question from Case 3 (digi&demo e.V.): *"Design of
feeds / 'For You': instead of algorithms that can reinforce bubbles, and
bubbles that form through self-selection, how can recommenders be designed to
inform users in a way that is varied but still topically relevant?"*

No self-trained ML model (see [`ObsidianGehirn/10 DTEW
Workshop/Team 13 - Digitale Demokratie.md`](../../ObsidianGehirn/10%20DTEW%20Workshop/Team%2013%20-%20Digitale%20Demokratie.md)),
but classic content-based filtering via TF-IDF + cosine similarity
(`scikit-learn`).

## Two feed modes (`ranking.py`)

- **Standard** (`standard_feed`): same perspective as the seed post first
  (similarity only sorts within that group) - bubble-reinforcing, like a
  typical "For You" feed. Pure global similarity isn't enough for that: on
  the small dataset, counter-perspective posts on the same topic often share
  just as much vocabulary as same-perspective posts, so a pure similarity
  ranking doesn't reliably show the bubble at all (see the docstring in
  `ranking.py`).
- **Diversity-aware** (`diversity_aware_feed`): same similarity base, but
  deliberately mixes in the most similar post with **the same topic but the
  opposite perspective** every `diversity_every` slots and flags it.

**Similarity quality on the real ~250-post dataset (checked 2026-09-10,
Felix's algorithm-review brief):** a plain, default-settings TF-IDF
vectorizer produced visibly bad neighborhoods once the seed dataset grew
past a handful of posts - a short post's few body sentences gave the
title's on-topic vocabulary no extra weight over incidental body words, so
e.g. the seed post "Speed up wind power expansion" (climate) ranked an
unrelated migration post ("Speed up procedures without cutting legal
protection") above other genuine climate posts, purely because both share
the word "speed". Fixed in `_post_text()`/`_tfidf_matrix()`: the title is
now counted twice, plus English stop words and word bigrams (catches short
domain phrases like "speed limit" that unigrams alone conflate with
unrelated posts sharing just one of the two words). Verified against the
real seed corpus (`seed_demo_accounts.py` + both `seed_more_posts*.py`
files, 250 posts) and covered by a regression test
(`test_similarity_ranking_prefers_genuine_topic_match_over_a_shared_incidental_word`
in `tests/test_ranking.py`). `_tfidf_matrix()` falls back to an untuned
vectorizer if the tuned settings would leave nothing to vectorize (e.g. a
post consisting only of stop words) - user-authored text is a real
boundary case, this route must never 500.

Also checked, no changes needed: `standard_feed()`'s proportional
`preferred_political_ratio` mix already has test coverage for a single
labeled like, exact ties and an empty bucket (see
`test_political_label_ratio_*`/`test_standard_feed_ratio_*` in
`tests/test_ranking.py`); `diversity_every` still visibly interrupts the
feed at the right cadence on the full 250-post dataset; a fully cold
account (no likes, no onboarding answers, seed post itself without a
`political_label`) renders a sane feed instead of erroring out; and
`standard_feed`/`diversity_aware_feed` are deterministic across repeated
calls with identical input (both now covered by an explicit regression
test - the earlier lack of one was itself a gap, not a bug: nothing here
ever depended on dict/set iteration order for tie-breaking).

**Account bias from like history:** for logged-in accounts, it's no longer
just the currently selected seed post that decides which perspective "wins" -
`ranking.dominant_perspective()` evaluates whether an account has liked
mostly "pro" or "contra" across its entire like history, and this
`preferred_perspective` value then overrides the seed post's perspective in
`standard_feed`/`diversity_aware_feed`. Result: the standard feed reinforces
itself in one direction with every further like, and does so *across any
seed post*, not just the one that was just liked - deliberately with no
built-in escape (that's the point of the demo). The diversity-aware feed
uses the same `preferred_perspective` value to deliberately break the
*actual* account lean instead of just the current seed post's. Without an
account or without prior likes (or on an exact tie), the old behavior
remains: the seed post's own perspective decides.

### A position, not just "pro/contra"

A bare `pro`/`contra` (e.g. "climate: pro") says little without the post in
front of you. `app.TOPIC_STANCES` therefore assigns each topic **a fixed
direction** for what "pro" and "contra" mean there (roughly: "pro" = more
ambition / more protection / more openness, "contra" = more weight on cost,
the market or the status quo), and `stance_label(topic, perspective)`
returns the short phrase for it - e.g. `climate/pro` -> "more climate
protection, faster", `economy/contra` -> "priority for businesses and the
market". Feed chips, `/dashboard` and the "why are you seeing this?" line on
each post show this phrase instead of just the word. Topics with no entry
(categories added later) fall back to the bare `pro`/`contra`.

So the phrase doesn't lie, `perspective` in the seed dataset
(`seed_demo_accounts.py`) is maintained **as a consistent axis per topic**:
all "pro" posts on a topic lean the same direction, all "contra" posts the
other way. Please add new posts on the same axis as the rest of their
topic. The phrasing is deliberately short and meant as a reading aid, not a
formal definition - individual cases can be fuzzy, and the post title sits
right next to it anyway.

## Political labeling (left/center/right) as a second, independent dimension

Until this feature, each post only had one axis: `perspective` (pro/contra
on its topic). Since this extension there is a second, independent axis:
`political_label` (`left`/`center`/`right`), e.g. a post can be both "pro
wind power expansion" **and** "left", or "pro wind power expansion" **and**
"right" - the two axes are orthogonal, not the same field twice.

**Deliberately no automatic left/right classifier.** Critical point 6 from
the DTEW 0209 note (`ObsidianGehirn/10 DTEW Workshop/DTEW 0209 - Kritische
Punkte, Problem Statements und Ideation.md`) names it directly: "How do you
even measure/show 'perspective diversity' rather than just subjectively
claiming it's more diverse now?" A reliable automatic detection of political
orientation from free text is an unsolved problem that is itself contested
in NLP research (inconsistent training data, culturally/temporally shifted
definitions of "left" and "right", high error rates especially on short
posts without much context) and isn't realistically achievable in a
two-week prototyping sprint without prior ML experience on the team (the
same assessment as for Lasse's fake-news-detector proposals, see
`ObsidianGehirn/10 DTEW Workshop/Team 13 - Digitale Demokratie.md`). A
prototype that internally claims "this is objectively left" would fake an
accuracy it doesn't have, and would itself reproduce exactly the kind of
invisible, unverifiable algorithmic judgment that this whole case is
supposed to make visible.

**Instead: users choose the label themselves**, when creating a post via a
dropdown, exactly like topic/perspective already work (`templates/
index.html`, field `political_label`, checked server-side against
`KNOWN_POLITICAL_LABELS` in `app.py:create_post`). No automatic adjustment,
no hidden scoring - the author sees their own label, everyone else sees it
on the post (a small three-segment "compass" chip, inspired by Felix's
brain-dump idea of a "perspective compass", see `ObsidianGehirn/07 Brain
Dump/Felix - Brain Dump.md`).

**Critical framing:** a self-chosen label is not an objective measure of
"actual" political position, it's self-reported. That brings its own biases
(self-selection, social-desirability bias, some users strategically label
"center" to seem neutral, others deliberately overstate), but it's honest
about what it is: an attribution by the author, not a truth claimed by the
app. For a demo prototype meant to show *how* a ranking can reinforce or
break a chosen dimension, this transparent label is enough - it doesn't
replace, and isn't meant to replace, a real, validated political-science
metric.

**How it feeds into the ranking (`ranking.py`):** `dominant_political_label()`
is the counterpart to `dominant_perspective()` - the majority label across
an account's entire like history (field `political_label` in
`db.fetch_liked_history()`, folded into the same query as topic/perspective
rather than querying the same likes join twice), `None` on missing signal or
a tie between multiple labels. In `standard_feed()`, the result
(`preferred_political_label`, or the seed post's own label as a fallback)
additionally sorts *within* the existing perspective tier by whether the
political label matches - a post that matches both perspective and
political camp ranks ahead of one that only matches the perspective. In
`diversity_aware_feed()`, a diversity slot prefers a "double counter" (differs
on *both* axes) over one that only differs on one axis.
`diversity_score_for_political_label()` measures the same diversity share as
`diversity_score_for_perspective()`, just for the political axis, and is
shown in the UI as a second value next to the perspective score (only when a
political signal actually exists). Both axes are independently testable
(`tests/test_ranking.py`) and don't change the existing, already-tested
perspective ranking when no `political_label` is set (backward compatible
with posts from before this extension).

**Bubble development over time, for both axes:** `ranking.bubble_trend()`
(perspective) previously had no counterpart for the political axis. New:
`ranking.political_bubble_trend()`, same idea (the share of likes so far
that belong to whichever value was dominant at that point, computed per like
rather than only as a snapshot), but for three possible values
(left/center/right) instead of two, so it needs its own counting logic
rather than reusing the pro/contra counters. Likes on posts with no label set
(liked before this extension existed, or the author didn't choose one) are
skipped rather than counted as a separate "no label" bar. In the UI
(`templates/index.html`) this shows up as a second sparkline panel ("Your
political bubble over time") below the existing one, only visible once at
least two labeled likes exist, color-distinguished (`--accent-ink` instead
of `--brand`) so the two axes don't read as one duplicated widget.

**Schema:** `supabase/migrations/0003_political_label.sql` adds the
`posts.political_label` column (nullable, `check` on the three allowed
values). Needs to be applied once like 0001/0002 (SQL editor or
`apply_schema.py`).

⚠️ **Found and fixed 2026-09-10:** 0003/0004 were edited after already being
applied to the real instance, to describe them as English-only in
hindsight - but `alter table ... add column if not exists` is a no-op once
the column exists, so the live check constraint still only accepted the
original German values (`links`/`mitte`/`rechts`), rejecting every English
value every form in the app has been submitting since the English switch.
`0010_political_label_english.sql` drops and recreates both constraints
with the English values and translates the 133 existing posts/4 profiles
that had a German label. Applied against the real instance - see that
migration's comment for the full story, and don't edit an already-applied
migration file's *behavior* again without a matching follow-up migration.

## UI: one feed, two modes (`templates/index.html`, `static/style.css`)

Discarded after user feedback ("looks like Claude design", "not a real
feed"): two side-by-side columns with a segmented control, a slider and a
score pill. Instead, a **single, vertically scrolling feed** with a tab
switcher on top ("Standard" / "Diversity-aware", `?mode=`), like an actual
switch between two feeds in an app:

> [!note] Second redesign (overnight session): away from the generic SaaS look
> The same feedback ("looks like Claude design") came a second time, this time
> about the concrete implementation (indigo gradient in the header, uniformly
> rounded white cards, sans-serif UI font) - typical traits of generic AI
> dashboard templates. `static/style.css` was then rebuilt entirely around an
> editorial look instead of just swapping colors: a warm paper background
> instead of cool gray, a serif font (Georgia) for the nameplate/post titles
> instead of sans-serif everywhere, a monospace font for metadata (handle,
> time, category chips) in the style of a news-agency byline, hairline rules
> instead of floating cards with shadows, no more gradient in the header (a
> flat surface with a double rule like a newspaper masthead). The new
> political labeling (see above) gets its own small three-segment "compass"
> chip instead of another generic badge, as a distinct visual element instead
> of a third color in the same chip style.

- Every post has a feed-typical header line (avatar, account name, handle,
  relative time) instead of a bare card - avatar/name/handle come from the
  real account that created the post.
- Counter-perspective posts get a small "Suggested" label instead of an
  attention-grabbing badge.
- The own seed post and diversity slider have moved into a collapsed "feed
  settings" element - visible/usable, but no longer the main surface of the
  page.

### Rotation on reload

So that "refresh" actually brings **new posts** instead of always the same
top slice, `index()` remembers the most recently shown post ids in the Flask
session (`seen_post_ids`, capped at `SEEN_HISTORY_CAP`). A plain browser
reload (without `?seed_id=`) then picks the next not-yet-shown post as the
seed post and hides the already-shown ones from the feed body
(`ranking.standard_feed()`/`diversity_aware_feed()` have an optional
`exclude_ids` parameter for this, `None` = old behavior). Once the whole
catalog has been shown, the rotation starts over. An **explicitly set**
`?seed_id=` (tab switch, "feed settings", seed post dropdown) deliberately
doesn't rotate - so the two modes stay comparable for the same post. The
existing "new posts" poll (`/posts/latest-id`, every ~15s) remains in
addition, for posts *other people* create in the meantime.

## Accounts, posts, comments, likes & category suggestion (Supabase)

There is no more static/hardcoded dataset - **all** posts in the feed come
from Supabase, created by real accounts via the "create new post" form. If
Supabase isn't configured/reachable or the table is empty, the page shows an
explicit empty state instead of any placeholder content. Storage is Supabase
Postgres, connected via `db.py`. Posting, liking and commenting requires a
**real, logged-in account** (Supabase Auth) - no anonymous interactions.

**Schema** (`supabase/migrations/0001_init.sql` + `0002_accounts.sql`):
`categories`, `authors` (fallback display for posts from before accounts
existed, see below), `posts` (references both plus `user_id`), `profiles`
(display name/handle/avatar per Supabase Auth account, `id` =
`auth.users.id`), `likes` (post + `user_id`, composite key - one like per
account and post), `comments` (post + `user_id` + text, deletable per
account). `posts.user_id`/`likes.user_id`/`comments.user_id` deliberately
point at `profiles(id)` rather than directly at `auth.users(id)` - that's
the only way PostgREST can embed the relation when querying (the `auth`
schema isn't visible to PostgREST). Embedding `profiles` in `fetch_posts()`
additionally needs the explicit hint `profiles!posts_user_id_fkey`, because
`likes` (with both `post_id` and `user_id`) forms a second, many-to-many
relationship between `posts` and `profiles` from PostgREST's point of view -
without the hint, PostgREST refuses the request as ambiguous.

- `.env` (not committed, see `.gitignore`) with `SUPABASE_URL`,
  `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`
- Data tables still run exclusively through the **secret key** (server-side,
  bypasses row level security) - **new:** registration/login go directly
  against the Supabase Auth API (GoTrue) with the **publishable key**, which
  is the key meant for that (see `db.sign_up`/`db.sign_in`)
- All tables have RLS enabled **without** policies - only the secret key can
  reach the data tables, direct access via the publishable key is
  deliberately blocked there
- In the Supabase dashboard under *Authentication -> Providers -> Email*,
  disable the **"Confirm email"** option - otherwise nobody can log in right
  after registering, because a confirmation link would first have to be
  clicked in an email (not configured in this setup)
- Create tables/migrations once: run the SQL from
  `supabase/migrations/*.sql` in order in the Supabase dashboard under *SQL
  Editor*, **or** run `apply_schema.py` (with no argument it automatically
  applies every migration in filename order; needs
  `SUPABASE_MANAGEMENT_TOKEN`, an account-wide personal access token from
  the Supabase account settings - direct Postgres port 5432 isn't reachable
  from some sandbox environments, so the script goes through the management
  API over HTTPS instead)
- Likes are keyed on `(post_id, user_id)` (already switched over by
  `0002_accounts.sql`, applied against the real instance). Posts from before
  accounts existed, with no `user_id`, still show the fictional `authors`
  entry as the author, new posts show the real account
- If Supabase is down/not configured, or no posts have been created yet, the
  page shows an empty state ("No posts found") instead of an error or made-up
  content

**Accounts:** `/register` (email, password, display name) creates a Supabase
Auth account plus a `profiles` row (the handle is derived from the display
name, with a numeric suffix on collision, see `db.create_unique_profile`).
`/login`/`/logout` manage the session (the Flask session cookie only stores
`user_id`/display name/handle, never the password). Without an account:
reading the feed still works, posting/liking/commenting requires login
(redirect to `/login`, a 401 for the fetch()-driven actions).

**Comments:** expandable per post via "💬 N comments" (loads via
`GET /posts/<id>/comments`), a new comment via a form
(`POST /posts/<id>/comments`, JSON, requires login). Your own comments can be
removed again via a "Delete" link (`DELETE /comments/<id>`) - the permission
is checked server-side (`db.delete_comment` additionally filters on
`user_id`), not just by hiding the button in the UI.

**Category suggestion:** `ranking.suggest_category()` (a pure, network-free
function, covered by a unit test) compares the draft's title+text via TF-IDF
against all existing posts and suggests the topic of the most similar post.
Wired up in the form via a "Suggest" button
(`POST /posts/suggest-category`), but doesn't overwrite anything
automatically - the dropdown stays editable.

**The topic list is live, not hardcoded:** `app.py:known_topics()` reads all
topics from the `categories` table (`db.fetch_categories()`). A new row
there (e.g. via the Supabase SQL editor) shows up everywhere on the next
request - the post form dropdown, `/dashboard` chips and validation when
creating a post - with no code change. Only if Supabase isn't
configured/reachable does it fall back to the hardcoded `DEFAULT_TOPICS`
list (demo mode with the static dataset). The sign-up survey
(`ONBOARDING_QUESTIONS`) stays deliberately manually curated, because every
question needs its own hand-written pro/contra statement - new topics
without their own question are simply left out of the survey (the survey is
optional anyway, see above).

**Likes:** toggled per account (`(post_id, user_id)` in the DB, requires
login). Since `dominant_perspective()`/`dominant_political_label()` (see
above), likes feed directly into the ranking, no longer just a plain
display count.

## Running locally

```bash
cd Code/feed-diversity-prototype
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5050`.

## Team dashboard: which account gets which feed and why (`/dashboard`)

Shows, for every account side by side, the current feed bias per topic
(pro/contra) and the political camp, including the source (real
likes/comments engagement, which always wins once it exists, vs. the sign-up
survey as a fallback without engagement) - see
`app.py:compute_preferences()`, shared between `index()` and `/dashboard` so
the two views can't drift apart. The reasoning for a single post in your own
feed is shown right on the post itself (ⓘ line,
`app.py:_feed_item_reason()`).

Gated behind `ADMIN_DASHBOARD_TOKEN` (`.env`) instead of being publicly
reachable, because it necessarily exposes every account's derived political
camp - call via `/dashboard?token=…`. An empty/missing token disables the
page entirely (shows a notice instead of an error), never open by default.

## Deployment (making it publicly reachable)

`deploy/` contains a ready-made systemd unit (Gunicorn instead of the Flask
dev server) and a Caddyfile (automatic HTTPS via reverse proxy), plus a
step-by-step guide including an Azure NSG firewall note and a
Tailscale-only alternative - see `deploy/README.md`. Not applied yet, only
prepared (see the guide there for why).

## Tests

```bash
pytest tests/
```

## Example accounts for the standard algorithm (`seed_demo_accounts.py`)

A convincing demo needs accounts with a clearly recognizable, opposing like
history, so `ranking.dominant_perspective()`/`dominant_political_label()`
becomes visible when presenting. `seed_demo_accounts.py` creates four
example accounts for this (different names, two of them consistently like
"contra"/"left" and two "pro"/"right") plus an admin account that publishes
the seed posts, and has the example accounts like matching posts.

The seed dataset (`SEED_POSTS` in the script) covers about **100 posts
across 12 topics** (the four default topics plus `education`, `health`,
`migration`, `housing`, `security`, `welfare`, `europe`, `foreign_policy` -
their `categories` rows are created by
`supabase/migrations/0006_more_categories.sql`, after which they
automatically flow into `known_topics()`/the dropdown/`/dashboard`/
validation). Each topic has several posts per perspective/political label,
at least one "contra/left" and one "pro/right", so every example account
finds matching content on every topic. So the like history stays readable
despite the large dataset, each account likes at most
`MAX_LIKES_PER_TOPIC` (default 1) matching posts per topic - resulting in
roughly a dozen same-direction likes per account. The content is
deliberately phrased neutrally and represents both sides fairly.
`0006_more_categories.sql` needs to be applied once against the real
Supabase instance (like 0003-0005), **before** the seed script runs.

**Credentials come exclusively from the environment/`.env`**
(`DEMO_ACCOUNT_A_EMAIL`/`_PASSWORD` through `DEMO_ACCOUNT_D_EMAIL`/
`_PASSWORD`, `DEMO_ADMIN_EMAIL`/`_PASSWORD`, in addition to the existing
`SUPABASE_*` variables) - the script aborts without these variables instead
of using placeholder values. A plain name/purpose overview of the accounts
(without credentials) lives in the vault at `ObsidianGehirn/06
Zugangsdaten/Feed-Diversity-Beispielaccounts.md`.

```bash
# Add to .env (SUPABASE_* plus the DEMO_* variables above), then once:
python3 seed_demo_accounts.py
```

## More seed posts (`seed_more_posts.py`)

Adds 50 more posts on top of `seed_demo_accounts.py`'s ~100, same 12 topics
and the same per-topic pro/contra axis, without needing an admin Supabase
Auth account - posted under a fictional "Community Desk" byline via
`db.ensure_author()`/`author_id` instead (the same legacy mechanism the
original static dataset used). Only needs `SUPABASE_URL`/
`SUPABASE_SECRET_KEY` in `.env`.

```bash
python3 seed_more_posts.py
```

Safe to re-run for the author (upserted by handle), but posts themselves
have no dedup key and will duplicate on a second run - only run once per
environment.

## Fediverse display (`fediverse.py`, read-only)

At the team's request from the brain dump ("look into fediverse and activity
pub and look how we can connect these things with each other", see
`ObsidianGehirn/07 Brain Dump/Felix - Brain Dump.md`), the feed shows an
additional, clearly marked-as-external section "From the Fediverse on
[topic]" with public Mastodon posts on the currently selected topic.

**Deliberately no ActivityPub implementation.** A full ActivityPub
client/server (its own actor, WebFinger, HTTP signatures, inbox/outbox) is
its own protocol stack realistically worth several weeks of effort, see the
detailed feasibility assessment in the vault (`ObsidianGehirn/10 DTEW
Workshop/Fediverse ActivityPub - Machbarkeitseinschaetzung.md`). Instead,
`fediverse.py` uses Mastodon's **public, unauthenticated REST API** (`GET
/api/v1/timelines/tag/{hashtag}`) - needs no account, no token, works purely
read-only against any Mastodon instance. Failures (instance unreachable,
timeout, unexpected response format) yield an empty list instead of an
error, the same as `db.py` does for an unreachable Supabase. External post
content comes back as HTML from the API and is reduced to plain text before
display (`fediverse._strip_html`) rather than rendered unfiltered into the
template - otherwise that would be an XSS risk via foreign, unmoderated
content.

**Topic coverage & quality filter:** `TOPIC_HASHTAGS` now covers all 12
topics; for a topic with no entry (e.g. a category added later),
`_hashtag_for()` falls back to the cleaned-up topic name as a hashtag
instead of leaving the section empty. While processing the timeline,
**boosts/reblogs** (the `reblog` field set - the actual entry is just a
wrapper) and **text-less posts** (media only) are skipped; the API query
correspondingly fetches more than `limit` entries so `limit` readable ones
remain after filtering. Very long posts are truncated to ~280 characters.

**Caching instead of live per page view:** `index()` calls
`fetch_public_posts()` on every `/` request, but a hashtag timeline doesn't
change fast enough to justify a fresh Mastodon request every time. Since
this overnight session, `fediverse.py` keeps successful responses per
(hashtag, limit) in process memory for `FEDIVERSE_CACHE_SECONDS` (default
300s, changeable via environment variable) instead of asking again on every
call. If a refresh fails after the cache expires (network error, instance
briefly unreachable), the last known cache value keeps being served instead
of showing an empty section - only an *empty* cache falls back to `[]`, the
same "fail open" style as the rest of the module. No Redis or similar needed
for a single-process prototype; with multiple Gunicorn workers (see
`deploy/`), each worker has its own cache, which is uncritical for this
purpose.

> [!warning] Not tested live against Mastodon
> This session's cloud sandbox only allows outbound connections to a fixed
> domain allowlist - a call against `mastodon.social` was blocked by the
> sandbox's own proxy with `403`. Unit-tested with mocked requests
> (`tests/test_fediverse.py`), but not yet verified against the real API -
> check once in an environment with normal internet access before presenting.

## Current status / open items

- [x] Standard and diversity-aware ranking with tests (`ranking.py`,
      dataset-independent - works with any posts, whether previously from
      `data/posts.json` or now from Supabase)
- [x] Supabase connection for all posts, categories, authors
- [x] Category suggestion via TF-IDF when creating a post
- [x] Real accounts (Supabase Auth: registration/login/logout), profiles
      with display name/handle, likes and comments per account instead of
      anonymous session cookies (`0002_accounts.sql`, applied against the
      real instance and verified end to end)
- [x] Own comments deletable (`DELETE /comments/<id>`, checked server-side
      for ownership)
- [x] Static dataset (`data/posts.json`) and the persona quick-picker built
      on it ("Mia"/"Tom") removed - the feed shows exclusively real Supabase
      posts, an empty state instead of placeholders when none exist yet
- [x] Likes as a ranking signal: the standard feed now reinforces the
      majority perspective of the account's own like history instead of
      just the currently selected seed post's (`dominant_perspective`)
- [x] Make a "perspective diversity" metric visible (see critical point 6 in
      the DTEW 0209 note) - besides the diversity score per feed view,
      there's now also a view of its development over time
      (`ranking.bubble_trend()`/`political_bubble_trend()`, sparkline
      panels in `templates/index.html`), for both axes (perspective and
      political label)
- [x] Political labeling (left/center/right) as a second, independent
      dimension next to pro/contra, user-chosen instead of automatically
      detected (see "Political labeling" above, `0003_political_label.sql`)
- [x] Visual redesign away from the generic SaaS/AI-dashboard look (paper
      look, serif/monospace instead of sans-serif throughout, compass chip
      instead of gradients/rounded cards everywhere, see "UI redesign"
      above)
- [x] Switched the whole prototype to English - UI, database content and the
      seed dataset (team decision from 2026-09-09, audience is
      English-speaking, see `NIGHTLY_TASK.md`). Categories/authors already
      applied to the real instance from `0001_init.sql` are renamed via a
      new `0007_english_content.sql` migration (`UPDATE` on existing rows,
      keeps `category_id`/`author_id` references intact - see that
      migration's comment for why an `UPDATE` was chosen over re-migrating
      with new rows) rather than editing the already-applied migration file
      in place
- [x] Apply `0003_political_label.sql`/`0006_more_categories.sql`/
      `0007_english_content.sql` against the real Supabase instance
- [x] Example accounts with an opposing like history for the demo
      (`seed_demo_accounts.py`, executed against the real instance)
- [x] Seed dataset expanded from 8 to ~100 posts across 12 topics
      (`SEED_POSTS` in `seed_demo_accounts.py`, now in English), demo likes
      per topic capped (`MAX_LIKES_PER_TOPIC`) so the like history stays
      readable
- [x] 50 more posts added on top of that (`seed_more_posts.py`, posted under
      a fictional "Community Desk" byline instead of a real account),
      executed against the real instance - 197 posts total as of 2026-09-10
- [x] Fixed a live check-constraint mismatch on `political_label` that
      silently rejected every English value the app was sending
      (`0010_political_label_english.sql`, see "Political labeling" above)
- [x] Feed rotates on reload to not-yet-shown posts (`seen_post_ids` in the
      session, `exclude_ids` in `ranking.py`), so "refresh" brings new posts
      - see "Rotation on reload"
- [x] `pro`/`contra` shown as a concrete position (`TOPIC_STANCES`/
      `stance_label()`) instead of just a word, in the feed chip,
      `/dashboard` and the reason line; seed `perspective` maintained per
      topic as a consistent axis - see "A position, not just pro/contra"
- [x] Fediverse: all 12 topics have a hashtag + name fallback for new
      categories, boosts/text-less posts are filtered (`fediverse.py`)
- [x] First, low-risk Fediverse step: show public Mastodon posts for a
      topic-dependent hashtag, read-only, in the feed (`fediverse.py`, see
      its own section below). A full ActivityPub server/actor remains a
      concept sketch, see the feasibility note in the vault under "10 DTEW
      Workshop"
- [ ] Verify the Fediverse display against the real Mastodon API (blocked in
      this sandbox by the network allowlist, see above)
- [x] Cache the Fediverse fetch instead of live per `/` call (`fediverse.py`,
      `FEDIVERSE_CACHE_SECONDS`, see its own section above)
- [x] Algorithm review against the real ~250-post dataset (2026-09-10 night
      session, per the brief at the top of `NIGHTLY_TASK.md`): found and
      fixed a real TF-IDF neighborhood-quality bug (see "Two feed modes"
      above), checked proportional-ratio edge cases/`diversity_every`
      effectiveness/cold start/determinism with nothing else to fix
- [x] Session cookie size checked for `SEEN_HISTORY_CAP = 60`: a signed
      session with 60 UUIDs plus the other session keys (user id, display
      name, handle) comes to about 2 KB, roughly half the 4 KB browser
      cookie limit - no change needed at the current cap
- [x] Dead-code sweep across `app.py`/`ranking.py`/`db.py`/`fediverse.py`
      (2026-09-10 night session): every function/constant traced to at
      least one real call site beyond its own definition, nothing found to
      remove
- [x] Feed-refresh rotation (`app.py`: `_rotation_plan()`) re-checked against
      the brief in `NIGHTLY_TASK.md` beyond what PR #148 already fixed: the
      "↑ New posts" poll banner's reload is a plain
      `window.location.reload()`, which preserves any `?seed_id=` already in
      the URL, so it can never fight an explicit pin from the dropdown/tab
      switch; small-vs-large dataset behavior and the never-freezes
      guarantee were already covered by `tests/test_rotation.py`. Nothing
      found to fix here.
- [x] Automated route-level test coverage for `app.py` (2026-09-11 night
      session): `pytest`/`ranking.py`/`_rotation_plan()` were covered, but no
      test file exercised the Flask routes themselves (`/`, `/dashboard`,
      `/login`, `/register`, the like/comment JSON endpoints) - every past
      session had only checked these by hand with a Flask test client and
      never committed it. New `tests/test_app.py` (13 tests) mocks the `db`/
      `fediverse` modules and asserts on both modes, the empty-catalogue
      state, `/dashboard`'s locked/unauthorized states, and the new
      accessibility attributes below.
- [x] Accessibility pass on `templates/index.html`/`dashboard.html`
      (2026-09-11 night session, per the "Accessibility/UX polish" item in
      NIGHTLY_TASK.md's next-steps list): added `aria-current="page"` to the
      active feed-mode/dashboard-scope tab, `aria-pressed` + a descriptive
      `aria-label` (kept in sync with the like count) on the like button,
      `aria-expanded` on the comments-toggle button (kept in sync in
      `toggleComments()`), `aria-live="polite"` on the comments list so a
      loaded/deleted comment is announced, and a dedicated visually-hidden
      `aria-live="polite"` status region (`#live-status`) so the "new posts
      available" state is announced to screen readers - the visible
      "↑ New posts" banner alone isn't reliably announced since it's
      `[hidden]` at load. Deliberately did not touch layout/visual design -
      the feed-as-real-app structure (single feed, mode tabs, avatar/handle/
      timestamp) was already built and verified in earlier sessions (see
      NIGHTLY_TASK.md's session log), this only closes gaps in how that
      existing structure is exposed to assistive technology.
