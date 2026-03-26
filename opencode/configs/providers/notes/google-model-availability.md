# Google Model Availability Notes

## As of 2026-03-26

### Confirmed Working (200 OK)

- gemini-2.5-flash
- gemini-2.5-flash-lite
- gemini-3-flash-preview
- gemini-flash-latest
- gemini-flash-lite-latest

### High Demand (503 UNAVAILABLE)

- **gemini-3.1-flash-lite-preview**: Returns HTTP 503 with message "This model is
  currently experiencing high demand.
  Spikes in demand are usually temporary.
  Please try again later."
  - Whitelisted in models section
  - Intermittent availability - may work on retry

### Rate Limited (429)

- **gemini-pro-latest**: Returns HTTP 429 under rapid sequential requests
  - Whitelisted in models section
  - Works with backoff between requests

### Confirmed 404 (Non-Existent, Now Blacklisted)

These models appeared in `command opencode models` but return 404 from Google API:
- gemini-2.5-flash-image-preview
- gemini-2.5-flash-lite-preview-06-17
- gemini-2.5-flash-preview-04-17
- gemini-2.5-flash-preview-05-20
- gemini-2.5-flash-preview-09-2025
- gemini-2.5-pro-preview-05-06
- gemini-2.5-pro-preview-06-05

All added to blacklist on 2026-03-26.

## Free Tier Rate Limits (as of 2026-03-26)

| Model | Category | RPM | TPM | RPD |
| --- | --- | --- | --- | --- |
| Gemma 3 4B | Other | 18/30 | 39/15K | 31/14.4K |
| Gemma 3 12B | Other | 24/30 | 33/15K | 31/14.4K |
| Gemma 3 27B | Other | 20/30 | 55/15K | 30/14.4K |
| Gemini 2.5 Flash | Text-out | 2/5 | 195K/250K | 23/20 |
| Gemini 2.5 Flash Lite | Text-out | 3/10 | 3/250K | 8/20 |
| Gemini 3 Flash | Text-out | 2/5 | 5/250K | 11/20 |
| Gemini 3.1 Flash Lite | Text-out | 1/15 | 4/250K | 8/500 |
| Gemini 2.5 Pro | Text-out | 0/0 | 0/0 | 0/0 |
| Gemini 3.1 Pro | Text-out | 0/0 | 0/0 | 0/0 |
| Gemini 2.5 Flash TTS | Multi-modal | 0/3 | 0/10K | 0/10 |
| Gemini Embedding 1 | Other | 0/100 | 0/30K | 0/1K |
| Gemini Embedding 2 | Other | 0/100 | 0/30K | 0/1K |
| Gemini Robotics ER 1.5 | Other | 0/10 | 0/250K | 0/20 |

Note: 0/0 limits = not available on free tier (paid only).
gemini-pro-latest, gemini-flash-latest, and gemini-flash-lite-latest are aliases that
inherit their limits from the underlying model.
