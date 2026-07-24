# HomeTogether Hire — Launch Scope & Roadmap

*Decision (July 2026): launch a focused, excellent hiring product now. Grow the rest only as real usage earns it. Partner — don't build — for payroll/tax and background checks.*

---

## What we're launching (the wedge — mostly built)

**The promise:** help a family *find, vet, and hire* a caregiver they trust — and help caregivers find private-pay work. That's a complete, valuable product on its own.

- **Family:** create an account, post a warm job centered on their loved one (story + photo + care + pay), share a private invite link, browse the vetted directory, review applicants with a private scorecard + notes, run or skip a background check, and use the hiring toolkit (interview questions, reference script, checklists, work-agreement template, pay guidance).
- **Caregiver:** create an account and profile, get interviewed and background-checked, earn a ✓ badge, appear in the directory, and apply to jobs / private invites.
- **Admin (you):** approve caregivers to the directory, set trust flags, manage families/jobs/applicants.
- **Trust engine:** AI phone interview, Checkr background checks, free OIG screen, badges.

**Launch checklist:**
- [ ] Re-skin the four real surfaces (Family hiring, Caregiver, Directory, Admin) to the new design system.
- [ ] One clear entry point that routes families → hire/browse and caregivers → join.
- [ ] Link the new pages from the main HomeTogether site; remove `noindex` when ready.
- [ ] Delete test data.
- [ ] Move the interview + background-check engine into the HomeTogether Hire project.
- [ ] Real email notifications (GHL or custom SMTP) on the new project.

---

## Add next (thin, cheap stickiness — earns the $25/mo)

Only after real families and caregivers are using the wedge. These keep the relationship on-platform without heavy machinery:

1. **On-platform messaging** (family ↔ caregiver).
2. **Work agreement + e-signature** and a simple document vault.
3. **A light shared schedule** and a simple "how's it going" care update / check-in.

---

## Partner, don't build

- **Payroll & household-employer tax** → integrate an existing household-payroll provider. Real money, real compliance, never-ending maintenance. Not something to build or own.
- **Background checks** → Checkr (already in use). Don't rebuild.
- **Identity verification / insurance** → buy, don't build.

---

## Parked (a real roadmap, not the next sprint)

Designed by Claude Design as the north-star vision; build only if real usage demands it *and* there's a team to run it:

- Full **Schedule** (recurring/open shifts, coverage, time-off).
- **Time Clock** with location verification, **Timesheets**, **Payroll Center**, **Expenses/mileage**.
- **Care Plan builder**, **Daily Visit Journal**, **Tasks & routines**, **Health & safety records / Emergency Binder**, **Care team roles**.
- **Household Employer Tax Center** (guide layer around the payroll partner).
- **Caregiver active-shift mode**, clock-in/out flows, offline PWA.
- Full **Admin operations suite**: verification queues, safety case management, support desk, payments/revenue, content management, reports.
- **Performance reviews**, notifications center, global search, granular family/admin permission roles.

---

## Why this order

Hiring is what attracts the first users; scheduling and pay are things people only need *after* they've hired, so they can't grow an empty marketplace. The heavy layers are high-liability and high-maintenance — best deferred and, where possible, partnered. Ship the wedge, prove families hire through it, then earn each next layer with real demand.
