---
name: Lumina Finance
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#bcc7de'
  on-secondary: '#263143'
  secondary-container: '#3e495d'
  on-secondary-container: '#aeb9d0'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e79400'
  on-tertiary-container: '#563400'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 4px
  xs: 0.5rem
  sm: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  container-max: 1440px
  gutter: 24px
---

## Brand & Style

The design system is engineered for a premium, high-trust financial environment driven by artificial intelligence. The brand personality is sophisticated, analytical, and forward-looking, aiming to evoke a sense of "digital precision" and "calm intelligence."

The visual style utilizes a refined **Glassmorphism** approach. It balances deep, obsidian-like surfaces with translucent layers and vibrant cyan accents to signify active AI processing and financial growth. Elements should feel like physical glass panels floating in a void, using light and blur to establish a clear hierarchy without relying on heavy solid containers.

## Colors

This design system utilizes a "Deep Space" palette optimized for OLED displays and high-end desktop environments.

- **Primary (#06b6d4):** A vibrant Cyan used for growth indicators, primary actions, and AI state transitions.
- **Secondary (#1e293b):** A Slate Blue used for elevated glass panels and secondary containers.
- **Neutral (#0f172a):** The core background color, providing a deep, stable foundation.
- **Tertiary (#f59e0b):** A muted Amber reserved strictly for cautionary data, warnings, or high-risk financial shifts.

Apply a 60% opacity to secondary surfaces when used in glass containers to allow background blurs to emerge.

## Typography

The typography system relies exclusively on **Inter** to maintain a systematic, utilitarian aesthetic that feels professional and legible. 

- **Display & Headlines:** Use tighter letter spacing and heavier weights to create a sense of authority. 
- **Data Points:** For financial figures, use `body-lg` with a medium weight to ensure numerical clarity.
- **Labels:** Use the `label-caps` style for small metadata and secondary navigation items to differentiate from conversational text.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for data density, transitioning to a fluid model for the chat interface.

- **Desktop:** 12-column grid with a 1440px max-width. Sidebar occupies 3 columns; main chat area occupies 9 columns.
- **Mobile:** Single column with 16px side margins.
- **Rhythm:** Utilize a 4px baseline. Components should generally use `md` (24px) padding for internal breathing room to reinforce the premium, airy feel.

## Elevation & Depth

Hierarchy is established through **Backdrop Blurs** and **Inner Glows** rather than traditional drop shadows.

- **Level 1 (Base):** Deep Charcoal (#0f172a).
- **Level 2 (Panels):** Secondary color at 40% opacity with a 20px backdrop blur and a 1px border at 10% white opacity.
- **Level 3 (Modals/Popovers):** Secondary color at 60% opacity with a 40px backdrop blur. Add a subtle "inner glow" using a top-left white stroke at 5% opacity to simulate light hitting the edge of the glass.

## Shapes

The design system utilizes **Pill-shaped (3)** geometry for all interactive and high-visibility elements. 

- **Primary Buttons & Chips:** Full pill radius (999px).
- **Cards & Chat Bubbles:** Rounded-xl (24px) for a soft, modern enclosure.
- **Inputs:** Pill-shaped to match the action-oriented nature of the assistant.

## Components

### Chat Bubbles
- **User:** Primary Cyan gradient background. Text is white/high-contrast. Right-aligned.
- **AI Assistant:** Secondary color glass panel (40% opacity). Text is light grey. Left-aligned with a subtle glow border.

### Floating Input Bar
- A pill-shaped container positioned at the bottom-center. 
- Features a 30px backdrop blur and a 1px subtle white border. 
- The "Send" button is a circular Cyan icon button that appears only when text is present.

### Action Chips
- Used for quick AI suggestions. 
- Pill-shaped with a transparent background and a 1px Cyan border. 
- Hover state: Background fills with 10% Cyan opacity.

### Glassy Sidebar
- A fixed vertical navigation bar on the left.
- No solid background; uses a "frost" effect (25px blur) that tints the underlying wallpaper.
- Active states are indicated by a vertical Cyan line and a subtle glow behind the icon.

### Cards & Finance Modules
- Glass panels with 16px padding.
- Headlines should be `title-md`. 
- Incorporate mini-sparklines using the Primary Cyan color to indicate financial trends.