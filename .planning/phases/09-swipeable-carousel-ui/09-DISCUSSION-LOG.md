# Phase 9: Swipeable Carousel UI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-10
**Phase:** 09-swipeable-carousel-ui
**Areas discussed:** Carousel Implementation, Layout Density, Slider Scope

---

## Carousel Implementation

| Option | Description | Selected |
|--------|-------------|----------|
| Embla Carousel (Recommended) | Use Embla Carousel (Lightweight, flexible, great touch support) | ✓ |
| Pure CSS Scroll Snap | Simple, no dependencies, but less control over desktop arrows | |
| Swiper.js | Feature rich, but larger bundle size | |

**User's choice:** Embla Carousel (Recommended)
**Notes:** User agreed it needs research and suggested library usage.

---

## Layout Density

| Option | Description | Selected |
|--------|-------------|----------|
| Partial peek (Recommended) | 1.2 cards visible to signal swiping | ✓ |
| Full width focus | One card at a time, clear focus | |

**User's choice:** Partial peek (Recommended)
**Notes:** -

---

## Slider Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Global Slider (Recommended) | One slider at top of section affects all cards | ✓ |
| Per-card Slider | Slider inside each card | |

**User's choice:** Global Slider (Recommended)
**Notes:** User explicitly stated "confidence slider should affect all cards".

---

## the agent's Discretion

- Visual styling of arrows.
- Expanded state handling in carousel.

## Deferred Ideas

- Carousel filtering.
- Route icons.
