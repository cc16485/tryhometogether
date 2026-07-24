# HomeTogether Hire — Phase 1 Architecture Blueprint

*The pre-design foundation. Hand this to design before any screens are styled.*
*Grounded in the platform as actually built (July 2026), then extended to the full three-app vision.*

---

## 0. What exists today vs. what this brief adds

Being honest about this up front, so effort is sequenced sanely. The brief describes a platform on the scale of **Care.com + Homebase + a payroll service + a care-management portal**. That is a large, multi-stage venture, not a restyle. Here is the real starting line:

**Already built and live (the Family Hiring slice + foundations):**
- Real accounts and login for families and caregivers (Supabase Auth), on HomeTogether Hire's own database.
- Family: post a job centered on the loved one (name, age, story, photo, care needs, schedule, pay), private invite link, applicant tracker with a private 5-star scorecard + notes + status, optional/waivable background check, public directory browse, and an 8-guide hiring toolkit.
- Caregiver: account, profile editor, status tracker (interview / check / published).
- Apply-by-link page (shows the full offer, optional "join HomeTogether Hire").
- Admin: publish caregivers to the directory, set trust flags, delete, view families/jobs/applicants.
- Security model: caregivers can't self-publish; families see only their own data; the public sees only approved profiles.

**Net-new in this brief (a roadmap, not a weekend):**
Scheduling, clock-in/out with location, timesheets, pay/payroll, expenses/mileage, care plans, visit journals, tasks/routines, health & safety records, care-team roles, employer-setup guide, the caregiver active-shift experience, messaging, documents/e-sign, notifications, the full admin operations suite (verification queues, safety cases, support, payments, content, reports), and PWA/offline.

**Recommendation:** treat what's built as **Family App → Hiring** (mostly done) and **Caregiver App → Profile** (partly done). Design the whole IA now so nothing is boxed in, but **build in the phased order in §6** so the near-term goal — getting real families and caregivers onboarded and marketing — isn't stalled behind a payroll engine.

---

## 1. Platform shape: one platform, three role-based apps

| App | Primary device | Emotional goal |
|---|---|---|
| **Family App** | Desktop + mobile | "I know what to do next, and I'm making a thoughtful decision." |
| **Caregiver App** | Mobile-first (PWA) | "I can present myself well, find good families, and manage my work easily." |
| **Admin App** | Desktop | "I can see what needs attention and resolve it efficiently." |

Role-based entry: after login, route to the correct app. A person can hold multiple roles and switches between them **intentionally** via the account menu. Never show admin controls to regular users. Everything is organized around the **loved one receiving care**.

---

## 2. Sitemap

### Family App
```
Home (command center, changes by stage: no-job / hiring / hired)
Hiring
  ├─ Overview (funnel + next step)
  ├─ Jobs (list, job wizard)
  ├─ Applicants (warm cards, statuses)
  ├─ Saved caregivers
  ├─ Interviews (interview mode)
  └─ Hiring setup (readiness tracker)
Care  (unlocks after first hire)
  ├─ Overview
  ├─ Care plan (AI-guided builder, family-approved)
  ├─ Visit journal
  ├─ Tasks & routines
  ├─ Health & safety info
  └─ Care team
Schedule  (week / month / list)
Time & Pay
  ├─ Time clock
  ├─ Timesheets
  ├─ Pay
  ├─ Expenses
  ├─ Employer setup
  └─ Reports
Messages
Documents
Guidance (resource center)
— user menu: loved-one switcher, family-member access, billing, settings, help —
```

### Caregiver App (mobile-first, 5 tabs)
```
Home (context-aware: looking-for-work / employed / active-shift mode)
Jobs (Recommended · Nearby · Saved · Applications · Private invitations)
Schedule (upcoming shifts, clock-in/out flow, time history)
Messages
Profile (about, experience, trust & verification, documents, visibility)
```

### Admin App (desktop)
```
Overview (operations dashboard: metrics + needs-attention + marketplace health)
People (Families · Caregivers · Admins)
Jobs & Hiring
Verification (queues: identity · background · references · certs · profile · badges)
Safety (dedicated case queues)
Support (case management)
Payments (platform billing / check billing / payroll / wages — kept separate)
Content (guides, templates, AI knowledge, state guidance)
Reports (marketplace / trust & safety / usage / revenue)
Settings
```

---

## 3. Role & permission map

**Family roles**
- **Primary family admin** — billing, hiring, approve timesheets, employer setup, all documents, manage members.
- **Family manager** — schedule, communicate, review care, participate in hiring, view timesheets.
- **Family viewer** — view schedule, care journal, updates, selected documents.
- **Financial manager** — view/approve timesheets, manage pay, view tax/payment docs.

**Caregiver** — sees only: jobs they may view, families they applied to, active/past relationships, and their own shifts, messages, documents, pay.

**Admin (separated duties, least-privilege)** — Support · Verification · Safety · Billing · Content · Analytics · Super admin. Sensitive records (background-check detail, health info) behind role-based permission + access logs.

*Current state:* the built system enforces the core of this at the database level (row-level security + column privileges). Family sub-roles and admin sub-roles are net-new and should be modeled as a `role` on a membership record (see entities).

---

## 4. Core entities (data model)

Already real as `htl_` tables: **User, Family, Caregiver, Job, Application** (with private scorecard/notes/status), plus profile/trust fields and a public job-lookup. To reach the full vision, add the entities below. Design should treat these as the shared vocabulary so the same data is never entered twice.

```
User ─┬─ FamilyMembership (role) ── Family ──┬─ LovedOne (1..n)
      └─ CaregiverProfile                    ├─ Job ── Application ── Interview
                                             │                    └─ Reference, BackgroundCheck
                                             ├─ EmploymentRelationship (Family × Caregiver × LovedOne)
                                             ├─ Schedule ── Shift ── ClockEvent ── VisitSummary
                                             ├─ CarePlan ── Task/Routine
                                             ├─ Timesheet ── PayRecord, Expense
                                             ├─ Message (thread)
                                             ├─ Document (category, e-sign)
                                             └─ Subscription
Admin side: SafetyReport, SupportCase, VerificationItem, ContentItem
```

Key relationship: **EmploymentRelationship** is the hinge that turns "an applicant" into "our caregiver," and it's what everything post-hire (schedule, care plan, timesheets, pay, messages) hangs off of.

---

## 5. The ten core workflows

Concise step lists; design one clean flow for each before polishing screens.

1. **Family creates a job & receives an applicant**
   Care profile of loved one → job wizard (person first, then care) → publish / private link → applicant lands → appears on Home "needs attention" + Applicants.

2. **Family invites a caregiver privately**
   Generate private link → share → caregiver opens the offer → applies → private applicant (only that family sees them).

3. **Family interviews & hires**
   Shortlist → interview mode (one question at a time, topic-based) → scorecard + notes → compare finalists (AI summarizes, never decides) → offer → accept → EmploymentRelationship created.

4. **Caregiver completes profile & applies**
   Sign up → build profile → identity/background steps → browse or receive invite → short apply (reuses profile) → status updates.

5. **Family schedules a shift**
   From a hired relationship → create shift (recurring/one-time/open) → caregiver notified → confirmed.

6. **Caregiver clocks in & completes a visit**
   Confirm shift → verify arrival (location/QR/manual) → review care plan & notes → work → clock-out flow (tasks, visit summary, concerns, mileage) → hours recorded.

7. **Family approves a timesheet**
   Completed shifts auto-build a timesheet → family reviews (regular/OT/mileage/adjustments) → approve or request correction → both sides see the same final record + audit history.

8. **Family starts employer setup**
   Guided household-employer center (EIN, forms, state accounts, payroll method, pay frequency, year-end) → "Hiring setup progress" tracker (never a misleading legal "compliance score") → clear "talk to a tax professional" moments.

9. **Admin reviews a background check**
   Item enters verification queue → admin sees submitted data, provider response, reason for manual review → approve/deny with audit log → badge updates → never over-expose sensitive data.

10. **Admin resolves a safety report**
    Flag or user report → safety queue (risk level) → review context/timeline/evidence/prior reports → act (contact, restrict, pause, remove, escalate, preserve) → document resolution → follow-up.

---

## 6. Recommended build sequence (so near-term goals aren't stalled)

1. **Now / near-term (mostly built):** Family Hiring + Caregiver Profile + Directory + Admin approval. Polish these with the new design system and get real people onboarded. *This is what makes the product marketable today.*
2. **Next:** Messaging (family ↔ caregiver, on-platform), Documents (work agreement + e-sign), Interview mode, Compare applicants, Hiring-setup tracker.
3. **Then:** Schedule → Shifts → Caregiver active-shift mode → Clock-in/out → Visit summaries. (This is the "Homebase" layer and the biggest single lift.)
4. **Then:** Timesheets → Pay/expenses → Employer-setup guide (with a real payroll partner integration decision).
5. **Then:** Care plan, visit journal, tasks/routines, health & safety records, care-team roles.
6. **Parallel, as volume grows:** the full Admin operations suite (verification queues, safety cases, support, payments, content, reports) and PWA/offline.

---

## 7. Design guardrails (from the brief, kept front-and-center)

- Feel like **a calm professional beside the user** — not agency software, not a medical chart, not payroll software, not a corporate ATS.
- Every main page answers: **What's happening? What needs my attention? What should I do next?**
- **Progressive disclosure** — show what's needed now.
- Brand: navy `#143A5E` (headings), teal `#1E7A8C` (primary actions), honey `#EFCE85` (progress/trust/celebration), soft off-white ground; **Fraunces** headings + **Nunito Sans** body; rounded cards, generous space, soft shadows, warm photography.
- Red only for genuine safety, destructive actions, overdue items, payment failures.
- Warm empty states that teach the next step.
- Honesty in language: private time tracking is **not** Medicaid EVV; HomeTogether is **not** the employer and does not supervise daily work; separate hours-calculation from payment from tax filing; AI never decides a hire, and never replaces 911, legal, tax, or medical professionals.
- "Ask HomeTogether" assistant present in all three apps, role- and page-aware.

---

*Prepared as the architecture layer for the HomeTogether Hire redesign. Once this IA and the ten workflows are agreed, design can proceed to the design system, then screen-by-screen per the brief's Phases 2–6.*
