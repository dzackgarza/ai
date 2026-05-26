---
name: ux-antipatterns
description: Reference guide for detecting and fixing UX anti-patterns in frontend code. Covers layout shifts, silent failures, double-submits, focus theft, missing feedback, and more. Use as reference when reviewing frontend UI code.
source: https://github.com/cassiozen/UX-antipatterns
---
# UX Anti-Pattern Detection Heuristics

Frontend UX anti-patterns that frustrate users.
Scan frontend code for patterns that cause measurable user harm.

## Table of Contents

1. [Layout Stability](#1-layout-stability)

2. [Feedback & Responsiveness](#2-feedback--responsiveness)

3. [Error Handling & Recovery](#3-error-handling--recovery)

4. [Forms & Input Interference](#4-forms--input-interference)

5. [Focus](#5-focus)

6. [Notifications, Interruptions & Dialogs](#6-notifications-interruptions--dialogs)

7. [Navigation, Routing & State Persistence](#7-navigation-routing--state-persistence)

8. [Scroll & Viewport](#8-scroll--viewport)

9. [Timing, Debounce & Race Conditions](#9-timing-debounce--race-conditions)

10. [Accessibility as UX](#10-accessibility-as-ux)

11. [Visual Layering & Rendering](#11-visual-layering--rendering)

12. [Mobile & Viewport-Specific](#12-mobile--viewport-specific)

13. [Cumulative Decay & Long-Term UX](#13-cumulative-decay--long-term-ux)

* * *

## 1. Layout Stability

### 1.1 Elements that shift after render

**Violation:** Content injected after initial paint (images, ads, banners, lazy-loaded
components) displaces already-visible interactive elements.
The user aims for one button and clicks another.

**Detect:**

- Images or media rendered without explicit dimensions (`width`/`height` attributes,
  `aspect-ratio` CSS, or equivalent constraint).

- Containers that depend on async content for their size (no `min-height`, no skeleton
  placeholder, no reserved space).

- Late-injected DOM nodes (cookie banners, chat widgets, promo bars) inserted at the top
  or middle of the content flow instead of using fixed/sticky positioning with
  pre-reserved space.

**Fix:** Reserve space for every async element before it loads.
Use explicit dimensions, `aspect-ratio`, skeleton placeholders, or `min-height` on
containers.

### 1.2 Click targets that shift on hover or focus

**Violation:** Interactive elements that change size, reflow siblings, or shift position
on `:hover` / `:focus` / state change.
The target moves out from under the user’s cursor or finger.

**Detect:**

- Hover/focus rules that use `padding`, `margin`, `font-size`, `width`, `height`,
  `display`, or `border-width` changes instead of layout-neutral properties.

- Spinners or status indicators inserted *adjacent to* a button (before/after in flow)
  rather than *overlaid on* or *inside* it.

**Fix:** If changing layout-affecting properties on interaction states, these properties
also need to be declared on the base selector.
Prefer limiting hover/focus effects to `transform`, `box-shadow`, `outline`, `opacity`,
`background`, `color`, or `filter`.

```css
/* VIOLATION: no base border, added on hover */
.btn:hover { border: 2px solid blue; } /* shifts by 2px */

/* Fix 1: Declared 2px transparent border on base */
.btn { border: 2px solid transparent; }
.btn:hover { border: 2px solid blue; }

/* FIX 2: use transform, box-shadow, or outline — no layout impact */
.btn:hover { box-shadow: 0 0 0 2px blue; }
```

* * *

## 2. Feedback & Responsiveness

### 2.1 No immediate feedback on action

**Violation:** User clicks/taps a button and nothing visibly changes.
No pressed state, no spinner, no disabled state.
The user doesn’t know if the system registered the input.

**Detect:**

- Submit buttons or primary actions with no loading/pending state management.

- Click handlers that fire an async operation without immediately updating the UI.

- Absence of `:active` styles or equivalent pressed state.

**Fix:** Every async action should *immediately* produce a visual state change (loading
indicator, disabled state, or animation) before the operation completes.

### 2.2 Optimistic UI that silently reverts

**Violation:** The UI updates instantly (optimistic update), but when the server rejects
the action, it quietly reverts with no explanation.
The user believes the action succeeded.

**Detect:**

- Optimistic state updates that lack an error/rollback handler.

- Rollback logic that doesn’t trigger a user-visible notification.

**Fix:** If an optimistic update must be rolled back, show an explicit notification
explaining what happened and offer a retry path.

### 2.3 Long-running operations with no progress indication

**Violation:** An operation takes 10+ seconds and the user sees only a spinner with no
progress bar, percentage, estimated time, or status message.
The user doesn’t know if the system is working, stuck, or nearly done.

**Detect:**

- Async operations that may exceed ~5 seconds (file uploads, data exports, batch
  processing) with only a spinner or generic “Loading …” indicator.

- Absence of progress tracking (percentage, step count, bytes transferred) for
  multi-second operations.

```jsx
{/* VIOLATION: indeterminate spinner for a long upload */}
{isUploading && <Spinner />}

{/* FIX: show progress for long operations */}
{isUploading && (
  <div role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
    Uploading: {progress}%
  </div>
)}
```

**Fix:** For operations that may exceed ~5 seconds, show determinate progress
(percentage, step N of M, bytes transferred).
If determinate progress is unavailable, show a status message that updates
("Preparing...", “Processing...”, “Almost done...”) so the user knows the system hasn’t
frozen.

* * *

## 3. Error Handling & Recovery

### 3.1 Error messages without recovery guidance

**Violation:** “Something went wrong.”
“Error 500.” "Request failed."
These tell the user nothing about what to do next.

**Detect:**

- Static error strings with no contextual information (what failed, why, what to do).

- Raw HTTP status codes, exception class names, or internal error IDs displayed to the
  user.

- Error UI with no actionable element (retry button, link to support, alternative path).

**Fix:** Every error message must include: (1) what failed in user-facing language, (2)
why, if known, (3) what the user can do about it.

### 3.2 Disabled controls with no explanation

**Violation:** A button or input is grayed out / non-interactive and the user has no
idea why or what to do to enable it.

**Detect:**

- `disabled` attribute or non-interactive state on controls with no adjacent hint,
  tooltip, or explanatory text.

```html
<!-- VIOLATION: disabled with no explanation -->
<button disabled>Submit</button>

<!-- FIX: explain the constraint -->
<button disabled aria-describedby="submit-hint">Submit</button>
<p id="submit-hint">Complete all required fields to submit.</p>
```

**Fix:** If a control is disabled, explain the precondition for enabling it.
Alternatively, keep the control enabled and validate on interaction with an explanatory
error.

### 3.3 Errors that block unrelated work

**Violation:** One failed module, widget, or API call locks the entire page/screen
instead of degrading gracefully.

**Detect:**

- Absence of per-section error containment (e.g., React error boundaries, isolated
  try/catch per module).

**Fix:** Contain failures to the affected region.
The rest of the UI should remain functional.
Show an inline error in the broken section with a retry option.

* * *

## 4. Forms & Input Interference

### 4.1 Paste blocked

**Violation:** Paste is disabled on input fields, especially for passwords, verification
codes, or “confirm email” fields.

**Detect:**

- Event listeners on `paste` that call `e.preventDefault()`.

- `onpaste="return false"` in markup.

**Fix:** Never block paste.
If the intent is to prevent auto-fill errors, validate the input instead.

### 4.2 Required fields not marked until submission fails

**Violation:** Nothing on the form indicates which fields are required.
The user submits, and only then do asterisks and error messages appear.

**Detect:**

- Required inputs without visual indicators (`*`, “(required)” label, `aria-required`).

- Required state only applied via form-level validation error rendering.

**Fix:** Mark required fields before the user interacts.
Use visual indicators and appropriate ARIA attributes from the start.

### 4.3 Autocorrect / autofill / smart-input interference

**Violation:** Platform autocorrect, autocapitalize, or autofill alters input in fields
where it shouldn’t — passwords modified, emails capitalized, verification codes
reformatted.

**Detect:**

- Password, code, or token inputs missing appropriate attributes to disable
  interference.

- Input fields for structured data (emails, codes, phone numbers) without `inputmode`,
  `autocomplete`, `autocorrect`, or `autocapitalize` attributes.

```html
<!-- VIOLATION: one-time code with no input hints -->
<input type="text" name="otp">

<!-- FIX: explicit input behavior -->
<input
  type="text"
  inputmode="numeric"
  autocomplete="one-time-code"
  autocorrect="off"
  autocapitalize="off"
>
```

**Fix:** Set the correct `type`, `inputmode`, `autocomplete`, `autocorrect`, and
`autocapitalize` attributes for every input field.
Match the attribute to the data semantics.

### 4.4 Hostile formatters

**Violation:** Phone, credit card, date, or other formatted fields reformat as you type
and break cursor position.
The user can’t delete or edit characters mid-string because the formatter repositions
the cursor or re-renders the value.

**Detect:**

- Input handlers that call `setValue()` or replace the entire input value on each
  keystroke.

- Formatting logic that does not track or restore cursor/caret position after
  reformatting.

**Fix:** If you reformat input on change, you *must* correctly manage the caret
position. Better: use dedicated input masking libraries that handle this, or format on
blur instead of on every keystroke.

### 4.5 Custom inputs that break standard editing

**Violation:** A custom input widget (tag input, rich editor, code field, segmented OTP
input) doesn’t support basic text-editing expectations: select all, arrow key
navigation, delete/backspace, clipboard shortcuts, undo/redo.

**Detect:**

- Custom input components that capture keyboard events and don’t propagate standard
  editing shortcuts.

- `onKeyDown` handlers with `preventDefault()` calls that block default text-editing
  behavior without reimplementing it.

**Fix:** Custom inputs must support the full set of standard editing interactions for
their platform. If you intercept keyboard events, verify that all standard editing
behaviors still work.

### 4.6 Multi-step forms that lose data on back-navigation

**Violation:** User clicks “Back” in a multi-step wizard and previous entries are gone.
Or browser back-button exits the wizard entirely and loses all progress.

**Detect:**

- Step-based forms where each step unmounts the previous step’s state.

- Wizard state stored only in component-local state, not persisted to
  session/URL/storage.

- No `beforeunload` or navigation-guard handling for unsaved wizard progress.

**Fix:** Persist form state across steps (session storage, URL params, or a global state
container). Warn before navigation that would discard data.

* * *

## 5. Focus

### 5.1 Focus Stealing

**Violation:** Auto-focus logic or dynamic DOM changes move the cursor away from where
the user is actively typing.

**Detect:**

- `autofocus` attributes or `.focus()` calls that fire after initial page load (e.g., in
  response to async events, timers, or state changes).

- Live-search or dynamic form sections that re-render and grab focus.

- Modal focus-traps that activate while the user is interacting with content underneath.

**Fix:** Never programmatically move focus while the user is actively interacting with
another element.
The only safe times to auto-focus are (1) on initial page/modal load, or
(2) in direct response to the user’s own action (e.g., opening a dialog).

* * *

## 6. Notifications, Interruptions & Dialogs

### 6.1 Repeated notifications in short succession

**Violation:** The same or similar notification fires multiple times within seconds.
Alert fatigue sets in immediately.

**Detect:**

- Notification/toast dispatch with no deduplication or throttle mechanism.

- Event handlers that fire on every occurrence of a rapid event (e.g., per-message
  notification in a burst of incoming messages).

**Fix:** Deduplicate identical notifications.
Batch or throttle similar ones ("3 new messages" instead of 3 separate toasts).
Offer mute/disable options.

```js
// VIOLATION: fires a toast for every event
socket.on("message", (msg) => showToast(msg.text));

// FIX: batch with a throttle window
let pending = [];
const flush = throttle(() => {
  if (pending.length === 1) showToast(pending[0].text);
  else if (pending.length > 1) showToast(`${pending.length} new messages`);
  pending = [];
}, 2000);
socket.on("message", (msg) => { pending.push(msg); flush(); });
```

### 6.2 Overlays that obscure content

**Violation:** Chat widgets, floating action buttons, or sticky CTAs that cover text,
form inputs, or interactive elements — especially on mobile viewports.

**Detect:**

- Fixed/sticky-positioned elements that overlap scrollable content areas.

- Floating elements on mobile with no minimize/collapse option and no responsive
  repositioning.

**Fix:** Floating elements must not obscure primary content.
Provide a minimize/collapse mechanism, or ensure they’re positioned to avoid overlap
(anchored to safe zones, responsive to viewport size).

### 6.3 Modals that can’t be dismissed with standard gestures

**Violation:** A modal that requires finding and clicking a tiny ✕ button.
Escape key doesn’t work.
Clicking outside doesn’t close it.

**Detect:**

- Modal components without a keydown listener for `Escape`.

- Absence of a backdrop/overlay click handler for dismissal.

- Missing or visually obscured close button.

**Fix:** All modals should support: (1) visible close button, (2) Escape key, (3)
click/tap outside to dismiss — unless the modal is a critical confirmation for a
destructive action, in which case Escape and click-outside may be omitted but the close
button must remain visible and obvious.

### 6.4 Destructive actions with no confirmation

**Violation:** Clicking “Delete,” "Remove," or “Clear all” immediately executes the
action with no confirmation step and no undo.
One misclick causes irreversible data loss.

**Detect:**

- Click handlers on destructive actions (delete, remove, overwrite, send, publish) that
  execute immediately without a confirmation dialog or undo mechanism.

- Absence of both a confirmation step AND an undo/soft-delete pattern for irreversible
  operations.

```jsx
// VIOLATION: immediate delete, no confirmation, no undo
<button onClick={() => deleteAccount(user.id)}>Delete Account</button>

// FIX: confirmation dialog for destructive action
<button onClick={() => setShowConfirm(true)}>Delete Account</button>
{showConfirm && (
  <dialog open>
    <p>This will permanently delete your account and all data.</p>
    <button onClick={() => setShowConfirm(false)}>Cancel</button>
    <button onClick={() => deleteAccount(user.id)}>Delete permanently</button>
  </dialog>
)}
```

**Fix:** Destructive actions must have at least one safety net: a confirmation dialog
that names the consequences, OR an undo window (soft-delete with time-limited recovery).
For high-stakes actions (account deletion, bulk data removal), use both.

* * *

## 7. Navigation, Routing & State Persistence

### 7.1 Redirects that lose the original target

**Violation:** User clicks a deep link → gets redirected for auth/SSO → after auth
completes, the app drops the original URL and dumps them on the homepage.

**Detect:**

- Auth/SSO redirect flows that don’t store and restore the original requested URL.

- Absence of a `returnUrl`, `redirect_uri`, or equivalent parameter in the auth flow.

**Fix:** Persist the originally requested URL through the redirect chain (query param,
session storage) and navigate there after authentication completes.

```js
// FIX: preserve original destination through auth
function requireAuth(req, res) {
  if (!req.user) return res.redirect(`/login?returnUrl=${encodeURIComponent(req.originalUrl)}`);
}
```

### 7.2 State not reflected in URL

**Violation:** Search queries, filters, pagination, or sort order stored only in
component state. Users can’t share, bookmark, or refresh without losing context.

**Detect:**

- Filter, search, sort, or pagination managed only in memory (component state, global
  store) without syncing to URL query params, hash, or path segments.

**Fix:** Meaningful UI state — anything a user would want to share, bookmark, or recover
on refresh — should be reflected in the URL.

```js
// FIX: sync filters to URL search params
const [searchParams, setSearchParams] = useSearchParams();
const filters = {
  category: searchParams.get("category") || "all",
  sort: searchParams.get("sort") || "newest",
};
```

* * *

## 8. Scroll & Viewport

### 8.1 Scroll with no position recovery

**Violation:** User scrolls deep into a list, clicks into an item, navigates back, and
is at the top again with no way to return to where they were.

**Detect:**

- Infinite scroll implementations without scroll position caching.

- List → detail → back navigation patterns that don’t restore the previous scroll offset
  and loaded data.

**Fix:** Cache scroll position and loaded data.
Restore both on back-navigation.
Alternatively (or additionally), offer traditional pagination as a fallback.

### 8.2 Sticky elements consuming excessive viewport

**Violation:** Fixed header + sticky nav + cookie banner + notification bar + floating
chat widget = the user can see 40% of actual content, especially on mobile.

**Detect:**

- Multiple fixed/sticky-positioned elements stacking vertically.

- Combined height of fixed elements exceeding ~15–20% of viewport on mobile, or ~10% on
  desktop.

**Fix:** Minimize fixed elements.
Auto-hide on scroll-down, show on scroll-up.
Combine or collapse fixed bars where possible.
Cookie banners and notifications should be dismissible and stay dismissed.

### 8.3 Horizontal overflow on mobile

**Violation:** Tables, code blocks, images, or layout sections that overflow the
viewport width on mobile, requiring horizontal scroll for the main content.

**Detect:**

- Elements with fixed widths larger than mobile viewport (~375–430px).

- Tables or pre-formatted content without responsive wrappers (`overflow-x: auto`
  containers, responsive table patterns).

- Absence of `<meta name="viewport" content="width=device-width">` or equivalent.

**Fix:** All content should fit within the viewport width at the smallest supported
breakpoint. Wrap overflow-prone content (tables, code) in scrollable containers.
Use responsive layout patterns.

### 8.4 Gesture conflicts

**Violation:** In-app swipe gestures conflict with OS or browser gestures.
Pull-to-refresh triggers when trying to scroll up.
Carousel swipe conflicts with navigation swipe.
Edge swipe conflicts with OS back gesture.

**Detect:**

- Touch event handlers on swipe-like gestures without considering the browser’s
  pull-to-refresh, edge-swipe (iOS back), or overscroll-behavior defaults.

- Horizontal carousels or swipeable panels nested within scrollable containers.

- Missing `overscroll-behavior` CSS or equivalent platform-specific gesture boundary
  handling.

**Fix:** Use `overscroll-behavior: contain` to prevent pull-to-refresh conflicts.
Inset touch targets away from screen edges to avoid OS gesture zones.

```css
.carousel {
  touch-action: pan-x;
  overscroll-behavior-x: contain;
}
```

* * *

## 9. Timing, Debounce & Race Conditions

### 9.1 Duplicate submission from double-click / double-tap

**Violation:** User double-clicks “Place Order,” "Send," or “Submit” and the action
fires twice. Duplicate orders, duplicate messages, duplicate records.

**Detect:**

- Submit/action handlers with no guard against rapid re-invocation.

- Buttons that remain enabled and clickable during async operation processing.

**Fix:** Disable the control on first click and re-enable on completion/error.
Additionally, implement server-side idempotency (idempotency keys) for critical
operations — client-side guards alone are insufficient.

### 9.2 Stale response overwriting newer intent

**Violation:** User types “appl” → search fires → user types “apple” → search fires →
the slower “appl” response returns *after* the “apple” response and overwrites it.

**Detect:**

- Async operations triggered by user input that don’t use request sequencing,
  AbortController, or similar cancellation/versioning.

- State updates from async results that don’t verify the result still corresponds to the
  current input/intent.

```js
// VIOLATION: no cancellation, stale result can overwrite
async function search(query) {
  const res = await fetch(`/search?q=${query}`);
  setResults(await res.json()); // might be stale
}

// FIX: abort previous request
let controller;
async function search(query) {
  controller?.abort();
  controller = new AbortController();
  const res = await fetch(`/search?q=${query}`, { signal: controller.signal });
  setResults(await res.json());
}
```

**Fix:** Cancel or ignore stale requests.
Use request abort/cancellation, sequence IDs, or check that the response still matches
the current user input before applying it.

### 9.3 Session expiration during active use

**Violation:** The user is mid-task — filling a form, composing a message, editing a
document — and the session expires silently.
Their next action either fails with a cryptic error, redirects to login and loses all
in-progress work, or silently discards the submission.

**Detect:**

- Session/token expiry that triggers a hard redirect to login with no preservation of
  in-progress state.

- API calls that return 401/403 after session timeout without client-side handling to
  warn the user or refresh the token.

- Absence of proactive session expiry warnings or silent token refresh mechanisms.

**Fix:**

1. Proactively warn before session expiry ("Your session expires in 2 minutes").

2. Attempt silent token refresh when possible.

3. If expiry is unavoidable, preserve in-progress state (localStorage, sessionStorage)
   before redirecting.

4. After re-authentication, restore state and return the user to where they were.

* * *

## 10. Accessibility as UX

### 10.1 Focus indicators removed

**Violation:** `outline: none` or `outline: 0` on interactive elements for aesthetics,
with no replacement focus indicator.
Keyboard users cannot see where they are.

**Detect:**

- CSS rules that remove `outline` on `:focus` without providing a replacement
  (`:focus-visible` styles, `box-shadow`, custom outline, ring indicator).

```css
/* VIOLATION */
*:focus { outline: none; }

/* FIX: remove only mouse-click outlines, keep keyboard outlines */
:focus:not(:focus-visible) { outline: none; }
:focus-visible { outline: 2px solid var(--focus-color); outline-offset: 2px; }
```

**Fix:** Never remove focus indicators globally.
Use `:focus-visible` to show focus rings only for keyboard navigation, or provide an
equivalent custom indicator.

### 10.2 Hover-only information or controls

**Violation:** Tooltips, action menus, edit buttons, or critical details that only
appear on mouse hover.
Unreachable on touch devices and invisible to keyboard-only users.

**Detect:**

- Information or interactive controls shown only in `:hover` pseudo-class or
  `mouseenter` event handlers.

- Absence of a `:focus` / `:focus-within` equivalent for hover-revealed content.

**Fix:** Any information or control accessible on hover must also be accessible on focus
(keyboard) and on tap/long-press (touch).
Use `hover` and `focus-within` together.

### 10.3 Touch targets too small

**Violation:** Interactive elements smaller than 44×44pt (Apple HIG) or 48×48dp
(Material). Especially bad when small targets are adjacent with no spacing.

**Detect:**

- Buttons, links, or interactive elements with computed size < 44×44px.

- Adjacent interactive elements with < 8px gap between them.

**Fix:** Ensure all interactive elements meet minimum touch target sizes.
If the visual element must be small, expand the clickable/tappable area with padding or
invisible hit areas.

### 10.4 Color as sole indicator

**Violation:** Using only red/green (or any color pair) to distinguish error/success,
enabled/disabled, or other states.

**Detect:**

- Status indicators that rely only on `color` or `background-color` with no icon, text
  label, or pattern differentiation.

- Form validation that only changes the border color of invalid fields.

**Fix:** Supplement color with at least one non-color indicator: icon, text label,
pattern, weight change, or position change.

### 10.5 Contrast failures

**Violation:** Placeholder text unreadable against the background.
Disabled state indistinguishable from enabled.
Light gray body text on white.
Dark text on dark background in dark mode.

**Detect:**

- Text with contrast ratio below WCAG AA thresholds (4.5:1 for normal text, 3:1 for
  large text).

- Placeholder color that doesn’t meet contrast requirements.

- Disabled state styling that differs from enabled state by only a small opacity or
  color change.

**Fix:** Meet WCAG AA contrast ratios.
Disabled states should be visually distinct through multiple cues (color, opacity,
pattern, text label, icon change), not just a slight dimming.

### 10.6 Keyboard traps

**Violation:** Focus enters a modal, widget, or custom component and can’t escape via
Tab or Escape.

**Detect:**

- Custom focus-trap implementations that don’t release on Escape.

- Modals without an Escape key handler.

- Custom widgets (dropdowns, menus, accordions) that intercept Tab but don’t provide a
  way out.

**Fix:** All focus traps must be escapable.
Modals should release focus on Escape.
Custom widgets should follow WAI-ARIA design patterns for keyboard interaction.

* * *

## 11. Visual Layering & Rendering

### 11.1 Z-index chaos

**Violation:** Dropdowns render behind modals.
Tooltips clipped by overflow containers.
Sticky headers overlap popovers.
No predictable stacking hierarchy.

**Detect:**

- Arbitrary or escalating `z-index` values (999, 9999, 99999) without a systematic
  layering scale.

- Elements that should float above their context but are children of `overflow: hidden`
  / `overflow: auto` containers, causing clipping.

- Absence of a defined z-index scale or design-token system for layers.

**Fix:** Define a z-index scale as named layers (e.g., dropdown=100, sticky=200,
modal=300, toast=400). Render overlays that must escape parent clipping via a
portal/teleport to the document root or a dedicated overlay container.

```css
:root {
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;
}
```

* * *

## 12. Mobile & Viewport-Specific

### 12.1 Virtual keyboard covers focused input

**Violation:** User taps a text field on mobile, the virtual keyboard opens and obscures
the input field. The page doesn’t scroll or resize to keep the input visible.

**Detect:**

- Input fields in the lower half of the viewport on mobile with no handling for keyboard
  appearance.

- Fixed-position elements that don’t adjust for the virtual keyboard’s presence.

**Fix:** Use `visualViewport` API or equivalent to detect keyboard and adjust.
Ensure focused inputs scroll into view.
Avoid fixed-position elements in areas that overlap with the virtual keyboard.

```js
if (window.visualViewport) {
  window.visualViewport.addEventListener("resize", () => {
    const keyboardHeight = window.innerHeight - window.visualViewport.height;
    document.documentElement.style.setProperty("--keyboard-height", `${keyboardHeight}px`);
  });
}
```

### 12.2 `100vh` jitter on mobile

**Violation:** Elements using `100vh` jump when mobile browser chrome (address bar)
shows/hides during scroll.

**Detect:**

- Use of `100vh` for full-screen layouts on mobile (hero sections, modals, splash
  screens).

**Fix:** Use `100dvh` (dynamic viewport height), `100svh` (small viewport height), or
JavaScript-based viewport detection instead of `100vh` on mobile.

* * *

## 13. Cumulative Decay & Long-Term UX

### 13.1 Updates that reset preferences

**Violation:** An app update silently reverts notification settings, theme, layout
customizations, or accessibility preferences to defaults.

**Detect:**

- Update/migration code that overwrites user preferences.

- Default state initialization that doesn’t check for existing saved preferences.

**Fix:** User preferences are priority.
Never overwrite them on update.
If a preference must change (deprecated option), notify the user and offer a migration
path.

```js
// VIOLATION: overwrite with defaults on init
const prefs = { theme: "light", notifications: true };
localStorage.setItem("prefs", JSON.stringify(prefs));

// FIX: merge defaults with existing preferences
const defaults = { theme: "light", notifications: true };
const saved = JSON.parse(localStorage.getItem("prefs") || "{}");
const prefs = { ...defaults, ...saved };
```

### 13.2 Cache / storage bloat

**Violation:** The application progressively slows down, consumes excessive storage, or
behaves erratically as cached data accumulates without cleanup.

**Detect:**

- Caching strategies with no TTL, LRU eviction, or maximum size limit.

- Local storage / IndexedDB / cache API usage without cleanup logic.

**Fix:** Implement cache eviction policies (TTL, LRU, max entries).
Monitor storage usage.

```js
function cacheResponse(key, data, ttlMs = 3600000) {
  const entry = { data, expires: Date.now() + ttlMs };
  localStorage.setItem(key, JSON.stringify(entry));
  evictIfOverLimit(50);
}
```

### 13.3 Stale feature flags and experiments

**Violation:** UI inconsistencies from A/B tests or feature flags that were never
cleaned up. Different users see different UI for no current reason.

**Detect:**

- Feature flags that have been “enabled for all” or “disabled for all” for an extended
  period but are still in the code.

- Conditional rendering based on flags with no documented experiment or rollout plan.

**Fix:** Clean up feature flags when experiments conclude.
Treat stale flags as tech debt.
