-- Feed-diversity prototype (Case 3): eight more topic categories on top of
-- the four seeded in 0001_init.sql (klima/verkehr/wirtschaft/digital), so
-- the ~100 seed posts in seed_demo_accounts.py and user-submitted posts can
-- spread across a realistic range of political topics instead of crowding
-- into four buckets. Run once via the Supabase SQL Editor, or apply_schema.py
-- (same approach as 0001-0005).
--
-- app.py reads the live topic list from this table (known_topics() ->
-- db.fetch_categories()), so once these rows exist they show up in the post
-- dropdown, /dashboard and post validation automatically - no code change
-- needed. db.insert_post()'s category_id lookup also needs them, otherwise
-- posts on these topics fall back to a null category ("sonstiges").

insert into categories (name) values
  ('bildung'),
  ('gesundheit'),
  ('migration'),
  ('wohnen'),
  ('sicherheit'),
  ('soziales'),
  ('europa'),
  ('aussenpolitik')
on conflict (name) do nothing;
