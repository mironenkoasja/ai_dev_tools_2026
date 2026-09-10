# Shared Household Chores — Backlog

Based on [_docs/plan.md](_docs/plan.md). Work in the existing Django `config` project and `core` app, in the order below. Django installation, the initial project/app scaffold, and task 1 are complete. Tasks 2–7 remain to be built.

## 1. Add login and the shared page layout

- [x] Add Django login/logout views and templates; require login for all household pages and actions.
- [x] Create a Bootstrap base template with navigation to the board, history, and categories. Include HTMX for incremental page updates.
- [x] Use built-in Django users as household members, with equal permissions in the application. Manage users through Django Admin.

Acceptance: A logged-out visitor is redirected to login. Any logged-in member can access household features; staff access remains required for Django Admin.

Verified with Django system checks and a temporary request-client walkthrough covering anonymous redirects, invalid and valid login, safe return URLs, CSRF protection, POST-only logout, member access, and staff-only Admin. Board, History, and Categories currently provide protected placeholders; HTMX is loaded for subsequent feature tasks.

## 2. Define the data model and configure Admin

- [ ] Add Category, Chore, and recurrence-series records with migrations and several default categories.
- [ ] Require a title, exactly one assignee, one category, and a date-only due date. Support optional notes, completion status, completion date, and completing user.
- [ ] Represent non-recurring chores and daily, weekly, monthly, and custom recurrence using a positive interval and unit.
- [ ] Register chores, categories, and recurrence records in Django Admin.

Acceptance: Migrations succeed on SQLite; Admin can manage all required records; invalid recurrence intervals and missing required fields are rejected.

## 3. Build chore creation, editing, and deletion

- [ ] Add Django forms and templates for creating and editing chores, including assignee, category, and recurrence inputs.
- [ ] Add deletion confirmation and allow any household member to manage any active chore.
- [ ] Use CSRF-protected POST requests for changes.

Acceptance: Members can create, update, assign, and delete a non-recurring chore. Invalid submissions show useful field errors. Recurring edit/delete scope is completed in task 5.

## 4. Build the shared board and overdue takeover

- [ ] Group active chores into Overdue, Today, and Upcoming using the local date; display assignee, category, and due date.
- [ ] Add member filtering and title search that work together, with useful empty states.
- [ ] Let members immediately take over overdue chores, assigning the selected occurrence to the logged-in user without approval. Validate eligibility on the server.
- [ ] Use HTMX to refresh affected board content after actions.

Acceptance: Grouping handles date boundaries correctly; completed chores are absent; search and filtering combine correctly; a takeover changes the assignee immediately and is unavailable for today's, upcoming, or completed chores.

## 5. Implement recurrence and completion

- [ ] Record the completing user and completion date, and make completion final.
- [ ] When a recurring chore is completed, create its next occurrence immediately in the same database transaction. Prevent repeated submissions from creating duplicates.
- [ ] Support editing or deleting either this occurrence only or this and all future occurrences, preserving completed history.
- [ ] Ensure future-scope changes also affect occurrences that have not yet been generated. Deleting one occurrence must leave the series able to continue without a background scheduler.

Acceptance: Each supported recurrence produces the expected next date; completion cannot be undone; one-occurrence changes preserve the series defaults; future-scope changes update or stop the remaining series.

Implementation decisions to settle before this task: Calculate the next due date from the previous due date or completion date; define catch-up behavior for overdue repeats; define monthly behavior for dates such as January 31; decide whether takeover changes only the current occurrence or future assignments. Suggested defaults: previous due date, one next occurrence per completion, clamp to the month's last day while retaining the original day for later months, and takeover of the current occurrence only.

## 6. Add completed-chore history and category management

- [ ] Show completed chores with title, completing member, and completion date, newest first.
- [ ] Let members create and delete categories.
- [ ] Require a replacement when deleting a category used by chores; reassign affected chores and recurrence defaults atomically before deletion.

Acceptance: History shows who completed the chore even after takeover. An unused category can be deleted directly; a used category cannot be deleted without a valid replacement, and no chore is left without a category. Category filtering is excluded.

## 7. Package local development and manually verify the MVP

- [ ] Add a Dockerfile, Docker Compose configuration, and `.dockerignore`; persist SQLite data in a local volume.
- [ ] Document `docker compose up`, migration setup, and creation of an admin account and household users in README.md.
- [ ] Manually walk through login, CRUD, board grouping, combined filters, takeover, all recurrence rules and scopes, completion/history, category replacement, and Admin using two members.
- [ ] Verify restart persistence and run Django's system checks.

Acceptance: A fresh checkout starts locally using the documented Docker Compose workflow; the plan's Definition of Done passes a manual walkthrough.

## Scope boundaries

One household only. Use Django Templates, HTMX, Bootstrap, SQLite, and minimal custom JavaScript. Automated test coverage is limited to three core authentication scenarios: protected-page redirects, successful login with a return URL, and logout ending access. Keep background scheduling, notifications, APIs, SPA frameworks, analytics, and production deployment out of this homework, as specified in the plan.
