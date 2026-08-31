-- Living Evidence Synthesis — review backend.
-- Run this once in the Supabase SQL editor (SQL Editor -> New query -> paste -> Run).
--
-- Auth model: open sign-in (any authenticated user may review — no invite
-- roster, unlike the oasisresearchlab reference). Identity comes straight
-- from Supabase Auth (auth.uid() / auth.email()); no separate roster table.

create table if not exists node_reviews (
  id             uuid primary key default gen_random_uuid(),
  reviewer_id    uuid not null default auth.uid(),
  reviewer_email text not null default auth.email(),  -- denormalized for easy export
  node_id        text not null,          -- e.g. "CLM-014", "EVD-062"
  dimension      text not null default 'overall',
  -- ✓ correct · ✎ edit · ✎ edit-major · ✎ edit-minor · ✗ wrong · ⟳ missing · — n/a
  -- (node-spec.md vocabulary, extended 2026-08 to split "edit" by severity)
  verdict        text not null check (verdict in ('correct', 'edit', 'edit-major', 'edit-minor', 'wrong', 'missing', 'na')),
  proposed       text,                   -- the corrected value / proposed diff, if verdict starts with 'edit'
  note           text,
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
-- Open sign-in model: any authenticated user can read all reviews (needed
-- for the aggregate /review dashboard) and write/edit their OWN rows only.
-- The anon key ships in the client bundle; with RLS below, unauthenticated
-- requests are rejected outright — a session is required for any access.
alter table node_reviews enable row level security;

drop policy if exists auth_read_all on node_reviews;
create policy auth_read_all on node_reviews
  for select to authenticated using (true);

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

-- ── Migration (2026-08): split "edit" by severity ───────────────────────────
-- If node_reviews already exists from an earlier run of this file, the
-- `create table if not exists` above is a no-op and its CHECK constraint
-- won't pick up the new verdict values automatically — run this once against
-- the live database (Supabase SQL editor) to widen it:
--
--   alter table node_reviews drop constraint node_reviews_verdict_check;
--   alter table node_reviews add constraint node_reviews_verdict_check
--     check (verdict in ('correct', 'edit', 'edit-major', 'edit-minor', 'wrong', 'missing', 'na'));
--
-- (Postgres auto-names the constraint node_reviews_verdict_check for a table
-- created via this script; confirm the actual name first with
-- `select conname from pg_constraint where conrelid = 'node_reviews'::regclass;`
-- if it was created some other way.)
