# Lessons Learned - Project Post-Mortem

**Date:** October 12, 2025
**Projects Analyzed:**
- Multiplayer Asteroids Game (`/games/asteroids/`)
- Record Your Story Timeline App (`/record-your-story/`)
- Classic Games Portal (main project)

---

## 📋 Executive Summary

This document catalogs errors, issues, and lessons learned across our development projects to prevent recurring mistakes and improve future development practices. Analysis is based on git history, changelogs, session summaries, and code review.

**Key Statistics:**
- **Total Commits Analyzed:** 50+
- **Bug Fixes Tracked:** 15+
- **Major Issues Resolved:** 8
- **Architecture Improvements:** 5

---

## 🎮 Project 1: Multiplayer Asteroids Game

### Overview
- **Tech Stack:** Node.js, Express, WebSocket, HTML5 Canvas
- **Status:** Deployed successfully with mobile support
- **Files:** `games/asteroids/index.html`, `client.js`, `mobile.html`

### Issues & Solutions

#### 1. **Localhost-Only WebSocket Connection**
**Problem:** Game initially only worked on localhost, failed when accessed remotely
**Root Cause:** Hardcoded `ws://localhost:8080` in client code
**Solution:** Dynamic WebSocket connection based on current host
```javascript
// BEFORE (hardcoded)
const ws = new WebSocket('ws://localhost:8080/ws');

// AFTER (dynamic)
const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
const ws = new WebSocket(`${protocol}//${location.host}/ws`);
```
**Lesson:** Never hardcode URLs - always use environment variables or dynamic detection

---

#### 2. **npx Permission Issues on Windows**
**Problem:** Could not run `npx ngrok` due to Windows permission restrictions
**Root Cause:** Corporate/admin restrictions on npx execution
**Solution:** Used `localtunnel` as alternative tunnel service
```bash
# INSTEAD OF: npx ngrok http 8080
npx localtunnel --port 8080
```
**Lesson:** Have backup tools ready for different OS/permission environments

---

#### 3. **Mobile Touch Controls Not Optimized**
**Problem:** Desktop version difficult to play on mobile (small buttons, no touch optimization)
**Root Cause:** Desktop-first design without mobile consideration
**Solution:** Created separate `mobile.html` with:
- Virtual joystick (analog control)
- Tilt controls (gyroscope)
- Volume button shooting
- Haptic feedback
- Fullscreen mode

**Lesson:** Mobile-first or responsive design from the start - retrofitting is harder

---

### Best Practices Established
✅ Dynamic configuration for different environments
✅ Graceful fallbacks for platform-specific features
✅ Separate mobile-optimized versions when touch UX differs significantly
✅ Document deployment options (ngrok, localtunnel, cloud hosting)

---

## 📖 Project 2: Record Your Story Timeline App

### Overview
- **Tech Stack:** TypeScript, Vite, Supabase, Claude AI, IndexedDB
- **Status:** Production (v2.7.2) - Live on Render
- **Major Versions:** v1.0 → v2.0 (TypeScript migration) → v2.7.2 (AI features)

---

## 🐛 Critical Bugs & Fixes

### 1. **Login Blank Screen Issue** (v2.0.2)
**Problem:** Users saw blank screen after successful login
**Root Cause:** Race condition in `showApp()` function - UI rendering before data loaded
**Impact:** High - prevented app usage after authentication

**Solution:**
```typescript
async function showApp() {
  try {
    // Added defensive null checks
    const user = supabase.getCurrentUser();
    if (!user) throw new Error('No authenticated user');

    // Wait for timeline data before rendering
    const timelines = await supabase.getTimelines() ?? [];

    // Null-coalescing operators throughout
    const currentTimeline = timelines[0] ?? await createDefaultTimeline();

    renderUI(currentTimeline);
  } catch (error) {
    console.error('Failed to load app:', error);
    showErrorUI(); // Graceful error with retry button
  }
}
```

**Lessons:**
- ❌ Don't assume async operations succeed
- ✅ Add try-catch wrappers around initialization code
- ✅ Provide user-facing error UI with recovery options
- ✅ Use null-coalescing (`??`) instead of truthy checks for optional values

---

### 2. **LocalStorage Quota Exceeded** (v1.0.0)
**Problem:** App crashed when users added multiple photos (>5MB limit)
**Root Cause:** Storing base64-encoded images in LocalStorage
**Error:** `QuotaExceededError: Failed to execute 'setItem' on 'Storage'`

**Solution:** Migrated photo storage to IndexedDB (unlimited capacity)
```typescript
// BEFORE: LocalStorage (5MB limit)
localStorage.setItem('events', JSON.stringify(events));

// AFTER: Hybrid approach
localStorage.setItem('events_metadata', JSON.stringify(eventsWithoutPhotos));
await indexedDB.put('photos', photoBlobs); // Unlimited
```

**Lessons:**
- ❌ Never store large binary data in LocalStorage
- ✅ Use IndexedDB for photos, videos, large files
- ✅ Keep lightweight metadata in LocalStorage for fast access
- ✅ Implement storage quota checks before writes

---

### 3. **UUID Error on Event Save** (v2.0.1)
**Problem:** Clicking "Add Event" threw `Invalid UUID` error
**Root Cause:** Event listener passed PointerEvent instead of eventId parameter

**Before (broken):**
```typescript
addEventBtn.addEventListener('click', handleEventSubmit);
// handleEventSubmit received PointerEvent as first parameter
```

**After (fixed):**
```typescript
addEventBtn.addEventListener('click', (e) => {
  e.preventDefault();
  handleEventSubmit(); // No parameters, reads from form directly
});
```

**Lessons:**
- ❌ Don't assume event handlers receive expected parameters
- ✅ Use arrow function wrappers for clarity
- ✅ Read DOM values inside handler, not from parameters
- ✅ Add TypeScript types to catch parameter mismatches

---

### 4. **Edit/Delete Buttons Not Working** (v2.0.1)
**Problem:** Buttons visible but clicks did nothing on page load
**Root Cause:** Event listeners attached before DOM elements existed

**Solution:**
```typescript
// Created dedicated function to attach listeners
function attachTimelineEventListeners() {
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent bubbling
      const eventId = (e.currentTarget as HTMLElement).dataset.eventId;
      handleEditEvent(eventId);
    });
  });
}

// Call after rendering timeline
renderTimeline();
attachTimelineEventListeners(); // ✅ Attached after DOM ready
```

**Lessons:**
- ❌ Don't attach listeners before elements exist
- ✅ Use `e.currentTarget` (element with listener) not `e.target` (clicked element)
- ✅ Call `stopPropagation()` to prevent event bubbling
- ✅ Create helper functions for re-attaching listeners after re-renders

---

### 5. **Quill Editor Not Loading When Editing** (v2.0.2)
**Problem:** Rich text editor blank when editing existing events
**Root Cause:** Stale Quill instance check prevented recreation

**Before (broken):**
```typescript
if (quillInstance) {
  quillInstance.setContents(event.description);
} else {
  quillInstance = new Quill('#editor', options);
}
// Editor never recreated when modal reopened
```

**After (fixed):**
```typescript
// Destroy previous instance
if (quillInstance) {
  quillInstance = null;
}

// Always create fresh instance on modal open
quillInstance = new Quill('#editor', options);
quillInstance.root.innerHTML = event.description || '';
```

**Lessons:**
- ❌ Don't reuse rich text editor instances across modal opens
- ✅ Destroy and recreate on each modal open
- ✅ Set content with `.root.innerHTML` for HTML strings
- ✅ Test edit workflows, not just create workflows

---

### 6. **TypeScript Type Conflicts** (v2.0.1)
**Problem:** `Event` interface conflicted with DOM `Event` type
**Error:** `Cannot redeclare block-scoped variable 'Event'`

**Solution:** Renamed custom interface to `TimelineEvent`
```typescript
// BEFORE (conflict with DOM Event)
interface Event {
  id: string;
  title: string;
  date: string;
}

// AFTER (no conflict)
interface TimelineEvent {
  id: string;
  title: string;
  date: string;
}
```

**Lessons:**
- ❌ Don't use generic names that conflict with browser globals
- ✅ Use specific, descriptive interface names
- ✅ Run TypeScript strict mode from day one
- ✅ Check for naming conflicts with DOM APIs

---

### 7. **Private Property Access Errors** (v2.0.1)
**Problem:** Direct access to `supabase.client` from outside service class
**Root Cause:** Private encapsulation not respected

**Solution:** Added public methods to service
```typescript
// SupabaseService class
class SupabaseService {
  private client: SupabaseClient;

  // ✅ Added public methods instead of exposing client
  async createEventConnection(connection: EventConnection) {
    return this.client.from('event_connections').insert(connection);
  }

  async getEventConnections(eventId: string) {
    return this.client.from('event_connections')
      .select('*')
      .eq('event_id', eventId);
  }
}
```

**Lessons:**
- ❌ Don't expose internal implementation details
- ✅ Use proper encapsulation with public methods
- ✅ Design service layer APIs before implementation
- ✅ Respect TypeScript access modifiers

---

### 8. **Google Drive OAuth Redirect URI Mismatch** (v2.7.1)
**Problem:** OAuth popup showed "redirect_uri_mismatch" error
**Root Cause:** Configured `http://localhost:5173/google-callback` but actual file was `.html`

**Solution:**
```typescript
// Google Cloud Console: Add both variations
// ✅ http://localhost:5173/google-callback.html
// ✅ http://localhost:5173/google-callback

// Code: Use exact .html path
const redirectUri = `${window.location.origin}/google-callback.html`;
```

**Lessons:**
- ❌ Don't assume OAuth providers strip .html extensions
- ✅ Match redirect URIs exactly (including .html)
- ✅ Add multiple variations in OAuth config for flexibility
- ✅ Test OAuth flow in production environment (different origin)

---

### 9. **Build Failures on Render Deployment** (v2.6.0)
**Problem:** Local builds passed, production builds failed with TypeScript errors
**Root Cause:** Different TypeScript strict settings, missing type imports

**Errors:**
```
Property 'adapt' does not exist on type 'Response'
Cannot find module '@supabase/auth-helpers-sveltekit'
```

**Solution:**
```typescript
// Added proper type imports
import type { SupabaseClient } from '@supabase/supabase-js';

// Fixed Response type handling
const textResponse = await response.text();
// Instead of: response.adapt()

// Removed unused adapter imports
// Cleaned up build configuration
```

**Lessons:**
- ❌ Don't ignore TypeScript warnings in dev mode
- ✅ Run `npm run build` before every deployment
- ✅ Use same TypeScript config in dev and prod
- ✅ Enable `strict: true` from project start

---

## 🏗️ Architecture & Design Issues

### 1. **V1 to V2 Migration Complexity**
**Problem:** Complete rewrite from vanilla JS to TypeScript was massive undertaking
**Impact:** 2-week rewrite, preserved v1 in `/v1` folder

**What Went Wrong:**
- Built entire v1 without type safety
- Mixed concerns (UI + data + business logic in one file)
- No service layer architecture

**What We Did Right in V2:**
```
src/
├── main.ts              # UI layer only
├── services/
│   ├── supabase.ts      # Data layer
│   ├── claude.ts        # AI integration
│   └── google-drive.ts  # External API
└── types/
    └── index.ts         # Shared types
```

**Lessons:**
- ✅ Start with TypeScript from day one
- ✅ Separate concerns early (UI, data, business logic)
- ✅ Create service layer for external dependencies
- ✅ Plan for migration path if rewrite needed

---

### 2. **Missing Collaboration in V1**
**Problem:** Built single-user app, users immediately asked for sharing
**Impact:** Required major schema refactor (v2.1.0)

**What Changed:**
```sql
-- V1: Single user only
CREATE TABLE events (
  id UUID PRIMARY KEY,
  user_id UUID,
  title TEXT
);

-- V2: Multi-user with RLS
CREATE TABLE events (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  timeline_id UUID REFERENCES timelines(id), -- ✅ Added
  title TEXT
);

CREATE TABLE shared_timelines ( -- ✅ New table
  timeline_id UUID,
  user_id UUID,
  permission_level TEXT
);
```

**Lessons:**
- ✅ Ask "Will users want to share?" before schema design
- ✅ Plan for multi-tenancy from start (even if not implemented)
- ✅ Use foreign keys and proper relations
- ✅ Design for Row Level Security (RLS) early

---

### 3. **Undo/Redo Not Persistent**
**Problem:** History lost on page reload (v2.0.3)
**Current State:** In-memory history stack (max 50 actions)

**Known Limitation:**
```typescript
// Cleared on reload ❌
let historyStack: HistoryAction[] = [];
let historyIndex = -1;

// TODO: Persist to LocalStorage
```

**Future Improvement:**
```typescript
// Save to LocalStorage
localStorage.setItem('undo_history', JSON.stringify(historyStack));

// Restore on load
historyStack = JSON.parse(localStorage.getItem('undo_history') || '[]');
```

**Lessons:**
- ✅ Document known limitations in changelog
- ✅ Mark TODOs for future enhancements
- ✅ Ship functional features even if not perfect
- ⚠️ Persistent undo history increases complexity (worth it?)

---

### 4. **AI API Key Client-Side Exposure**
**Problem:** Anthropic API key visible in browser bundle
**Security Risk:** Users can extract key and use our quota

**Current State:**
```typescript
// .env file (not in git) ✅
VITE_ANTHROPIC_API_KEY=sk-ant-api03-...

// But embedded in client bundle ❌
const ANTHROPIC_API_KEY = import.meta.env.VITE_ANTHROPIC_API_KEY;
```

**Better Solution (Future):**
```typescript
// Supabase Edge Function (server-side) ✅
export async function handleAIRequest(request: Request) {
  const apiKey = Deno.env.get('ANTHROPIC_API_KEY'); // Server-only
  const response = await fetch('https://api.anthropic.com/...', {
    headers: { 'x-api-key': apiKey }
  });
  return response;
}
```

**Lessons:**
- ⚠️ Client-side API keys are ALWAYS exposed
- ✅ Use server-side proxies for production
- ✅ Implement rate limiting per user
- ✅ Document security considerations in README

---

### 5. **Google Photos Import Initially Serverless**
**Problem:** Tried to import photos client-side, hit CORS issues
**Solution:** Moved to Supabase Edge Function

**Evolution:**
```typescript
// V1: Client-side (CORS errors) ❌
const response = await fetch(photo.baseUrl);
const blob = await response.blob();

// V2: Supabase Edge Function (works) ✅
const { data } = await supabase.functions.invoke('import-google-photos', {
  body: { photos: selectedPhotos }
});
```

**Lessons:**
- ❌ External APIs often block client-side requests
- ✅ Use edge functions for external API proxying
- ✅ Server-side can handle authentication tokens safely
- ✅ Start with edge function if API has CORS restrictions

---

## 🔄 Development Process Issues

### 1. **Autonomous Development Sessions**
**What Happened:** Claude worked overnight while user slept (v2.0.3, v2.6.0)

**Good Results:**
- ✅ Undo/redo feature completed (v2.0.3)
- ✅ AI timeline summary added (v2.6.0)
- ✅ All changes documented in session summaries
- ✅ Git commits properly tagged

**Challenges:**
- ⚠️ User needs to review and test after autonomous work
- ⚠️ Some features incomplete (collaboration UI pending)
- ⚠️ Need to align on priorities before autonomous sessions

**Lessons:**
- ✅ Autonomous mode works for well-defined features
- ✅ Document everything in session summaries
- ✅ Tag commits and update changelogs
- ⚠️ Get user approval before shipping to production

---

### 2. **Missing Testing Strategy**
**Current State:** Manual testing only, no automated tests

**What We're Missing:**
```typescript
// No unit tests ❌
// No integration tests ❌
// No E2E tests ❌

// Relying on manual testing:
// "Try signing up with test account"
// "Test undo/redo (Ctrl+Z)"
// "Create event with photo"
```

**Future Improvement:**
```typescript
// Vitest unit tests ✅
import { describe, it, expect } from 'vitest';
import { SupabaseService } from './supabase';

describe('SupabaseService', () => {
  it('creates event with valid data', async () => {
    const event = await supabase.createEvent({...});
    expect(event.id).toBeDefined();
  });
});

// Playwright E2E tests ✅
test('user can create and edit event', async ({ page }) => {
  await page.goto('/');
  await page.click('[data-testid="add-event"]');
  await page.fill('#title', 'Test Event');
  await page.click('[data-testid="save"]');
  expect(page.locator('.event-card')).toContainText('Test Event');
});
```

**Lessons:**
- ⚠️ Manual testing doesn't scale
- ✅ Add tests before features become complex
- ✅ Test edge cases (empty states, errors)
- ✅ Use data-testid attributes for stable selectors

---

### 3. **Version Management Best Practices**
**What Went Well:**
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Detailed CHANGELOG.md with version history
- ✅ Git tags for each release (`v2.0.3`, `v2.7.2`)
- ✅ Preserved v1 code in `/v1` folder

**Example from CHANGELOG.md:**
```markdown
## [2.0.3] - 2025-10-05
### ↶ Undo/Redo System
- Undo Operations: Ctrl+Z
- Redo Operations: Ctrl+Y
- Smart History: Max 50 actions
```

**Lessons:**
- ✅ Update CHANGELOG.md with every release
- ✅ Use git tags (`git tag v2.0.3`)
- ✅ Write release notes for users (what changed, why)
- ✅ Keep old versions accessible for reference

---

## 📊 Common Patterns & Anti-Patterns

### ❌ Anti-Patterns to Avoid

1. **Hardcoded Values**
   ```typescript
   // ❌ Bad
   const API_URL = 'http://localhost:3000';

   // ✅ Good
   const API_URL = import.meta.env.VITE_API_URL;
   ```

2. **Missing Error Handling**
   ```typescript
   // ❌ Bad
   const data = await fetch('/api/events').json();

   // ✅ Good
   try {
     const response = await fetch('/api/events');
     if (!response.ok) throw new Error('Fetch failed');
     const data = await response.json();
   } catch (error) {
     console.error('Failed to load:', error);
     showErrorMessage('Could not load events');
   }
   ```

3. **Assuming Success**
   ```typescript
   // ❌ Bad
   const user = supabase.getCurrentUser();
   renderApp(user.id); // Crashes if user is null

   // ✅ Good
   const user = supabase.getCurrentUser();
   if (!user) {
     redirectToLogin();
     return;
   }
   renderApp(user.id);
   ```

4. **Tight Coupling**
   ```typescript
   // ❌ Bad (UI directly calls Supabase)
   const { data } = await supabaseClient
     .from('events')
     .select('*');

   // ✅ Good (service layer)
   const events = await supabaseService.getEvents();
   ```

---

### ✅ Best Practices to Follow

1. **Defensive Programming**
   ```typescript
   // Always validate inputs
   function createEvent(title: string, date: string) {
     if (!title?.trim()) throw new Error('Title required');
     if (!isValidDate(date)) throw new Error('Invalid date');
     // ...
   }
   ```

2. **Graceful Degradation**
   ```typescript
   // Feature detection
   if (!('SpeechRecognition' in window)) {
     showMessage('Voice recording not supported in this browser');
     hideVoiceButton();
   }
   ```

3. **Progressive Enhancement**
   ```typescript
   // Core features work without AI
   if (ANTHROPIC_API_KEY) {
     enableAIFeatures();
   } else {
     console.warn('AI features disabled - add API key to enable');
   }
   ```

4. **Separation of Concerns**
   ```typescript
   // UI layer (main.ts)
   async function handleSaveEvent() {
     const event = getFormData();
     await eventService.save(event);
     renderTimeline();
   }

   // Data layer (supabase.ts)
   class EventService {
     async save(event: TimelineEvent) {
       return this.client.from('events').insert(event);
     }
   }
   ```

---

## 🚀 Key Takeaways by Category

### TypeScript & Type Safety
✅ Start with TypeScript from day one (migration is painful)
✅ Enable strict mode immediately
✅ Avoid generic names that conflict with DOM (Event, Response)
✅ Run `npm run build` before every deployment
✅ Use interfaces for all data structures

### Storage & Data
✅ LocalStorage for metadata (<5MB)
✅ IndexedDB for photos/large files (unlimited)
✅ Supabase for cloud sync and collaboration
✅ Design schema for multi-tenancy early
✅ Use Row Level Security (RLS) policies

### Authentication & Security
✅ Client-side API keys are always exposed
✅ Use Supabase Edge Functions for sensitive operations
✅ Add redirect URIs exactly (including .html)
✅ Test OAuth flows in production environment
✅ Implement rate limiting for AI features

### UI & UX
✅ Attach event listeners after DOM renders
✅ Destroy/recreate rich text editors on modal reopen
✅ Use `e.currentTarget` for reliable event handling
✅ Provide toast notifications instead of alerts
✅ Add undo/redo for destructive actions

### Development Process
✅ Document everything in CHANGELOG.md
✅ Write session summaries for async work
✅ Tag releases with semantic versioning
✅ Test locally before deploying
✅ Keep old versions accessible (v1/ folder)

### Error Handling
✅ Wrap initialization in try-catch
✅ Provide user-facing error messages
✅ Add retry/reload buttons for failures
✅ Log errors with context for debugging
✅ Test error states (network failures, bad data)

---

## 📈 Improvement Roadmap

### Short-Term (Next Sprint)
- [ ] Add Vitest unit tests for services
- [ ] Implement persistent undo history
- [ ] Move AI API calls to Edge Functions
- [ ] Add error boundary component
- [ ] Create testing checklist

### Medium-Term (Next Quarter)
- [ ] Add Playwright E2E tests
- [ ] Implement rate limiting for AI features
- [ ] Add performance monitoring
- [ ] Create CI/CD pipeline
- [ ] Add accessibility audit

### Long-Term (Future)
- [ ] Migrate to server-side API key management
- [ ] Add real-time collaboration sync
- [ ] Implement conflict resolution
- [ ] Add comprehensive logging
- [ ] Create developer documentation

---

## 🔗 Related Documentation

- [CHANGELOG.md](record-your-story/CHANGELOG.md) - Full version history
- [COLLABORATION.md](record-your-story/COLLABORATION.md) - Collaboration architecture
- [AI_FEATURES.md](record-your-story/AI_FEATURES.md) - AI implementation guide
- [RENDER_DEPLOYMENT.md](record-your-story/RENDER_DEPLOYMENT.md) - Deployment guide
- [SESSION_SUMMARY.md](record-your-story/SESSION_SUMMARY.md) - Autonomous session notes
- [AUTONOMOUS_SESSION_SUMMARY.md](record-your-story/AUTONOMOUS_SESSION_SUMMARY.md) - V2.6 work log

---

## 💡 Questions for Reflection

**For future projects, ask:**
1. Will users want to share/collaborate? (Design for multi-tenancy)
2. Will this need mobile support? (Mobile-first or responsive?)
3. What's the data size? (Choose appropriate storage)
4. Will this use external APIs? (Plan for Edge Functions)
5. Can we use TypeScript? (Always yes!)
6. What happens when it fails? (Error handling strategy)
7. How will we test this? (Testing strategy upfront)
8. Will this scale? (Performance considerations)

---

**Last Updated:** October 12, 2025
**Maintainer:** Claude + Human collaboration
**Status:** Living document - update after each major issue/fix

---

*"Those who cannot remember the past are condemned to repeat it."* - George Santayana

Let's learn from our mistakes and build better software together! 🚀
