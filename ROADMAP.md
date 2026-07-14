# Pulse Messenger — Product Roadmap
> **Roadmap set:** [Clean implementation path](ROADMAP.md) · [Broad product vision](BROAD_ROADMAP.md) · [Master premium features](MASTER_FEATURE_PLAN.md)


## 1. Product goal

**Pulse will be a fast, private, mobile-first messenger for direct chats and small groups.**

The product should feel simple like WhatsApp, responsive like Telegram, and polished enough to use every day. Pulse should first become excellent at reliable text messaging before adding calls, communities, AI, or other advanced features.

### Core promise

> Open Pulse, find a person, and send a message that arrives quickly and reliably on any device.

### Target users

- Friends and families
- Students and small communities
- Small teams that need lightweight private chat
- Mobile users on slow or unstable networks

### Product principles

1. **Messages must never disappear silently.**
2. **Private conversations must actually be private.**
3. **The interface must remain simple as features grow.**
4. **Mobile performance comes before decorative effects.**
5. **Security and moderation are launch requirements, not later extras.**

---

## 2. Current state — v0.2

Pulse currently supports:

- Public room-based chat
- Real-time-style message updates
- Online user list
- Typing indicators
- Mobile and desktop layouts
- Connection and send status
- Rate limiting and secure response headers
- Health/version endpoints
- Automated Python regression tests
- Public Render deployment

### Current limitations

- No registered user accounts
- Anyone who knows a room name can enter it
- Messages are stored in a local JSON file
- Render can erase local message history during restart or deployment
- Sessions and presence exist only in one server process
- Short polling is used instead of WebSockets
- No private direct messages or conversation authorization
- No attachments, notifications, read receipts, or moderation system

**Do not market the current build as a secure private messenger. It is a public-room prototype.**

---

# 3. Release path

## Release 0.3 — Reliable room chat

**Goal:** Make the current public-room app dependable while the production backend is prepared.

### Features

- Automatic session recovery after temporary disconnects
- Optimistic message bubbles with `Sending`, `Sent`, and `Failed` states
- Tap-to-retry for failed messages
- Duplicate-message prevention using client message IDs
- Better empty, loading, offline, and error screens
- Join/leave notifications that do not interrupt message reading
- Copy message action
- Clear chat locally
- Room invite link with encoded room name
- App version visible in settings/about

### Engineering

- Expand tests for reconnects, duplicates, room separation, rate limits, and invalid sessions
- Add uptime monitoring and error tracking
- Add deployment smoke test after every release
- Add structured JSON logs without storing message contents
- Document backup and rollback procedure

### Done when

- Two users can chat for 30 minutes across mobile networks without silent loss
- Failed messages can be retried
- Reconnect tests pass consistently
- Every deployment is automatically tested

---

## Release 0.5 — Private beta foundation

**Goal:** Replace anonymous public rooms with secure accounts and durable private conversations.

### New user features

- Sign up, sign in, sign out
- Username, display name, profile photo, and bio
- Email verification
- Forgot/reset password
- Direct one-to-one chats
- Private group chats
- Conversation list with last message and unread count
- Create group, rename group, add/remove members, leave group
- Search users by exact username
- Profile and account settings
- Log out from all devices

### Backend migration

- Move API to **FastAPI (Python)**
- Replace short polling with authenticated **WebSockets**
- Add **PostgreSQL** for users, conversations, memberships, messages, and receipts
- Add **Redis** for presence, typing, WebSocket fan-out, and temporary state
- Add Alembic database migrations
- Add secure password hashing with Argon2
- Add expiring access sessions and rotating refresh sessions
- Authorize conversation membership on every message request

### Essential data tables

- `users`
- `sessions`
- `conversations`
- `conversation_members`
- `messages`
- `message_receipts`
- `blocks`
- `reports`

### Done when

- Messages survive deployments and restarts
- A user cannot read or send to a conversation they do not belong to
- Two server instances deliver the same events through Redis
- Account, authorization, and message tests pass

---

## Release 0.7 — Premium messaging beta

**Goal:** Deliver the everyday features expected from a modern messenger.

### Messaging

- Delivered and read receipts
- Reply to message
- Emoji reactions
- Edit sent message
- Delete for me / delete for everyone
- Forward message
- Pin and star messages
- Message search
- Date separators and unread divider
- Draft saved per conversation
- @mentions in groups
- Mute conversation

### Media

- Image and document uploads
- Upload progress, cancel, and retry
- Image preview and compression
- Video thumbnail and playback
- Voice notes with duration, waveform, and playback speed
- File validation, size limits, signed URLs, and malware scanning
- S3-compatible object storage; never store uploads on Render’s local disk

### Premium interface

- Redesigned conversation list
- Modern message bubbles and grouped messages
- Smooth but subtle transitions
- Light, dark, and system themes
- Adjustable text size
- Emoji picker
- Keyboard shortcuts on desktop
- Full keyboard and screen-reader support
- WCAG 2.2 AA color contrast and focus states

### Done when

- Core text and media messaging works on mobile and desktop
- Weak-network tests pass
- Upload failures recover without losing the draft
- Accessibility review passes

---

## Release 0.9 — Installable and notification-ready

**Goal:** Make Pulse behave like a real installed messaging app.

### Features

- Progressive Web App installation
- Web push notifications
- Notification permission education screen
- Per-conversation notification settings
- Mute for 1 hour, 8 hours, 1 week, or forever
- Quiet hours
- Offline app shell
- Offline outgoing message queue
- Background retry after reconnection
- Multi-device sessions and device list
- Unread badge count
- Deep links that open the correct conversation

### Done when

- A user receives notifications while Pulse is closed
- Pending messages recover after network loss
- Pulse is installable on Android and desktop
- Device sessions can be reviewed and revoked

---

## Release 1.0 — Safe public launch

**Goal:** Launch a trustworthy messenger, not only a feature-rich demo.

### Safety and moderation

- Block and unblock users
- Report user, message, or group
- Spam and abuse rate limits
- Admin moderation dashboard
- Account suspension and appeal process
- Group admin roles and permissions
- Invite-link expiration and revocation
- Privacy controls for presence, read receipts, and profile visibility

### Security

- Independent security review
- Threat model for accounts, sessions, chat access, uploads, and abuse
- Strict Content Security Policy
- Encrypted HTTPS transport and encrypted managed backups
- Secret rotation and least-privilege service credentials
- Audit log for security-sensitive actions
- Backup restore test
- Dependency and vulnerability scanning

### Legal and operations

- Privacy policy
- Terms of service
- Community guidelines
- Data export
- Account and data deletion
- Retention policy
- Incident response plan
- Status page and support contact

### Scale and reliability

- Load tests for concurrent WebSockets and message throughput
- Idempotent message creation and duplicate suppression
- Database indexes and pagination
- Redis-backed horizontal scaling
- Point-in-time database recovery
- Monitoring for latency, failures, reconnects, and queue depth
- Defined service-level objectives

### Done when

- Security and privacy launch checklist passes
- Backups can be restored
- Abuse reports have an operational response path
- Load test meets launch targets
- Production monitoring and alerts are active

---

## Release 1.2 — Groups and communities

**Goal:** Support larger social spaces without damaging the simplicity of direct chat.

### Features

- Group roles: owner, admin, moderator, member
- Join requests and approval
- Public/private group discovery controls
- Announcement-only mode
- Polls
- Events and reminders
- Topics or threads for larger groups
- Shared media and file gallery
- Group analytics for administrators
- Strong anti-spam and slow-mode controls

**Rule:** Build this only after direct and small-group chat is stable.

---

## Release 1.5 — Voice and video

**Goal:** Add reliable calling after messaging quality is proven.

### Features

- One-to-one voice calls
- One-to-one video calls
- Incoming call screen
- Mute, camera toggle, speaker selection, and camera switch
- Call history and missed-call notifications
- Network quality indicator
- Group calls after one-to-one calls are stable
- Screen sharing on supported browsers

### Engineering

- WebRTC
- Managed or self-hosted STUN/TURN
- Call signaling through authenticated WebSockets
- Call quality metrics without recording call content

### Done when

- Calls work across major browsers, Wi-Fi, and mobile networks
- TURN fallback is tested
- Permission and call-failure states are understandable

---

## Release 2.0 — Advanced privacy and intelligence

**Goal:** Add advanced capabilities carefully without weakening trust.

### Possible features

- Disappearing messages
- Scheduled messages
- Chat archive and folders
- Username-based contact without exposing email
- Optional encrypted backups
- End-to-end encryption only using a proven, independently reviewed protocol
- Optional on-device transcription for voice notes
- Optional AI summaries for groups, strictly opt-in and privacy-reviewed

**Do not invent custom encryption. Do not send private chat content to AI services by default.**

---

# 4. Clean technical path

## Recommended architecture

```text
Mobile/Desktop PWA
        |
 HTTPS + authenticated WebSocket
        |
 FastAPI application
   |          |            |
PostgreSQL   Redis     Object storage
accounts,    presence, media and files
chats,       pub/sub,
messages     queues
```

### Recommended stack

- Frontend: current HTML/CSS/JavaScript, later modularized with Vite if needed
- Backend: FastAPI + Uvicorn
- Database: PostgreSQL + SQLAlchemy + Alembic
- Realtime: WebSockets + Redis pub/sub
- Background work: Dramatiq or Celery
- Media: S3-compatible object storage
- Tests: Pytest + Playwright two-browser tests
- Monitoring: Sentry, structured logs, uptime checks
- Hosting: Render web service + managed PostgreSQL + managed Redis

### Migration order

1. Design database schema
2. Add PostgreSQL and migrations
3. Add accounts and sessions
4. Add private conversation authorization
5. Store and paginate messages in PostgreSQL
6. Introduce WebSockets
7. Add Redis presence and cross-instance fan-out
8. Migrate the interface to the new APIs
9. Run both systems in staging
10. Switch production after migration tests pass

---

# 5. Feature priority rules

Use this order when deciding what to build:

1. Security and access control
2. Message durability
3. Delivery reliability
4. Direct and group conversation basics
5. Notifications and offline behavior
6. Media and premium interface
7. Moderation and scale
8. Calls and advanced features

### Do not build yet

- AI chat features
- Public communities
- Cryptocurrency or payments
- Stories/status feed
- Custom end-to-end encryption
- Large group calls

These features create complexity before Pulse has secure accounts and dependable messaging.

---

# 6. 90-day execution plan

## Days 1–14: v0.3 reliability

- Finish reconnect, retry, duplicate prevention, invite links, monitoring, and expanded tests
- Establish staging and production release checklist

## Days 15–45: v0.5 private beta

- FastAPI project structure
- PostgreSQL schema and migrations
- Accounts and secure sessions
- Private direct chats and groups
- WebSocket messaging
- Redis presence and pub/sub

## Days 46–70: v0.7 premium messaging

- Receipts, replies, reactions, edit/delete
- Search and drafts
- Image/document uploads
- Polished responsive interface

## Days 71–90: v0.9 release candidate

- PWA installation
- Push notifications
- Offline queue
- Block/report tools
- Security testing and private beta feedback

---

# 7. Success metrics

Track quality before growth:

- Message delivery success: target **99.9%+**
- P95 send-to-receive latency: target **under 1 second** in normal conditions
- Successful reconnect rate: target **99%+**
- Error-free sessions
- Failed upload rate
- Day-1, Day-7, and Day-30 retention
- Weekly active users
- Messages per active user
- Abuse report response time

Never store private message text in analytics or ordinary application logs.

---

# 8. Immediate next sprint

The next development sprint is **Release 0.3 — Reliable room chat**.

### Build next

1. Client-generated message IDs and duplicate prevention
2. Optimistic message bubbles with retry
3. Automatic session recovery
4. Shareable room invite links
5. Improved connection/offline banner
6. Reconnect and room-isolation tests
7. Uptime and error monitoring
8. Deployment smoke test

After v0.3 passes its completion criteria, begin the PostgreSQL and account migration for v0.5.
