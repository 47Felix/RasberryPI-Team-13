-- Feed-diversity prototype (Case 3): independent political self-label
-- ('left'/'center'/'right'), separate from the existing pro/contra
-- perspective per topic. Builds on 0001_init.sql/0002_accounts.sql. Run
-- once via the Supabase SQL Editor, or apply_schema.py (same approach as
-- 0001/0002).
--
-- This is a user-chosen label picked in the "new post" form, the same way
-- perspective already works - not an automatically detected one. See
-- README.md ("Political labeling") for why an automatic left/right
-- classifier was deliberately not attempted here.
--
-- Nullable on purpose: posts created before this migration have no value
-- (there is nothing to infer it from), and ranking.py already treats a
-- missing political_label as "no signal"/"differs from any bias" rather
-- than erroring.
--
-- Values are English ('left'/'center'/'right') since this column was never
-- applied to the real Supabase instance before the team's 2026-09-09
-- English-only decision (see NIGHTLY_TASK.md) - no rename migration needed,
-- unlike categories.name/authors below (see 0007_english_content.sql).

alter table posts add column if not exists political_label text
  check (political_label in ('left', 'center', 'right'));

create index if not exists posts_political_label_idx on posts(political_label);
