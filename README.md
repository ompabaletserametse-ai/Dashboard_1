# Network Operations Centre MVP

This project is a first-stage Streamlit concept demo for an AI-supported Network Operations Centre (NOC) platform. It presents fictional network data for cell sites across South Africa and focuses on network overview and site inspection only.

## Included in this MVP

- Dark operations-dashboard styling for mobile and desktop
- Summary cards for total, healthy, degraded, unavailable, and affected-customer counts
- Priority panel highlighting the most urgent affected site using transparent rules
- Search, region, technology, and status filters
- Site inspection with all six core technical metrics
- Clear handling of missing measurements and stale telemetry
- Visible "Simulated network data" label throughout the experience

## Run locally

Prerequisite: install `uv` if you do not already have it.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install dependencies and launch the app:

```bash
uv sync
uv run streamlit run streamlit_app.py
```

## Files

- `streamlit_app.py` — Streamlit entrypoint that runs the app
- `app.py` — dashboard logic and demo data
- `requirements.txt` — Streamlit runtime dependencies

## Notes

- This is a fictional concept demo and does not connect to real network systems or external AI services.
- The sample data is intentionally consistent and designed to tell a believable operational story.
