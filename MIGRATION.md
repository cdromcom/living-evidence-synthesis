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
   - adds `display_name` (optional, 1 to 40 characters) and drops `reviewer_email`;
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
   and writes `display_name`. Deploying the code before the SQL breaks the review panel
   (the view does not exist yet); running the SQL before the code makes the old site fail
   to submit reviews (it still sends `reviewer_email`). Do steps 2 and 3 close together.
4. **Check** while signed in as a normal user: `select * from node_reviews` returns only your
   own rows, and `select * from node_reviews_public` returns everyone's without email.

Fresh installs: `supabase/schema.sql` already contains the final design; do not run the
migration on top of it.

To change the rate limit, edit the `60` in `enforce_review_rate_limit()`.

## Decision for JP

Display names are free text chosen by the reviewer. If you want accountability among
reviewers (for example real names), say so and the "Anonymous reviewer" fallback can go.
