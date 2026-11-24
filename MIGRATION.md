# Supabase migration: reviewer privacy

This change stops signed-in reviewers from seeing each other's email addresses.
Nothing here has been applied. JP runs it by hand in the Supabase SQL editor.

## Order of steps

1. **Optional backup of emails.** The migration drops `node_reviews.reviewer_email`.
   If you want a record of who wrote which review, run this first and save the result
   (the `auth.users` table still holds the emails afterwards):
   `select id, reviewer_id, reviewer_email, node_id, verdict, updated_at from node_reviews;`
2. **Run the migration.** Paste `supabase/migrations/2026-11-reviewer-privacy.sql` into
   SQL Editor, New query, Run. It is safe to run twice. It:
   - drops `reviewer_email`;
   - adds a `reviewer_aliases` table, a trigger, and the function `assign_reviewer_alias`: each reviewer gets one random,
     unique galaxy name (166 names; once all are used, "Name II", "Name III", and so on) at their first review,
     kept for good. The name is enforced unique by a database constraint. Existing reviewers are given names by
     the migration. Clients cannot read the alias table directly;
   - adds checks: `node_id` format (e.g. `EVD-062`), note and proposed at most 2000
     characters, dimension length. They apply to new and edited rows; old rows are not
     re-checked (`not valid`). Once you are happy, `alter table node_reviews validate
     constraint <name>;` checks old rows too. The verdict check already exists;
   - adds a trigger limiting each user to 60 distinct review rows written per hour
     (re-saving the same row does not count against others, so it limits breadth, not edits);
   - replaces the `auth_read_all` policy with `auth_read_own`, so the table itself is
     readable only by the row owner (owners can still insert, update and delete their own);
   - creates the view `node_reviews_public` (no email, no user id, with an `is_mine` flag)
     for everyone else.
3. **Deploy this branch's code** (after step 2). The site now reads `node_reviews_public`
   and no longer sends a name. Deploying the code before the SQL breaks the review panel
   (the view does not exist yet); running the SQL before the code makes the old site fail
   to submit reviews (it still sends `reviewer_email`). Do steps 2 and 3 close together.
4. **Check** while signed in as a normal user: `select * from node_reviews` returns only your
   own rows, and `select * from node_reviews_public` returns everyone's without email.

Fresh installs: `supabase/schema.sql` already contains the final design; do not run the
migration on top of it.

To change the rate limit, edit the `60` in `enforce_review_rate_limit()`.

To see who is behind a galaxy name (for moderation), run as the project owner in SQL Editor:
`select a.alias, u.email from reviewer_aliases a join auth.users u on u.id = a.reviewer_id;`
