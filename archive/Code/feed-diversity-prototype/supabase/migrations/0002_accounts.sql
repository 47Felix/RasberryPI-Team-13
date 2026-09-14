-- Feed-diversity prototype (Case 3): real accounts instead of anonymous
-- session cookies. Builds on 0001_init.sql. Run once via the Supabase SQL
-- Editor, or apply_schema.py (same approach as 0001).
--
-- Adds Supabase Auth-backed accounts: `profiles` mirrors auth.users with the
-- display name/handle/avatar shown in the feed, `posts.user_id`/`likes` /
-- new `comments` table all reference profiles(id) instead of auth.users(id)
-- directly - PostgREST can only embed relations it can see in the public
-- schema, and auth.users isn't exposed there.
--
-- Breaking change: likes were previously keyed on an anonymous Flask session
-- cookie (session_id). That can't be attributed to any account, so this
-- drops existing like rows and switches the composite key to (post_id,
-- user_id). Fine for workshop/demo data; re-liking after this migration
-- just requires being logged in.

create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null,
  handle text not null unique,
  avatar text not null default '🙂',
  created_at timestamptz not null default now()
);

alter table posts add column if not exists user_id uuid references profiles(id) on delete set null;

delete from likes;
alter table likes drop constraint if exists likes_pkey;
alter table likes drop column if exists session_id;
alter table likes add column if not exists user_id uuid references profiles(id) on delete cascade;
alter table likes add primary key (post_id, user_id);

create table if not exists comments (
  id uuid primary key default gen_random_uuid(),
  post_id uuid not null references posts(id) on delete cascade,
  user_id uuid not null references profiles(id) on delete cascade,
  content text not null,
  created_at timestamptz not null default now()
);

create index if not exists posts_user_idx on posts(user_id);
create index if not exists likes_user_idx on likes(user_id);
create index if not exists comments_post_idx on comments(post_id);
create index if not exists comments_user_idx on comments(user_id);

alter table profiles enable row level security;
alter table comments enable row level security;
-- No policies on either, same posture as 0001: only the Flask backend
-- (secret key, bypasses RLS) can read/write. Signup/login go through
-- Supabase Auth directly (GoTrue), not through these REST tables.
