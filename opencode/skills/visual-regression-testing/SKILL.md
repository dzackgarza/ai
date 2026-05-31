---
name: visual-regression-testing
description: Use when detecting unintended UI changes through screenshot comparison, visual diff testing, or catching layout and rendering regressions. Trigger with phrases like "visual regression test", "compare screenshots", "screenshot diff", "detect UI changes", or "check for visual regressions".
---
# Visual Regression Testing

Detect unintended visual changes in UI components by capturing screenshots and comparing
them pixel-by-pixel against approved baselines.
Supports Playwright visual comparisons, Percy, Chromatic, BackstopJS, and reg-suit.

## When to use

- Verifying that a UI change did not break existing component or page appearance

- Checking layout fidelity across viewports after CSS or markup changes

- Catching rendering differences between browser environments or font stacks

- Automating visual QA as part of CI/CD

## Prerequisites

- Browser automation tool installed (Playwright, Puppeteer, or Cypress)

- Visual regression library configured (Playwright `toHaveScreenshot`, Percy, Chromatic,
  or BackstopJS)

- Baseline screenshots committed to version control or stored in a cloud service

- Consistent rendering environment (Docker or CI with fixed OS, fonts, GPU settings)

## Workflow

1. **Identify coverage targets** -- scan component directories and route definitions to
   determine which UI surfaces need visual tests.

2. **Create visual test file** for each component or page:

   - Navigate to the URL or Storybook story.

   - Wait for all network requests, animations, and lazy-loaded images to finish.

   - Set a consistent viewport (e.g., 1280x720 desktop, 375x812 mobile).

3. **Capture with deterministic settings**:

   - Disable animations and transitions: inject
     `* { animation: none !important; transition: none !important; }`.

   - Mask dynamic content (timestamps, random avatars, ads) with CSS overlays or `mask`
     option.

   - Use `fullPage: true` for scrollable pages.

4. **Compare against baselines**:

   - Configure pixel-difference threshold (recommended: 0.1% for components, 0.5% for
     full-page).

   - Generate diff images highlighting changed regions.

   - Flag tests as failed when differences exceed the threshold.

5. **Capture responsive variants** at key breakpoints:

   - Mobile: 375px width

   - Tablet: 768px width

   - Desktop: 1280px width

   - Wide: 1920px width

6. **Classify each failure**:

   - Intentional change -- update baseline with `--update-snapshots`.

   - Regression -- file a bug with the diff image attached.

7. **Integrate into CI** so visual tests run on every pull request, with diff images
   uploaded as artifacts.

## Example: Playwright visual regression

```typescript
import { test, expect } from '@playwright/test';

test('homepage matches baseline', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.addStyleTag({ content: '* { animation: none !important; }' });
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.001,
    fullPage: true,
  });
});
```

## Environment traps

- **Anti-aliasing differs across OS** -- Font rendering varies between macOS, Linux, and
  Windows. Run visual tests in Docker with fixed fonts; use `threshold` to allow
  sub-pixel variance.

- **Flaky screenshots from animations** -- CSS transitions or JS animations may still be
  running at capture time.
  Inject `prefers-reduced-motion` or disable animations via `addStyleTag` before
  capture.

- **Missing baseline on first run** -- No previous screenshot exists.
  Run with `--update-snapshots` to create initial baselines and commit them to the
  repository.

- **Viewport size mismatch** -- Browser chrome or scrollbar width differs between
  environments. Use `setViewportSize` explicitly; hide scrollbars with CSS
  `overflow: hidden`.

- **Dynamic content causes false failures** -- Timestamps, user avatars, or ads change
  between runs. Mask dynamic elements with the `mask` option or replace content via
  `page.evaluate`.

## Output expectations

- Baseline screenshots stored in `__screenshots__/` or equivalent directory

- Diff images showing pixel-level changes between baseline and current

- Visual regression test report with pass/fail per component

- CI artifacts containing captured, baseline, and diff images

- Responsive coverage matrix showing results across breakpoints
