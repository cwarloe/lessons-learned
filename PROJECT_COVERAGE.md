# Lessons Learned - Project Coverage

**Last Updated:** October 13, 2025

---

## Overview

This repository catalogs lessons learned from **3 major projects** across different domains:
- Multiplayer gaming (Asteroids)
- Personal timeline app (Record Your Story)
- Classic games portal (Node.js infrastructure)

Plus emerging lessons from:
- Knowledge Harvest (screen recording/knowledge capture)

---

## Project Breakdown

### 1. Multiplayer Asteroids Game
**Status:** Deployed, operational with mobile support
**Tech Stack:** Node.js, Express, WebSocket, HTML5 Canvas
**Lessons Documented:** 7 major issues

**Key Lessons:**
- WebSocket error handling (JSON.parse in try-catch)
- Server-side input validation (SECURITY)
- Canvas DPI scaling for high-resolution displays
- Dynamic WebSocket URLs (no hardcoded localhost)
- Mobile touch controls optimization
- Toast notifications for connection feedback
- Volume button integration for mobile

**Document:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) (Project 1 section)
**Analysis:** [ASTEROIDS_ISSUES_ANALYSIS.md](ASTEROIDS_ISSUES_ANALYSIS.md)

**Applicable To:**
- Real-time multiplayer games
- WebSocket applications
- Canvas-based graphics
- Mobile gaming
- Client-server architecture

---

### 2. Record Your Story Timeline App
**Status:** Production (v2.7.2) - Live on Render
**Tech Stack:** TypeScript, Vite, Supabase, Claude AI, IndexedDB
**Lessons Documented:** 9 critical bugs + architecture patterns

**Key Lessons:**
- Race conditions in async initialization
- LocalStorage quota exceeded (5MB limit)
- Hybrid storage architecture (LocalStorage + IndexedDB + Supabase)
- Event delegation for dynamic content
- Rich text editor lifecycle (Quill.js)
- TypeScript naming conflicts with DOM globals
- OAuth redirect URI exact matching
- Undo/Redo system implementation
- Performance optimizations (debouncing, lazy loading)

**Document:** [RECORD_YOUR_STORY_LESSONS.md](RECORD_YOUR_STORY_LESSONS.md)
**Also In:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) (Project 2 section - summarized)

**Applicable To:**
- Timeline/journal applications
- Photo/media apps with local storage
- Supabase-based apps
- AI-integrated applications
- Multi-device sync applications
- TypeScript migrations

---

### 3. Classic Games Portal
**Status:** Active development
**Tech Stack:** Node.js, Express, WebSocket, HTML5 Canvas
**Lessons Documented:** Deployment and infrastructure

**Key Lessons:**
- Dynamic port configuration (PORT env var)
- Manifest-driven game loading
- Separate servers for different game types
- Docker deployment (Dockerfile, Procfile)
- Cloud deployment (Render, Railway, Fly.io)

**Document:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) (mentioned in Project 1)

**Applicable To:**
- Multi-app portals
- Game hosting platforms
- Express-based infrastructure
- Docker deployments

---

### 4. Knowledge Harvest (Emerging)
**Status:** Early development (MVP phase)
**Tech Stack:** React, Express, PostgreSQL, LocalStack S3, Docker
**Lessons Documented:** 1 bug fix (React state)

**Known Issues:**
- Recording limit state management (React hooks)
- S3 integration incomplete
- Video playback missing
- Component refactoring needed

**Document:** Not yet comprehensive (project too early)

**Future Lessons:**
- WebRTC screen recording
- Video streaming implementation
- S3 file upload patterns
- LocalStack → AWS transition
- Docker Compose orchestration

**Applicable To:**
- Screen recording applications
- Video storage/streaming
- Knowledge management systems
- WebRTC applications

---

## Cross-Project Patterns

### Storage Strategies

| Project | Strategy | Lesson |
|---------|----------|--------|
| Asteroids | Server-side state | WebSocket game state sync |
| Record Your Story | Hybrid (3-tier) | LocalStorage + IndexedDB + Supabase |
| Knowledge Harvest | S3 + PostgreSQL | Large file storage + metadata |

**Lesson:** Choose storage based on data size and sync requirements
- LocalStorage: Small metadata (<5MB)
- IndexedDB: Large files locally (unlimited)
- S3: Large files in cloud
- Supabase: Structured data with sync

---

### Error Handling Patterns

**All Projects Share:**
- ✅ Try-catch around all async operations
- ✅ User-friendly error messages (toasts, not alerts)
- ✅ Console logging with context
- ✅ Graceful degradation
- ✅ Retry mechanisms for network failures

**Common Anti-Pattern:**
- ❌ Silent error catching (`catch {}`)
- ❌ Assuming operations succeed
- ❌ No error boundaries

---

### TypeScript Adoption

| Project | Language | Lesson |
|---------|----------|--------|
| Asteroids | Vanilla JS | Works for small games |
| Record Your Story v1 | Vanilla JS | Became unwieldy → rewrote in TS |
| Record Your Story v2 | TypeScript | Much better maintainability |
| Knowledge Harvest | JavaScript (React) | Should migrate to TS |

**Lesson:** Start with TypeScript for anything beyond a simple prototype

---

### Authentication & Security

| Project | Auth Method | Lesson |
|---------|-------------|--------|
| Asteroids | None (anonymous) | Simple for games |
| Record Your Story | Supabase Auth | Proper OAuth, row-level security |
| Knowledge Harvest | Not yet implemented | Plan early for multi-user |

**Security Lessons:**
- ✅ Never trust client input (validate server-side)
- ✅ API keys belong on server, not in client bundles
- ✅ Use OAuth for third-party integrations
- ✅ Test redirect URIs exactly (including .html)

---

### Mobile Support

| Project | Mobile Strategy | Lesson |
|---------|----------------|--------|
| Asteroids | Separate mobile.html | Touch controls very different from desktop |
| Record Your Story | Responsive | Works on mobile but not optimized |

**Lesson:** Decide mobile-first vs responsive vs separate versions early

---

## Common Mistakes Across All Projects

### 1. Hardcoded Values
```javascript
// ❌ Seen in multiple projects
const API_URL = 'http://localhost:3000';
const ws = new WebSocket('ws://localhost:8080');

// ✅ Should be
const API_URL = import.meta.env.VITE_API_URL;
const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
const ws = new WebSocket(`${protocol}//${location.host}/ws`);
```

### 2. Missing Null Checks
```javascript
// ❌ Seen in Record Your Story, Asteroids
const name = user.name;  // Crashes if user is null

// ✅ Should be
const name = user?.name ?? 'Unknown';
```

### 3. Assuming Async Success
```javascript
// ❌ Seen in all projects initially
const data = await fetch('/api/events').json();
renderEvents(data);

// ✅ Should be
try {
  const response = await fetch('/api/events');
  if (!response.ok) throw new Error('Fetch failed');
  const data = await response.json();
  renderEvents(data);
} catch (error) {
  console.error('Failed to load events:', error);
  showErrorMessage('Could not load events. Please try again.');
}
```

### 4. Event Listeners Before DOM
```javascript
// ❌ Record Your Story v2.0.1
function init() {
  attachListeners();  // Elements don't exist yet!
  renderUI();
}

// ✅ Should be
function init() {
  renderUI();
  attachListeners();  // Now elements exist
}
```

---

## Lessons by Category

### Storage (All Projects)
- ✅ LocalStorage: Max 5MB, synchronous, good for metadata
- ✅ IndexedDB: Unlimited, asynchronous, good for large files
- ✅ Supabase Storage: Cloud-based, good for multi-device sync
- ✅ S3: Large file storage, streaming support
- ❌ Never store base64 images in LocalStorage

### WebSocket (Asteroids, Portal)
- ✅ Always wrap JSON.parse in try-catch
- ✅ Dynamic host detection (not hardcoded)
- ✅ Reconnection logic with exponential backoff
- ✅ Visual feedback for connection state
- ✅ Server-side input validation

### TypeScript (Record Your Story)
- ✅ Start with TypeScript from day one
- ✅ Use strict mode
- ✅ Avoid names that conflict with DOM globals (Event, Response)
- ✅ Run `npm run build` before deploying
- ✅ Proper service layer separation

### React (Knowledge Harvest, partial Record Your Story)
- ✅ Use functional components with hooks
- ✅ Be careful with stale closures in useEffect
- ✅ Debounce expensive operations
- ⚠️ Knowledge Harvest had React state closure bug

### Canvas Graphics (Asteroids, Portal)
- ✅ Account for devicePixelRatio (high-DPI displays)
- ✅ Update both canvas.width/height AND style
- ✅ Scale context to match DPI
- ✅ Use requestAnimationFrame for smooth rendering

---

## Emerging Patterns

### Toast Notifications
**Used In:** Asteroids (connections), Record Your Story (actions)
**Better Than:** `alert()` or `confirm()`
**Implementation:** Reusable toast function with auto-dismiss

### Undo/Redo Systems
**Used In:** Record Your Story
**Pattern:** History stack with action tracking
**Limit:** 50 actions to prevent memory issues

### Hybrid Storage
**Used In:** Record Your Story
**Pattern:** 3-tier (LocalStorage + IndexedDB + Cloud)
**Benefit:** Fast UI, unlimited local, multi-device sync

### Service Layer Pattern
**Used In:** Record Your Story v2
**Pattern:** Separate UI, data, and business logic
**Files:** `services/supabase.ts`, `services/claude.ts`

---

## Statistics

- **Projects Documented:** 3 major + 1 emerging
- **Total Issues Analyzed:** 23+
- **Critical Bugs Fixed:** 15+
- **Architecture Patterns:** 8+
- **Total Documentation:** ~70KB across 4 files
- **Lines of Lesson Code Examples:** 500+

---

## Quick Reference Matrix

| Need | Project | Document | Line/Section |
|------|---------|----------|--------------|
| WebSocket error handling | Asteroids | LESSONS_LEARNED.md | Issue #4 |
| Storage quota exceeded | Record Your Story | RECORD_YOUR_STORY_LESSONS.md | Issue #2 |
| Event delegation | Record Your Story | RECORD_YOUR_STORY_LESSONS.md | Issue #3 |
| Canvas DPI scaling | Asteroids | LESSONS_LEARNED.md | Issue #6 |
| OAuth redirect URIs | Record Your Story | RECORD_YOUR_STORY_LESSONS.md | Issue #6 |
| TypeScript naming | Record Your Story | RECORD_YOUR_STORY_LESSONS.md | Issue #5 |
| Server input validation | Asteroids | LESSONS_LEARNED.md | Issue #5 |
| Undo/Redo system | Record Your Story | RECORD_YOUR_STORY_LESSONS.md | Best Practices #4 |

---

## Future Project Coverage

**When adding new projects:**
1. Create project-specific `PROJECT_NAME_LESSONS.md` if substantial
2. Add summary to main `LESSONS_LEARNED.md`
3. Update this `PROJECT_COVERAGE.md`
4. Update main `README.md` with new project
5. Commit with descriptive message

**Template for new project lessons:**
```markdown
# Project Name - Lessons Learned

## Overview
- Tech Stack:
- Status:
- Timeline:

## Critical Bugs
### 1. Bug Title
**Problem:**
**Root Cause:**
**Solution:**
**Lesson:**

## Architecture Decisions
## Best Practices Established
## Development Checklist
```

---

**Status:** Living document - update as new projects are added
**Next Review:** When Knowledge Harvest reaches MVP completion
