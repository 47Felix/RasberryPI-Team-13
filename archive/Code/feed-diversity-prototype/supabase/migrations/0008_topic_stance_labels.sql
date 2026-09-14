-- Feed-diversity prototype (Case 3): move the per-topic pro/contra stance
-- phrases (e.g. migration/pro -> "more open, more admission and inclusion")
-- from the hardcoded TOPIC_STANCES dict in app.py into the categories
-- table, so they follow the same "lives in Supabase, editable without a
-- code change" pattern known_topics()/db.fetch_categories() already use for
-- the category list itself (see 0006_more_categories.sql). Felix asked for
-- this 2026-09-10 - the raw "pro"/"contra" labels shouldn't be user-facing
-- anywhere, only the concrete phrase, and a category added directly in
-- Supabase should get real phrasing instead of silently falling back to the
-- bare word.
--
-- pro_label/contra_label are nullable: a category without either (added via
-- Supabase without setting them, or one of the pre-existing rows before
-- this migration backfills them below) simply falls back to app.py's
-- TOPIC_STANCES entry if one exists, or the bare "pro"/"contra" word as the
-- last resort - same fallback chain known_topics() already has for
-- DEFAULT_TOPICS. Run once via the Supabase SQL Editor, or apply_schema.py.

alter table categories add column if not exists pro_label text;
alter table categories add column if not exists contra_label text;

update categories set
  pro_label = 'more climate protection, faster',
  contra_label = 'more weight on cost/affordability'
where name = 'climate';

update categories set
  pro_label = 'priority for bikes, transit and rail',
  contra_label = 'priority for cars / status quo'
where name = 'transport';

update categories set
  pro_label = 'more redistribution and worker protection',
  contra_label = 'priority for businesses and the market'
where name = 'economy';

update categories set
  pro_label = 'civil rights and privacy first',
  contra_label = 'fewer rules / more investigative powers'
where name = 'digital';

update categories set
  pro_label = 'more redistribution, longer shared schooling',
  contra_label = 'more achievement and tracking'
where name = 'education';

update categories set
  pro_label = 'solidarity-based, more state control',
  contra_label = 'more competition and personal contribution'
where name = 'health';

update categories set
  pro_label = 'more open, more admission and inclusion',
  contra_label = 'tighter limits and controls'
where name = 'migration';

update categories set
  pro_label = 'more rent regulation and social housing',
  contra_label = 'fewer rules, focus on new construction'
where name = 'housing';

update categories set
  pro_label = 'more presence and police powers',
  contra_label = 'prevention and civil liberties first'
where name = 'security';

update categories set
  pro_label = 'higher, more reliable benefits',
  contra_label = 'more personal responsibility and incentives'
where name = 'welfare';

update categories set
  pro_label = 'more shared EU authority',
  contra_label = 'more national control'
where name = 'europe';

update categories set
  pro_label = 'diplomacy and civilian means first',
  contra_label = 'deterrence and defense first'
where name = 'foreign_policy';
