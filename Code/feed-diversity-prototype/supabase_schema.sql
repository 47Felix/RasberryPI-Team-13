-- Table for user-submitted posts in the feed-diversity prototype (Case 3).
-- Run this once in the Supabase Dashboard -> SQL Editor (or via
-- apply_schema.py, see README). Row level security stays enabled with no
-- policies: only the Flask backend (using the secret key, which bypasses
-- RLS) can read/write, the publishable key alone has no access to this
-- table on purpose.

create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text not null,
  topic text not null,
  perspective text not null check (perspective in ('pro', 'contra')),
  created_at timestamptz not null default now()
);

alter table posts enable row level security;
