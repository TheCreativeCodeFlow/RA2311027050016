# Campus Notification Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CRA TypeScript frontend that fetches notifications, supports pagination/filtering, tracks viewed state, and provides a priority inbox with MUI styling.

**Architecture:** A separate CRA app in `notification_app_fe/` using React Router for navigation. Data access is centralized in `services/api.ts`, UI is composed from small components, and viewed state persists via `state/viewedStore.ts`.

**Tech Stack:** React (CRA + TypeScript), React Router, MUI, Axios, localStorage.

---

## File Structure (planned)
- Create: `notification_app_fe/` (CRA app)
- Create: `notification_app_fe/src/components/NotificationCard.tsx`
- Create: `notification_app_fe/src/components/NotificationList.tsx`
- Create: `notification_app_fe/src/components/FilterBar.tsx`
- Create: `notification_app_fe/src/components/PaginationControl.tsx`
- Create: `notification_app_fe/src/pages/AllNotifications.tsx`
- Create: `notification_app_fe/src/pages/PriorityInbox.tsx`
- Create: `notification_app_fe/src/services/api.ts`
- Create: `notification_app_fe/src/hooks/useNotifications.ts`
- Create: `notification_app_fe/src/state/viewedStore.ts`
- Create: `notification_app_fe/src/utils/priority.ts`
- Create: `notification_app_fe/src/styles/global.css`
- Modify: `notification_app_fe/src/App.tsx`
- Modify: `notification_app_fe/src/index.tsx`
- Create: `notification_app_fe/.env.example`
- Create: `notification_app_fe/README.md`
- Tests: `notification_app_fe/src/state/viewedStore.test.ts`, `notification_app_fe/src/utils/priority.test.ts`

---

### Task 1: Scaffold CRA app and install dependencies

**Files:**
- Create: `notification_app_fe/`

- [ ] **Step 1: Create CRA TypeScript app**

Run:
```bash
npx create-react-app notification_app_fe --template typescript
```
Expected: CRA outputs project files under `notification_app_fe/`.

- [ ] **Step 2: Install dependencies**

Run:
```bash
cd notification_app_fe
npm install @mui/material @emotion/react @emotion/styled axios react-router-dom
```
Expected: packages installed with no errors.

- [ ] **Step 3: Commit**

```bash
git add notification_app_fe/package.json notification_app_fe/package-lock.json notification_app_fe/src

git commit -m "chore: scaffold notification_app_fe"
```

---

### Task 2: Global styles and app shell

**Files:**
- Create: `notification_app_fe/src/styles/global.css`
- Modify: `notification_app_fe/src/index.tsx`
- Modify: `notification_app_fe/src/App.tsx`

- [ ] **Step 1: Add global CSS**

```css
/* notification_app_fe/src/styles/global.css */
:root {
  color-scheme: light;
}

body {
  margin: 0;
  background: #f6f7fb;
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
```

- [ ] **Step 2: Wire global CSS in index**

```tsx
// notification_app_fe/src/index.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/global.css";
import App from "./App";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

- [ ] **Step 3: Create App shell with navigation**

```tsx
// notification_app_fe/src/App.tsx
import React from "react";
import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import {
  AppBar,
  Box,
  Container,
  Toolbar,
  Typography,
} from "@mui/material";
import AllNotifications from "./pages/AllNotifications";
import PriorityInbox from "./pages/PriorityInbox";

const linkStyle = {
  color: "inherit",
  textDecoration: "none",
  marginLeft: 16,
};

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppBar position="sticky" color="primary">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Campus Notifications
          </Typography>
          <NavLink to="/all" style={linkStyle}>
            All Notifications
          </NavLink>
          <NavLink to="/priority" style={linkStyle}>
            Priority Inbox
          </NavLink>
        </Toolbar>
      </AppBar>
      <Box sx={{ py: 3 }}>
        <Container maxWidth="lg">
          <Routes>
            <Route path="/" element={<AllNotifications />} />
            <Route path="/all" element={<AllNotifications />} />
            <Route path="/priority" element={<PriorityInbox />} />
          </Routes>
        </Container>
      </Box>
    </BrowserRouter>
  );
};

export default App;
```

- [ ] **Step 4: Commit**

```bash
git add notification_app_fe/src/styles/global.css notification_app_fe/src/index.tsx notification_app_fe/src/App.tsx

git commit -m "feat: add app shell and global styles"
```

---

### Task 3: API service and notification hook

**Files:**
- Create: `notification_app_fe/src/services/api.ts`
- Create: `notification_app_fe/src/hooks/useNotifications.ts`

- [ ] **Step 1: Add API client**

```ts
// notification_app_fe/src/services/api.ts
import axios from "axios";

export type NotificationType = "placement" | "result" | "event";

export interface NotificationItem {
  id: string;
  type: NotificationType;
  timestamp: string | number;
}

export interface NotificationResponse {
  items: NotificationItem[];
  total?: number;
}

const API_BASE = "http://20.207.122.201/evaluation-service/notifications";

export async function getNotifications(params: {
  page: number;
  limit: number;
  type?: string;
}): Promise<NotificationResponse> {
  const token = process.env.REACT_APP_API_TOKEN;
  const response = await axios.get(API_BASE, {
    headers: { Authorization: `Bearer ${token}` },
    params: {
      page: params.page,
      limit: params.limit,
      notification_type: params.type && params.type !== "all" ? params.type : undefined,
    },
  });

  const data = response.data;
  if (Array.isArray(data)) {
    return { items: data };
  }

  if (data && Array.isArray(data.notifications)) {
    return { items: data.notifications, total: data.total };
  }

  if (data && Array.isArray(data.items)) {
    return { items: data.items, total: data.total };
  }

  return { items: [] };
}
```

- [ ] **Step 2: Add data hook**

```ts
// notification_app_fe/src/hooks/useNotifications.ts
import { useEffect, useState } from "react";
import { getNotifications, NotificationItem } from "../services/api";

export function useNotifications(options: {
  page: number;
  limit: number;
  type: string;
}) {
  const [items, setItems] = useState<NotificationItem[]>([]);
  const [total, setTotal] = useState<number | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);

    getNotifications({ page: options.page, limit: options.limit, type: options.type })
      .then((result) => {
        if (!active) return;
        setItems(result.items);
        setTotal(result.total);
      })
      .catch((err) => {
        if (!active) return;
        setError(err?.message ?? "Failed to fetch notifications");
      })
      .finally(() => {
        if (!active) return;
        setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [options.page, options.limit, options.type]);

  return { items, total, loading, error };
}
```

- [ ] **Step 3: Commit**

```bash
git add notification_app_fe/src/services/api.ts notification_app_fe/src/hooks/useNotifications.ts

git commit -m "feat: add API service and notifications hook"
```

---

### Task 4: Viewed state store

**Files:**
- Create: `notification_app_fe/src/state/viewedStore.ts`
- Create: `notification_app_fe/src/state/viewedStore.test.ts`

- [ ] **Step 1: Implement viewed store**

```ts
// notification_app_fe/src/state/viewedStore.ts
const STORAGE_KEY = "viewed_notifications";

export function loadViewed(): Set<string> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return new Set();
    const list = JSON.parse(raw);
    if (!Array.isArray(list)) return new Set();
    return new Set(list.map(String));
  } catch {
    return new Set();
  }
}

export function isViewed(id: string): boolean {
  return loadViewed().has(id);
}

export function markViewed(id: string): void {
  const set = loadViewed();
  set.add(id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...set]));
}
```

- [ ] **Step 2: Write failing test**

```ts
// notification_app_fe/src/state/viewedStore.test.ts
import { loadViewed, markViewed } from "./viewedStore";

describe("viewedStore", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("stores and reloads viewed ids", () => {
    expect(loadViewed().has("a")).toBe(false);
    markViewed("a");
    expect(loadViewed().has("a")).toBe(true);
  });
});
```

- [ ] **Step 3: Run test to verify it passes**

Run:
```bash
npm test -- --watchAll=false viewedStore.test.ts
```
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add notification_app_fe/src/state/viewedStore.ts notification_app_fe/src/state/viewedStore.test.ts

git commit -m "feat: add viewed state persistence"
```

---

### Task 5: Priority calculation utility

**Files:**
- Create: `notification_app_fe/src/utils/priority.ts`
- Create: `notification_app_fe/src/utils/priority.test.ts`

- [ ] **Step 1: Add priority helper**

```ts
// notification_app_fe/src/utils/priority.ts
import { NotificationItem } from "../services/api";

const TYPE_WEIGHTS: Record<string, number> = {
  placement: 3,
  result: 2,
  event: 1,
};

function toSeconds(ts: string | number): number {
  if (typeof ts === "number") {
    return ts > 10_000_000_000 ? ts / 1000 : ts;
  }
  return new Date(ts).getTime() / 1000;
}

export function referenceTimeSeconds(items: NotificationItem[]): number {
  if (!items.length) return Date.now() / 1000;
  return Math.max(...items.map((item) => toSeconds(item.timestamp)));
}

export function priorityScore(item: NotificationItem, reference: number): number {
  const weight = TYPE_WEIGHTS[item.type] ?? 0;
  const diff = Math.max(0, reference - toSeconds(item.timestamp));
  return weight * 1000 - diff;
}

export function topNByPriority(items: NotificationItem[], n: number): NotificationItem[] {
  if (n <= 0) return [];
  const reference = referenceTimeSeconds(items);

  const scored = items.map((item) => ({
    item,
    score: priorityScore(item, reference),
  }));

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, n).map((entry) => entry.item);
}
```

- [ ] **Step 2: Write failing test**

```ts
// notification_app_fe/src/utils/priority.test.ts
import { topNByPriority } from "./priority";

const sample = [
  { id: "1", type: "event", timestamp: 1700000000 },
  { id: "2", type: "result", timestamp: 1700000000 },
  { id: "3", type: "placement", timestamp: 1700000000 },
];

describe("priority", () => {
  it("orders by type weight when timestamps equal", () => {
    const top = topNByPriority(sample, 2);
    expect(top.map((i) => i.id)).toEqual(["3", "2"]);
  });
});
```

- [ ] **Step 3: Run test to verify it passes**

Run:
```bash
npm test -- --watchAll=false priority.test.ts
```
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add notification_app_fe/src/utils/priority.ts notification_app_fe/src/utils/priority.test.ts

git commit -m "feat: add priority calculation utilities"
```

---

### Task 6: Shared UI components

**Files:**
- Create: `notification_app_fe/src/components/NotificationCard.tsx`
- Create: `notification_app_fe/src/components/NotificationList.tsx`
- Create: `notification_app_fe/src/components/FilterBar.tsx`
- Create: `notification_app_fe/src/components/PaginationControl.tsx`

- [ ] **Step 1: NotificationCard**

```tsx
// notification_app_fe/src/components/NotificationCard.tsx
import React from "react";
import { Card, CardContent, Chip, Typography } from "@mui/material";
import { NotificationItem } from "../services/api";

interface Props {
  item: NotificationItem;
  viewed: boolean;
  onClick: () => void;
}

const NotificationCard: React.FC<Props> = ({ item, viewed, onClick }) => {
  return (
    <Card
      onClick={onClick}
      sx={{
        cursor: "pointer",
        border: viewed ? "1px solid #e0e0e0" : "1px solid #1565c0",
        backgroundColor: viewed ? "#ffffff" : "#eaf2ff",
        transition: "transform 120ms ease",
        "&:hover": { transform: "translateY(-2px)" },
      }}
    >
      <CardContent>
        <Typography variant="h6" sx={{ fontWeight: viewed ? 400 : 700 }}>
          {item.type.toUpperCase()} Notification
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {new Date(item.timestamp).toLocaleString()}
        </Typography>
        <Chip
          label={item.type}
          size="small"
          color={item.type === "placement" ? "primary" : item.type === "result" ? "success" : "warning"}
          sx={{ mt: 1 }}
        />
      </CardContent>
    </Card>
  );
};

export default NotificationCard;
```

- [ ] **Step 2: NotificationList**

```tsx
// notification_app_fe/src/components/NotificationList.tsx
import React from "react";
import { Grid, Typography } from "@mui/material";
import { NotificationItem } from "../services/api";
import NotificationCard from "./NotificationCard";

interface Props {
  items: NotificationItem[];
  viewedIds: Set<string>;
  onItemClick: (id: string) => void;
}

const NotificationList: React.FC<Props> = ({ items, viewedIds, onItemClick }) => {
  if (!items.length) {
    return <Typography>No notifications found.</Typography>;
  }

  return (
    <Grid container spacing={2}>
      {items.map((item) => (
        <Grid item xs={12} sm={6} md={4} key={item.id}>
          <NotificationCard
            item={item}
            viewed={viewedIds.has(item.id)}
            onClick={() => onItemClick(item.id)}
          />
        </Grid>
      ))}
    </Grid>
  );
};

export default NotificationList;
```

- [ ] **Step 3: FilterBar**

```tsx
// notification_app_fe/src/components/FilterBar.tsx
import React from "react";
import { Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";

interface Props {
  type: string;
  onTypeChange: (value: string) => void;
  limit: number;
  onLimitChange: (value: number) => void;
}

const FilterBar: React.FC<Props> = ({ type, onTypeChange, limit, onLimitChange }) => {
  const handleType = (event: SelectChangeEvent) => onTypeChange(event.target.value);
  const handleLimit = (event: SelectChangeEvent) => onLimitChange(Number(event.target.value));

  return (
    <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mb: 2 }}>
      <FormControl size="small" sx={{ minWidth: 180 }}>
        <InputLabel id="type-label">Type</InputLabel>
        <Select labelId="type-label" value={type} label="Type" onChange={handleType}>
          <MenuItem value="all">All</MenuItem>
          <MenuItem value="placement">Placement</MenuItem>
          <MenuItem value="result">Result</MenuItem>
          <MenuItem value="event">Event</MenuItem>
        </Select>
      </FormControl>

      <FormControl size="small" sx={{ minWidth: 140 }}>
        <InputLabel id="limit-label">Per page</InputLabel>
        <Select labelId="limit-label" value={String(limit)} label="Per page" onChange={handleLimit}>
          <MenuItem value={10}>10</MenuItem>
          <MenuItem value={20}>20</MenuItem>
          <MenuItem value={30}>30</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
};

export default FilterBar;
```

- [ ] **Step 4: PaginationControl**

```tsx
// notification_app_fe/src/components/PaginationControl.tsx
import React from "react";
import { Box, Pagination } from "@mui/material";

interface Props {
  page: number;
  count: number;
  onChange: (page: number) => void;
}

const PaginationControl: React.FC<Props> = ({ page, count, onChange }) => {
  return (
    <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
      <Pagination page={page} count={count} onChange={(_, value) => onChange(value)} />
    </Box>
  );
};

export default PaginationControl;
```

- [ ] **Step 5: Commit**

```bash
git add notification_app_fe/src/components

git commit -m "feat: add shared notification UI components"
```

---

### Task 7: All Notifications page

**Files:**
- Create: `notification_app_fe/src/pages/AllNotifications.tsx`

- [ ] **Step 1: Implement page**

```tsx
// notification_app_fe/src/pages/AllNotifications.tsx
import React, { useMemo, useState } from "react";
import { Alert, CircularProgress, Typography } from "@mui/material";
import FilterBar from "../components/FilterBar";
import NotificationList from "../components/NotificationList";
import PaginationControl from "../components/PaginationControl";
import { useNotifications } from "../hooks/useNotifications";
import { loadViewed, markViewed } from "../state/viewedStore";

const AllNotifications: React.FC = () => {
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [type, setType] = useState("all");
  const { items, total, loading, error } = useNotifications({ page, limit, type });

  const viewedIds = useMemo(() => loadViewed(), [items]);
  const pageCount = total ? Math.max(1, Math.ceil(total / limit)) : Math.max(1, page);

  const handleItemClick = (id: string) => {
    markViewed(id);
  };

  return (
    <div>
      <Typography variant="h5" sx={{ mb: 2 }}>
        All Notifications
      </Typography>
      <FilterBar
        type={type}
        onTypeChange={(next) => {
          setType(next);
          setPage(1);
        }}
        limit={limit}
        onLimitChange={(next) => {
          setLimit(next);
          setPage(1);
        }}
      />

      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}

      {!loading && !error && (
        <NotificationList items={items} viewedIds={viewedIds} onItemClick={handleItemClick} />
      )}

      {!loading && !error && items.length === 0 && (
        <Typography sx={{ mt: 2 }}>No notifications available.</Typography>
      )}

      {!loading && !error && (
        <PaginationControl page={page} count={pageCount} onChange={setPage} />
      )}
    </div>
  );
};

export default AllNotifications;
```

- [ ] **Step 2: Commit**

```bash
git add notification_app_fe/src/pages/AllNotifications.tsx

git commit -m "feat: add all notifications page"
```

---

### Task 8: Priority Inbox page

**Files:**
- Create: `notification_app_fe/src/pages/PriorityInbox.tsx`

- [ ] **Step 1: Implement page**

```tsx
// notification_app_fe/src/pages/PriorityInbox.tsx
import React, { useMemo, useState } from "react";
import { Alert, CircularProgress, FormControl, InputLabel, MenuItem, Select, Typography } from "@mui/material";
import NotificationList from "../components/NotificationList";
import { useNotifications } from "../hooks/useNotifications";
import { loadViewed, markViewed } from "../state/viewedStore";
import { topNByPriority } from "../utils/priority";

const PriorityInbox: React.FC = () => {
  const [topN, setTopN] = useState(10);
  const { items, loading, error } = useNotifications({ page: 1, limit: 100, type: "all" });
  const viewedIds = useMemo(() => loadViewed(), [items]);

  const topItems = useMemo(() => {
    return topNByPriority(items, topN);
  }, [items, topN]);

  return (
    <div>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Priority Inbox
      </Typography>

      <FormControl size="small" sx={{ minWidth: 160, mb: 2 }}>
        <InputLabel id="topn-label">Top N</InputLabel>
        <Select
          labelId="topn-label"
          value={String(topN)}
          label="Top N"
          onChange={(event) => setTopN(Number(event.target.value))}
        >
          <MenuItem value={10}>10</MenuItem>
          <MenuItem value={15}>15</MenuItem>
          <MenuItem value={20}>20</MenuItem>
        </Select>
      </FormControl>

      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}

      {!loading && !error && (
        <NotificationList
          items={topItems}
          viewedIds={viewedIds}
          onItemClick={(id) => markViewed(id)}
        />
      )}

      {!loading && !error && topItems.length === 0 && (
        <Typography>No priority notifications available.</Typography>
      )}
    </div>
  );
};

export default PriorityInbox;
```

- [ ] **Step 2: Commit**

```bash
git add notification_app_fe/src/pages/PriorityInbox.tsx

git commit -m "feat: add priority inbox page"
```

---

### Task 9: Environment example and README

**Files:**
- Create: `notification_app_fe/.env.example`
- Create: `notification_app_fe/README.md`

- [ ] **Step 1: Add .env example**

```
# notification_app_fe/.env.example
REACT_APP_API_TOKEN=your_token_here
```

- [ ] **Step 2: Add README**

```md
# Campus Notification Frontend

## Setup

```bash
cd notification_app_fe
npm install
npm start
```

App runs on http://localhost:3000

## Environment
Copy `.env.example` to `.env` and add your token:

```
REACT_APP_API_TOKEN=your_token_here
```
```

- [ ] **Step 3: Commit**

```bash
git add notification_app_fe/.env.example notification_app_fe/README.md

git commit -m "docs: add frontend setup instructions"
```

---

### Task 10: Final verification

**Files:**
- Test: `notification_app_fe/src/state/viewedStore.test.ts`
- Test: `notification_app_fe/src/utils/priority.test.ts`

- [ ] **Step 1: Run tests**

Run:
```bash
cd notification_app_fe
npm test -- --watchAll=false
```
Expected: All tests PASS.

- [ ] **Step 2: Manual run**

Run:
```bash
npm start
```
Expected: Dev server at http://localhost:3000 with All Notifications and Priority Inbox pages visible.

- [ ] **Step 3: Commit**

```bash
git add notification_app_fe

git commit -m "chore: verify frontend build"
```

---

## Self-Review
1. **Spec coverage:** All requirements are mapped: CRA app, MUI UI, pagination, filter, viewed state, priority logic, error/loading states, responsiveness, API params, .env example.
2. **Placeholder scan:** No TODO/TBD text in tasks.
3. **Type consistency:** Types and helper usage are consistent across tasks.
