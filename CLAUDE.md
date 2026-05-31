# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Factory Inventory Management System — full-stack demo app (Claude Code workshop). Vue 3 frontend, Python FastAPI backend, in-memory mock data from JSON files (no database).

## Commands

### Start/Stop Servers

```bash
# One-command startup (installs deps if missing, runs both servers in background)
./scripts/start.sh

# Stop all servers
./scripts/stop.sh

# Manual startup:
cd server && uv run python main.py          # Backend on http://localhost:8001
cd client && npm install && npm run dev      # Frontend on http://localhost:3000
```

### Tests

```bash
# All backend tests (run from tests/ directory using server's venv)
cd tests && uv run --project ../server pytest backend/ -v

# Single test file
cd tests && uv run --project ../server pytest backend/test_inventory.py -v

# Single test
cd tests && uv run --project ../server pytest backend/test_inventory.py::TestInventoryEndpoints::test_get_all_inventory -v

# With coverage
cd tests && uv run --project ../server pytest backend/ --cov=../server
```

### Build

```bash
cd client && npm run build    # Output: client/dist/
```

## Architecture

### Stack
- **Frontend**: Vue 3 (Composition API) + Vue Router + Vite (port 3000) + Axios
- **Backend**: FastAPI + Pydantic + uvicorn (port 8001)
- **Data**: JSON files in `server/data/` loaded into memory at startup via `server/mock_data.py`

### Data Flow
Vue composable filters → `client/src/api.js` (Axios) → FastAPI endpoints (`server/main.py`) → in-memory filtering of data from `server/mock_data.py` → Pydantic validation → JSON response → Vue computed properties

### Frontend Architecture
- **Routing**: Defined in `client/src/main.js` — 6 routes: `/` (Dashboard), `/inventory`, `/orders`, `/spending`, `/demand`, `/reports`
- **Shared state via singleton composables** (module-level refs, not per-component):
  - `useFilters.js` — 4 global filter refs (period, location, category, status) shared across all views
  - `useI18n.js` — i18n with English/Japanese, locale-driven currency (USD/JPY), product/customer/warehouse name translation
  - `useAuth.js` — mock user with locale-aware profile data and tasks
- **API client**: `client/src/api.js` — centralized Axios calls, builds URLSearchParams from filter state
- **Global styles**: All in `client/src/App.vue` `<style>` (not scoped) — cards, tables, badges, stat-cards, nav
- **Charts**: Custom SVG (no chart library)
- **Currency**: `client/src/utils/currency.js` — USD/JPY conversion at fixed 150x rate

### Backend Architecture
- **Single-file API**: All endpoints in `server/main.py` with Pydantic models defined inline
- **Filtering**: `apply_filters()` for warehouse/category/status, `filter_by_month()` for month/quarter date filtering
- **Quarter mapping**: Hardcoded `QUARTER_MAP` dict for Q1-Q4 2025
- **Data loading**: `server/mock_data.py` reads all JSON files at import time into module-level variables

### Filter System
4 filters apply globally: Time Period, Warehouse (San Francisco/London/Tokyo), Category (Circuit Boards/Sensors/Power Supplies/Connectors/Mechanical Components), Order Status (Delivered/Shipped/Processing/Backordered). Inventory endpoints only support warehouse and category (no time dimension). The `'all'` value means no filter.

### API Endpoints
- `GET /api/inventory` — warehouse, category filters
- `GET /api/inventory/{id}` — single item, 404 if missing
- `GET /api/orders` — warehouse, category, status, month filters
- `GET /api/orders/{id}` — single order, 404 if missing
- `GET /api/dashboard/summary` — all filters, returns computed metrics
- `GET /api/demand`, `/api/backlog` — no filters
- `GET /api/spending/summary|monthly|categories|transactions` — no filters
- `GET /api/reports/quarterly|monthly-trends` — computed from orders data
- API docs: http://localhost:8001/docs

### Testing
- Backend only (no frontend tests). 55 pytest tests using FastAPI TestClient.
- Fixtures in `tests/backend/conftest.py` — `client` fixture provides TestClient, sample data fixtures available.
- Tests organized by feature: `test_inventory.py`, `test_dashboard.py`, `test_misc_endpoints.py` + orders tests.

## Key Constraints

1. Use unique keys in `v-for` (use `sku`, `id`, `month` — never array index)
2. Validate dates before calling `.getMonth()` — data comes from JSON strings
3. Update Pydantic models in `server/main.py` when changing JSON data structure in `server/data/`
4. Inventory filters don't support month (no time dimension in inventory data)
5. Revenue goals: $800K/month single warehouse, $9.6M YTD across all months
6. No emojis in UI

## Release Standards

1. All changes require test evidence (passing tests or test output) before merging
2. No direct commits to main — all changes go through pull requests
3. Every PR must include a one-line business impact summary in the description

## Subagents and Tools

- **vue-expert**: Delegate when creating or significantly modifying `.vue` files
- **code-reviewer**: Use after writing significant code for quality review
- **security-auditor**: Fast security review of changed files
- **backend-api-test** skill: Use when writing/modifying tests in `tests/backend/`
- **GitHub MCP tools** (`mcp__github__*`): Use for all GitHub operations (exception: local-only branches use `git checkout -b`)
- **Playwright MCP tools** (`mcp__playwright__*`): Use for browser testing against localhost:3000 (frontend) and localhost:8001 (API)
