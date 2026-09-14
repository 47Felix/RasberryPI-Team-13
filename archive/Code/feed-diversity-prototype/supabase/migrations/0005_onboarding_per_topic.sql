-- Feed-diversity prototype (Case 3): the registration survey's perspective
-- answers were originally collapsed into one account-wide
-- onboarding_perspective (pro/contra) via a majority vote across all
-- topics - same flaw the team pointed out in the real engagement signal
-- (dominant_perspective() ignoring topic), just baked into onboarding too.
-- Replaces it with one answer per topic instead, matching
-- ranking.dominant_perspective_by_topic()'s {"transport": "pro", ...} shape,
-- so an account can start out "pro" on one topic and "contra" on another.
--
-- jsonb rather than one column per topic: KNOWN_TOPICS in app.py already
-- owns the canonical topic list and can grow without another migration.

alter table profiles drop column if exists onboarding_perspective;

alter table profiles add column if not exists onboarding_perspective_by_topic jsonb;
