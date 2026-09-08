-- Feed-diversity prototype (Case 3): normalized schema replacing the
-- posts-only draft from PR #87 (never applied). Run once via the Supabase
-- SQL Editor, or apply_schema.py (Management API over HTTPS, since direct
-- Postgres port 5432 isn't reachable from this sandbox's network).
--
-- RLS is enabled on every table with NO anon policies: all reads/writes go
-- through the Flask backend using the secret key (bypasses RLS), same
-- security posture as PR #87. Direct anon/publishable-key access is blocked
-- on purpose.

create table if not exists categories (
  id uuid primary key default gen_random_uuid(),
  name text not null unique
);

create table if not exists authors (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  handle text not null unique,
  avatar text
);

create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  author_id uuid references authors(id),
  category_id uuid references categories(id),
  title text not null,
  content text not null,
  perspective text not null check (perspective in ('pro', 'contra')),
  created_at timestamptz not null default now()
);

create table if not exists likes (
  post_id uuid references posts(id) on delete cascade,
  session_id text not null,
  created_at timestamptz not null default now(),
  primary key (post_id, session_id)
);

create index if not exists posts_category_idx on posts(category_id);
create index if not exists posts_author_idx on posts(author_id);
create index if not exists likes_post_idx on likes(post_id);

alter table categories enable row level security;
alter table authors enable row level security;
alter table posts enable row level security;
alter table likes enable row level security;

-- Seed data matching the existing static dataset (data/posts.json) and the
-- per-(topic, perspective) fictional accounts from app.py:AUTHOR_META, so
-- user-submitted posts plug into the same "feels like a real account"
-- design instead of introducing anonymous rows.
insert into categories (name) values
  ('klima'), ('verkehr'), ('wirtschaft'), ('digital')
on conflict (name) do nothing;

insert into authors (name, handle, avatar) values
  ('Klimaschutz Jetzt', '@klimajetzt', '🌱'),
  ('Energie Realistisch', '@energierealistisch', '⚡'),
  ('Mobilitätswende', '@mobilwende', '🚲'),
  ('Freie Fahrt', '@freiefahrt', '🚗'),
  ('Faire Löhne', '@fairelöhne', '🧾'),
  ('Mittelstand Stimme', '@mittelstandstimme', '🏭'),
  ('Digitale Rechte', '@digitalerechte', '🔒'),
  ('Tech Standort', '@techstandort', '🚀')
on conflict (handle) do nothing;
