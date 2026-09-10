# Shared Household Chores — Homework Plan

## Goal

Build a simple web application for managing shared household chores in one household.

The app should make it easy to:
- see what needs to be done today;
- see overdue chores;
- notice when another household member may need help;
- take over overdue chores;
- manage recurring household tasks.

---

## MVP Scope

### Household

- The app supports exactly **one household**.
- Household members are represented by Django users.
- Users log in with **Django's built-in authentication**.
- Every household member has equal permissions inside the app.
- Any member can create, edit, delete, assign, complete, or take over chores.

### Chores

Each chore has:

- title;
- assignee;
- due date;
- recurrence;
- notes;
- category.

A chore is assigned to exactly **one person**.

No priority field is required.

Dates are date-only; there is no time-of-day scheduling.

### Recurrence

Supported recurrence:

- daily;
- weekly;
- monthly;
- custom interval, e.g. every 2 weeks.

When a recurring chore is completed, the app immediately creates the next occurrence based on the recurrence rule.

No background scheduler is required.

When editing a recurring chore, the user can choose:

- this occurrence only;
- this and all future occurrences.

When deleting a recurring chore, the user can choose:

- this occurrence only;
- this and all future occurrences.

### Shared Board

The home screen is a shared household board.

Chores are grouped by:

1. Overdue
2. Today
3. Upcoming

Each chore clearly shows its assignee.

The board supports:

- filtering by household member;
- simple text search by chore title.

There is no separate dashboard summary.

### Completing Chores

A user can mark a chore as completed.

Completion is final; there is no undo.

Completed chores disappear from the active board.

### Taking Over Overdue Chores

Any household member can take over an overdue chore.

Takeover:

- happens immediately;
- does not require approval;
- changes the assignee to the person taking over the chore.

### History

Provide a simple completed-chore history.

For each completed chore, store/display:

- chore title;
- person who completed it;
- completion date.

The history does not need to preserve the original assignee after a takeover.

### Categories

Provide several default categories.

Users can:

- create categories;
- delete categories.

Every chore must have exactly one category.

If a category is deleted while it is used by chores, the user must select a replacement category.

All affected chores are reassigned to the replacement category.

Categories are labels only; category filtering is out of scope.

### Django Admin

Enable Django Admin for development and maintenance.

It can be used to inspect and manage:

- users;
- chores;
- categories;
- recurrence-related records.

---

## Technology Stack

### Backend

- Python
- Django
- Django ORM
- Django built-in authentication
- Django Admin

### Frontend

- Django Templates
- HTMX
- Bootstrap
- Minimal custom JavaScript only where necessary

There is no separate SPA frontend.

### Database

- SQLite

### Local Development

- Docker
- Docker Compose

The application only needs to run locally.

Example target command:

```bash
docker compose up
```

---

## Suggested Django Models

### User

Use Django's built-in `User` model for authentication.

### Category

Possible fields:

- `id`
- `name`
- `created_at`

### Chore

Possible fields:

- `id`
- `title`
- `notes`
- `assignee`
- `category`
- `due_date`
- `status`
- `recurrence_type`
- `recurrence_interval`
- `recurrence_series_id`
- `created_at`
- `completed_at`
- `completed_by`

Possible status values:

- active
- completed

`recurrence_series_id` can connect occurrences belonging to the same recurring chore series.

---

## Main User Flows

### Create Chore

1. Open chore form.
2. Enter title.
3. Select assignee.
4. Select due date.
5. Select category.
6. Add optional notes.
7. Configure recurrence if needed.
8. Save.

### View Household Board

1. Log in.
2. See Overdue, Today, and Upcoming sections.
3. Optionally filter by household member.
4. Optionally search by chore title.

### Complete Chore

1. Click Complete.
2. Chore is moved to history.
3. If recurring, the next occurrence is created immediately.

### Take Over Chore

1. Find an overdue chore assigned to another member.
2. Click Take Over.
3. Assignee changes immediately to the logged-in user.

### Edit Recurring Chore

1. Click Edit.
2. Change the chore.
3. Choose:
   - this occurrence only;
   - this and future occurrences.
4. Save.

### Delete Recurring Chore

1. Click Delete.
2. Choose:
   - this occurrence only;
   - this and future occurrences.
3. Confirm deletion.

### Delete Category

1. Select a category to delete.
2. If it is unused, delete it.
3. If it is used, select a replacement category.
4. Reassign affected chores.
5. Delete the old category.

---

## Out of Scope

The homework does **not** include:

- multiple households;
- invitation links or email invitations;
- smart chore assignment;
- automatic workload balancing;
- chore rotation;
- multiple assignees per chore;
- notifications or reminders;
- email;
- push notifications;
- priority levels;
- chore time-of-day;
- category filtering;
- dashboard analytics;
- undo completion;
- approval workflow for taking over chores;
- background scheduling with Celery;
- REST API;
- Django REST Framework;
- React, Vue, or another SPA framework;
- automated tests beyond the three core authentication scenarios (protected-page redirects, successful login, and logout);
- production deployment.

---

## Definition of Done

The homework is complete when:

- users can log in;
- users can create, edit, and delete chores;
- chores can be assigned to one household member;
- chores can have required categories;
- recurring chores generate their next occurrence after completion;
- the board shows Overdue, Today, and Upcoming chores;
- users can filter by member and search by title;
- overdue chores can be taken over;
- completed chores appear in simple history;
- categories can be created and safely deleted with replacement;
- Django Admin works;
- the complete application runs locally with Docker Compose.
