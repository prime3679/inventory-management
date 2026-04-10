# Application Ship Check — Reference Files

Key entry points and configuration files to read when running a ship check. These are the files most likely to be affected by or reveal issues from a change.

## Frontend Entry Points
- `client/src/main.js` — App bootstrap and router definition
- `client/src/App.vue` — Root component, global layout, and global styles
- `client/src/api.js` — All API calls (the frontend side of every API contract)

## Frontend Shared State
- `client/src/composables/useFilters.js` — Global filter state shared across views
- `client/src/composables/useI18n.js` — Translation system, locale, and currency
- `client/src/composables/useAuth.js` — User session and profile data

## Frontend Locales
- `client/src/locales/en.js` — English translations
- `client/src/locales/ja.js` — Japanese translations

## Backend Entry Points
- `server/main.py` — All API endpoints and Pydantic models
- `server/mock_data.py` — Data loading from JSON files

## Data Files
- `server/data/inventory.json`
- `server/data/orders.json`
- `server/data/demand_forecasts.json`
- `server/data/backlog_items.json`
- `server/data/spending.json`
- `server/data/transactions.json`
- `server/data/purchase_orders.json`

## Test Entry Points
- `tests/backend/conftest.py` — Test fixtures and client setup
- `tests/pytest.ini` — Pytest configuration

## Configuration
- `.env.example` — Environment variable template
- `client/vite.config.js` — Frontend build configuration
- `server/pyproject.toml` — Backend dependencies and project metadata
- `client/package.json` — Frontend dependencies
