-- Living Evidence Synthesis — review backend.
-- Run this once in the Supabase SQL editor (SQL Editor -> New query -> paste -> Run).
--
-- Auth model: open sign-in (any authenticated user may review — no invite
-- roster, unlike the oasisresearchlab reference). Identity comes straight
-- from Supabase Auth (auth.uid() / auth.email()); no separate roster table.

create table if not exists node_reviews (
  id             uuid primary key default gen_random_uuid(),
  reviewer_id    uuid not null default auth.uid(),
  display_name   text check (display_name is null or char_length(display_name) between 1 and 40),  -- optional, chosen by reviewer; email is never stored
  node_id        text not null check (node_id ~ '^(QUE|CLM|EVD|CVT|SRC|EP)-[0-9]{3,4}$'),  -- e.g. "CLM-014", "EVD-062"
  dimension      text not null default 'overall' check (char_length(dimension) between 1 and 40),
  -- ✓ correct · ✎ edit · ✎ edit-major · ✎ edit-minor · ✗ wrong · ⟳ missing · — n/a
  -- (node-spec.md vocabulary, extended 2026-08 to split "edit" by severity)
  verdict        text not null check (verdict in ('correct', 'edit', 'edit-major', 'edit-minor', 'wrong', 'missing', 'na')),
  proposed       text check (proposed is null or char_length(proposed) <= 2000),                   -- the corrected value / proposed diff, if verdict starts with 'edit'
  note           text check (note is null or char_length(note) <= 2000),
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

-- One row per (reviewer, node, dimension) — re-submitting updates the same row.
create unique index if not exists node_reviews_uniq
  on node_reviews (reviewer_id, node_id, dimension);

create index if not exists node_reviews_node_idx on node_reviews (node_id);

-- Keep updated_at current on edit.
create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists node_reviews_set_updated_at on node_reviews;
create trigger node_reviews_set_updated_at
  before update on node_reviews
  for each row execute function set_updated_at();

-- ── Row-level security ────────────────────────────────────────────────────
-- Open sign-in model. A user can read, write and delete only their OWN rows in
-- the table. Everyone else's reviews are visible only through the
-- node_reviews_public view below, which omits email and user id.
alter table node_reviews enable row level security;

drop policy if exists auth_read_all on node_reviews;
drop policy if exists auth_read_own on node_reviews;
create policy auth_read_own on node_reviews
  for select to authenticated using (reviewer_id = auth.uid());

drop policy if exists auth_write_own on node_reviews;
create policy auth_write_own on node_reviews
  for insert to authenticated
  with check (reviewer_id = auth.uid());

drop policy if exists auth_update_own on node_reviews;
create policy auth_update_own on node_reviews
  for update to authenticated
  using (reviewer_id = auth.uid())
  with check (reviewer_id = auth.uid());

drop policy if exists auth_delete_own on node_reviews;
create policy auth_delete_own on node_reviews
  for delete to authenticated
  using (reviewer_id = auth.uid());

-- Per-user rate limit: at most 60 distinct review rows written per hour.
create or replace function enforce_review_rate_limit()
returns trigger as $$
begin
  if (select count(*) from node_reviews
        where reviewer_id = new.reviewer_id
          and updated_at > now() - interval '1 hour'
          and id <> new.id) >= 60 then
    raise exception 'Review rate limit reached (60 per hour). Try again later.'
      using errcode = 'P0001';
  end if;
  return new;
end;
$$ language plpgsql;

drop trigger if exists node_reviews_rate_limit on node_reviews;
create trigger node_reviews_rate_limit
  before insert or update on node_reviews
  for each row execute function enforce_review_rate_limit();

-- Public view: what other signed-in users see. No email, no user id.
drop view if exists node_reviews_public;
create view node_reviews_public as
  select id, node_id, dimension, verdict, proposed, note,
         coalesce(display_name, 'Anonymous reviewer') as reviewer_name,
         (reviewer_id = auth.uid()) as is_mine,
         created_at, updated_at
  from node_reviews;
revoke all on node_reviews_public from anon, public;
grant select on node_reviews_public to authenticated;

-- Existing databases: do NOT re-run this file; run
-- supabase/migrations/2026-11-reviewer-privacy.sql instead (see MIGRATION.md).
