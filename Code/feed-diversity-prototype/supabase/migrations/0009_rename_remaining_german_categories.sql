-- Feed-diversity prototype (Case 3): rename the remaining German category
-- names to English, completing the 2026-09-09 English-only decision that
-- 0007_english_content.sql started.
--
-- Discovered 2026-09-10 while wiring up 0008_topic_stance_labels.sql: the
-- real Supabase instance's `categories` table still had German names for
-- 8 of the 12 topics ('bildung', 'gesundheit', 'wohnen', 'sicherheit',
-- 'soziales', 'europa', 'aussenpolitik' - 0006_more_categories.sql's insert
-- was written in English under the assumption these rows didn't exist yet,
-- but they'd apparently already been added by hand with German names before
-- that migration was written, so its `on conflict (name) do nothing` insert
-- was a silent no-op for all eight instead of creating them). Because
-- app.py's TOPIC_STANCES/known_topic_stances() are keyed by the English
-- names, every post in these German-named categories was silently falling
-- back to the bare "pro"/"contra" word instead of a phrase - only
-- 'digital' and 'migration' (identical in both languages) ever matched.
-- This is a plain rename (UPDATE, not a new row), same approach and same
-- safety reasoning as 0007: `categories.id` is a foreign key from
-- `posts.category_id`, so a rename-by-UPDATE keeps every existing post
-- correctly linked with no follow-up needed, unlike inserting a fresh
-- English row would.
--
-- 'politik' is deliberately NOT renamed here - it doesn't correspond to
-- any of the 12 topics TOPIC_STANCES/0008 know about (not in
-- 0006_more_categories.sql's list either), so it's left as-is rather than
-- guessed at. Flag for Felix/Anton to decide: fold it into an existing
-- topic, give it its own TOPIC_STANCES entry, or remove it.
--
-- Safe to run more than once (each UPDATE matches zero rows the second
-- time, same as 0007).

update categories set name = 'education'      where name = 'bildung';
update categories set name = 'health'         where name = 'gesundheit';
update categories set name = 'housing'        where name = 'wohnen';
update categories set name = 'security'       where name = 'sicherheit';
update categories set name = 'welfare'        where name = 'soziales';
update categories set name = 'europe'         where name = 'europa';
update categories set name = 'foreign_policy' where name = 'aussenpolitik';
