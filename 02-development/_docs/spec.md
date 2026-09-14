# FairShare — Expense Splitter Specification

## 1. Goal

**FairShare** is a simple web application for splitting a single shared expense between several people.

A registered user can create an expense, choose who paid, add participants, split the expense equally or by custom amounts, see who owes whom, and save the result to their personal history.

The application is intended to run locally.

---

## 2. Technology Stack

- Python
- Django
- Bootstrap
- SQLite
- Django built-in authentication
- Django test framework

No Docker and no production deployment are required.

---

## 3. Core Features

### 3.1 User Authentication

Users can:

- Register with username and password
- Log in
- Log out
- View only their own saved expenses

Password reset and email verification are out of scope.

---

### 3.2 Dashboard

After login, the user sees a small dashboard containing:

- A clear **Create Expense** button
- The 5 most recent saved expenses
- A link to the full expense history

No aggregate statistics are required.

---

### 3.3 Create Expense

A user can create one shared expense.

Each expense contains:

- Title
- Total amount
- Date
- Optional note
- Payer
- Participants
- Split type

Currency is always EUR.

Participants do not need application accounts. They are stored as names.

The payer must be one of the participants.

Participants are added dynamically using an **Add person** action.

---

## 4. Split Types

### 4.1 Equal Split

The total amount is divided equally between all participants, including the payer.

Example:

- Total: €90
- Participants: Anna, Bob, Chris
- Payer: Anna

Each participant's share is €30.

Result:

- Bob owes Anna €30
- Chris owes Anna €30
- Anna owes nothing because she already paid the full expense

---

### 4.2 Custom Split

The user can enter an exact amount for each participant.

Example:

- Total: €100
- Anna: €50
- Bob: €30
- Chris: €20

The custom amounts must add up exactly to the total expense amount.

If they do not, the expense must not be saved and the user must see a validation error.

---

## 5. Result Page

After successfully creating an expense, the user is taken directly to a result page.

The result page shows:

- Expense title
- Date
- Optional note
- Total amount
- Payer
- Each participant
- Each participant's share
- Who owes whom
- Amount owed by each person

The result must be easy to verify visually.

---

## 6. Expense History

Users can view a full history of their own saved expenses.

The history page should show at least:

- Title
- Date
- Total amount
- Payer
- Link to the detailed result

Users can:

- View an expense
- Delete an expense

Users cannot edit an existing expense.

If a saved split is wrong, it must be deleted and recreated.

No CSV export or printable export is required.

---

## 7. Data Model

A reasonable Django model structure is:

### Expense

Fields:

- `id`
- `owner` — ForeignKey to Django User
- `title`
- `total_amount`
- `date`
- `note` — optional
- `split_type` — equal or custom
- `created_at`

### Participant

Fields:

- `id`
- `expense` — ForeignKey to Expense
- `name`
- `share_amount`
- `is_payer`

Alternative model structures are acceptable if they support the same behavior.

---

## 8. Business Rules

The application must enforce the following rules:

1. An expense must have at least 2 participants.
2. Participant names cannot be blank.
3. The payer must be one of the participants.
4. There must be exactly one payer.
5. The total amount must be greater than 0.
6. Participant shares must not be negative.
7. For equal split, shares are calculated automatically.
8. For custom split, participant shares must sum exactly to the total amount.
9. The payer is included in the split.
10. Only the expense owner can view or delete the expense.
11. Users must be authenticated to access expense functionality.

Money calculations should use decimal values rather than floating-point numbers.

---

## 9. Main Pages

The application should contain these pages:

### Public

- Register
- Login

### Authenticated

- Dashboard
- Create Expense
- Expense Result / Detail
- Expense History
- Delete Expense confirmation

---

## 10. Main User Flow

1. User registers or logs in.
2. User opens the dashboard.
3. User clicks **Create Expense**.
4. User enters:
   - title
   - total amount
   - date
   - optional note
5. User adds participant names.
6. User selects one participant as payer.
7. User chooses:
   - Equal split
   - Custom split
8. If custom split is selected, user enters each person's amount.
9. Application validates the input.
10. Expense is saved.
11. User is redirected to the result page.
12. The result page shows the complete split and debts.
13. The expense also appears in the user's history.

---

## 11. UI Requirements

Use Bootstrap for simple styling.

The UI should prioritize clarity over visual complexity.

Important UI elements:

- Clear navigation
- Create Expense button
- Dynamic Add Person control
- Clear payer selection
- Equal / Custom split selection
- Validation messages near invalid fields
- Easy-to-read result breakdown
- Delete confirmation before removing an expense

No advanced JavaScript framework is required.

Small amounts of JavaScript may be used for dynamically adding participant fields.

---

## 12. Tests

Automated tests are required.

### Model / Business Logic Tests

Test:

- Equal split calculation
- Custom split calculation
- Custom amounts summing correctly
- Rejection when custom amounts do not equal total
- Payer included in split
- Invalid zero or negative total
- Invalid participant data

### Authentication Tests

Test:

- Registration
- Login
- Logout
- Unauthenticated users cannot access private pages

### Permission Tests

Test:

- User can view their own expense
- User cannot view another user's expense
- User can delete their own expense
- User cannot delete another user's expense

### View / Flow Tests

Test:

- Dashboard loads correctly
- Dashboard shows only the latest 5 expenses
- Expense creation works
- Valid expense redirects to result page
- Invalid expense shows validation errors
- Expense appears in history after creation
- Expense deletion works

---

## 13. Out of Scope

The following features are intentionally excluded:

- Multiple payers
- Multiple expenses inside one trip or group
- Recurring expenses
- Registered participants
- Shared groups
- Expense editing
- Multiple currencies
- Currency conversion
- Categories
- Dashboard statistics
- CSV export
- PDF export
- Email notifications
- Password reset
- Email verification
- Social login
- Docker
- Cloud deployment
- Mobile application

---

## 14. Definition of Done

The homework is complete when:

- A user can register and log in.
- A logged-in user can create a one-time expense.
- Participants can be added dynamically.
- One participant can be selected as payer.
- Equal split works correctly.
- Custom exact-amount split works correctly.
- Invalid custom totals are rejected.
- The result page clearly shows shares and debts.
- Expenses are saved to personal history.
- The dashboard shows the 5 most recent expenses.
- Users can view and delete their own expenses.
- Users cannot access another user's expenses.
- Automated tests cover the main calculations, views, authentication, and permissions.
- The application runs locally using Django and SQLite.

---

## 15. Backend Implementation Specification

This section turns the frontend mock contract into the backend requirements for the Django implementation. The backend is the source of truth for authentication, persistence, validation, permissions, split calculations, and expense ownership.

### 15.1 Backend architecture

Use a small Django project with the following responsibilities:

- Django built-in `User` model for authentication.
- An `expenses` (or equivalent) Django app for expense models, forms/services, views, URLs, and tests.
- SQLite for local persistence.
- Django sessions for login state.
- Django templates/views or JSON endpoints are both acceptable, but the API contract in section 16 must be supported if the existing frontend is retained as the client.
- Business rules and money calculations must live in a reusable service/domain layer, not only in JavaScript or templates.

The backend must never trust totals, participant shares, payer flags, owner IDs, or permissions supplied by the browser.

### 15.2 Persistence model

#### Expense

Recommended fields:

- `id` — AutoField or UUID primary key.
- `owner` — `ForeignKey(User, on_delete=CASCADE, related_name="expenses")`.
- `title` — non-empty `CharField`, maximum length 200.
- `total_amount` — `DecimalField(max_digits=12, decimal_places=2)`; must be greater than zero.
- `date` — `DateField`.
- `note` — optional `TextField` or `CharField`; blank is allowed.
- `split_type` — choices `equal` and `custom`.
- `created_at` — `DateTimeField(auto_now_add=True)`.

Recommended database ordering: newest `created_at` first, then newest `date` first.

#### Participant

- `id` — AutoField or UUID primary key.
- `expense` — `ForeignKey(Expense, on_delete=CASCADE, related_name="participants")`.
- `name` — non-empty `CharField`, maximum length 100.
- `share_amount` — `DecimalField(max_digits=12, decimal_places=2)`; must not be negative.
- `is_payer` — `BooleanField(default=False)`.
- Preserve participant input order with `position` (`PositiveIntegerField`) or an equivalent ordering mechanism.

Database constraints should enforce non-negative `total_amount` and `share_amount` where supported. Application/service validation remains required because cross-row rules cannot be fully expressed with simple field constraints.

The participant collection must be deleted automatically when its expense is deleted. Deleting a user must delete that user's expenses through the configured foreign-key behavior.

### 15.3 Split calculation service

Create a testable service such as `calculate_expense_split(total_amount, participants, payer_index, split_type)`.

The service must:

1. Convert incoming values to `Decimal`, never binary floating-point values.
2. Quantize money to two decimal places using a documented rounding mode.
3. For an equal split, divide the total in cents and assign any remainder deterministically to the final participant in input order. The resulting shares must sum exactly to the total.
4. For a custom split, preserve the submitted participant amounts after Decimal normalization and reject the request unless their sum equals the total exactly to two decimal places.
5. Return exactly one payer and set the payer flag from the server-side payer index/name validation.
6. Return participant shares suitable for persistence and result rendering.

The service must not calculate debts by using floating-point subtraction. For the current single-payer product, each non-payer with a positive share owes that share to the payer; the payer's owed amount is zero. A separate debt table is not required.

### 15.4 Server-side validation

Expense creation must reject the request with field-level errors when:

- The user is unauthenticated.
- `title` is blank or exceeds its maximum length.
- `date` is missing or invalid.
- `total_amount` is missing, malformed, zero, negative, or has more than two decimal places.
- Fewer than two participants are submitted.
- Any participant name is blank, whitespace-only, or too long.
- Participant names are duplicated after normalization, unless duplicate names are explicitly supported by a later product decision.
- A participant share is missing, malformed, negative, or has more than two decimal places.
- The payer is not one of the submitted participants.
- There is not exactly one payer.
- The split type is not `equal` or `custom`.
- Custom shares do not add up exactly to the total.
- Equal-split client-provided shares do not match the server-calculated result; the server should ignore/recalculate them rather than trusting them.

Validation errors should be returned close to the relevant field and also include a non-field error for cross-field failures such as a mismatched custom total.

### 15.5 Authentication and sessions

#### Registration

`POST /api/auth/register/`

Request:

```json
{
  "username": "maya",
  "password": "secret-password",
  "name": "Maya Chen"
}
```

Behavior:

- Validate required fields and Django password rules.
- Reject duplicate usernames with HTTP 400.
- Create the user with a hashed password; never store the raw password.
- Log the new user in through the Django session.
- Return the authenticated user summary.

#### Login

`POST /api/auth/login/`

Request:

```json
{
  "username": "maya",
  "password": "secret-password"
}
```

On success, establish a Django session and return the user summary. Invalid credentials must return HTTP 400 or 401 without revealing whether the username or password was wrong.

#### Current session

`GET /api/auth/me/`

Return the current user summary when authenticated. Return HTTP 401 when there is no authenticated session.

#### Logout

`POST /api/auth/logout/`

Log out the current user and flush/invalidate the session. Return HTTP 204 or a small success response.

User summary shape:

```json
{
  "username": "maya",
  "name": "Maya Chen"
}
```

All state-changing session requests must use Django CSRF protection. The frontend API adapter must send credentials/cookies as required by the chosen deployment setup.

### 15.6 Expense API contract

All expense endpoints require authentication. The backend must derive the owner from `request.user`; clients must not provide an owner ID.

#### List expenses

`GET /api/expenses/`

Return only the authenticated user's expenses, ordered newest first. The dashboard can use `?limit=5`; the history page uses the unbounded list for this small local application.

Response:

```json
[
  {
    "id": "expense-id",
    "title": "Weekend cabin",
    "total": "240.00",
    "date": "2026-09-12",
    "note": "Groceries and firewood",
    "splitType": "equal",
    "payer": "Maya",
    "participants": [
      {"name": "Maya", "share": "80.00", "isPayer": true},
      {"name": "Jon", "share": "80.00", "isPayer": false}
    ],
    "createdAt": "2026-09-12T10:00:00Z"
  }
]
```

The wire format above mirrors the current `frontend/api.js` mock. Django model field names may remain `total_amount` and `share_amount`; serialization should map them to `total` and `share` until the frontend adapter is intentionally changed.

#### Get one expense

`GET /api/expenses/<id>/`

Return the complete expense detail, including all participants and calculated debt information if the backend chooses to include it. A missing expense and an expense belonging to another user must both return HTTP 404 to avoid leaking its existence.

#### Create an expense

`POST /api/expenses/`

Request:

```json
{
  "title": "Dinner at Luigi's",
  "total": "100.00",
  "date": "2026-09-14",
  "note": "Optional context",
  "splitType": "custom",
  "payer": "Anna",
  "participants": [
    {"name": "Anna", "share": "50.00"},
    {"name": "Bob", "share": "30.00"},
    {"name": "Chris", "share": "20.00"}
  ]
}
```

The backend must validate, calculate/recalculate, and save the expense and all participants inside one database transaction. If any validation or persistence step fails, no partial expense or participant rows may remain. On success return HTTP 201 with the complete result representation.

The payer may be represented by the `payer` name in the frontend contract, but the backend must validate that it matches exactly one submitted participant after the agreed normalization rules. The final stored `is_payer` value is assigned by the backend.

#### Delete an expense

`DELETE /api/expenses/<id>/`

Delete only when the authenticated user owns the expense. Return HTTP 204 on success. Return HTTP 404 for another user's expense or a nonexistent ID. There is no update endpoint: editing an existing expense is intentionally unsupported.

### 15.7 Error response format

Use a consistent JSON shape for API validation errors:

```json
{
  "detail": "Please correct the highlighted fields.",
  "errors": {
    "title": ["This field is required."],
    "participants": ["At least two participants are required."],
    "non_field_errors": ["Custom shares must add up to €100.00."]
  }
}
```

Recommended status codes:

- `201 Created` — successful registration or expense creation.
- `204 No Content` — successful logout or expense deletion.
- `400 Bad Request` — invalid input or credentials.
- `401 Unauthorized` — unauthenticated request.
- `403 Forbidden` — authenticated request blocked by CSRF or other access policy.
- `404 Not Found` — missing resource or resource owned by another user.

### 15.8 URL/view requirements

The backend must provide equivalent server routes if the frontend is server-rendered, or the API routes above if the existing SPA is retained:

- Public: register and login.
- Authenticated: dashboard, create expense, expense result/detail, history, delete confirmation.
- A private route must redirect to login for an HTML client or return HTTP 401 for an API client.
- Detail and delete queries must filter by `owner=request.user` before accessing the object.

### 15.9 Frontend integration changes

When the backend is ready, replace the localStorage implementation in `frontend/api.js` only. Keep the public methods and their async behavior stable:

- `register({ username, password, name })`
- `login({ username, password })`
- `logout()`
- `currentUser()`
- `listExpenses()`
- `getExpense(id)`
- `createExpense(expense)`
- `deleteExpense(id)`

The adapter should translate backend snake_case fields to the current frontend shape, handle HTTP errors using the documented `errors` object, and include session cookies/CSRF tokens. No view should call `fetch` directly; all backend calls remain centralized in `api.js`.

### 15.10 Backend test requirements

In addition to the tests in section 12, backend tests must verify:

- Passwords are hashed and are never returned in API responses.
- Duplicate usernames are rejected.
- Session login, current-user lookup, and logout work.
- Unauthenticated API requests return 401.
- Every expense query is owner-scoped.
- Another user cannot retrieve or delete an expense by guessing its ID.
- Create is atomic: invalid participant data cannot leave an `Expense` row behind.
- Equal-split rounding always produces a two-decimal total equal to the original total.
- Decimal and string amounts are accepted consistently, while invalid precision is rejected.
- The dashboard limit returns at most the five newest expenses.
- Deleting an expense deletes its participants.
