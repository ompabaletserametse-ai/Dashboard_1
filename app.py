from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Network Operations Centre",
    page_icon="📡",
    layout="wide",
)

# This app uses fictional demonstration data only.
# Priority is intentionally transparent: unavailable and degraded sites with the most affected customers rise first.
PROVINCES = {
    "Eastern Cape": {"lat": -32.6, "lon": 27.1},
    "Free State": {"lat": -28.5, "lon": 26.4},
    "Gauteng": {"lat": -26.2, "lon": 28.0},
    "KwaZulu-Natal": {"lat": -29.4, "lon": 30.7},
    "Limpopo": {"lat": -23.8, "lon": 29.1},
    "Mpumalanga": {"lat": -25.5, "lon": 30.8},
    "North West": {"lat": -25.7, "lon": 25.7},
    "Northern Cape": {"lat": -29.0, "lon": 22.3},
    "Western Cape": {"lat": -33.9, "lon": 18.5},
}

PROVINCE_ORDER = list(PROVINCES.keys())
PROVINCE_CODES = {
    "Eastern Cape": "EC",
    "Free State": "FS",
    "Gauteng": "GT",
    "KwaZulu-Natal": "KZN",
    "Limpopo": "LP",
    "Mpumalanga": "MP",
    "North West": "NW",
    "Northern Cape": "NC",
    "Western Cape": "WC",
}

SITE_OFFSETS = [
    (-0.35, -0.35),
    (0.25, -0.22),
    (-0.15, 0.32),
    (0.3, 0.28),
    (-0.28, 0.15),
    (0.18, -0.18),
    (-0.08, -0.2),
    (0.22, 0.15),
]

STATUS_COLORS = {
    "Healthy": "#22C55E",
    "Degraded": "#F59E0B",
    "Unavailable": "#EF4444",
    "Stale telemetry": "#7C8598",
    "No reading": "#7C8598",
}


def province_center(province: str) -> tuple[float, float]:
    center = PROVINCES[province]
    return center["lat"], center["lon"]


def telemetry_state(site: dict[str, Any]) -> str:
    if site["last_updated"] is None:
        return "No reading"
    age_minutes = (datetime.now(timezone.utc) - site["last_updated"]).total_seconds() / 60
    if site["status"] == "Unavailable":
        return "No reading"
    if age_minutes > 30:
        return "Stale"
    return "Fresh"


def display_status(site: dict[str, Any]) -> str:
    if site["status"] == "Unavailable":
        return "Unavailable"
    if telemetry_state(site) in {"Stale", "No reading"}:
        return "Stale telemetry"
    return site["status"]


def status_rank(status: str) -> int:
    return {"Healthy": 0, "Degraded": 1, "Unavailable": 2, "Stale telemetry": 3, "No reading": 4}.get(status, 0)


def format_metric(value: float | int | None, unit: str = "") -> str:
    if value is None:
        return "Unavailable"
    if unit == "%":
        return f"{value:.1f}%"
    if unit == "ms":
        return f"{int(value)} ms"
    if unit == "ppm":
        return f"{value:.1f} ppm"
    return str(value)


def freshness_label(site: dict[str, Any]) -> str:
    state = telemetry_state(site)
    if state == "No reading":
        return "No reading"
    if state == "Stale":
        return "Telemetry stale"
    return "Fresh"


def status_label(site: dict[str, Any]) -> str:
    return display_status(site)


def status_badge_html(status: str) -> str:
    color = STATUS_COLORS.get(status, "#38BDF8")
    return (
        "<span style='display:inline-block;padding:0.28rem 0.65rem;"
        f"background:{color};color:#08111d;border-radius:999px;font-size:0.76rem;"
        "font-weight:700;letter-spacing:0.02em;'>"
        f"{status}</span>"
    )


def generate_demo_sites() -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    sites: list[dict[str, Any]] = []
    base_statuses = [
        "Healthy",
        "Healthy",
        "Healthy",
        "Degraded",
        "Degraded",
        "Unavailable",
        "Unavailable",
        "Healthy",
    ]

    for province_index, province in enumerate(PROVINCE_ORDER):
        center_lat, center_lon = province_center(province)
        province_code = PROVINCE_CODES[province]

        for offset_index in range(8):
            lat = center_lat + SITE_OFFSETS[offset_index][0]
            lon = center_lon + SITE_OFFSETS[offset_index][1]
            status = base_statuses[offset_index]
            stale = province_index % 2 == 0 and offset_index == 7

            if status == "Unavailable":
                latency_ms = None
                cpu_util_pct = None
                availability_pct = None
                packet_loss_pct = None
                bandwidth_util_pct = None
                error_rate_ppm = None
                affected_customers = 2600 + province_index * 420 + offset_index * 310
                last_updated = now - timedelta(minutes=80 + offset_index * 6)
            elif stale:
                latency_ms = 58 + offset_index * 3
                cpu_util_pct = 46 + offset_index * 2
                availability_pct = 99.72 + offset_index * 0.05
                packet_loss_pct = 1.5 + offset_index * 0.3
                bandwidth_util_pct = 56 + offset_index * 4
                error_rate_ppm = 4.8 + offset_index * 0.6
                affected_customers = 700 + province_index * 240 + offset_index * 150
                last_updated = now - timedelta(minutes=46 + offset_index * 5)
                status = "Healthy"
            else:
                if status == "Healthy":
                    latency_ms = 32 + offset_index * 6
                    cpu_util_pct = 36 + offset_index * 5
                    availability_pct = 99.88 + offset_index * 0.04
                    packet_loss_pct = 0.4 + offset_index * 0.15
                    bandwidth_util_pct = 42 + offset_index * 5
                    error_rate_ppm = 1.8 + offset_index * 0.5
                    affected_customers = 120 + province_index * 100 + offset_index * 70
                    last_updated = now - timedelta(minutes=6 + offset_index)
                else:
                    latency_ms = 125 + offset_index * 12
                    cpu_util_pct = 72 + offset_index * 4
                    availability_pct = 99.2 + offset_index * 0.1
                    packet_loss_pct = 3.6 + offset_index * 0.7
                    bandwidth_util_pct = 77 + offset_index * 4
                    error_rate_ppm = 12.0 + offset_index * 1.8
                    affected_customers = 1800 + province_index * 350 + offset_index * 260
                    last_updated = now - timedelta(minutes=20 + offset_index * 4)

            site_id = f"ZA-{province_code}-{offset_index + 1:02d}"
            site_name = f"{province} {chr(65 + offset_index)}{offset_index + 1}"
            sites.append(
                {
                    "site_id": site_id,
                    "name": site_name,
                    "province": province,
                    "region": province,
                    "technology": "5G" if offset_index % 2 == 0 else "4G",
                    "status": status,
                    "latency_ms": latency_ms,
                    "cpu_util_pct": cpu_util_pct,
                    "availability_pct": availability_pct,
                    "packet_loss_pct": packet_loss_pct,
                    "bandwidth_util_pct": bandwidth_util_pct,
                    "error_rate_ppm": error_rate_ppm,
                    "affected_customers": affected_customers,
                    "last_updated": last_updated,
                    "lat": lat,
                    "lon": lon,
                }
            )

    return sites


SITE_DATA = generate_demo_sites()


def summarize_sites(sites: list[dict[str, Any]]) -> tuple[int, int, int, int, int, int]:
    total = len(sites)
    healthy = sum(1 for site in sites if display_status(site) == "Healthy")
    degraded = sum(1 for site in sites if display_status(site) == "Degraded")
    unavailable = sum(1 for site in sites if display_status(site) == "Unavailable")
    stale = sum(1 for site in sites if display_status(site) == "Stale telemetry")
    affected_customers = sum(int(site["affected_customers"] or 0) for site in sites)
    return total, healthy, degraded, unavailable, stale, affected_customers


def average_metric(sites: list[dict[str, Any]], field: str) -> tuple[float | None, int]:
    valid_values = [
        site[field]
        for site in sites
        if site[field] is not None and telemetry_state(site) == "Fresh"
    ]
    if not valid_values:
        return None, 0
    return sum(valid_values) / len(valid_values), len(valid_values)


def kpi_summary(sites: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = [
        ("Availability", "availability_pct", "%"),
        ("Latency", "latency_ms", "ms"),
        ("CPU utilisation", "cpu_util_pct", "%"),
        ("Packet loss", "packet_loss_pct", "%"),
        ("Bandwidth utilisation", "bandwidth_util_pct", "%"),
        ("Error rate", "error_rate_ppm", "ppm"),
    ]
    rows: list[dict[str, Any]] = []
    for label, field, unit in metrics:
        value, count = average_metric(sites, field)
        rows.append({"label": label, "value": value, "count": count, "unit": unit})
    rows.append({"label": "Affected customers", "value": sum(int(site["affected_customers"] or 0) for site in sites), "count": len(sites), "unit": "customers"})
    return rows


def priority_site(sites: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not sites:
        return None

    def score(site: dict[str, Any]) -> tuple[int, float, int]:
        if site["status"] == "Unavailable":
            base = 1000
        elif telemetry_state(site) == "Stale":
            base = 700
        elif site["status"] == "Degraded":
            base = 500
        else:
            base = 0

        issue_score = 0.0
        if site["packet_loss_pct"] is not None:
            issue_score += site["packet_loss_pct"] * 12
        if site["latency_ms"] is not None:
            issue_score += max(0, site["latency_ms"] - 80) * 0.6
        if site["error_rate_ppm"] is not None:
            issue_score += site["error_rate_ppm"] * 1.3
        if site["bandwidth_util_pct"] is not None:
            issue_score += min(site["bandwidth_util_pct"], 100) * 0.3
        impact = int(site["affected_customers"] or 0)
        return (base, issue_score, impact)

    return max(sites, key=score)


def site_explanation(site: dict[str, Any]) -> str:
    if display_status(site) == "Unavailable":
        return (
            "This site is offline. No current telemetry is available, so the operator should check "
            "power, backhaul, fibre, or radio equipment before re-establishing service."
        )

    if freshness_label(site) == "Telemetry stale":
        age_minutes = int((datetime.now(timezone.utc) - site["last_updated"]).total_seconds() / 60)
        return (
            f"Telemetry is stale at {age_minutes} minutes old. The site is still serving traffic, but its readings may be delayed "
            "and should be validated before assuming the issue is fully understood."
        )

    reasons: list[str] = []
    if site["latency_ms"] is not None and site["latency_ms"] > 100:
        reasons.append(f"latency is {int(site['latency_ms'])} ms")
    if site["packet_loss_pct"] is not None and site["packet_loss_pct"] > 2:
        reasons.append(f"packet loss is {site['packet_loss_pct']:.1f}%")
    if site["cpu_util_pct"] is not None and site["cpu_util_pct"] > 70:
        reasons.append(f"CPU is {site['cpu_util_pct']:.1f}%")
    if site["bandwidth_util_pct"] is not None and site["bandwidth_util_pct"] > 80:
        reasons.append(f"traffic utilisation is {site['bandwidth_util_pct']:.1f}%")

    if not reasons:
        return (
            "The site is operating within normal thresholds, with stable latency, acceptable packet loss, "
            "and healthy utilisation."
        )

    reason_text = ", ".join(reasons)
    return (
        f"This site is degraded because {reason_text}. The operator should review capacity and service quality before customers experience further impact."
    )


def build_dataframe(sites: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for site in sites:
        rows.append(
            {
                "Site ID": site["site_id"],
                "Site name": site["name"],
                "Province": site["province"],
                "Technology": site["technology"],
                "Status": display_status(site),
                "Latency": format_metric(site["latency_ms"], "ms"),
                "CPU": format_metric(site["cpu_util_pct"], "%"),
                "Availability": format_metric(site["availability_pct"], "%"),
                "Packet loss": format_metric(site["packet_loss_pct"], "%"),
                "Traffic": format_metric(site["bandwidth_util_pct"], "%"),
                "Error rate": format_metric(site["error_rate_ppm"], "ppm"),
                "Affected customers": site["affected_customers"],
                "Last update": site["last_updated"].strftime("%Y-%m-%d %H:%M UTC"),
            }
        )
    return pd.DataFrame(rows)


def render_metric_card(title: str, value: str, accent: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: #162235; border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px;
            padding: 0.9rem 1rem; margin-bottom: 0.8rem; min-height: 104px;
        ">
            <div style="color:#8DA3BE; font-size:0.78rem; text-transform: uppercase; letter-spacing:0.06em; margin-bottom:0.3rem;">{title}</div>
            <div style="color:{accent}; font-size:1.9rem; font-weight:700; line-height:1.2;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_map(sites: list[dict[str, Any]]) -> None:
    fig = go.Figure()
    for status in ["Healthy", "Degraded", "Unavailable", "Stale telemetry"]:
        subset = [site for site in sites if display_status(site) == status]
        if not subset:
            continue
        fig.add_trace(
            go.Scattergeo(
                lon=[site["lon"] for site in subset],
                lat=[site["lat"] for site in subset],
                mode="markers",
                marker={
                    "size": 12,
                    "color": STATUS_COLORS[status],
                    "line": {"color": "#E8EEF5", "width": 1},
                },
                customdata=[
                    [
                        site["name"],
                        site["province"],
                        display_status(site),
                        format_metric(site["latency_ms"], "ms"),
                        format_metric(site["availability_pct"], "%"),
                        format_metric(site["packet_loss_pct"], "%"),
                        format_metric(site["bandwidth_util_pct"], "%"),
                        format_metric(site["error_rate_ppm"], "ppm"),
                        site["site_id"],
                    ]
                    for site in subset
                ],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Site ID: %{customdata[8]}<br>"
                    "Province: %{customdata[1]}<br>"
                    "Status: %{customdata[2]}<br>"
                    "Latency: %{customdata[3]}<br>"
                    "Availability: %{customdata[4]}<br>"
                    "Packet loss: %{customdata[5]}<br>"
                    "Bandwidth: %{customdata[6]}<br>"
                    "Error rate: %{customdata[7]}<extra></extra>"
                ),
                name=status,
            )
        )

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        font={"color": "#E8EEF5"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0.01},
        geo={
            "scope": "africa",
            "projection": {"type": "mercator"},
            "showland": True,
            "landcolor": "#162235",
            "countrycolor": "#2D3B4F",
            "showcoastlines": False,
            "showframe": False,
            "bgcolor": "#0B1220",
            "fitbounds": "locations",
        },
    )
    st.plotly_chart(fig, use_container_width=True)


def render_kpi_panel(sites: list[dict[str, Any]], label: str) -> None:
    st.markdown(f"<div class='section-title'>{label}</div>", unsafe_allow_html=True)
    kpis = kpi_summary(sites)
    cols = st.columns(4)
    for index, metric in enumerate(kpis[:4]):
        with cols[index]:
            if metric["value"] is None:
                value = "No reading"
                accent = "#8DA3BE"
            elif metric["label"] == "Affected customers":
                value = f"{int(metric['value']):,}"
                accent = "#E8EEF5"
            elif metric["unit"] == "%":
                value = f"{metric['value']:.1f}%"
                accent = "#38BDF8"
            elif metric["unit"] == "ms":
                value = f"{int(metric['value'])} ms"
                accent = "#38BDF8"
            elif metric["unit"] == "ppm":
                value = f"{metric['value']:.1f} ppm"
                accent = "#F59E0B"
            else:
                value = str(int(metric["value"]))
                accent = "#E8EEF5"
            st.markdown(
                f"""
                <div style="background:#162235;border:1px solid rgba(148,163,184,0.2);border-radius:12px;padding:0.8rem 0.9rem;margin-bottom:0.8rem;">
                    <div style="color:#8DA3BE;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;">{metric['label']}</div>
                    <div style="color:{accent};font-size:1.4rem;font-weight:700;margin-top:0.25rem;">{value}</div>
                    <div style="color:#8DA3BE;font-size:0.72rem;margin-top:0.2rem;">{metric['count']} readings</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    cols = st.columns(3)
    for index, metric in enumerate(kpis[4:]):
        with cols[index]:
            if metric["value"] is None:
                value = "No reading"
                accent = "#8DA3BE"
            elif metric["unit"] == "%":
                value = f"{metric['value']:.1f}%"
                accent = "#38BDF8"
            elif metric["unit"] == "ms":
                value = f"{int(metric['value'])} ms"
                accent = "#38BDF8"
            else:
                value = f"{metric['value']:.1f} ppm"
                accent = "#F59E0B"
            st.markdown(
                f"""
                <div style="background:#162235;border:1px solid rgba(148,163,184,0.2);border-radius:12px;padding:0.8rem 0.9rem;margin-bottom:0.8rem;">
                    <div style="color:#8DA3BE;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;">{metric['label']}</div>
                    <div style="color:{accent};font-size:1.4rem;font-weight:700;margin-top:0.25rem;">{value}</div>
                    <div style="color:#8DA3BE;font-size:0.72rem;margin-top:0.2rem;">{metric['count']} readings</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def main() -> None:
    st.title("Network Operations Centre")
    st.caption("AI-supported network management concept")
    st.markdown("<div class='simulated-badge'>Simulated network data</div>", unsafe_allow_html=True)

    site_scope = SITE_DATA
    selected_province = st.sidebar.selectbox("Province", ["All provinces", *PROVINCE_ORDER])

    search_query = st.sidebar.text_input("Search by site name or ID")
    technology_filter = st.sidebar.selectbox("Technology", ["All", "4G", "5G"])
    status_filter = st.sidebar.selectbox("Status", ["All", "Healthy", "Degraded", "Unavailable", "Stale telemetry"], index=0)

    if selected_province != "All provinces":
        site_scope = [site for site in SITE_DATA if site["province"] == selected_province]

    filtered_sites = [
        site
        for site in site_scope
        if (not search_query or search_query.lower() in site["name"].lower() or search_query.lower() in site["site_id"].lower())
        and (technology_filter == "All" or site["technology"] == technology_filter)
        and (status_filter == "All" or display_status(site) == status_filter)
    ]

    filtered_sites = sorted(
        filtered_sites,
        key=lambda site: (
            status_rank(display_status(site)),
            -int(site["affected_customers"] or 0),
            site["name"],
        ),
    )

    scope_label = selected_province if selected_province != "All provinces" else "National network"
    total_sites, healthy_sites, degraded_sites, unavailable_sites, stale_sites, affected_customers = summarize_sites(SITE_DATA)
    current_total, current_healthy, current_degraded, current_unavailable, current_stale, current_affected = summarize_sites(filtered_sites)

    st.markdown("<div class='section-title'>National summary</div>", unsafe_allow_html=True)
    summary_cols = st.columns(5)
    metric_values = [
        ("Total sites", total_sites, "#38BDF8"),
        ("Healthy", healthy_sites, "#22C55E"),
        ("Degraded", degraded_sites, "#F59E0B"),
        ("Unavailable", unavailable_sites, "#EF4444"),
        ("Affected customers", f"{affected_customers:,}", "#E8EEF5"),
    ]
    for col, (label, value, color) in zip(summary_cols, metric_values):
        with col:
            render_metric_card(label, str(value), color)

    scope_note = f"Current view: {scope_label} · {current_total} sites · {current_healthy} healthy · {current_degraded} degraded · {current_unavailable} unavailable · {current_affected:,} affected customers"
    st.caption(scope_note)

    priority = priority_site(filtered_sites if filtered_sites else site_scope)
    st.markdown("<div class='section-title'>Priority</div>", unsafe_allow_html=True)
    if priority is not None:
        prio_status = display_status(priority)
        st.markdown(
            f"""
            <div class='priority-box'>
                <div style='font-size:0.76rem;text-transform:uppercase;letter-spacing:0.08em;color:#8DA3BE;'>Most urgent site</div>
                <div style='font-size:1.5rem;font-weight:700;margin:0.35rem 0;color:#E8EEF5;'>{priority['name']}</div>
                <div>{status_badge_html(prio_status)} <span style='color:#8DA3BE; margin-left:0.5rem;'> {priority['province']} · {priority['technology']}</span></div>
                <div style='margin-top:0.8rem;color:#E8EEF5;line-height:1.6;'>
                    {priority['name']} ({priority['site_id']}) is the current priority because it is affecting approximately {priority['affected_customers']:,} customers.
                    {site_explanation(priority)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No site data is available for the current selection.")

    st.markdown("<div class='section-title'>Map</div>", unsafe_allow_html=True)
    map_sites = filtered_sites if filtered_sites else site_scope
    render_map(map_sites)

    left_col, right_col = st.columns([1.6, 1.2])
    with left_col:
        render_kpi_panel(map_sites, f"Province KPI panel · {scope_label}")
    with right_col:
        st.markdown("<div class='section-title'>Legend</div>", unsafe_allow_html=True)
        for status, color in STATUS_COLORS.items():
            st.markdown(
                f"<div style='display:flex;align-items:center;margin-bottom:0.45rem;'><span style='display:inline-block;width:14px;height:14px;background:{color};border-radius:50%;margin-right:0.6rem;'></span>{status}</div>",
                unsafe_allow_html=True,
            )
        st.caption("All values are fictional and intended for demonstration only.")

    st.markdown("<div class='section-title'>Sites</div>", unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered_sites)} of {len(site_scope)} sites in {scope_label}")
    if not filtered_sites:
        st.warning("No sites match the current filters.")
        return

    site_table = build_dataframe(filtered_sites)
    st.dataframe(
        site_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(width="small"),
            "Province": st.column_config.TextColumn(width="small"),
            "Latency": st.column_config.TextColumn(width="small"),
            "CPU": st.column_config.TextColumn(width="small"),
            "Availability": st.column_config.TextColumn(width="small"),
            "Packet loss": st.column_config.TextColumn(width="small"),
            "Traffic": st.column_config.TextColumn(width="small"),
            "Error rate": st.column_config.TextColumn(width="small"),
            "Affected customers": st.column_config.NumberColumn(format="%d"),
        },
    )

    selected_site_name = st.selectbox("Inspect a site", options=[site["name"] for site in filtered_sites], index=0)
    selected_site = next(site for site in filtered_sites if site["name"] == selected_site_name)

    st.markdown("<div class='section-title'>Site inspection</div>", unsafe_allow_html=True)
    info_cols = st.columns([1.3, 2.2])
    with info_cols[0]:
        site_stat = display_status(selected_site)
        st.markdown(
            f"""
            <div style='background:#162235;border:1px solid rgba(148,163,184,0.2);border-radius:14px;padding:1rem;height:100%;'>
                <div style='color:#8DA3BE;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;'>Selected site</div>
                <div style='font-size:1.6rem;color:#E8EEF5;font-weight:700;margin:0.5rem 0;'>{selected_site['name']}</div>
                <div>{status_badge_html(site_stat)}</div>
                <div style='margin-top:1rem;color:#E8EEF5;line-height:1.7;'><strong>ID:</strong> {selected_site['site_id']}<br>
                <strong>Province:</strong> {selected_site['province']}<br>
                <strong>Technology:</strong> {selected_site['technology']}<br>
                <strong>Last update:</strong> {selected_site['last_updated'].strftime('%Y-%m-%d %H:%M UTC')}<br>
                <strong>Telemetry:</strong> {freshness_label(selected_site)}<br>
                <strong>Affected customers:</strong> {selected_site['affected_customers']:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with info_cols[1]:
        st.markdown(
            f"""
            <div style='background:#162235;border:1px solid rgba(148,163,184,0.2);border-radius:14px;padding:1rem;height:100%;'>
                <div style='font-size:0.8rem;color:#8DA3BE;text-transform:uppercase;letter-spacing:0.06em;'>Operational note</div>
                <div style='margin-top:0.75rem;color:#E8EEF5;line-height:1.6;'>{site_explanation(selected_site)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    metric_cards = [
        ("Latency", format_metric(selected_site["latency_ms"], "ms"), "#38BDF8"),
        ("CPU utilisation", format_metric(selected_site["cpu_util_pct"], "%"), "#38BDF8"),
        ("Availability", format_metric(selected_site["availability_pct"], "%"), "#22C55E"),
        ("Packet loss", format_metric(selected_site["packet_loss_pct"], "%"), "#F59E0B"),
        ("Bandwidth utilisation", format_metric(selected_site["bandwidth_util_pct"], "%"), "#38BDF8"),
        ("Error rate", format_metric(selected_site["error_rate_ppm"], "ppm"), "#F59E0B"),
    ]
    metric_cols = st.columns(3)
    for index, (title, value, accent) in enumerate(metric_cards):
        with metric_cols[index % 3]:
            render_metric_card(title, value, accent)


if __name__ == "__main__":
    main()
