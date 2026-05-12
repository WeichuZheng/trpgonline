# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TRPG Online — 在线跑团网站，支持 6-8 人同时在线。GM（主持人）创建模组和管理游戏，玩家通过房间号加入。

## Development Commands

### Backend (conda env: `trpg`)
```bash
conda activate trpg
python -m uvicorn backend.main:app --reload          # Start dev server (port 8000)
python init_db.py                                      # Rebuild SQLite database (deletes all data)
```

### Frontend (in `frontend/` directory)
```bash
npm run dev       # Vite dev server (port 5173, proxies /api and /ws to backend)
npm run build     # Production build → frontend/dist/
```

Vite proxies `/api` → `http://127.0.0.1:8000`, `/ws` → `ws://127.0.0.1:8000`, `/uploads` → backend static files.

## Architecture

### Backend: FastAPI + SQLAlchemy async + SQLite

```
backend/
├── main.py          # FastAPI app, CORS, lifespan, mounts routes + /uploads + /ws
├── config.py        # Settings from env/.env (DB URL, JWT secret, upload dir)
├── database.py      # Async engine, session factory, get_db dependency
├── auth.py          # JWT (python-jose), bcrypt, get_current_user dependency
├── websocket.py     # ConnectionManager per-room, broadcasts dice/unit/map events
├── api/
│   ├── auth.py      # /api/auth/* — register, login, me
│   ├── modules.py   # /api/modules/* — CRUD + character templates
│   ├── resources.py # /api/modules/{id}/resources — create (FormData), update, toggle-visible
│   ├── rooms.py     # /api/rooms/* — create, join, characters, dice, map units, resources
│   └── maps.py      # /api/modules/{id}/maps — CRUD maps + units
├── models/models.py # SQLAlchemy models (User, Module, Resource, Room, CharacterCard, Map, MapUnit, CharacterTemplate, GameLog)
└── schemas/schemas.py # Pydantic v2 schemas with ResourceTypeEnum, enums
```

Key patterns:
- All endpoints use `Depends(get_current_user)` for auth
- Database sessions use `Depends(get_db)` with auto-commit/rollback
- Resource creation uses `FormData` (multipart) for file uploads
- WebSocket: room-scoped broadcast via `ConnectionManager`, message types: `dice_roll`, `unit_move`, `hp_change`, `unit_created`, `unit_updated`, `unit_deleted`, `active_map_changed`, `resource_visible`

### Frontend: Vue 3 + Pinia + Vue Router + TipTap

```
frontend/src/
├── main.js              # Creates app, installs Pinia + router + AppToast
├── router/routes.js     # Auth-guarded routes: dashboard, module-edit, game-room
├── stores/
│   ├── auth.js          # Token, user state, login/logout
│   ├── game.js          # Room state: resources, characters, mapUnits, ws, dice
│   ├── modules.js       # Module list
│   └── rooms.js         # Room list
├── services/
│   ├── api.js           # Axios instance, auth interceptor, 401→login redirect
│   ├── authService.js   # Login, register, me
│   ├── moduleService.js # Module CRUD
│   ├── resourceService.js # Resource CRUD (FormData for create)
│   ├── roomService.js   # Room operations, characters, dice rolls
│   ├── mapService.js    # Map/unit CRUD
│   └── characterService.js, characterTemplateService.js, diceService.js
├── views/
│   ├── ModuleEditView.vue  # Module editor: tabs for resources/maps/templates
│   └── GameRoomView.vue    # Game room: narrative/battle modes, WebSocket, resource viewer
├── components/
│   ├── editor/          # TipTap rich text system
│   │   ├── ResourceEditor.vue    # WYSIWYG editor (useEditor, v-if="editor" guard required)
│   │   ├── ResourceViewer.vue    # Read-only renderer (generateHTML, filters gm-only/hidden nodes)
│   │   ├── EditorToolbar.vue     # Formatting + GM visibility buttons
│   │   └── VisibilityExtension.js # Custom TipTap extension: paragraph visibility (visible/gm-only/hidden)
│   ├── map/MapCanvas.vue # Canvas-based map with tokens, drag, detail panel
│   ├── common/          # AppButton, AppCard, AppInput, AppSelect, AppModal, AppToast, AvatarUploader
│   └── game/CharacterSheet.vue
└── css/style.css        # Global CSS variables (theme colors, fonts, spacing)
```

Key patterns:
- API calls go through `services/api.js` axios instance with auto-token injection
- WebSocket managed in GameRoomView: connects on mount, broadcasts via `ws.send(JSON.stringify({type, ...}))`
- Game state in Pinia `useGameStore`: resources, characters, mapUnits, ws connection
- TipTap `useEditor` returns `ShallowRef<Editor | undefined>` — always guard with `v-if="editor"` before rendering toolbar/content
- TipTap imports: `TextStyle` and `Color` use **named** imports (`{ TextStyle }`, `{ Color }`), not default

### Rich Text / Resource System

Resources are TipTap ProseMirror JSON documents stored in `Resource.content`. The `VisibilityExtension` adds a `visibility` attribute to block nodes:
- `visible` (default) — everyone sees it
- `gm-only` — only GM sees it (red left border + lock icon in editor/GM view)
- `hidden` — only GM sees it, collapsible (gray left border + eye icon)
- `ResourceViewer` calls `filterInvisibleNodes()` to strip gm-only/hidden nodes for players

### Database

SQLite via `aiosqlite`. Schema defined in `backend/models/models.py`. To apply schema changes: delete `database.db` and run `python init_db.py`. This destroys all data.

## Common Gotchas

- After model changes in `models.py`, must rebuild DB (`rm database.db && python init_db.py`)
- TipTap `useEditor` is async — template must use `v-if="editor"` guard or crash on undefined
- Resource API uses `FormData` (not JSON) for creation due to file upload support
- `DisplayTypeEnum` and `doc_type` have been removed — do not re-add document type classification
- Backend runs on port 8000, frontend dev on 5173 with proxy
- use conda environment 'trpg' to run backend/frontend/tests