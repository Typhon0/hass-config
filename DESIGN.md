---
name: Obsidian Cockpit
description: Glassmorphic dark-mode tablet & mobile home control dashboard with tactile feedback and Apple SF typography
colors:
  primary: "#3182b7"
  primary-light: "#57a5dc"
  secondary: "#7a7d7f"
  danger: "#8b3333"
  neutral-bg: "#0c0d0d"
  neutral-surface: "#1e2223"
  neutral-surface-muted: "rgba(115, 115, 115, 0.25)"
  neutral-surface-active: "rgba(255, 255, 255, 0.85)"
  neutral-text: "rgba(255, 255, 255, 0.96)"
  neutral-text-muted: "rgba(151, 152, 156, 0.9)"
  neutral-text-dark: "#4b5254"
typography:
  display:
    fontFamily: "sf display, SF Pro Display, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 5.25vw, 4.5rem)"
    fontWeight: 300
    lineHeight: "0.95"
    letterSpacing: "-0.06em"
  headline:
    fontFamily: "sf display, SF Pro Display, system-ui, sans-serif"
    fontSize: "clamp(2rem, 3.1vw, 3.2rem)"
    fontWeight: 760
    lineHeight: "0.98"
    letterSpacing: "-0.055em"
  title:
    fontFamily: "sf text, SF Pro Text, system-ui, sans-serif"
    fontSize: "clamp(1.1rem, 1.55vw, 1.6rem)"
    fontWeight: 650
    lineHeight: "1.2"
    letterSpacing: "-0.03em"
  body:
    fontFamily: "sf text, SF Pro Text, system-ui, sans-serif"
    fontSize: "clamp(0.85rem, 1.12vw, 1.1rem)"
    fontWeight: 430
    lineHeight: "1.36"
    letterSpacing: "normal"
  label:
    fontFamily: "sf text, SF Pro Text, system-ui, sans-serif"
    fontSize: "clamp(0.7rem, 0.9vw, 0.95rem)"
    fontWeight: 520
    lineHeight: "1.15"
    letterSpacing: "-0.02em"
rounded:
  sm: "0.65vw"
  md: "1.22vw"
  lg: "30px"
  pill: "9999px"
  full: "50%"
spacing:
  xs: "0.4vw"
  sm: "0.8vw"
  md: "1.3vw"
  lg: "2.05vw"
  xl: "2.8vh"
components:
  button-primary:
    backgroundColor: "{colors.neutral-surface-muted}"
    textColor: "{colors.neutral-text-muted}"
    rounded: "{rounded.md}"
    padding: "1.2vw"
  button-primary-active:
    backgroundColor: "{colors.neutral-surface-active}"
    textColor: "{colors.neutral-text-dark}"
    rounded: "{rounded.md}"
    padding: "1.2vw"
  badge-notify:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.neutral-text}"
    rounded: "{rounded.full}"
    padding: "0.3vw"
---

# Design System: Obsidian Cockpit

## Overview

**Creative North Star: "The Obsidian Cockpit"**

The Obsidian Cockpit is a disciplined, architectural dark-mode design system built for wall-mounted tablet kiosk interfaces and daily mobile companion control. Drawing inspiration from high-end aerospace consoles and Apple's refined human interface ergonomics, it balances extreme glanceability with quiet residential discretion. The interface recedes peacefully into the living room environment, coming alive with tactile energy only when engaged.

Depth is achieved not through artificial heavy drop shadows, but through physical tonal layering, translucency, and frosted glass blurs (`backdrop-filter`). Information is structured in strict spatial hierarchies anchored by typography from the Apple San Francisco (SF UI) family, ensuring critical metrics are immediately legible from across the room.

**Key Characteristics:**
- **Luminescent Translucency:** Frosted obsidian backgrounds layered over dark substrates.
- **Physical Inversion:** Idle cards sleep in smoked glass; activated cards invert into crisp, luminous white surfaces.
- **Micro-Spring Tactility:** Haptic feedback paired with responsive scale bounce animations on every tap.
- **Restrained Color Economy:** A single electric cyan blue accent for active entities, preserving night-time eye comfort.

## Colors

The palette relies on deep mineral neutrals with high-contrast functional inversion and a tightly metered blue indicator accent.

### Primary
- **Electric Cyan Blue** (`#3182b7`): Used exclusively for active state icons, toggle highlights, and interactive selection indicators. Never sprayed decoratively across backgrounds.

### Secondary
- **Slate Track** (`#7a7d7f`): Used for slider grooves, secondary active controls, and subtle structural dividers.

### Neutral
- **Deep Obsidian Void** (`#0c0d0d`): Canvas background behind all views.
- **Smoked Glass Surface** (`rgba(30, 34, 35, 0.78)`): Base surface for interactive cards, popups, and dialog overlays.
- **Translucent Idle Tile** (`rgba(115, 115, 115, 0.25)`): Background for inactive, unpowered, or idle tiles.
- **Inverted Luminous Tile** (`rgba(255, 255, 255, 0.85)`): High-contrast background for active or running states.
- **Frosted Sidebar Glass** (`rgba(12, 12, 14, 0.52)`): Dedicated blur container for persistent time and household status.
- **Primary Text** (`rgba(255, 255, 255, 0.96)`): Primary labels, room names, and large time readouts.
- **Secondary Text** (`rgba(151, 152, 156, 0.9)`): State labels, timestamps, and secondary sensor readouts.
- **Active Dark Text** (`#4b5254`): Foreground text inside inverted white cards.

### Danger / Alert
- **Crimson Beacon** (`#8b3333`): Notification count badges, firmware update alerts, and security alarm triggers.

### Named Rules
**The Single Accent Rule.** `#3182b7` is strictly reserved for live interactive states and connected hardware feedback. The accent must never exceed 5% of any screen surface.
**The Binary Inversion Rule.** When an appliance or light transitions from off to on, the card inverts from translucent dark (`rgba(115,115,115,0.25)`) to luminous white (`rgba(255,255,255,0.85)`) with dark text (`#4b5254`), making active rooms instantly visible from across the room.

## Typography

**Display Font:** `sf display` (SF UI Display, with system fallback `SF Pro Display, system-ui, sans-serif`)
**Body Font:** `sf text` (SF UI Text, with system fallback `SF Pro Text, Roboto, sans-serif`)
**Label/Mono Font:** `sf mono` (SFMono, for precise sensor logs and code)

**Character:** Architectural, precise, and understated. Numbers and timestamps dominate the display scale with ultralight precision, while room titles maintain confident, authoritative weight.

### Hierarchy
- **Display** (weight `300`, `5.25vw` / `clamp(2.5rem, 5.25vw, 4.5rem)`, line-height `0.95`, letter-spacing `-0.06em`): Primary glanceable clock on the sidebar.
- **Headline** (weight `760`, `clamp(34px, 3.1vw, 50px)`, line-height `0.98`, letter-spacing `-0.055em`): Room section headers (e.g. "Salon", "Cuisine").
- **Title** (weight `650`, `1.55vw` / `clamp(1.1rem, 1.55vw, 1.6rem)`, line-height `1.2`, letter-spacing `-0.03em`): Date subtitles, card names, and primary entities.
- **Body** (weight `430`, `1.12vw` / `clamp(0.85rem, 1.12vw, 1.1rem)`, line-height `1.36`): Sensor readings, climate statuses, and weather copy.
- **Label** (weight `520`, `0.9vw` / `clamp(0.7rem, 0.9vw, 0.95rem)`, line-height `1.15`, letter-spacing `-0.02em`): Subtitles, schedule next-events, and badge chips.

### Named Rules
**The Glance Scale Rule.** If a number or time reading cannot be deciphered at 2 meters on a wall tablet, it must either be scaled up to Display/Headline or removed from the default view.

## Layout

The spatial model uses an asymmetrical responsive grid layout driven by `custom:grid-layout`:

- **Master Desktop / Kiosk View (`> 1200px`):**
  - Left column: Fixed 1fr sidebar housing date, clock, household occupants, and persistent weather.
  - Center & Right columns: 4 equal content columns (`repeat(4, minmax(0, 1fr))`) mapping dedicated room zones (`salon`, `bureau`, `cuisine`, `chambre`, `media`, `buanderie`, `maison`, `footer`).
  - Grid Gap: `calc(var(--custom-layout-card-padding) * 0.92)` (~2vw).
- **Tablet Intermediate View (`801px – 1200px`):**
  - 0.95fr sidebar + 2 content columns, vertically stacked.
- **Mobile View (`< 800px`):**
  - 2 equal columns with full-width top sidebar and stacked room containers.
  - Grid Gap expands to `calc(var(--custom-layout-card-padding) * 1.45)`.

## Elevation & Depth

Surfaces are intentionally flat and un-shadowed at rest (`ha-card-box-shadow: none`). Spatial depth is conveyed exclusively through frosted glass materials, backdrop-filter blurs, and translucent surface stackings:

- **Frosted Blur (Sidebar):** `backdrop-filter: blur(18px)` over `rgba(12, 12, 14, 0.52)`.
- **Frosted Modal (Popups):** `backdrop-filter: blur(2.6em) brightness(0.72)` over `rgba(30, 34, 35, 0.92)`.
- **Inset Depth (Bar cards):** Recessed gauges use `radial-gradient(circle, rgba(52, 57, 58, 0.1) 0%, rgba(17, 18, 18, 0.2) 75%)` with inner shadow `inset 0 0 25px rgba(0,0,0,0.27)`.
- **Header Separation:** Room headers carry subtle text depth with `text-shadow: 0 1px 10px rgba(0, 0, 0, 0.16)`.

### Named Rules
**The Flat-At-Rest Rule.** Never add drop shadows to resting cards. Shadows belong only to recessed gauges (as insets) or dialog backdrops.

## Shapes

- **Interactive Room Tiles:** Curvilinear squircle corner radius of `1.22vw` (~16px–20px depending on screen width).
- **Sidebar Container:** Generous `30px` rounded frame.
- **Dialog & Popups:** Soft `1.35em` radius.
- **Pills & Footers:** Tight `0.65vw` radius for utility action chips.
- **Status & Notification Badges:** Circular `50%` pill badges.

## Components

### Buttons & Interactive Tiles
- **Shape:** Border-radius `1.22vw` with zero borders (`border: none`).
- **Aspect Ratio:** Square 1:1 ratio for room appliance switches.
- **Idle State:** Background `rgba(115, 115, 115, 0.25)`, icon color `#9da0a2`, text color `#97989c`.
- **Active State:** Background `rgba(255, 255, 255, 0.85)`, icon color `#3182b7`, text color `#4b5254`.
- **Tap Animation (`card_bounce`):** 800ms cubic-bezier(0.22, 1, 0.36, 1) spring compression to scale `0.94` (tablet) or `0.92` (phone).
- **Haptic:** `medium` on tap, `success` on double-tap.

### Room Section Headers
- **Structure:** Title with trailing subtle chevron icon (`rgba(255,255,255,0.26)`), subtitle or next scheduled event underneath.
- **Typography:** `font-weight: 760`, size `clamp(34px, 3.1vw, 50px)`.
- **Background:** Transparent with `margin: 0` and zero padding underneath.

### Sidebar Kiosk Panel
- **Material:** Dark frosted glass `rgba(12, 12, 14, 0.52)` with `blur(18px)`.
- **Elements:** Large digital clock, French formatted day & date, household avatar presences, climate summary, and energy tariff pill (`HP` / `HC`).

### Notification Badges
- **Shape:** Circular `border-radius: 50%`, size `1.8vw`.
- **Colors:** Crimson `#8b3333` with bright text `#d6d6d6`, bold font weight `700`.
- **Positioning:** Floating top-right corner of card (`top: -0.9vw`, `right: -1vw`).

## Do's and Don'ts

### Do:
- **Do** respect the binary inversion: active devices must pop with clear contrast against inactive devices.
- **Do** use `sf display` for numbers and large headers, and `sf text` for all multi-line content.
- **Do** maintain touch target sizes of at least 48x48px on wall tablets to allow easy tapping from an angle.
- **Do** keep animations fast and elastic: duration ≤ 800ms using `cubic-bezier(0.22, 1, 0.36, 1)`.

### Don't:
- **Don't** add colored backgrounds (red, green, yellow) across full cards unless alerting a critical house failure.
- **Don't** introduce heavy outer drop shadows or multi-colored borders.
- **Don't** crowd the layout with decorative graphs when a single glanceable metric is sufficient.
- **Don't** use standard browser serif fonts or generic Arial/Comic styles.

