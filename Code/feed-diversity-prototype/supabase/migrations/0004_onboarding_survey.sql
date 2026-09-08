-- Feed-diversity prototype (Case 3): short opt-in onboarding survey at
-- registration ("wo stehst du bei diesen Themen?"), so the feed has an
-- initial lean before an account has liked/commented on anything - without
-- it, standard_feed()/dominant_perspective() have zero signal for a brand
-- new account and just fall back to the seed post's own perspective.
--
-- Same self-chosen-label philosophy as posts.political_label (see
-- 0003_political_label.sql/README "Politische Einordnung"): both columns
-- are answers the account explicitly picked in the registration form, never
-- inferred - and both stay nullable since the survey is skippable.
-- Real engagement (likes/comments) always overrides this once it exists,
-- see dominant_perspective()/dominant_political_label() callers in app.py.

alter table profiles add column if not exists onboarding_perspective text
  check (onboarding_perspective in ('pro', 'contra'));

alter table profiles add column if not exists onboarding_political_label text
  check (onboarding_political_label in ('links', 'mitte', 'rechts'));
