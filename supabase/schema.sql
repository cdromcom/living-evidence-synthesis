-- Living Evidence Synthesis — review backend.
-- Run this once in the Supabase SQL editor (SQL Editor -> New query -> paste -> Run).
--
-- Auth model: open sign-in (any authenticated user may review — no invite
-- roster, unlike the oasisresearchlab reference). Identity comes straight
-- from Supabase Auth (auth.uid() / auth.email()); no separate roster table.

create table if not exists node_reviews (
  id             uuid primary key default gen_random_uuid(),
  reviewer_id    uuid not null default auth.uid(),
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

-- ── Reviewer aliases ─────────────────────────────────────────────────────────
-- Each reviewer gets one random, unique galaxy name at their first review. It is
-- stored once and never changes. Table is not readable by clients at all; the
-- public view joins it as the view owner.
create table if not exists reviewer_aliases (
  reviewer_id uuid primary key,
  alias       text not null unique
);
alter table reviewer_aliases enable row level security;  -- no policies: clients cannot read or write

create or replace function to_roman(n int) returns text as $$
declare
  vals int[] := array[1000,900,500,400,100,90,50,40,10,9,5,4,1];
  syms text[] := array['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I'];
  out text := '';
  i int;
begin
  for i in 1..13 loop
    while n >= vals[i] loop
      out := out || syms[i];
      n := n - vals[i];
    end loop;
  end loop;
  return out;
end;
$$ language plpgsql immutable;

-- Returns the caller's alias, creating it on first use. Picks a random unused galaxy
-- name; when every name is taken, tries "Name II", then "Name III", and so on.
create or replace function assign_reviewer_alias(uid uuid) returns text as $$
declare
  galaxies text[] := array[
    'Andromeda',
    'Triangulum',
    'Sombrero',
    'Whirlpool',
    'Pinwheel',
    'Cartwheel',
    'Cigar',
    'Black Eye',
    'Sunflower',
    'Tadpole',
    'Antennae',
    'Sculptor',
    'Centaurus A',
    'Messier 87',
    'Milky Way',
    'Large Magellanic Cloud',
    'Small Magellanic Cloud',
    'Hoags Object',
    'Needle',
    'Condor',
    'Fireworks',
    'Butterfly',
    'Mice',
    'Medusa',
    'Sparkler',
    'Bode',
    'Comet',
    'Spindle',
    'Leo I',
    'Leo II',
    'Draco',
    'Ursa Minor',
    'Carina',
    'Fornax',
    'Sextans',
    'Phoenix',
    'Pegasus Dwarf',
    'Wolf-Lundmark-Melotte',
    'Barnards',
    'IC 1613',
    'NGC 1300',
    'NGC 1365',
    'NGC 2403',
    'NGC 253',
    'NGC 300',
    'NGC 4565',
    'NGC 4631',
    'NGC 6946',
    'NGC 7331',
    'NGC 891',
    'NGC 1097',
    'NGC 1512',
    'NGC 3628',
    'NGC 4414',
    'NGC 5033',
    'NGC 5907',
    'NGC 6744',
    'NGC 7793',
    'Messier 33',
    'Messier 51',
    'Messier 63',
    'Messier 64',
    'Messier 74',
    'Messier 77',
    'Messier 81',
    'Messier 82',
    'Messier 83',
    'Messier 87 Jet',
    'Messier 94',
    'Messier 100',
    'Messier 101',
    'Messier 104',
    'Messier 106',
    'Cosmos Redshift',
    'Circinus',
    'Dragonfly',
    'Eye of Sauron',
    'Blinking',
    'Hockey Stick',
    'Southern Pinwheel',
    'Silver Coin',
    'Sculptor Dwarf',
    'Coma Pinwheel',
    'Cats Eye',
    'Andromeda I',
    'Andromeda II',
    'Andromeda III',
    'Cygnus A',
    'Pictor A',
    'Hercules A',
    'Perseus A',
    'Virgo A',
    'Centaurus B',
    'Fornax A',
    'Bear Paw',
    'Cocoon',
    'Lindsay-Shapley Ring',
    'Arp 244',
    'Arp 273',
    'Arp 299',
    'Arp 220',
    'Zwicky 18',
    'Malin 1',
    'Stephans Quintet',
    'Seyferts Sextet',
    'Siamese Twins',
    'Question Mark',
    'Integral Sign',
    'Mayalls Object',
    'Hoag Ring',
    'Sagittarius Dwarf',
    'Canis Major Dwarf',
    'Bootes I',
    'Bootes II',
    'Hercules Dwarf',
    'Segue 1',
    'Willman 1',
    'Coma Berenices Dwarf',
    'Ursa Major I',
    'Ursa Major II',
    'Canes Venatici I',
    'Canes Venatici II',
    'Tucana',
    'Aquarius Dwarf',
    'Leo A',
    'Leo T',
    'Sagittarius Irregular',
    'Triangulum II',
    'Draco II',
    'Carina II',
    'Carina III',
    'Horologium II',
    'Phoenix II',
    'Tucana II',
    'Virgo I',
    'Pisces II',
    'Aquarius II',
    'Sextans II',
    'Maffei 1',
    'Maffei 2',
    'Dwingeloo 1',
    'Dwingeloo 2',
    'Messier 32',
    'Messier 49',
    'Messier 58',
    'Messier 59',
    'Messier 60',
    'Messier 61',
    'Messier 65',
    'Messier 66',
    'Messier 84',
    'Messier 85',
    'Messier 86',
    'Messier 88',
    'Messier 89',
    'Messier 90',
    'Messier 91',
    'Messier 95',
    'Messier 96',
    'Messier 98',
    'Messier 99',
    'Messier 102',
    'Messier 105',
    'Messier 108',
    'Messier 109',
    'Messier 110'
  ];
  existing text;
  candidate text;
  tier int := 1;
begin
  select alias into existing from reviewer_aliases where reviewer_id = uid;
  if existing is not null then return existing; end if;

  perform pg_advisory_xact_lock(hashtext('reviewer_alias_assign'));
  select alias into existing from reviewer_aliases where reviewer_id = uid;
  if existing is not null then return existing; end if;

  loop
    select g into candidate
      from unnest(galaxies) as g
      where not exists (
        select 1 from reviewer_aliases a
        where a.alias = case when tier = 1 then g else g || ' ' || to_roman(tier) end
      )
      order by random() limit 1;
    if candidate is not null then
      if tier > 1 then candidate := candidate || ' ' || to_roman(tier); end if;
      insert into reviewer_aliases (reviewer_id, alias) values (uid, candidate);
      return candidate;
    end if;
    tier := tier + 1;
  end loop;
end;
$$ language plpgsql security definer set search_path = public;
revoke all on function assign_reviewer_alias(uuid) from public, anon, authenticated;

create or replace function node_reviews_assign_alias() returns trigger as $$
begin
  perform assign_reviewer_alias(new.reviewer_id);
  return new;
end;
$$ language plpgsql security definer set search_path = public;

drop trigger if exists node_reviews_alias on node_reviews;
create trigger node_reviews_alias
  before insert on node_reviews
  for each row execute function node_reviews_assign_alias();

-- Public view: what other signed-in users see. No email, no user id.
drop view if exists node_reviews_public;
create view node_reviews_public as
  select r.id, r.node_id, r.dimension, r.verdict, r.proposed, r.note,
         a.alias as reviewer_name,
         (r.reviewer_id = auth.uid()) as is_mine,
         r.created_at, r.updated_at
  from node_reviews r
  join reviewer_aliases a on a.reviewer_id = r.reviewer_id;
revoke all on node_reviews_public from anon, public;
grant select on node_reviews_public to authenticated;

-- Existing databases: do NOT re-run this file; run
-- supabase/migrations/2026-11-reviewer-privacy.sql instead (see MIGRATION.md).
