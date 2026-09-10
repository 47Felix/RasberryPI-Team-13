-- Feed-diversity prototype (Case 3): eight more topic categories on top of
-- the four seeded in 0001_init.sql (climate/transport/economy/digital - see
-- 0007_english_content.sql for why those four are English via a rename
-- rather than here), so the ~100 seed posts in seed_demo_accounts.py and
-- user-submitted posts can spread across a realistic range of political
-- topics instead of crowding into four buckets. Run once via the Supabase
-- SQL Editor, or apply_schema.py (same approach as 0001-0005).
--
-- app.py reads the live topic list from this table (known_topics() ->
-- db.fetch_categories()), so once these rows exist they show up in the post
-- dropdown, /dashboard and post validation automatically - no code change
-- needed. db.insert_post()'s category_id lookup also needs them, otherwise
-- posts on these topics fall back to a null category ("other").
--
-- Names are English directly (unlike the original four, this migration was
-- never applied to the real Supabase instance before the team's 2026-09-09
-- English-only decision, see NIGHTLY_TASK.md).

insert into categories (name) values
  ('education'),
  ('health'),
  ('migration'),
  ('housing'),
  ('security'),
  ('welfare'),
  ('europe'),
  ('foreign_policy')
on conflict (name) do nothing;
