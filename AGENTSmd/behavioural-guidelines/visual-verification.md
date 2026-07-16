---
order: 70
tags:
- source-system-contract
- source-observed-model-failure
- function-constrain
- function-procedure
- function-route
- function-evaluate
- failure-proxy-evidence
- failure-completion-laundering
- retest-model-self-evaluation
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Visual Verification
---

Any work that implies something renders or looks correct — web pages, HTML, CSS or
styling changes, dashboards, slide decks, or any GUI application whatsoever — is not done
until you have generated actual visual snapshots of the rendered output and viewed them
yourself.

Never call such work "fixed", "working", "ready", "good", or "done" on the basis of code
that looks right, a passing build, a clean diff, or a server that starts. Rendered output
is the only evidence that a visual change is correct; the diff, the logs, and the absence
of errors are receipts, not proof.

Before reporting any work that implies a visual surface is correct:

- Render the real artifact — screenshot the page or app, export the deck, capture the
  GUI — automating capture with Playwright or the framework's own snapshot tooling where
  possible.
- Open and inspect the images for actual correctness: layout, overflow, alignment,
  spacing, color, typography, component state, and broken or missing assets. Confirming a
  file was produced is not inspection.
- Fix every defect you observe and re-capture until the snapshots are correct.

Generating a screenshot file is a receipt; the evidence is your inspection of it. This is
correctness inspection of rendered output, which is distinct from golden or
visual-regression comparison against a stored baseline.

Use your vision. You can see images, so look at the rendered artifact directly rather than
reasoning about it through proxies. Do not substitute measuring box dimensions, element
sizes, gaps, margins, computed styles, or DOM structure for actually viewing the
screenshot — those engineering-brained proxies are an error-prone stand-in for the thing
you are perfectly capable of just looking at. Inspect the image first and reason from what
you see; reserve measurement for confirming a specific value after your eyes have already
located the problem. Never fix a visual you have not looked at.

Load `design` for the render-and-verify workflow, `responsive-design` for multi-viewport
checks, and `test-guidelines` for the mandatory GUI screenshot-suite obligation.
`visual-regression-testing` covers golden comparison and does not by itself satisfy this
rule.
