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
