---
name: Sonic Luminescence
colors:
  surface: '#151023'
  surface-dim: '#151023'
  surface-bright: '#3c364a'
  surface-container-lowest: '#100b1d'
  surface-container-low: '#1e192b'
  surface-container: '#221d2f'
  surface-container-high: '#2c273a'
  surface-container-highest: '#373246'
  on-surface: '#e8def9'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e8def9'
  inverse-on-surface: '#332d41'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dce6'
  primary: '#e0fdff'
  on-primary: '#00373a'
  primary-container: '#00f2fe'
  on-primary-container: '#006a70'
  inverse-primary: '#00696f'
  secondary: '#ffb1c4'
  on-secondary: '#65002e'
  secondary-container: '#ff4a8d'
  on-secondary-container: '#590028'
  tertiary: '#fff5f0'
  on-tertiary: '#4d2600'
  tertiary-container: '#ffd2b1'
  on-tertiary-container: '#924e00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ff6ff'
  primary-fixed-dim: '#00dce6'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#ffd9e1'
  secondary-fixed-dim: '#ffb1c4'
  on-secondary-fixed: '#3f001a'
  on-secondary-fixed-variant: '#8f0044'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#151023'
  on-background: '#e8def9'
  surface-variant: '#373246'
typography:
  display-xl:
    fontFamily: Syne
    fontSize: 56px
    fontWeight: '800'
    lineHeight: 64px
    letterSpacing: -0.03em
  display-xl-mobile:
    fontFamily: Syne
    fontSize: 36px
    fontWeight: '800'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Syne
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Syne
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Syne
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Syne
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  gutter-lg: 2rem
  margin: 2rem
  margin-mobile: 1rem
  margin-desktop: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

The design system blends computational precision with club-culture kinetic energy. Engineered for music producers, audio engineers, A&R scouts, and digital audiophiles, the interface delivers an immersive studio atmosphere: intense, high-focus, and visually acoustic.

The aesthetic fuses **Glassmorphism** with **Futuristic High-Contrast Neon**:
- **Atmospheric Depths:** Multi-tiered midnight violet backdrops recreate the physical feel of dim hardware mastering rooms.
- **Electric Precision:** High-frequency neon accents (cyan, magenta, amber) evoke audio visualizers, peak meters, and laser optics without cluttering usability.
- **Frosted Sonic Substrates:** Translucent tinted layers with micro-borders provide optical grounding for dynamic waveforms, radar graphs, and confidence scores.

## Colors

The palette operates under a native dark architecture where luminous signals emerge from midnight voids.

### Palette Roles & Usage
- **Primary (`#00F2FE` Electric Cyan):** Represents sonic clarity and core intelligence. Used for primary interactive triggers, active audio waveforms, predictive genre tags, and peak equalizer signals. Supported by gradient sibling `#4FACFE`.
- **Secondary (`#FF007F` Neon Magenta):** Represents cadence, rhythm, and secondary predictions. Applied to high-confidence highlights, frequency band indicators, and real-time recording states. Supported by soft violet `#E040FB`.
- **Tertiary (`#FF8C00` Amber Pulse):** Highlights rhythmic tempo (BPM), transient energy metrics, and cautionary alerts.
- **Neutral Canvas (`#0F0A1C` to `#18112C`):** Deep midnight obsidian and bruised violet base canvas. 
- **Surface Tiers:**
  - Base canvas: `#0F0A1C`
  - Elevated glass surface: `#21173D` at 65%–80% opacity with backdrop blur.
  - Interactive hover state: `#2A1E4E`.
  - Structural boundary: `#3A2A68` at 70% opacity.
- **Text & Contrast Hierarchy:**
  - High Emphasis: `#FFFFFF` (100%)
  - Medium Emphasis: `#B8B2CE` (70%)
  - Low Emphasis: `#6F658E` (45%)

## Typography

The type scale juxtaposes **Syne’s** structural, avant-garde geometry against **Plus Jakarta Sans’s** ergonomic, high-legibility letterforms.

- **Syne (Headlines & Metrics):** Delivers distinct sonic character for genre titles, model prediction outcomes, and numerical data points. All display weights sit between 600 and 800 with tight tracking to evoke audio mastering hardware panels.
- **Plus Jakarta Sans (Body & Controls):** Retains geometric balance while remaining crisp against dark, saturated glass layers. 
- **Micro-Labels & Technical Telemetry:** `label-sm` applies uppercase styling with expanded letter-spacing (`0.08em`) to mimic rack-mounted synthesizers and spectrometer dials.

## Layout & Spacing

The layout is built on a responsive 12-column fluid grid system engineered for real-time audio visualization, waveform analysis, and split-screen comparison tools.

### Grid Breakpoints
- **Mobile (< 768px):** 4-column layout, `margin-mobile: 1rem`, `gutter-sm: 1rem`. Dynamic stack flow: audio dropzones convert to full-width targets, collapsing secondary confidence graphs into swipeable sheets.
- **Tablet (768px – 1024px):** 8-column layout, `margin: 2rem`, `gutter: 1.5rem`. Side-by-side analysis view with fixed player dock.
- **Desktop (> 1024px):** 12-column layout, max-width `1440px`, `margin-desktop: 3rem`, `gutter-lg: 2rem`. Multitrack visual layout supporting continuous side-by-side genre distribution charts and real-time spectral analyzers.

### Spatial Rhythms
Spacing operates on a strict 8pt rhythm (scaled down to 4pt for compact component internals). Component padding follows a `space-sm` to `space-md` distribution to maintain tight, tool-grade ergonomics.

## Elevation & Depth

Visual hierarchy uses a calibrated triple-layer glass system illuminated by chromatic backlights.

### Surface Tiers
1. **Level 0 (Floor Canvas):** Flat `#0F0A1C` with ambient radial gradients (`#18112C` at top-center; faint `#3A2A68` glow at bottom-right).
2. **Level 1 (Docked Containers & Workspaces):** Background `rgba(33, 23, 61, 0.55)`, backdrop-filter `blur(16px)`, border `1px solid rgba(58, 42, 104, 0.6)`. Casts a subtle deep drop shadow: `0 12px 32px -4px rgba(5, 3, 10, 0.6)`.
3. **Level 2 (Active Cards & Floating Drawers):** Background `rgba(33, 23, 61, 0.85)`, backdrop-filter `blur(24px)`, border `1px solid rgba(0, 242, 254, 0.25)`. Shadow: `0 16px 40px -8px rgba(0, 0, 0, 0.7)`.
4. **Level 3 (Overlays, Modals, Peak Elements):** Background `rgba(24, 17, 44, 0.95)`, border `1px solid rgba(255, 0, 127, 0.4)`. Casts a dual shadow: `0 24px 48px -12px rgba(0, 0, 0, 0.8)`, paired with a tinted ambient glow `0 0 32px rgba(255, 0, 127, 0.15)`.

### Chromatic Glow System
High-certainty AI results and active audio states utilize glowing borders:
- **Cyan Resonance:** `box-shadow: 0 0 20px -2px rgba(0, 242, 254, 0.35)`
- **Magenta Resonance:** `box-shadow: 0 0 20px -2px rgba(255, 0, 127, 0.35)`

## Shapes

The interface balances sleek organic tech curves with precise audio hardware edges.

- **Primary Radius (`0.5rem` / 8px):** Applied to buttons, input fields, slider handles, and segment controllers.
- **Card Radius (`1rem` / 16px):** Applied to glass panels, spectrogram wrappers, file drop zones, and analytics containers.
- **Outer Shell Radius (`1.5rem` / 24px):** Reserved for floating player bars, persistent control shells, and primary modal wrappers.
- **Pill Geometry (Full Curve):** Reserved specifically for genre identification badges, AI certainty tags, status pips, and media controls.

## Components

### Buttons
- **Primary Kinetic:** Gradient fill (`linear-gradient(135deg, #00F2FE, #4FACFE)`), text `#0F0A1C` (bold), shape `0.5rem`, shadow `0 4px 16px rgba(0, 242, 254, 0.3)`. Hover: translateY(-1px), glow expansion to `24px`.
- **Secondary Glass:** Background `rgba(33, 23, 61, 0.6)`, border `1px solid #3A2A68`, text `#FFFFFF`. Hover: border-color `#00F2FE`, background `rgba(42, 30, 78, 0.8)`.
- **Accent Magenta Action:** Gradient fill (`linear-gradient(135deg, #FF007F, #E040FB)`), text `#FFFFFF`, shadow `0 4px 16px rgba(255, 0, 127, 0.3)`. Reserved for live recording and export actions.

### Cards & Glass Panels
- Base surface `rgba(33, 23, 61, 0.65)` layered with `backdrop-filter: blur(16px)`.
- Perimeter outline `1px solid rgba(58, 42, 104, 0.5)`.
- Padding `1.5rem`. When card is focused or actively playing, border transitions to `rgba(0, 242, 254, 0.5)` with Cyan Resonance glow.

### Chips & Genre Tags
- **Base Style:** Pill-shaped, height `28px`, padding `0 12px`, typography `label-md`.
- **Predicted Top Genre:** Background `rgba(0, 242, 254, 0.12)`, border `1px solid #00F2FE`, text `#00F2FE`.
- **Secondary Sub-genre:** Background `rgba(255, 0, 127, 0.12)`, border `1px solid #FF007F`, text `#FF007F`.
- **Inactive/Candidate Tag:** Background `rgba(58, 42, 104, 0.3)`, border `1px solid transparent`, text `#B8B2CE`.

### Inputs & Audio Dropzones
- **Text/Search Inputs:** Height `44px`, background `rgba(15, 10, 28, 0.7)`, border `1px solid #3A2A68`, font `body-md`, placeholder `#6F658E`. Focus: border `#00F2FE`, box-shadow `0 0 0 3px rgba(0, 242, 254, 0.15)`.
- **Audio Drag-and-Drop Zone:** Min-height `180px`, dashed boundary `2px dashed #3A2A68`, background `rgba(24, 17, 44, 0.4)`. Drag-over state transitions border to `#00F2FE`, fill to `rgba(0, 242, 254, 0.05)`.

### Controls & Visualization Elements
- **Sliders (EQ / Confidence / Gain):** Track height `4px`, background `#2A1E4E`. Filled progress gradient `linear-gradient(90deg, #4FACFE, #00F2FE)`. Thumb size `16px` circular, solid `#FFFFFF` with `#00F2FE` drop shadow.
- **Metric Badges:** Monospaced Syne readout mounted inside a dark recessed container (`#0F0A1C`), bordered by `#3A2A68`, with amber `#FF8C00` indicators for tempo/BPM and electric cyan for AI certainty percentages.
- **Dynamic Waveform Containers:** Canvas background `rgba(15, 10, 28, 0.9)`, border `1px solid #3A2A68`, rounded `0.75rem`. Unplayed track rendered in `#3A2A68`, active audio rendered in `#00F2FE` gradient with animated playback playhead in neon `#FF007F`.