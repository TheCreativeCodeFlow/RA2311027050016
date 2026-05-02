# Campus Notification Frontend Design

## Overview
Build a Create React App (TypeScript) frontend for a Campus Notification System. The UI uses Material UI (MUI) only, supports pagination and filtering, tracks viewed vs new notifications, and provides a Priority Inbox based on type weight plus recency. The app runs on http://localhost:3000 and integrates with the provided API using query params and a bearer token from `.env`.

## Goals
- Provide a clean, responsive UI for notifications and priority inbox.
- Support pagination, filtering, and viewed state persistence.
- Keep architecture modular and simple for extension.

## Non-Goals
- No Next.js, Storybook, Tailwind, or other UI toolchains.
- No backend changes or mock-only data.

## Architecture
- App located in `notification_app_fe/` (separate from backend).
- CRA TypeScript app with React Router for navigation.
- MUI components for layout, cards, filters, pagination, and feedback.

### Directory Layout
```
src/
├── components/
│   ├── NotificationCard.tsx
│   ├── NotificationList.tsx
│   ├── FilterBar.tsx
│   ├── PaginationControl.tsx
│
├── pages/
│   ├── AllNotifications.tsx
│   ├── PriorityInbox.tsx
│
├── services/
│   └── api.ts
│
├── hooks/
│   └── useNotifications.ts
│
├── state/
│   └── viewedStore.ts
│
├── styles/
│   └── global.css
│
└── App.tsx
```

## Data Model
- Notification fields: `id`, `type`, `timestamp` (string or number).
- Types: `placement`, `result`, `event`.

## API Integration
- Endpoint: `http://20.207.122.201/evaluation-service/notifications`.
- Authorization header: `Bearer ${REACT_APP_API_TOKEN}`.
- Query params: `page`, `limit`, `notification_type`.
- API service exposes `getNotifications({ page, limit, type })`.

## State Management
- React hooks only.
- Viewed state persisted in `localStorage` with a set of IDs.
- `viewedStore` provides `isViewed(id)`, `markViewed(id)` and `loadViewed()`.

## Pages
### All Notifications
- Fetch from API with pagination and filter.
- UI controls: type filter dropdown, pagination.
- Notification cards with viewed/new styling.
- Loading spinner, error alert, empty state messaging.

### Priority Inbox
- Fetch a larger page (configurable, default 100) once per filter change.
- Compute top N using memoized priority logic.
- N is selectable: 10, 15, 20.

## Priority Logic
- Type weights: placement=3, result=2, event=1.
- Recency: reference time = max timestamp in current dataset (seconds).
- Priority score: `(typeWeight * 1000) - (referenceTime - timestamp)`.
- Use memoization and partial selection to avoid full sorting on each render.

## UX & Responsiveness
- Responsive layout with `Container`, `Grid`, `useMediaQuery`.
- New notifications: bold title + subtle highlight.
- Viewed notifications: subdued color and normal weight.

## Error/Loading/Empty States
- `CircularProgress` on load.
- `Alert` on API error.
- Empty state text when list is empty.

## Testing & Verification
- Manual verification of routes, pagination, filters, viewed state persistence.
- Confirm API calls include query params and auth header.

## Environment
- `.env` sample:
```
REACT_APP_API_TOKEN=your_token_here
```

## Run
- `npm install`
- `npm start`
- App available at `http://localhost:3000`.
