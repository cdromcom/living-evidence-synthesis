-- Creates only what the app needs to list reviews: the galaxy-name aliases and the
-- node_reviews_public view. Unlike 2026-11-reviewer-privacy.sql it drops nothing
-- (no email or display_name columns, no policy changes), so it is safe to run now
-- in the Supabase SQL editor, and safe to run twice. Run the full privacy
-- migration later, after exporting emails (see MIGRATION.md).

-- 6. Galaxy-name aliases (unique, assigned once, stable).
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

-- Give every existing reviewer an alias now, so the view shows their old reviews.
select assign_reviewer_alias(reviewer_id) from (select distinct reviewer_id from node_reviews) t;

-- 7. Everyone else sees reviews through this view: no email, no user id.
--    It runs with the view owner's rights (so it can read all rows) but exposes
--    only the columns listed. is_mine lets a client spot its own row.
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
