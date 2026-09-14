-- Feed-diversity prototype (Case 3): fix a mismatch between the migration
-- files and the real Supabase instance discovered 2026-09-10 while seeding
-- more posts (seed_more_posts.py) - every insert with an English
-- political_label ('left'/'center'/'right') failed with a check-constraint
-- violation (23514).
--
-- Root cause: 0003_political_label.sql/0004_onboarding_survey.sql were
-- edited after already being applied to the real instance, to describe the
-- 2026-09-09 English-only decision as if it had always been the case (their
-- comments even claim "no rename migration needed" for this column). But a
-- plain `alter table ... add column if not exists ... check (...)` is a
-- no-op once the column exists - rewriting the file never touched the
-- constraint actually enforced on the live database, which was created
-- with the original German values ('links'/'mitte'/'rechts') and still had
-- 133 posts and 4 profiles using them as of this migration. Every form in
-- the English-only app has been submitting English values against that
-- constraint ever since, failing silently wherever callers don't surface
-- Supabase errors (db.insert_post()/create_unique_profile() both just
-- return False/log-and-continue) - this was a live, silent bug in
-- production, not just a seeding-script problem.
--
-- Same UPDATE-in-place approach as 0007_english_content.sql (categories/
-- authors rename): keeps row ids stable, translates existing data instead
-- of orphaning it. Safe to run more than once (UPDATEs match zero rows the
-- second time, and postgres allows re-dropping an already-dropped
-- constraint via IF EXISTS).

alter table posts drop constraint if exists posts_political_label_check;
alter table profiles drop constraint if exists profiles_onboarding_political_label_check;

update posts set political_label = 'left' where political_label = 'links';
update posts set political_label = 'center' where political_label = 'mitte';
update posts set political_label = 'right' where political_label = 'rechts';

update profiles set onboarding_political_label = 'left' where onboarding_political_label = 'links';
update profiles set onboarding_political_label = 'center' where onboarding_political_label = 'mitte';
update profiles set onboarding_political_label = 'right' where onboarding_political_label = 'rechts';

alter table posts add constraint posts_political_label_check
  check (political_label in ('left', 'center', 'right'));
alter table profiles add constraint profiles_onboarding_political_label_check
  check (onboarding_political_label in ('left', 'center', 'right'));
