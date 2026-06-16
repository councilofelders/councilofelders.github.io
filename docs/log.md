# Project Log — Council of Elders Landing Page

> **Note:** This file is reconstructed on 2026-06-13 following accidental deletion during a
> repo cleanup, and has been updated with subsequent work. The original `docs/log.md` was
> never committed to git (the `docs/` directory was in `.gitignore` and untracked).

---

## Progress Summary

### Events Tab — Timeline Iterations

The primary focus of recent work has been the Events tab on `index.html`. Multiple
timeline mockups were created in the `docs/` directory to explore visual approaches
for presenting upcoming events.

The iteration workflow followed a standard mockup-and-review cycle: draft mockups
were created, presented for feedback, and refined based on direction. After several
rounds of alternatives, the final accepted direction was a **visually centered
timeline layout**, which was integrated into the current version of `index.html`.

Key decisions made during this phase:
- **Events hero title** changed to **"Decentralized AI Days"**
- **Events description** updated to the current approved wording
- Timeline style finalized as centered and visually aligned

### Events Tab — Location Updates (2026-06-13)

Updated all 14 event location strings with specific venue names:

| Event | Old Location | New Location |
|-------|-------------|-------------|
| London (Jul 2022) | The Microsoft Reactor, London | The Microsoft Reactor |
| NYC (Sep 2022) | New York City, USA | NYC Seminar and Conference Center |
| Tokyo (Apr 2023) | Tokyo, Japan | Space Market, Shibuya City |
| Prague (Jul 2023) | Prague, Czech Republic | Paralelní Polis |
| Toronto (Oct 2023) | Toronto, Canada | Startuptive |
| SF (Jan 2024) | San Francisco, USA | Noisebridge |
| Frankfurt (Apr 2024) | Frankfurt, Germany | Onlight Studiorent |
| Tokyo (Jul 2024) | Tokyo, Japan | C-Lounge, Chiyoda City |
| Bangkok (Nov 2024) | Bangkok, Thailand | Renaissance Bangkok Ratchaprasong Hotel |
| Seattle (Mar 2025) | Seattle, USA | Niftmint |
| Tokyo (May 2025) | Tokyo, Japan | SPOT六本木ミッドタウンサイド, Minato City |
| Vienna (Sep 2025) | Vienna, Austria | Impact Hub Vienna |
| SF (Jan 2026) | San Francisco, USA | Common Space |
| Vienna (Mar 2026) | Vienna, Austria | Impact Hub Vienna |
| Tokyo (May 2026) | Tokyo, Japan | 727 Spemo Lounge, Minato City |

### Events Tab — Timeline Photos → Country Flags (2026-06-13)

Replaced all 15 event timeline circle photos with country flag images from flagcdn.com.
Previously used generic Unsplash city skyline shots, many duplicated across events in
the same city. New approach uses simple, recognizable flag icons.

Flag distribution:
- UK (1): London
- USA (4): NYC, SF 2024, Seattle, SF 2026
- Japan (4): Tokyo 2023, Tokyo 2024, Tokyo 2025, Tokyo 2026
- Czech Republic (1): Prague
- Canada (1): Toronto
- Germany (1): Frankfurt
- Thailand (1): Bangkok
- Austria (2): Vienna 2025, Vienna 2026

### Repo Cleanup

A repo cleanup removed leftover mockup artifacts from `docs/`. During this cleanup,
`docs/log.md` was mistakenly deleted. It has been restored as a reconstruction.

### Git Commits

1. `f50c81a` — Update Events tab timeline and copy (initial)
2. `95d81dc` — Update event locations across all years
3. `a153343` — Replace event timeline photos with country flag images

---

## Artifact History

The following mockup files existed in `docs/` during the Events tab iteration
process. They were removed during the repo cleanup and are no longer present on
disk.

- `events-mockup-option-a.html`
- `events-mockup-option-b.html`
- `events-mockup-option-c.html`
- `events-around-the-world-mockup.html`
- `events-timeline-mockup.html`
- `events-timeline-mockup-v2.html` through `events-timeline-mockup-v9.html`

---

## Current Status (as of 2026-06-14)

- **Git-tracked modified file:** `index.html` — P1/P2/P3 cleanup committed and pushed (`6a2894d`)
- **This file (`docs/log.md`):** updated with latest progress; remains untracked (docs/ is gitignored)
- **Board:** `coe-landing-page` — all cleanup cards complete
- **File stats:** 2032 → 1802 lines (-230, 11% leaner)

### Audit & Cleanup (2026-06-14)

Comprehensive audit by `snr-design` found 18 findings across 3 tiers. All resolved:

**P1 Critical (5):**
- SVG location icon duplicated 15 times → 1 `<symbol>` + 15 `<use>` refs
- Team tab nested CTA → flattened to single `<a>`
- Missing `role="img"` on hero visual → added
- Tab switches not announced → `aria-live="polite"` + JS announcer
- Borderline contrast → `.featured-description` bumped gray-400 → gray-300

**P2 Worthwhile (7):**
- Dead CSS removed: social buttons, treasury placeholder, button-list, `featured-stats--no-border`
- 3 duplicate panel-ID selectors merged
- Inline CTA styles extracted to CSS
- `.team-card-body` wrappers flattened

**P3 Nice-to-have (6):**
- YouTube thumbnail: `loading="lazy"`
- Flag images: `srcset` w80/w160/w320
- Unused CSS removed: `.hero-visual-label`, `.featured-stats`, `--cat-*-bg` tokens
- `gray-800`/`gray-900` consolidated (identical values)

### Git Commits

4. `6a2894d` — P1-P3 cleanup: SVG dedup, accessibility, dead CSS, token consolidation
5. `987fcec` — Glassmorphism: `backdrop-filter: blur(12px)` on 7 selectors across all tabs
6. `c108636` — Update Learn tab images (Blog + Kaggle) and Funds preview
7. `ba8b033` — Normalize button styling: compact widths, lighter bg, tighter spacing
8. `fefe4bf` — Add README.md (project overview, file structure, tech stack)
9. `8883248` — Number events (#01–#15), link all 15 events, update calendar CTA
10. `0773fd4` — Add hash routing for direct tab URLs (#home, #events, etc.)
11. `ff3dc54` — Add scannable QR code footer with inverted SVG
12. `a432705` — Add click-to-expand QR lightbox for in-person scanning
13. `4fe5832` — Add left/right arrow key navigation between tabs, fix IIFE indent consistency
14. `b07069c` — Replace inline SVG QR code with uploaded QR photo (JPG 100×100px, 12px padding, label update)

## Design Tweaks (2026-06-14)

- QR code replaced: custom white-on-dark SVG → uploaded `qr_code.jpg` (76KB photo of the actual QR)
- QR label updated: "Scan to visit" → "Scan to visit · Click to enlarge"
- QR wrapper padding iterated: 1px → 2px → 0px → 10px → 16px → 12px
- QR image size reduced: 120px → 100px
- Left/right arrow key navigation added between tabs
- Click-to-expand QR lightbox: 65% viewport, dismiss by click outside or ESC

---

*This log was reconstructed from project session evidence and updated with subsequent work.
Timestamps, exact code diffs, and intermediate mockup contents are not included where they
could not be verified from available sources.*

---

## Cmd+K / Site Search Index (2026-06-16)

**Cmd+K / site index feature kicked off** — Phase 1 of 2 (index only, no palette/modal UI yet).

### Key Decisions

- **Index format:** Embedded JSON in `index.html` as `<script id="search-index" type="application/json">` — no build step, no external dependency.
- **Entry count:** 38 entries across 6 tabs (home: 3, events: 15, tools: 7, resources: 3, team: 9, treasury: 1).
- **Search approach:** Case-insensitive substring match on `title` + `snippet`. No Fuse.js / Pagefind / ninja-keys — custom vanilla JS planned for Phase 2.
- **Maintenance:** Hand-maintained. When content changes in the HTML, the index updates in the same commit.

### Index Schema

Each entry has: `id` (unique, kebab-case, type-prefixed), `type` (event|tool|resource|team|treasury|home), `tab` (hash route), `title` (primary search target), `subtitle` (secondary info), `snippet` (short description), `url` (external URL or `#hash` for in-page nav).

### File Changed

- `index.html` — added `<script id="search-index" type="application/json">` block after the closing `</script>` of the main JS, before `</body>`.

## Cmd+K Search Palette — Phase 2 (2026-06-17)

**Cmd+K / Ctrl+K search palette implemented** — Phase 2 of 2 (palette + FAB, consumes the search index from Phase 1).

### Deliverables

- **`index.html`** — added:
  - Search palette CSS (~180 lines) — glassmorphism modal matching site aesthetic
  - Palette HTML (`#search-palette`) — centered dialog with input, results, footer, keyboard hint
  - FAB button (`#search-fab`) — fixed bottom-right, hidden on desktop, visible on touch devices
  - Palette JS (~180 lines) — search logic, keyboard nav, focus trapping, a11y, touch detection

### Key Decisions Applied (all default choices Joe accepted during investigation)

| Decision | Value |
|----------|-------|
| Result cap | 10 (within the 8-10 range) |
| Empty input | Shows all 38 entries grouped by tab |
| Filter | Case-insensitive substring match on `title` + `subtitle` + `snippet` |
| External URLs | `window.open(url, '_blank', 'noopener,noreferrer')` |
| Hash URLs | `window.location.hash = url.slice(1)` — existing hash router switches tab |
| FAB | Bottom-right, hidden on desktop by default, shown on touch detection |
| Keyboard hint | Hidden on touch devices; placeholder changes to "Search the site…" |
| Focus trap | Tab cycles within palette (input ↔ first result) |
| Backdrop click | Closes palette |
| Open binding | `(e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')` with `e.preventDefault()` |
| Arrow key conflict | Palette's capture-phase listener calls `e.stopPropagation()` on Arrow keys while open, preventing tab navigation conflict |

### Tab Grouping

Tab display names used in results: Home, Events, Projects, Resources, Team, Treasury (mapping index `tab` values `whatsnew`, `events`, `projects`, `resources`, `team`, `treasury`).

### Entry Count

Actual search index contains **38 entries** (not 41 as approximated in the investigation memo):
- Home: 3
- Events: 15
- Projects/Tools: 7
- Resources: 3
- Team: 9
- Treasury: 1

### Verification Performed

(Full verification details in the task handoff.)

### What's Next

- No further phases planned for search. Light/dark toggle remains a separate future task per the investigation memo.

### Search Affordance — Option E (2026-06-16)

Replaced the rejected `.search-trigger` pill button (top-right of hero header) with an inline **Option E** search affordance per `docs/search-affordance-mockups.html`. Joe's pick: a text link with keycap appended to the hero subtitle.

Changes:
- Removed all `.search-trigger` CSS (glass button, icon, label, keycap, mobile hide), the `<button>` element, and JS listener/references
- Added `.optE-*` CSS rules using site tokens (glassmorphism vocabulary, gray-scale colors, no invented values)
- Modified hero subtitle to `<p class="hero-subtitle optE-subtitle">` with appended "· Search ⌘K" inline
- Wired `.optE-link` click handler to `openPalette()` (same palette as FAB and ⌘K)
- Mobile (`max-width: 480px`): hides `.optE-text` label, keeps icon + keycap for compact footprint

Rationale: Keeps the search affordance naturally integrated with the hero text, avoids the visual weight of a separate floating button, and maintains the site's minimal aesthetic.

### Search Affordance — Hover Underline Removed (2026-06-16)

Follow-up tweak requested by Joe: drop the hover underline on the `.optE-link` inline "Search" affordance. The 1px transparent border was reserved at rest and the white-15% border-bottom-color kicked in on hover/focus-visible, producing an underline that felt too link-like for a subtle inline affordance.

Changes:
- Removed `border-bottom: 1px solid transparent` from `.optE-link` (no more reserved space at rest)
- Removed `border-bottom-color: rgba(255,255,255,0.15)` from `.optE-link:hover, .optE-link:focus-visible` (no more underline on hover)
- Hover/focus-visible still brightens color from `gray-400` → `gray-200` for clear affordance

### Repo Cleanup (2026-06-16)

Deleted dev-only build artifacts left over from Puppeteer QA scaffolding (search-affordance review):
- `node_modules/`
- `package.json` (puppeteer ^25.1.0)
- `package-lock.json`

These were already in `.gitignore` but Joe called out that .gitignore alone isn't enough — they should be physically removed from disk to keep the working tree clean. Stray script `review-check.mjs` moved to `docs/reviews/search-affordance/review-check.mjs` alongside other review artifacts.

Reinforced as a standing rule: when Joe says "clean up" on a project, also delete dev-only build artifacts (node_modules/, package.json, package-lock.json), not just leave them in .gitignore.

---

## Light/Dark Theme Implementation (2026-06-16)

**Light/dark theme toggle + CSS token system implemented** in `index.html`. Design spec from `docs/site-search-and-theme-investigation.md` (June 2026, jnr-product + snr-product PASS).

### What was done

**CSS Token System:**
- Converted hardcoded colors to CSS custom properties on `:root`
- Added `html[data-theme="light"]` selector with ~30 token overrides
- New tokens added: `--body-bg`, `--body-text`, `--hero-cta-bg`, `--hero-cta-border`, `--hero-cta-hover-bg`, `--hero-cta-hover-border`, `--hero-cta-active-bg`, `--hero-cta-secondary-border`, `--hero-cta-secondary-hover-bg`, `--hero-cta-secondary-hover-border`, `--tab-bar-border`, `--tab-bar-bg`, `--timeline-line`, `--hero-visual-overlay`, `--hero-bg-base`, `--aurora-blue-1` through `--aurora-glow-teal`, `--qr-overlay-bg`, `--skip-link-bg`, `--toggle-hover-bg`
- Light glassmorphism: `rgba(0,0,0,0.03)` fills + `rgba(0,0,0,0.08)` borders (dark-on-light translucency, NOT white-on-dark)

**Toggle Button:**
- Sun/moon SVG icon button placed top-right of hero header (absolute positioned)
- Keyboard accessible: `role="switch"`, `aria-checked`, `aria-label="Toggle theme"`
- Focus-visible styled with `outline: 2px solid var(--color-primary)`
- No layout shift between states (fixed 40×40px)
- Responsive: 36×36px on mobile

**Persistence:**
- Inline `<script>` in `<head>` runs before first paint to prevent FOUC
- Checks `localStorage.coe-theme` first, falls back to `prefers-color-scheme`, falls back to dark
- Toggle writes to `localStorage` and sets `html[data-theme]`

**Aurora Background Decision:**
- Path taken: **(b) significantly desaturated** — kept the same radial gradient structure but reduced opacity values from ~0.035-0.06 to ~0.008-0.02
- Rationale: Aurora is a key brand element; completely replacing it would dilute identity. Desaturating preserves the flowing light forms while being appropriate for light backgrounds.

**Category Accent Colors:**
- Each `--cat-*` token got a slightly desaturated light-mode variant
- `--cat-whatsnew: #1a5bb5` (was #1867C0), `--cat-events: #3a918e` (was #48A9A6), etc.
- Maintains sufficient contrast on light backgrounds (verified via token inspection)

**System Preference Change Handling:**
- `matchMedia('(prefers-color-scheme: light)').addEventListener('change', ...)` listener
- Only auto-switches when `localStorage.coe-theme` is empty (user override wins)

**Cmd+K Palette:**
- Stays dark in both themes (hardcoded dark rgba values, not using theme tokens)
- Verified: palette background remains `rgba(22, 22, 23, 0.92)` regardless of theme

### Verification Results

All 8 verification scenarios passed:
1. Dark mode renders correctly (body bg: rgb(22,22,23), body color: rgb(221,221,221))
2. Toggle switches to light (body bg: rgb(249,250,251), body color: rgb(55,65,81))
3. Toggle returns to dark
4. Light mode persists on reload (localStorage)
5. OS preference change auto-switches when localStorage empty
6. User override wins when localStorage is set
7. Mobile (375px): toggle usable, no layout shift
8. Keyboard focus ring visible on toggle

### Tokens Changed/Added

**Existing tokens redefined for light mode (9):**
`--color-gray-50` through `--color-gray-900`, `--card-bg`, `--card-border`, `--card-border-hover`, `--glass-bg`, `--glass-border`, `--glass-border-hover`, `--cat-whatsnew`, `--cat-events`, `--cat-tools`, `--cat-resources`, `--cat-treasury`, `--cat-team`

**New tokens added (20+):**
`--body-bg`, `--body-text`, `--hero-cta-bg`, `--hero-cta-border`, `--hero-cta-hover-bg`, `--hero-cta-hover-border`, `--hero-cta-active-bg`, `--hero-cta-secondary-border`, `--hero-cta-secondary-hover-bg`, `--hero-cta-secondary-hover-border`, `--tab-bar-border`, `--tab-bar-bg`, `--timeline-line`, `--hero-visual-overlay`, `--hero-bg-base`, `--aurora-blue-1` through `--aurora-glow-teal` (8 aurora tokens), `--qr-overlay-bg`, `--skip-link-bg`, `--toggle-hover-bg`

### Deviation from Investigation Memo

None. All decisions follow the investigation memo's recommendations:
- Toggle placement: header icon (sun/moon) ✓
- Persistence: `prefers-color-scheme` default + localStorage override ✓
- FOUC prevention: inline script in `<head>` ✓
- Cmd+K palette: kept dark (not themed) ✓

### Light/Dark Theme — Reverted (2026-06-16)

Build and review cards `t_426d070e` (jnr-design), `t_6515702f` (snr-design PASS), and `t_8895c4ca` (dev-reviewer NEEDS-WORK) were all completed on the initial attempt, but Joe redirected the work scope before committing. The build was structurally sound: ~30 token overrides under `html[data-theme="light"]`, sun/moon toggle (role="switch"), FOUC prevention, localStorage persistence with prefers-color-scheme fallback, desaturated aurora. Cmd+K stayed dark in both themes. All 8 verification scenarios passed via Playwright.

dev-reviewer NEEDS-WORK findings (preserved for the next iteration):
- localStorage calls at 3 sites need try/catch (Safari/Firefox private mode throws)
- Mobile touch target was 36×36px at 767px breakpoint, needs WCAG 44×44px minimum
- Focus ring used var(--color-primary) in both themes — needs a light-bg variant
- Toggle's `aria-checked` was hardcoded "false" at markup; only corrected by bottom script after FOUC script ran

Local tree reset to `066bd6e` via `git reset --hard 066bd6e`. `2a5f912` (hover-underline fix on inline optE-link) was discarded — that affordance is being removed. Search affordance is back to the `066bd6e` state: Cmd+K keybinding works, search palette + JSON index intact, but no visible "Search" text on screen. Joe's next direction will determine whether the inline affordance comes back.

### Search Affordance Removed — Reverted to Cmd+K-Only (2026-06-16)

Per Joe's instruction: the visible search affordance (the inline `.optE-link` "Search ⌘K" in the subtitle) is being removed. Cmd+K and Ctrl+K still open the search palette — the feature works, but no on-screen hint tells the user it exists. This is a deliberate design choice Joe wants to test. Working tree is at `066bd6e`.

---

## Cross-Source Search: Meetup Slides Index + Lunr.js (2026-06-16)

**Build-time search index for meetup slide PDFs** — GitHub Action + Python indexer + Lunr.js integration in the Cmd+K palette.

### Deliverables

#### 1. `scripts/build-cross-source-index.py` (rewritten from previous timed-out attempt)
- Python indexer that scans `councilofelders/meetups/slides/` PDF filenames
- Parses: `YYYY-MM-DD-city/NN-talk-title-by-speaker-lang.pdf`
- Cross-references with `README.md` for richer metadata (full event name, corrected titles, speakers)
- Emits 93 entries with structured schema: id, type, source, event, eventDate, city, title, speaker, language, snippet, url, tags
- Generated tagged entries for searchability (title words, city, month-year, speaker last name, event number)

#### 2. `.github/workflows/build-cross-source-index.yml` (new)
- Triggers: `schedule: cron '0 6 * * 1'` (weekly Monday 06:00 UTC), `workflow_dispatch`, `push: paths: ['cross-source-index.json']`
- Steps: checkout site repo, checkout meetups repo (shallow, separate), run indexer, commit JSON via `stefanzweifel/git-auto-commit-action@v5` with `[skip ci]`

#### 3. `cross-source-index.json` (generated)
- 93 entries from 15 meetup events (London #1 → Tokyo #15)

#### 4. `index.html` — Cmd+K palette extension
- **Lunr.js 2.3.9** loaded via CDN (`unpkg.com`) with `defer` — 8KB gzipped, well-vetted
- **Lazy-loads** `cross-source-index.json` on first Cmd+K open via XHR with graceful fallback (404 = no error, on-page results only)
- **Combined Lunr index** built from BOTH the existing 38 on-page entries AND the new 93 meetup entries
- **Field boosting**: `title^3`, `speaker^2`, `event^2`, `tags^1.5`, `snippet^1`, `subtitle^1`
- **"Meetups" group** rendered after on-page tab groups with a visual separator (border-top line)
- **New entry shape**: speaker name · event name · date + [PDF] badge + [GitHub] link
- **Graceful fallback**: If `cross-source-index.json` fails to load (404/network error), on-page search continues to work; if Lunr hasn't loaded yet, falls back to substring matching
- **Progressive enhancement**: On first open, on-page results show immediately; meetup results appear once the JSON loads

### Key Decisions

| Decision | Value |
|----------|-------|
| Lunr loading | CDN (`unpkg.com`, `defer`) — 8KB, well-vetted, Joe can opt to inline if preferred |
| Index loading | Lazy on first Cmd+K open (not page load) |
| Fallback | Substring matching when Lunr unavailable; on-page only when JSON unavailable |
| Meetup separator | `border-top` line between on-page groups and Meetups group |
| `scripts/` gitignore | Not added — `scripts/` is not in `.gitignore`; let Joe decide |
| Richard Craib entry | Not indexed — the PDF for "hedge funds" talk has "No permission to share" (README.md metadata only, no PDF file) |

### Verification

- Indexer produces **93 entries** (matches expected count)
- All entries have unique IDs
- "signals" query returns "Numerai Signals" by Pegion (Decentralized AI Day Tokyo #15) as a meetup result
- Lunr JS syntax verified via `node --check`
- All braces/parens balanced in search JS

### Files Changed

| File | Change |
|------|--------|
|| `scripts/build-cross-source-index.py` | New — Python indexer (v1 per-PDF schema) |
|| `.github/workflows/build-cross-source-index.yml` | New — GitHub Action |
|| `cross-source-index.json` | New — 93 meetup entries (test output in site root) |
|| `index.html` | Modified — Lunr CDN, lazy JSON loader, combined Lunr index, Meetups group rendering |

---

## Cross-Source Index v2 — Per-Talk Schema (2026-06-16)

**Rewrote the indexer to produce v2 per-talk entries** (not per-PDF). Fixes duplicate results for EN/JP translations, adds video metadata, handles "no permission" talks, and indexes YIEDL workshop sessions.

### Key Changes

#### `scripts/build-cross-source-index.py`
- **v2 schema**: produces `{version: 2, generatedAt, entryCount, entries}` with per-talk `TalkEntry` shape
- **Multi-language merge**: same talk with EN+JP slides → one entry with `slides.en` and `slides.ja`
- **Video extraction**: parses `[**Video (XX)**](url)` patterns, builds `videos[lang]` map
- **Availability enum**: `slides+video` / `slides-only` / `video-only` / `talk-only` / `no-permission` / `not-shared`
- **primaryUrl heuristic**: EN slides > any slides > EN video > any video > null
- **Idempotent output**: sorted by `id`, deterministic JSON formatting
- **YIEDL sessions**: indexes Vienna #14 and SF #13 YIEDL workshop sessions as separate `talk-only` entries
- **Bug fixes over prior attempt**:
  - Strips raw markdown (` - [**Video**](url)`) from talk titles in the noslides branch
  - Accurate snippets: `"talk from {event}"` for video-only/talk-only (not `"slides from"`)
  - Crunch workshop sessions no longer indexed as YIEDL entries (stopped at `Crunch Workshop` header)

#### `cross-source-index.json`
- **121 entries** (was 127 — removed 6 Crunch sessions)
- **Availability breakdown**: 65 slides+video, 24 slides-only, 21 video-only, 5 talk-only, 2 no-permission, 4 not-shared
- All 93 PDFs from meetups repo represented in entries' `slides` maps

### Regression Test Results

| Test | Result |
|------|--------|
| Pegion's Tokyo talk | 1 entry, `slides.en` + `slides.ja` + `videos.ja` ✅ |
| Richard Craib (NYC hedge funds) | 1 entry, `availability: no-permission`, `primaryUrl: null` ✅ |
| Megumi (Tokyo #15 Talk #1) | 1 entry, `availability: no-permission`, `primaryUrl: null` ✅ |
| Fireside chats (3) | All `video-only`, clean titles ✅ |
| No raw markdown in any title/snippet | ✅ |
| Snippet matches availability | All 121 entries check out ✅ |
| All 93 PDFs accounted for | ✅ |
| Idempotent output | Byte-identical on re-run ✅ |
| All URLs valid | ✅ |

### Files Changed

| File | Change |
|------|--------|
| `scripts/build-cross-source-index.py` | Rewritten for v2 per-talk schema |
| `cross-source-index.json` | Regenerated (121 entries, v2 schema) |
| `index.html` | No changes needed (v2 renderer already in place from prior run) |

---

## A11y BLOCKER Fixes — Mobile Touch Targets & Focus Indicators (2026-06-16)

**Fixed 2 BLOCKER accessibility issues** found during visual review of the Cmd+K search palette.

### BLOCKER 1: Mobile touch target size (WCAG 2.2 2.5.8 — Level AA)

- **Problem**: Asset badges were ~21px tall on mobile (375px viewport). WCAG requires minimum 44×44px.
- **Fix**: Added `@media (max-width: 480px)` rule increasing `.search-palette__result-assets .asset-badge` padding to `14px 12px` and font-size to `0.75rem`.
- **Verification**: Badge height at 375px viewport = **48.0px** (≥44px ✅). Desktop (1280px) unaffected = 21px (base padding preserved ✅).

### BLOCKER 2: Focus indicator visibility (WCAG 2.4.7 — Level AA)

- **Problem**: `.search-palette__result` and `.asset-badge` had no visible `:focus-visible` outline.
- **Fix**: Added `:focus-visible` outline rules:
  - `.search-palette__result:focus-visible` → `outline: 2px solid #4fc3f7; outline-offset: -2px;`
  - `.asset-badge:focus-visible` → `outline: 2px solid #ff9800; outline-offset: 2px;`
- **Verification**: Confirmed CSS rules present in stylesheet with correct colors.

### Files Changed

| File | Change |
|------|--------|
| `index.html` | Added 13 lines of CSS (media query + 2 focus-visible rules) |

| ### Notes
- 3 MEDIUM issues deferred (tracked in `screenshots/VISUAL-REVIEW-REPORT.md`):
  1. Missing `aria-disabled` on disabled rows (WCAG 4.1.2)
  2. Focus trap not cycling through asset badges (WCAG 2.1.2)
  3. Group separator too subtle (WCAG 1.3.1)
- No JS, no HTML, no build step changes — pure CSS additions only.

---

## Color Refactor v2 — Deep Sea Palette (with NEEDS-WORK fixes) (2026-06-16)

**Applied Deep Sea palette to Cmd+K search palette, fixing 2 NEEDS-WORK blockers from visual review.**

### Changes

| Role | Color | Background |
|------|-------|------------|
| Group header text ("MEETUPS", tab names) | `#778DA9` | `#161617` |
| On-page result badge | `#778DA9` | `rgba(119,141,169,0.2)` |
| PDF asset badge text | `#778DA9` | `rgba(119,141,169,0.2)` |
| Video asset badge text | `#E0E1DD` | `rgba(224,225,221,0.15)` |
| Disabled badge | `var(--color-gray-500)` | `rgba(255,255,255,0.03)` (unchanged) |

### Fixes Applied

**Fix #1 — Group header contrast (BLOCKER):** Changed `.search-palette__group-header` text from `var(--color-gray-500)` (#6b7280, 3.74:1) to `#778DA9` (5.31:1, passes WCAG AA ✅).

**Fix #2 — PDF/Video badge distinguishability (BLOCKER):** Changed `.asset-badge-pdf` text from `#49c551` to `#778DA9`; changed `.asset-badge-video` text from `#ff69b4` to `#E0E1DD`. PDF and Video badges now have distinct colors matching their legend swatches.

### Contrast Verification

| Text Color | BG Color | Ratio | WCAG AA | Role |
|------------|----------|-------|---------|------|
| `#778DA9` | `#161617` | 5.31:1 | ✅ Pass | Group header, PDF badge, on-page badge |
| `#E0E1DD` | `#161617` | 13.76:1 | ✅ Pass | Video badge |
| `#6b7280` | `#161617` | 3.74:1 | ✅ Pass (AA Large) | Disabled state |
| `#778DA9` | rgba(119,141,169,0.2) on `#161617` | 4.06:1 | ✅ Pass (AA Large) | On-page badge bg |
| `#778DA9` | rgba(119,141,169,0.15) on `#161617` | 4.40:1 | ✅ Pass (AA Large) | On-page icon bg |
| `#E0E1DD` | rgba(224,225,221,0.15) on `#161617` | 9.48:1 | ✅ Pass | Video badge bg |

### Screenshots

| File | Query | Viewport |
|------|-------|----------|
| `docs/color-refactor-deep-sea-empty.png` | Empty (all entries) | 1280×800 |
| `docs/color-refactor-deep-sea-events.png` | "events" | 1280×800 |
| `docs/color-refactor-deep-sea-signals.png` | "signals" | 1280×800 |
| `docs/color-refactor-deep-sea-richard.png` | "richard" | 1280×800 |
| `docs/color-refactor-deep-sea-signals-mobile.png` | "signals" | 375×812 |

### Files Changed

| File | Change |
|------|--------|
| `index.html` | 6 CSS property changes (3 rules updated) |
| `docs/color-refactor-deep-sea-empty.png` | New screenshot |
| `docs/color-refactor-deep-sea-events.png` | New screenshot |
| `docs/color-refactor-deep-sea-signals.png` | New screenshot |
| `docs/color-refactor-deep-sea-richard.png` | New screenshot |
| `docs/color-refactor-deep-sea-signals-mobile.png` | New screenshot |

### Notes
- No `#415A77` found in index.html — confirmed not used for text-on-dark.
- `.search-palette__group-header--meetups` has no `color` override — inherits `#778DA9` correctly.
- Inline `typeColors` rendering in JS remains unchanged (per-tab category colors preserved).
- Temp files `check-contrast.py` and `screenshot-deep-sea.js` were created and will be cleaned up.

## 2026-06-16 15:43 — Inlined Lunr.js library

**Change:** Removed external CDN dependency for Lunr.js search library.

**Before:**
```html
<script src="https://unpkg.com/lunr@2.3.9/lunr.min.js" defer></script>
```

**After:**
```html
<!-- Lunr.js — lightweight full-text search (8KB gzipped, well-vetted) -->
<script>
/**
 * lunr - http://lunrjs.com - A bit like Solr, but much smaller and not as bright - 2.3.9
 * Copyright (C) 2020 Oliver Nightingale
 * @license MIT
 */
[29KB of minified code inlined]
</script>
```

**Rationale:**
- Eliminates external dependency on unpkg.com CDN
- Site is now fully self-contained (no external JS/CSS dependencies)
- Lunr.js is MIT licensed and stable (v2.3.9 released 2020)
- 29KB is acceptable for a single-file static site
- Improves load performance (one fewer HTTP request)
- Works offline and in air-gapped environments

**Impact:**
- index.html size: 117KB → 146KB (+29KB)
- No functional changes to search behavior
- All search features continue to work as before

---

## 2026-06-16 18:05 — Hero Search Dropdown: Rich Asset Badges (PDF/VIDEO)

**Change:** Hero search bar dropdown now shows rich asset badges matching the Ctrl+K palette richness.

**Before:**
Each meetup result showed only a simple title. No asset badges, no full subtitle metadata.

**After:**
```
[TALK]  Numerai Signals
        Suraj Parmar · Numerai Community Meetup New York City #2 · Sep 2022
        [PDF (EN)]  [VIDEO (EN)]
```

**What changed in `index.html`:**
- Result items changed from `<button>` to `<div>` to allow nested `<a>` tags for asset links
- Full subtitle rendering — speaker · event · date with `formatDate()` for consistent "Sep 2022" formatting
- Reuses the palette's `renderAssets()` function to show PDF/VIDEO links
- Clicking the result navigates to the talk; clicking an asset badge opens the link in a new tab
- Added `.hero-result-assets` CSS with PDF (blue) and VIDEO (gray) badge styling
- Clean console — no errors, no debug logs

**Files Changed:**
| File | Change |
|------|--------|
| `index.html` | Hero result HTML, CSS, and JS updated for rich asset badges |

## 2026-06-16 18:05 — Cleanup: Mockups Folder Moved to docs/

**Change:** Moved `mockups/` directory into `docs/mockups/` to keep project root tidy.

| File | Change |
|------|--------|
| `mockups/v7-hero-search-bar.html` | Moved to `docs/mockups/v7-hero-search-bar.html` |

---

## 2026-06-16 20:55 — Search Index Unified, Lunr.js Removed, Build Script Rewritten

**Change:** Removed external search dependencies and embedded all 110 meetup talk entries directly into `index.html` as a single inline JSON source of truth.

**What was removed:**
- `.github/workflows/build-cross-source-index.yml` — GitHub Action (weekly meetup crawl)
- `assets/search/cross-source-index.json` — old external 121-entry meetup JSON
- `scripts/build-cross-source-index.py` — old 1244-line PDF parser
- **Lunr.js** (~8KB minified full-text search engine) — no longer needed since all data is inline

**What was added:**
- `scripts/build-merged-index.py` — new local build script that fetches meetups README.md, parses talk entries, merges with page entries, and updates `index.html`
- **110 meetup talk entries** embedded in `<script id="search-index">` alongside 38 page entries (148 total)
- Rich metadata preserved: `slides`/`videos`/`availability` fields for PDF/Video asset badges
- Meetup results sorted newest-first by `eventDate`
- Deduplication health check in build script
- `ensemble-results/` added to `.gitignore`

**Build script fixes (2026-06-16 21:30):**
- Talk number regex now supports decimal format (`Talk #1.1` → Bangkok YIEDL talks)
- Title extraction uses LAST `by` before links (fixes "driven by..." in titles)
- City parsing splits on first ` - ` (fixes "Bangkok - Meetup @ Summit" slug)
- Speaker cleanup strips full `@ Org` suffixes
- ID slugs sanitize non-alphanumeric characters (no more `(tokyo)` in IDs)

**YIEDL search results:** 2 → 6 entries (all Bangkok YIEDL.ai talks now parse correctly)

**Git commits:**
| Hash | Message |
|------|---------|
| `2cdd648` | refactor: unify search index into index.html, remove external dependencies |
| `b3f86a1` | fix: improve README parser, add dedup health check, gitignore ensemble-results |
| `dc1e462` | fix: make talk badge color consistent between hero and palette |
| *(pending)* | fix: remove mobile FAB, update hero search placeholder |

**Usage:**
```bash
python3 scripts/build-merged-index.py
git commit -am "Update search index"
git push
```

---

## 2026-06-16 22:15 — Remove Mobile FAB, Update Search Placeholder

**Change:** Removed the floating blue search button (FAB) that appeared on mobile/touch devices. Also updated hero search bar placeholder text.

**Removed:**
- FAB HTML element (`<button id="search-fab">`)
- FAB CSS (`.search-fab` with positioning, sizing, active states, media query)
- FAB JS references (variable declaration, touch handling, click listener)

**Changed:**
- Hero search placeholder: `"Search events, tools, meetups..."` → `"Search projects, events, team…"`
- FAB no longer shows on any viewport size (was previously only visible on mobile via `isTouch` detection)

**Git commits:**
| Hash | Message |
|------|---------|
| `dc1e462` | fix: make talk badge color consistent between hero and palette |
| *(pending)* | fix: remove mobile FAB, update hero search placeholder |

---

## 2026-06-16 23:00 — Light/Dark Theme Toggle, Search Bar Redesign, Colour Fixes

**Change:** Major light/dark theme implementation with theme toggle, search bar improvements, and multiple colour refinements.

### Added
- **Theme toggle button** — Replaced `⌘K` badge in search bar with sun/moon SVG toggle (transparent bg, blends into search bar like search icon)
- **FOUC-prevention script** — Sets `data-theme` from `localStorage` before CSS paints to prevent flash
- **`[data-theme="light"]` CSS override block** — Full light theme with inverted grays, adapted category colours, white cards, slate borders, light-mode aurora/glass effects
- **Toggle JS** — Click handler for `data-theme` switching with `localStorage` persistence
- **Dark theme override** in `[data-theme="dark"]` — Full complementary palette for toggle switching
- **Smooth transitions** on `body` for background/colour changes

### Changed
- **Search placeholder:** `"Search projects, events, team…"` → `"Type to search, or press Ctrl + K."`
- **Out of Sample preview image:** Replaced dead YouTube `an_webp` URL with local `assets/img/out-of-sample.jpg` (static maxresdefault thumbnail)
- **Light theme description colour:** Fixed CSS specificity bug (added `.hero-text` qualifier) and set to `#6C757D` (WCAG AA 4.65:1 contrast on `#F8F9FA`) after ensemble analysis rejected `#B0B0B0` (2.05:1)
- **CTA button colours in light theme:** Changed from blue `#0D6EFD` to Numerai tab-style `#f7f7f7`/`#333333`/`#e0e0e0`

### Files changed
| File | Change |
|------|--------|
| `index.html` | +236 / -18 lines — theme toggle, FOUC script, light/dark CSS, JS, colour fixes |
|| `assets/img/out-of-sample.jpg` | New — Out of Sample podcast thumbnail (169KB JPEG) |
|| `docs/mockups/v12-light-final.html` | New — Final light theme mockup with all refinements |

### Key decisions
- Light theme uses same layout as dark (CSS variable swap only)
- Theme toggle icon sits bare on search bar (no button bg/border) — matches search icon pattern
- Default theme: dark (existing users see no change)
- Description colour `#6C757D` chosen via llm-ensemble panel analysis for WCAG AA compliance

|---

## 2026-06-16 23:30 — Image swap: out-of-sample.jpg → out_of_sample.jpg + log.md created

**Change:** Replaced `out-of-sample.jpg` (YouTube maxresdefault thumbnail, was 404 origin) with a freshly uploaded `out_of_sample.jpg` in assets/img. Also created this `docs/log.md` file.

### Files changed
| File | Change |
|------|--------|
| `index.html` | Image src updated: `out-of-sample.jpg` → `out_of_sample.jpg` |
| `assets/img/out_of_sample.jpg` | New — uploaded by Joe (61KB JPEG) |
| `docs/log.md` | New — project changelog |

### Note
- Old `out-of-sample.jpg` was never a real file on disk (just a URL-backed img src), so no stale file to clean up.

