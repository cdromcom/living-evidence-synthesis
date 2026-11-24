-- Reviewer privacy migration. Run by hand in the Supabase SQL editor (see MIGRATION.md).
-- Idempotent: safe to run twice.

-- 1. Optional short display name chosen by the reviewer.
alter table node_reviews add column if not exists display_name text;

-- 2. Remove the stored email. (Export it first if you want a record: see MIGRATION.md.)
alter table node_reviews drop column if exists reviewer_email;

-- 3. Constraints. NOT VALID enforces them on new/updated rows without failing on old rows.
alter table node_reviews drop constraint if exists node_reviews_node_id_format;
alter table node_reviews add constraint node_reviews_node_id_format
  check (node_id ~ '^(QUE|CLM|EVD|CVT|SRC|EP)-[0-9]{3,4}$') not valid;

alter table node_reviews drop constraint if exists node_reviews_note_len;
alter table node_reviews add constraint node_reviews_note_len
  check (note is null or char_length(note) <= 2000) not valid;

alter table node_reviews drop constraint if exists node_reviews_proposed_len;
alter table node_reviews add constraint node_reviews_proposed_len
  check (proposed is null or char_length(proposed) <= 2000) not valid;

alter table node_reviews drop constraint if exists node_reviews_dimension_len;
alter table node_reviews add constraint node_reviews_dimension_len
  check (char_length(dimension) between 1 and 40) not valid;

alter table node_reviews drop constraint if exists node_reviews_display_name_len;
alter table node_reviews add constraint node_reviews_display_name_len
  check (display_name is null or char_length(display_name) between 1 and 40) not valid;

-- (The verdict check already exists in schema.sql: node_reviews_verdict_check.)

-- 4. Per-user rate limit: at most 60 distinct review rows written per hour.
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

-- 5. Reads: the table is now readable only by its owner.
drop policy if exists auth_read_all on node_reviews;
drop policy if exists auth_read_own on node_reviews;
create policy auth_read_own on node_reviews
  for select to authenticated using (reviewer_id = auth.uid());
-- insert/update/delete-own policies from schema.sql stay as they are.

-- 6. Everyone else sees reviews through this view: no email, no user id.
--    It runs with the view owner's rights (so it can read all rows) but exposes
--    only the columns listed. is_mine lets a client spot its own row.
drop view if exists node_reviews_public;
create view node_reviews_public as
  select id, node_id, dimension, verdict, proposed, note,
         coalesce(display_name, 'Anonymous reviewer') as reviewer_name,
         (reviewer_id = auth.uid()) as is_mine,
         created_at, updated_at
  from node_reviews;

revoke all on node_reviews_public from anon, public;
grant select on node_reviews_public to authenticated;
