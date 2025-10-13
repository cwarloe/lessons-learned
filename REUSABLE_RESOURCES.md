# Reusable Tools, Services & Code Templates

**Last Updated:** October 13, 2025

A catalog of proven tools, services, and code patterns that can be reused across future projects. Don't reinvent the wheel!

---

## 🛠️ Tools & Services (Proven Stack)

### Development & Deployment

| Tool/Service | Used In | Purpose | Cost | Recommendation |
|--------------|---------|---------|------|----------------|
| **Render** | Record Your Story | Static hosting, auto-deploy from Git | Free tier available | ⭐⭐⭐⭐⭐ Best for quick deploys |
| **Supabase** | Record Your Story | PostgreSQL + Auth + Storage + Edge Functions | Free tier generous | ⭐⭐⭐⭐⭐ Backend-as-a-service |
| **Vite** | Record Your Story | Build tool, dev server | Free | ⭐⭐⭐⭐⭐ Fast alternative to webpack |
| **Docker** | Knowledge Harvest | Containerization, local dev environment | Free | ⭐⭐⭐⭐⭐ For multi-service projects |
| **LocalStack** | Knowledge Harvest | Local AWS emulator (S3, etc) | Free tier | ⭐⭐⭐⭐ Test cloud services locally |

### Frontend Libraries

| Library | Used In | Purpose | Bundle Size | Recommendation |
|---------|---------|---------|-------------|----------------|
| **Quill.js** | Record Your Story | Rich text editor | ~150KB | ⭐⭐⭐⭐ Best WYSIWYG editor |
| **Quill** | Record Your Story | WYSIWYG text formatting | Medium | ⭐⭐⭐⭐ Production-ready |
| **jsPDF** | Record Your Story | Generate PDF exports | ~100KB | ⭐⭐⭐⭐ Client-side PDFs |
| **Anthropic SDK** | Record Your Story | Claude AI integration | ~50KB | ⭐⭐⭐⭐⭐ Best AI SDK |

### Backend & APIs

| Service | Used In | Purpose | Pricing | Recommendation |
|---------|---------|---------|---------|----------------|
| **Supabase Edge Functions** | Record Your Story | Serverless functions (Deno) | Pay per invocation | ⭐⭐⭐⭐⭐ For API keys |
| **PostgreSQL** | Record Your Story, KH | Relational database | Free (Supabase) | ⭐⭐⭐⭐⭐ Gold standard |
| **WebSocket (ws)** | Asteroids, Portal | Real-time communication | Free (library) | ⭐⭐⭐⭐⭐ For multiplayer |
| **Express** | Portal, KH | Web server framework | Free | ⭐⭐⭐⭐⭐ Node.js standard |

### Storage Solutions

| Solution | Capacity | Speed | Use Case | Recommendation |
|----------|----------|-------|----------|----------------|
| **LocalStorage** | 5-10MB | Instant | User settings, metadata | ⭐⭐⭐⭐⭐ For small data |
| **IndexedDB** | ~50% disk | Fast | Photos, large files locally | ⭐⭐⭐⭐⭐ Unlimited local |
| **Supabase Storage** | Unlimited | Medium | Cloud files with auth | ⭐⭐⭐⭐⭐ Easy setup |
| **S3 (AWS)** | Unlimited | Fast | Production file storage | ⭐⭐⭐⭐ Enterprise-grade |
| **LocalStack S3** | Limited | Fast | Local S3 testing | ⭐⭐⭐⭐ Dev environment |

### Developer Tools

| Tool | Used In | Purpose | Recommendation |
|------|---------|---------|----------------|
| **TypeScript** | Record Your Story | Type safety | ⭐⭐⭐⭐⭐ Use for all new projects |
| **localtunnel** | Asteroids | Expose localhost to internet | ⭐⭐⭐⭐ Alternative to ngrok |
| **ngrok** | (mentioned) | Expose localhost to internet | ⭐⭐⭐⭐ If npx works |
| **Chrome DevTools** | All | Debugging, performance | ⭐⭐⭐⭐⭐ Essential |

---

## 📦 Reusable Code Modules

### 1. Supabase Service Class (TypeScript)

**Source:** `record-your-story/src/services/supabase.ts` (481 lines)

**Provides:**
- ✅ Complete auth wrapper (sign up, sign in, OAuth, sign out)
- ✅ CRUD operations pattern
- ✅ Real-time subscriptions
- ✅ Collaboration/sharing system
- ✅ Photo storage methods
- ✅ Row-level security integration

**Copy to new project:**
```bash
cp record-your-story/src/services/supabase.ts new-project/src/services/
```

**Configuration:**
```typescript
// .env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

**Usage:**
```typescript
import { supabase } from '@/services/supabase';

// Auth
await supabase.signUp(email, password);
await supabase.signIn(email, password);
const user = await supabase.getCurrentUser();

// CRUD
await supabase.createEvent(event);
const { data } = await supabase.getEvents(timeline_id);
await supabase.updateEvent(id, updates);
await supabase.deleteEvent(id);

// Real-time
supabase.subscribeToEvents(timeline_id, (event) => {
  console.log('Event changed:', event);
});
```

**Adaptable for:**
- Any app needing authentication
- Multi-user applications
- Real-time collaborative apps
- Apps with photos/files

---

### 2. Toast Notification System

**Source:** Implemented in Record Your Story and Asteroids

**Code Template:**
```typescript
// toast.ts - Reusable notification system
export function showToast(
  message: string,
  type: 'success' | 'error' | 'info' = 'info',
  duration: number = 3000
): void {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  // Styling
  toast.style.cssText = `
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 10000;
    font-size: 14px;
    font-weight: 500;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  `;

  document.body.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
  });

  // Auto dismiss
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
```

**Usage:**
```typescript
// Success
showToast('Event saved successfully!', 'success');

// Error
showToast('Failed to save event', 'error');

// Info
showToast('Syncing with server...', 'info', 5000);
```

**Better than:** `alert()`, `confirm()` (blocking, ugly)

---

### 3. IndexedDB Helper (Hybrid Storage)

**Source:** Record Your Story storage pattern

**Code Template:**
```typescript
// indexedDB.ts - Photo/file storage
export class IndexedDBHelper {
  private dbName: string;
  private dbVersion: number;

  constructor(dbName: string = 'AppStorage', version: number = 1) {
    this.dbName = dbName;
    this.dbVersion = version;
  }

  async openDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Create object stores
        if (!db.objectStoreNames.contains('photos')) {
          db.createObjectStore('photos', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('files')) {
          db.createObjectStore('files', { keyPath: 'id' });
        }
      };
    });
  }

  async savePhoto(id: string, blob: Blob, metadata?: any): Promise<void> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['photos'], 'readwrite');
      const store = transaction.objectStore('photos');

      const request = store.put({
        id,
        blob,
        metadata,
        timestamp: Date.now()
      });

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getPhoto(id: string): Promise<Blob | null> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['photos'], 'readonly');
      const store = transaction.objectStore('photos');
      const request = store.get(id);

      request.onsuccess = () => {
        const result = request.result;
        resolve(result ? result.blob : null);
      };
      request.onerror = () => reject(request.error);
    });
  }

  async deletePhoto(id: string): Promise<void> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['photos'], 'readwrite');
      const store = transaction.objectStore('photos');
      const request = store.delete(id);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getAllPhotos(): Promise<any[]> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['photos'], 'readonly');
      const store = transaction.objectStore('photos');
      const request = store.getAll();

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
}

// Export singleton
export const storage = new IndexedDBHelper();
```

**Usage:**
```typescript
import { storage } from '@/services/indexedDB';

// Save photo
const photoId = `photo-${Date.now()}`;
await storage.savePhoto(photoId, photoBlob, { eventId: '123' });

// Retrieve photo
const blob = await storage.getPhoto(photoId);
if (blob) {
  const url = URL.createObjectURL(blob);
  imgElement.src = url;
}

// Delete photo
await storage.deletePhoto(photoId);
```

**Use for:**
- Photo storage (unlimited)
- Video files
- Audio recordings
- Large documents
- Any file >1MB

---

### 4. WebSocket Connection Manager

**Source:** Asteroids game pattern

**Code Template:**
```typescript
// websocket.ts - Robust WebSocket with reconnection
export class WebSocketManager {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  private messageHandlers: Map<string, Function[]> = new Map();

  constructor(path: string = '/ws') {
    // ✅ Dynamic URL (not hardcoded)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    this.url = `${protocol}//${window.location.host}${path}`;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            // ✅ Always wrap JSON.parse in try-catch
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
            console.error('Raw message:', event.data);
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };

        this.ws.onclose = () => {
          console.log('WebSocket disconnected');
          this.attemptReconnect();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})...`);

    setTimeout(() => {
      this.connect().catch(error => {
        console.error('Reconnection failed:', error);
      });
    }, delay);
  }

  send(type: string, data: any): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket not connected');
      return;
    }

    try {
      this.ws.send(JSON.stringify({ type, ...data }));
    } catch (error) {
      console.error('Failed to send WebSocket message:', error);
    }
  }

  on(type: string, handler: Function): void {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type)!.push(handler);
  }

  private handleMessage(data: any): void {
    const handlers = this.messageHandlers.get(data.type);
    if (handlers) {
      handlers.forEach(handler => handler(data));
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

**Usage:**
```typescript
const ws = new WebSocketManager('/game');
await ws.connect();

// Listen for messages
ws.on('gameState', (data) => {
  console.log('Game state:', data);
});

ws.on('playerJoined', (data) => {
  showToast(`${data.playerName} joined!`, 'info');
});

// Send messages
ws.send('input', { keys: { left: true, up: false } });
```

**Features:**
- ✅ Automatic reconnection with exponential backoff
- ✅ Dynamic URL (works in dev and prod)
- ✅ Error handling (JSON.parse wrapped)
- ✅ Type-based message routing

---

### 5. Undo/Redo System

**Source:** Record Your Story

**Code Template:**
```typescript
// history.ts - Undo/Redo system
interface HistoryAction<T = any> {
  type: string;
  before: T | null;
  after: T | null;
  timestamp: number;
}

export class HistoryManager<T = any> {
  private stack: HistoryAction<T>[] = [];
  private index: number = -1;
  private maxSize: number = 50;

  push(type: string, before: T | null, after: T | null): void {
    // Remove any redo actions after current index
    this.stack.splice(this.index + 1);

    // Add new action
    this.stack.push({
      type,
      before,
      after,
      timestamp: Date.now()
    });

    this.index++;

    // Limit stack size
    if (this.stack.length > this.maxSize) {
      this.stack.shift();
      this.index--;
    }
  }

  canUndo(): boolean {
    return this.index >= 0;
  }

  canRedo(): boolean {
    return this.index < this.stack.length - 1;
  }

  undo(): HistoryAction<T> | null {
    if (!this.canUndo()) return null;

    const action = this.stack[this.index];
    this.index--;
    return action;
  }

  redo(): HistoryAction<T> | null {
    if (!this.canRedo()) return null;

    this.index++;
    const action = this.stack[this.index];
    return action;
  }

  clear(): void {
    this.stack = [];
    this.index = -1;
  }

  getStack(): readonly HistoryAction<T>[] {
    return this.stack;
  }
}
```

**Usage:**
```typescript
interface Event {
  id: string;
  title: string;
  description: string;
}

const history = new HistoryManager<Event>();

// Track changes
function updateEvent(id: string, updates: Partial<Event>) {
  const before = getEvent(id);
  const after = { ...before, ...updates };

  // Save to database
  saveEvent(after);

  // Track in history
  history.push('update', before, after);
}

// Undo (Ctrl+Z)
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
    const action = history.undo();
    if (action && action.before) {
      saveEvent(action.before);  // Restore previous state
      showToast('Undone', 'info');
    }
  }

  // Redo (Ctrl+Y or Ctrl+Shift+Z)
  if ((e.ctrlKey && e.key === 'y') || (e.ctrlKey && e.shiftKey && e.key === 'z')) {
    const action = history.redo();
    if (action && action.after) {
      saveEvent(action.after);  // Restore next state
      showToast('Redone', 'info');
    }
  }
});
```

**Use for:**
- Text editors
- Drawing applications
- Data entry forms
- Any destructive actions

---

### 6. Debounce Helper

**Source:** Record Your Story search

**Code Template:**
```typescript
// debounce.ts - Prevent excessive function calls
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number = 300
): (...args: Parameters<T>) => void {
  let timeoutId: number;

  return function(this: any, ...args: Parameters<T>) {
    clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}
```

**Usage:**
```typescript
import { debounce } from '@/utils/debounce';

// Search input - only search after user stops typing
const debouncedSearch = debounce(async (query: string) => {
  const results = await searchEvents(query);
  renderResults(results);
}, 300);

searchInput.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});

// Window resize - only update layout after resize stops
const debouncedResize = debounce(() => {
  updateLayout();
}, 150);

window.addEventListener('resize', debouncedResize);
```

**Prevents:**
- Excessive API calls
- Layout thrashing
- Performance issues

---

### 7. Canvas DPI Scaling Helper

**Source:** Asteroids game

**Code Template:**
```typescript
// canvas.ts - High-DPI rendering
export function setupCanvas(canvas: HTMLCanvasElement): CanvasRenderingContext2D {
  const ctx = canvas.getContext('2d')!;
  const dpr = window.devicePixelRatio || 1;

  // Get CSS size
  const rect = canvas.getBoundingClientRect();

  // Set display size (CSS pixels)
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';

  // Set actual size in memory (scaled by DPR)
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;

  // Scale all drawing operations by DPR
  ctx.scale(dpr, dpr);

  return ctx;
}

export function resizeCanvas(canvas: HTMLCanvasElement, ctx: CanvasRenderingContext2D): void {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  // Only resize if size changed
  if (canvas.width !== rect.width * dpr || canvas.height !== rect.height * dpr) {
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    // Reapply scale after resize
    ctx.scale(dpr, dpr);
  }
}
```

**Usage:**
```typescript
const canvas = document.getElementById('game') as HTMLCanvasElement;
const ctx = setupCanvas(canvas);

// Handle resize
window.addEventListener('resize', () => {
  resizeCanvas(canvas, ctx);
});

// Draw (use CSS pixel coordinates, scaling handled automatically)
ctx.fillRect(10, 10, 100, 100);  // Sharp on Retina/4K displays
```

**Fixes:** Blurry canvas on high-DPI displays (Retina, 4K)

---

## 🏗️ Architecture Patterns

### Pattern 1: Service Layer (TypeScript)

**Used In:** Record Your Story
**Structure:**
```
src/
├── main.ts                 # UI layer (DOM manipulation, events)
├── services/
│   ├── supabase.ts        # Data access layer
│   ├── claude.ts          # AI service layer
│   ├── google-drive.ts    # External API layer
│   └── events.ts          # Business logic layer
└── types/
    └── index.ts           # Shared types
```

**Benefits:**
- ✅ Clear separation of concerns
- ✅ Easy to test each layer independently
- ✅ Reusable services across features
- ✅ Type safety with TypeScript

---

### Pattern 2: Hybrid Storage (3-Tier)

**Used In:** Record Your Story
**Architecture:**
```
[User Action]
     ↓
[LocalStorage] ← Fast access, metadata (<5MB)
     ↓
[IndexedDB] ← Large files, unlimited
     ↓
[Supabase/Cloud] ← Multi-device sync, backup
```

**Implementation:**
```typescript
// Save event
async function saveEvent(event: Event, photos: Blob[]) {
  // Tier 1: Save metadata to LocalStorage (instant UI)
  const metadata = { ...event, photoIds: [] };
  localStorage.setItem(`event-${event.id}`, JSON.stringify(metadata));

  // Tier 2: Save photos to IndexedDB (fast, unlimited)
  for (const photo of photos) {
    const photoId = `${event.id}-${Date.now()}`;
    await storage.savePhoto(photoId, photo);
    metadata.photoIds.push(photoId);
  }

  // Tier 3: Sync to cloud (background, can fail)
  try {
    await supabase.createEvent(event);
    for (const photo of photos) {
      await supabase.storage.from('photos').upload(photoId, photo);
    }
  } catch (error) {
    console.warn('Cloud sync failed, will retry later', error);
    // Queue for retry
  }
}
```

---

### Pattern 3: Event Delegation (Dynamic DOM)

**Used In:** Record Your Story
**Pattern:**
```typescript
// ❌ WRONG: Attach to elements directly
document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.addEventListener('click', handleEdit);
});
// Won't work for future buttons!

// ✅ CORRECT: Attach to parent container
document.getElementById('timeline')!.addEventListener('click', (e) => {
  const target = e.target as HTMLElement;

  // Check what was clicked
  if (target.classList.contains('edit-btn')) {
    const eventId = target.closest('[data-event-id]')?.dataset.eventId;
    handleEdit(eventId);
  }

  if (target.classList.contains('delete-btn')) {
    const eventId = target.closest('[data-event-id]')?.dataset.eventId;
    handleDelete(eventId);
  }
});
```

**Benefits:**
- Works with dynamically added content
- Only one event listener (performance)
- No need to re-attach after re-renders

---

## 📝 Configuration Templates

### 1. Vite + TypeScript Project

**Files to copy from Record Your Story:**
```bash
# Core config
vite.config.ts
tsconfig.json
package.json (dependencies section)

# Environment
.env.example
```

**vite.config.ts template:**
```typescript
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

**tsconfig.json template:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

---

### 2. Render Deployment

**render.yaml template:**
```yaml
services:
  - type: web
    name: your-app-name
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    headers:
      - path: /*
        name: Cache-Control
        value: public, max-age=31536000, immutable
      - path: /
        name: Cache-Control
        value: no-cache
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

**Auto-deploy from Git:**
1. Connect GitHub repo
2. Add `render.yaml` to root
3. Set environment variables in Render dashboard
4. Push to trigger deploy

---

### 3. Supabase Project Setup

**Schema template (PostgreSQL):**
```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends auth.users)
CREATE TABLE public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own profile"
  ON public.users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.users FOR UPDATE
  USING (auth.uid() = id);
```

**Environment variables:**
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

---

### 4. Docker Compose (Multi-Service)

**Template from Knowledge Harvest:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  localstack:
    image: localstack/localstack
    environment:
      SERVICES: s3
      DEFAULT_REGION: us-east-1
    ports:
      - "4566:4566"

  api:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://app:password@postgres:5432/appdb
      AWS_ENDPOINT: http://localstack:4566
    depends_on:
      - postgres
      - localstack

  web:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - api

volumes:
  postgres_data:
```

---

## 🎯 Decision Matrix: Choose the Right Tool

### When to use each storage?

| Data Type | Size | Sync Needed | Recommendation |
|-----------|------|-------------|----------------|
| User settings | <1KB | No | LocalStorage |
| User preferences | <5KB | Yes | LocalStorage + sync to Supabase |
| Form data | <100KB | No | LocalStorage |
| Photos (local) | 1-10MB | No | IndexedDB |
| Photos (cloud) | Any | Yes | Supabase Storage or S3 |
| Videos | >10MB | Yes | S3 with CDN |
| Database records | Any | Yes | Supabase (PostgreSQL) |

### When to use each deployment platform?

| Platform | Best For | Free Tier | Recommendation |
|----------|----------|-----------|----------------|
| **Render** | Static sites, auto-deploy | 100GB bandwidth | ⭐⭐⭐⭐⭐ Quick projects |
| **Netlify** | Static sites, serverless | 100GB bandwidth | ⭐⭐⭐⭐⭐ Similar to Render |
| **Vercel** | Next.js, React | 100GB bandwidth | ⭐⭐⭐⭐ If using Next.js |
| **Railway** | Full-stack, databases | $5 credit/month | ⭐⭐⭐⭐ Need database |
| **Fly.io** | Docker apps | 3 VMs | ⭐⭐⭐⭐ Complex apps |
| **Supabase** | PostgreSQL + backend | 500MB DB | ⭐⭐⭐⭐⭐ Need auth/DB |

---

## ⚡ Quick Start Templates

### New TypeScript + Vite Project
```bash
# Create project
npm create vite@latest my-app -- --template vanilla-ts
cd my-app

# Copy reusable services
cp ../lessons-learned/templates/supabase.ts src/services/
cp ../lessons-learned/templates/toast.ts src/utils/
cp ../lessons-learned/templates/indexedDB.ts src/services/

# Install common dependencies
npm install @supabase/supabase-js

# Setup environment
cp .env.example .env
# Edit .env with your keys

# Start dev server
npm run dev
```

### New WebSocket Game
```bash
# Server
npm init -y
npm install express ws

# Copy WebSocket manager
cp ../lessons-learned/templates/websocket-server.js server.js
cp ../lessons-learned/templates/websocket-client.ts client.ts

# Start
node server.js
```

---

## 📚 Learning Resources

### Supabase
- Docs: https://supabase.com/docs
- Auth Guide: https://supabase.com/docs/guides/auth
- Row Level Security: https://supabase.com/docs/guides/auth/row-level-security

### Vite
- Getting Started: https://vitejs.dev/guide/
- Config Reference: https://vitejs.dev/config/

### IndexedDB
- MDN Guide: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API

### WebSocket
- MDN WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

---

## 🔄 Next Steps

**When starting a new project:**
1. ✅ Review this document first
2. ✅ Choose appropriate tools from decision matrix
3. ✅ Copy relevant code templates
4. ✅ Adapt configuration files
5. ✅ Don't reinvent the wheel!

**When you discover a new reusable pattern:**
1. Document it in this file
2. Extract it into a template
3. Add usage examples
4. Update decision matrices
5. Commit to lessons-learned repo

---

**Status:** Living document - update as new tools/patterns are discovered
