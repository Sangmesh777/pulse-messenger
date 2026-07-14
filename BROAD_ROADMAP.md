# Pulse Messenger — Premium Product Roadmap
> **Roadmap set:** [Clean implementation path](ROADMAP.md) · [Broad product vision](BROAD_ROADMAP.md) · [Master premium features](MASTER_FEATURE_PLAN.md)


## Product vision

Build Pulse into a fast, private, polished messenger for one-to-one conversations, groups, communities, and reliable communication across mobile and desktop.

> The current release is a working prototype. It uses in-memory sessions, JSON message storage, and short polling. These are suitable for validation—not a secure, scalable production messenger.

## Guiding principles

1. **Reliability first** — delivery state must always be clear.
2. **Privacy by design** — collect the minimum data and protect it.
3. **Fast everywhere** — excellent on weak mobile networks.
4. **Simple, premium interface** — minimal friction and consistent design.
5. **Accessible by default** — keyboard, screen-reader, contrast, and motion support.

---

## Phase 0 — Stabilize the prototype

**Target: 1 week**

- Add health, readiness, and version endpoints.
- Add structured server logs and error tracking.
- Add request validation, payload limits, rate limits, and secure headers.
- Add automated tests for joining, sending, reconnecting, rooms, and malformed requests.
- Add CI checks on every GitHub pull request.
- Show connection states: connecting, live, reconnecting, offline, failed.
- Add optimistic sending with retry and failed-message indicators.
- Stop relying on Render's ephemeral filesystem for permanent history.

**Exit criteria**

- Core message tests pass consistently.
- Errors are observable.
- A failed network request never silently loses a message.

---

## Phase 1 — Real accounts and durable data

**Target: 2–3 weeks**

### Backend

- Move to **FastAPI (Python)** with native WebSockets.
- Use **PostgreSQL** for users, conversations, memberships, and messages.
- Use **Redis** for presence, typing state, pub/sub, and temporary session data.
- Add database migrations, indexes, pagination, backups, and retention controls.
- Use UUID/ULID message IDs and server timestamps.

### Identity and safety

- Email/password registration and login.
- Secure password hashing with Argon2.
- Email verification and password reset.
- Signed, expiring sessions with refresh rotation.
- Logout from individual or all devices.
- Usernames, display names, avatars, and profiles.
- Block and report controls.

### Messaging foundation

- Direct conversations and private groups.
- Conversation membership authorization on every request.
- Delivery states: sending, sent, delivered, read, failed.
- Unread counts and last-read positions.
- Message history pagination and reliable reconnect sync.

**Exit criteria**

- Users cannot access conversations they do not belong to.
- Messages survive restarts and deployments.
- Multiple server instances deliver the same events through Redis.

---

## Phase 2 — Premium messaging experience

**Target: 3–4 weeks**

- Replies, reactions, editing, deletion, forwarding, and copy actions.
- Attach images, video, audio, PDFs, and documents.
- Object storage with signed uploads, validation, size limits, and malware scanning.
- Image thumbnails, video previews, upload progress, cancel, and retry.
- Voice notes with waveform and playback speed.
- Search conversations and messages.
- Pinned, saved, and starred messages.
- Mentions, typing indicators, read receipts, and presence privacy.
- Group admins, roles, invite links, member controls, and leave/remove actions.
- Message drafts stored per conversation.
- Emoji picker and rich link previews.
- Light/dark/system themes and adjustable text size.
- Responsive desktop sidebar and premium mobile navigation.
- Accessible focus states, labels, reduced motion, and keyboard shortcuts.

**Exit criteria**

- Complete daily-use feature set.
- Smooth behavior on low-bandwidth mobile connections.
- WCAG 2.2 AA accessibility review completed.

---

## Phase 3 — Notifications and installable apps

**Target: 2–3 weeks**

- Progressive Web App with install prompt and offline shell.
- Web push notifications with per-conversation controls.
- Notification grouping, mute durations, and quiet hours.
- Background sync for pending messages.
- Offline message queue and reconnect reconciliation.
- Multi-device sessions and device management.
- Optional email notification summaries.

**Exit criteria**

- Users receive notifications when Pulse is closed.
- Pending messages recover cleanly after network loss.
- Installable experience passes PWA checks.

---

## Phase 4 — Calls and richer communication

**Target: 4–6 weeks**

- One-to-one voice and video calls using WebRTC.
- TURN/STUN infrastructure for reliable connectivity.
- Incoming call screen, mute, camera switch, speaker selection, and call history.
- Group calls after one-to-one reliability is proven.
- Screen sharing on supported devices.
- Optional disappearing messages and scheduled messages.

**Exit criteria**

- Calls work across major browsers and mobile networks.
- Connection quality and failure metrics are observable.

---

## Phase 5 — Trust, privacy, and scale

**Target: ongoing**

### Security

- Threat modeling and independent security review.
- CSRF/XSS/SQL injection protections and strict Content Security Policy.
- Abuse controls, IP/user rate limiting, spam detection, and moderation queues.
- Audit log for sensitive account and admin actions.
- Encrypted transport, encrypted backups, secret rotation, and least-privilege access.
- Optional end-to-end encryption only after a proven protocol and expert review—never custom cryptography.

### Reliability

- Load testing for concurrent sockets and message throughput.
- Redis-backed WebSocket fan-out and horizontal scaling.
- Database replicas, point-in-time recovery, and tested restore procedures.
- Idempotent message submission and duplicate suppression.
- Metrics for latency, delivery failures, reconnects, and active users.
- Service-level objectives and incident response runbooks.

### Compliance

- Privacy policy, terms, cookie policy, and community guidelines.
- Account export and deletion.
- Data retention and moderation policies.
- Age and regional compliance review before public launch.

---

## Recommended Python architecture

```text
Browser / PWA
     |
HTTPS + WebSocket
     |
FastAPI application
  |       |       |
Postgres  Redis   Object storage
(users,   (pubsub, (media and files)
chats,    presence,
messages) queues)
```

### Suggested components

- **API/realtime:** FastAPI + Uvicorn
- **Database:** PostgreSQL + SQLAlchemy + Alembic
- **Realtime scale:** Redis pub/sub
- **Background jobs:** Celery or Dramatiq
- **Files:** S3-compatible object storage
- **Testing:** Pytest + Playwright
- **Observability:** Sentry + structured logs + uptime monitoring
- **Deployment:** Render web service, managed PostgreSQL, and managed Redis

---

## Core data model

- `users`
- `user_sessions`
- `conversations`
- `conversation_members`
- `messages`
- `message_receipts`
- `message_reactions`
- `attachments`
- `blocks`
- `reports`
- `notification_preferences`

Every message should include a stable ID, conversation ID, sender ID, server timestamp, optional client-generated idempotency key, edit timestamp, and deletion state.

---

## Product design system

- Define Pulse colors, typography, spacing, radii, shadows, iconography, and motion tokens.
- Build reusable components for buttons, inputs, dialogs, message bubbles, menus, avatars, toasts, and empty states.
- Design every state: loading, empty, offline, error, disabled, sending, delivered, read, and failed.
- Test at 320px mobile width through large desktop displays.
- Keep the interface calm and neutral; use color primarily for status and action.

---

## Testing strategy

- Unit tests for authorization and message rules.
- API integration tests against PostgreSQL and Redis.
- Two-browser end-to-end tests for delivery, receipts, typing, reconnect, and blocking.
- Mobile viewport and weak-network tests.
- Security, accessibility, load, backup-restore, and migration tests.
- Staged deployments with automatic rollback on failed health checks.

---

## Release milestones

| Milestone | Outcome |
|---|---|
| **0.2 Reliable Prototype** | Tests, retries, monitoring, secure request handling |
| **0.5 Private Beta** | Accounts, direct/group chats, Postgres, Redis, WebSockets |
| **0.7 Premium Beta** | Attachments, replies, reactions, search, polished UX |
| **0.9 Release Candidate** | PWA, notifications, offline recovery, moderation |
| **1.0 Public Launch** | Security review, backups, observability, policies, load-tested scale |
| **1.5 Communication Suite** | Voice/video calls, screen sharing, advanced privacy |

---

## Metrics that matter

- Successful message delivery rate
- P50/P95 send-to-receive latency
- Reconnect success rate
- Crash/error-free sessions
- Daily/weekly active users
- Messages per active user
- Day-1, Day-7, and Day-30 retention
- Notification opt-in and open rates
- Abuse report response time

Avoid optimizing vanity metrics before reliability and retention.

---

## Immediate next sprint

1. Replace JSON persistence with PostgreSQL.
2. Introduce real accounts and conversation membership authorization.
3. Replace short polling with authenticated FastAPI WebSockets.
4. Add Redis-backed presence and multi-instance event delivery.
5. Add message IDs, optimistic UI, retry, delivery state, and reconnect synchronization.
6. Add Pytest and two-browser Playwright tests in GitHub Actions.
7. Add monitoring, rate limiting, and secure headers.

This sprint transforms Pulse from a public-room prototype into the foundation of a genuine production messenger.


## Complete high-end feature catalog

See [MASTER_FEATURE_PLAN.md](MASTER_FEATURE_PLAN.md) for the full Telegram/WhatsApp-class feature universe and original Pulse signature features.
