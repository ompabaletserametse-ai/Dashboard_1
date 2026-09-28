# Network Operations Centre MVP

This Streamlit dashboard is a fictional, mobile-friendly concept demo for a South African network operations environment. It shows an overview of 72 simulated cell sites across all nine provinces, and supports province-focused inspection of network health and service impact.

## Included in this stage

- Dark operations-dashboard styling with a consistent NOC look and feel
- National summary cards for total, healthy, degraded, unavailable, and affected-customer counts
- Province selector that narrows the map, site list, and KPI panel to the selected province
- Interactive South Africa map with 8 fictional sites per province (72 total)
- Green, amber, red, and grey markers for healthy, degraded, unavailable, and stale or missing telemetry
- Tooltip-style site detail cards on hover
- Province-level KPI calculations for availability, latency, CPU usage, packet loss, bandwidth, error rate, and affected customers
- Search, technology, and status filters that still work alongside the province selector
- Site inspection details for all six metrics, plus plain-language explanations of the issue state
- Clear "Simulated network data" labels and fictitious data only

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
- `app.py` — dashboard logic, map rendering, demo data, KPI aggregation, and inspection logic
- `requirements.txt` — runtime dependencies

## Notes

- All data is simulated and intentionally consistent so the dashboard feels believable without connecting to a real network.
- Province KPI averages exclude missing or stale readings from the calculations and show how many readings were used.
- The app is designed to remain usable on a phone-sized browser viewport without requiring horizontal scrolling for the main tasks.
