-- Feed-diversity prototype (Case 3): rename the German seed content from
-- 0001_init.sql to English, per the team's 2026-09-09 decision to switch
-- the whole prototype to English for an English-speaking audience (see
-- NIGHTLY_TASK.md).
--
-- Migration approach considered and chosen: UPDATE existing rows rather
-- than re-migrating with new rows. 0001_init.sql's categories/authors rows
-- were already applied to the real Supabase instance (see README.md
-- "Aktueller Stand" / git history), so editing 0001_init.sql itself
-- wouldn't rename anything there (its "on conflict do nothing" inserts are
-- no-ops against an instance that already has the German rows) and would
-- misrepresent what that migration actually did when it ran. Re-migrating
-- with brand-new English rows was the other option, but categories.id is a
-- foreign key from posts.category_id (and authors.id from posts.author_id)
-- - new rows would mean either leaving existing posts pointing at
-- newly-orphaned German rows, or a second pass to repoint every post's
-- category_id/author_id. A plain UPDATE keeps the same id, so any post
-- already linked to a renamed row (none existed yet as of this migration -
-- see NIGHTLY_TASK.md, the seed script never ran against the real instance
-- - but this also covers any post a team member created by hand through
-- the UI in the meantime) stays correctly linked with no follow-up needed.
--
-- Safe to run more than once (each UPDATE simply matches zero rows the
-- second time). Safe to run against a brand-new instance that only ran
-- 0001_init.sql moments before (same idempotent UPDATE-by-old-name
-- approach) - a fresh clone runs 0001-0007 in order and ends up with the
-- English names either way.
--
-- Post rows themselves (title/content) are NOT touched here: unlike
-- categories/authors, there is no fixed list to match against, and this
-- migration can't tell a real user-submitted German post from one that
-- should simply be re-translated - guessing would risk silently altering
-- someone's actual content. Any German posts already live on the real
-- instance (the demo/seed posts were never successfully run there, per
-- NIGHTLY_TASK.md, so this is only a concern for posts a team member
-- created by hand) need a manual look, not a blind find/replace.

update categories set name = 'climate' where name = 'klima';
update categories set name = 'transport' where name = 'verkehr';
update categories set name = 'economy' where name = 'wirtschaft';
-- 'digital' is already the same word in both languages - no rename needed.

update authors set name = 'Climate Action Now', handle = '@climateactionnow' where handle = '@klimajetzt';
update authors set name = 'Realistic Energy', handle = '@realisticenergy' where handle = '@energierealistisch';
update authors set name = 'Mobility Transition', handle = '@mobilitytransition' where handle = '@mobilwende';
update authors set name = 'Free to Drive', handle = '@freetodrive' where handle = '@freiefahrt';
update authors set name = 'Fair Wages', handle = '@fairwages' where handle = '@fairelöhne';
update authors set name = 'Voice of Small Business', handle = '@smallbizvoice' where handle = '@mittelstandstimme';
update authors set name = 'Digital Rights', handle = '@digitalrights' where handle = '@digitalerechte';
update authors set name = 'Tech Hub', handle = '@techhub' where handle = '@techstandort';
