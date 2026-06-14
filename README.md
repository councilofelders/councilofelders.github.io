# Numerai Council of Elders Hub

A curated landing page for Numerai community initiatives — events, tools, learning resources, and the Council of Elders team.

**Site:** [councilofelders.github.io](https://councilofelders.github.io)

---

## About

The Council of Elders is a community-elected body of Numerai participants who bridge the Numerai team and the broader community. This hub serves as a central entry point to everything CoE:

- **Decentralized AI Days** — global meetup series (Tokyo, Vienna, San Francisco, and more)
- **Community tools** — NumerBay, Numeroo, Shiny Numerati, YAND, Tippening, NumerDiff, NumeraiAgentBench
- **Educational content** — meetup archives, blog posts, Kaggle notebooks
- **Team profiles** — the 9 current elders
- **Treasury transparency** — Safe multi-sig wallet

---

## Tabs

| Tab | Content |
|-----|---------|
| 🏠 **Home** | Spotlight (Out of Sample podcast) + Join the Discussion |
| 🛠️ **Projects** | 7 community-built tools in a 3-column card grid |
| 📅 **Events** | Decentralized AI Days hero + timeline of 15 global meetups (2022–2026) |
| 📚 **Learn** | Meetup Materials, Blog, and Kaggle Notebooks cards |
| 👥 **Team** | 9 elder profiles with clickable Numerai profile photos |
| 💰 **Funds** | CoE multi-sig wallet overview |

---

## Tech Stack

- **Single HTML file** — pure HTML, CSS, and vanilla JS (no frameworks, no build tools)
- **Dark theme** — `#161617` base with glassmorphism (`backdrop-filter: blur(12px)`)
- **Responsive** — 4 breakpoints: desktop (≥1024px), tablet (768–1023px), mobile (<768px), small mobile (≤480px)
- **ARIA tabs** — keyboard-navigable, screen-reader announcements, skip link
- **Aurora background** — CSS-animated gradient layers with `prefers-reduced-motion` support
- **Hosted on** — GitHub Pages (org repo)

---

## File Structure

```
councilofelders.github.io/
├── index.html              ← Single-page landing (all CSS + JS inlined)
├── README.md               ← This file
├── .gitignore
└── assets/img/
    ├── coe_logo.png        ← Logo
    ├── decentralized-ai-days.jpeg  ← Events hero visual
    ├── funds.jpg           ← Funds tab preview
    ├── join_the_discussion.jpg     ← Home tab community card
    ├── numerbay.jpg        ← Project cards ×7
    ├── numeroo.jpg
    ├── shiny_numerati.jpg
    ├── yand.jpg
    ├── tippening.jpg
    ├── numerdiff.jpg
    ├── numerai_agent_bench.jpg
    └── elders/             ← Elder profile photos ×9
        ├── aventurine.jpg
        ├── correlator.png
        ├── ia_ai.jpg
        ├── jefferythewind.jpg
        ├── jrb.jpg
        ├── numerologist.jpg
        ├── shatteredx.jpg
        ├── uuazed.jpg
        └── wigglemuse.jpg
```

---

## Key Design Decisions

- **All-or-nothing tab overflow** — when any tab label would overflow, all labels hide (emoji-only mode) rather than progressive right-to-left hiding
- **Glassmorphism tokens** — shared `:root` custom properties (`--glass-bg`, `--glass-border`, `--glass-blur`) applied via concrete selectors across 7 container types
- **Button standardization** — all CTAs follow `.featured-cta` with `width: fit-content`, consistent height (51px), padding (13px 24px), and border-radius (8px)
- **Flag circles for timeline** — event timeline uses country flag images (`flagcdn.com`) with `srcset` (w80/w160/w320) for responsive photo dots
- **SVG sprite** — location pin icon deduplicated via hidden `<symbol>` with `<use>` references

---

## External Links

- **Podcast:** [YouTube @NumeraiCoE](https://www.youtube.com/@NumeraiCoE)
- **Community:** [X @NumeraiCoE](https://x.com/NumeraiCoE) · [Discord](https://discord.gg/numerai)
- **Events calendar:** [Luma](https://luma.com/decentralized_ai_events)
- **Forum:** [forum.numer.ai](https://forum.numer.ai/)
- **Blog:** [Medium](https://medium.com/numerai-council-of-elders)
- **Meetup archive:** [GitHub](https://github.com/councilofelders/meetups)
- **Treasury:** [Safe Wallet](https://app.safe.global/home?safe=eth:0xF58B7c28DAF13926329ef0c74FA3f7258f5A9131)

---

## Credits

- **Design:** [ia_ai / @matlabulous](https://x.com/matlabulous)
- **Funding:** [Numerai](https://numer.ai/)
- **Built by:** The Numerai community

---

## Development

The page is a single `index.html` — no build step required. To preview locally, serve with any static file server:

```bash
python3 -m http.server 8000
# or
npx serve .
```

All edits go directly into `index.html`. Contributions and suggestions welcome via the [Numerai forum](https://forum.numer.ai/).

---

*Prototype · 2026*
