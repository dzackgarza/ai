---
order: 30
tags:
- purpose-preference
- purpose-procedure
- purpose-reference
- stability-policy-contingent
- stability-tool-contingent
title: Monitoring PR Activity
---

To track activity on a PR without polling — new commits, review comments, check-run
results, status changes — subscribe to the relevant GitHub webhook events and react to
the callbacks instead of repeatedly fetching state.

Load `webhook-subscriptions` for the subscription and callback workflow. This pairs with
the background-job ETA rule in Engineering Rules: when you hand a PR off to CI or a
reviewer and stop to wait, a webhook callback is the signal that work has returned.
