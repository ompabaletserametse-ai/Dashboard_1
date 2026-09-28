from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Network Operations Centre",
    page_icon="📡",
    layout="wide",
)

# This app uses fictional demonstration data only.
# The priority rule is intentionally simple and transparent:
# 1) offline sites are highest priority,
# 2) then degraded sites with the most affected customers and worst KPI readings,
# 3) healthy sites are not flagged for action.
SITE_DATA: list[dict[str, Any]] = [
    {
        "site_id": "ZA-GT-01",
        "name": "Sandton Core",
        "region": "Gauteng",
        "technology": "5G",
        "status": "Healthy",
        "latency_ms": 38,
        "cpu_util_pct": 48,
        "availability_pct": 99.98,
        "packet_loss_pct": 0.8,
        "bandwidth_util_pct": 62,
        "error_rate_ppm": 3.2,
        "affected_customers": 0,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=5),
    },
    {
        "site_id": "ZA-KZN-02",
        "name": "Durban South",
        "region": "KwaZulu-Natal",
        "technology": "4G",
        "status": "Degraded",
        "latency_ms": 123,
        "cpu_util_pct": 76,
        "availability_pct": 99.7,
        "packet_loss_pct": 3.1,
        "bandwidth_util_pct": 78,
        "error_rate_ppm": 12.4,
        "affected_customers": 2300,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=15),
    },
    {
        "site_id": "ZA-WC-03",
        "name": "Cape Town CBD",
        "region": "Western Cape",
        "technology": "5G",
        "status": "Healthy",
        "latency_ms": 29,
        "cpu_util_pct": 52,
        "availability_pct": 99.99,
        "packet_loss_pct": 0.5,
        "bandwidth_util_pct": 58,
        "error_rate_ppm": 2.1,
        "affected_customers": 0,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=12),
    },
    {
        "site_id": "ZA-WC-04",
        "name": "Khayelitsha East",
        "region": "Western Cape",
        "technology": "4G",
        "status": "Degraded",
        "latency_ms": 167,
        "cpu_util_pct": 81,
        "availability_pct": 99.4,
        "packet_loss_pct": 5.8,
        "bandwidth_util_pct": 87,
        "error_rate_ppm": 18.9,
        "affected_customers": 4200,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=43),
    },
    {
        "site_id": "ZA-GT-05",
        "name": "Pretoria North",
        "region": "Gauteng",
        "technology": "5G",
        "status": "Unavailable",
        "latency_ms": None,
        "cpu_util_pct": None,
        "availability_pct": None,
        "packet_loss_pct": None,
        "bandwidth_util_pct": None,
        "error_rate_ppm": None,
        "affected_customers": 6000,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=70),
    },
    {
        "site_id": "ZA-LP-06",
        "name": "Polokwane West",
        "region": "Limpopo",
        "technology": "4G",
        "status": "Healthy",
        "latency_ms": 51,
        "cpu_util_pct": 46,
        "availability_pct": 99.95,
        "packet_loss_pct": 1.0,
        "bandwidth_util_pct": 49,
        "error_rate_ppm": 2.7,
        "affected_customers": 0,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=10),
    },
    {
        "site_id": "ZA-FS-07",
        "name": "Bloemfontein East",
        "region": "Free State",
        "technology": "4G",
        "status": "Degraded",
        "latency_ms": 134,
        "cpu_util_pct": 73,
        "availability_pct": 98.8,
        "packet_loss_pct": 4.2,
        "bandwidth_util_pct": 76,
        "error_rate_ppm": 11.7,
        "affected_customers": 3100,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=26),
    },
    {
        "site_id": "ZA-EC-08",
        "name": "Gqeberha Waterfront",
        "region": "Eastern Cape",
        "technology": "5G",
        "status": "Healthy",
        "latency_ms": 44,
        "cpu_util_pct": 39,
        "availability_pct": 99.98,
        "packet_loss_pct": 0.7,
        "bandwidth_util_pct": 57,
        "error_rate_ppm": 1.8,
        "affected_customers": 0,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=9),
    },
    {
        "site_id": "ZA-GT-09",
        "name": "Johannesburg East",
        "region": "Gauteng",
        "technology": "4G",
        "status": "Unavailable",
        "latency_ms": None,
        "cpu_util_pct": None,
        "availability_pct": None,
        "packet_loss_pct": None,
        "bandwidth_util_pct": None,
        "error_rate_ppm": None,
        "affected_customers": 4800,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=58),
    },
    {
        "site_id": "ZA-MP-10",
        "name": "Nelspruit West",
        "region": "Mpumalanga",
        "technology": "5G",
        "status": "Healthy",
        "latency_ms": 46,
        "cpu_util_pct": 42,
        "availability_pct": 99.99,
        "packet_loss_pct": 0.6,
        "bandwidth_util_pct": 53,
        "error_rate_ppm": 2.3,
        "affected_customers": 0,
        "last_updated": datetime.now(timezone.utc) - timedelta(minutes=8),
    },
]

STATUS_COLORS = {
    "Healthy": "#22C55E",
    "Degraded": "#F59E0B",
    "Unavailable": "#EF4444",
    "Stale telemetry": "#38BDF8",
}


def status_rank(status: str) -> int:
    return {"Healthy": 0, "Degraded": 1, "Unavailable": 2}.get(status, 0)


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
    if site["last_updated"] is None:
        return "No reading"
    age_minutes = (datetime.now(timezone.utc) - site["last_updated"]).total_seconds() / 60
    if age_minutes > 30:
        return "Telemetry stale"
    return "Fresh"


def status_label(site: dict[str, Any]) -> str:
    if site["status"] == "Unavailable":
        return "Unavailable"
    if freshness_label(site) == "Telemetry stale":
        return "Degraded"
    return site["status"]


def status_badge_html(status: str) -> str:
    color = STATUS_COLORS.get(status, "#38BDF8")
    return (
        "<span style='display:inline-block;padding:0.28rem 0.65rem;"
        f"background:{color};color:#08111d;border-radius:999px;font-size:0.76rem;"
        "font-weight:700;letter-spacing:0.02em;'>"
        f"{status}</span>"
    )


def summary_cards() -> tuple[int, int, int, int, int]:
    total = len(SITE_DATA)
    healthy = sum(1 for site in SITE_DATA if status_label(site) == "Healthy")
    degraded = sum(1 for site in SITE_DATA if status_label(site) == "Degraded")
    unavailable = sum(1 for site in SITE_DATA if status_label(site) == "Unavailable")
    affected_customers = sum(int(site["affected_customers"] or 0) for site in SITE_DATA)
    return total, healthy, degraded, unavailable, affected_customers


def priority_site(sites: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not sites:
        return None

    def score(site: dict[str, Any]) -> tuple[int, float, int]:
        if site["status"] == "Unavailable":
            base = 1000
        elif freshness_label(site) == "Telemetry stale":
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
    if site["status"] == "Unavailable":
        return (
            "This site is offline. No current telemetry is available, so the operator should check"
            " power, backhaul, fibre, or radio equipment before re-establishing service."
        )

    if freshness_label(site) == "Telemetry stale":
        return (
            f"Telemetry is stale at {int((datetime.now(timezone.utc) - site['last_updated']).total_seconds() / 60)} minutes old. "
            "The site is still serving traffic, but its readings may be delayed and should be validated "
            "before assuming the issue is fully understood."
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
        f"This site is degraded because {reason_text}. The operator should review capacity and service "
        "quality before customers experience further impact."
    )


def build_dataframe(sites: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for site in sites:
        rows.append(
            {
                "Site ID": site["site_id"],
                "Site name": site["name"],
                "Region": site["region"],
                "Technology": site["technology"],
                "Status": status_label(site),
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


def main() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #0B1220; color: #E8EEF5; }
        .block-container { padding-top: 1.2rem; }
        div[data-testid="stMetric"] { background: #162235; border-radius: 12px; }
        .simulated-badge {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #E8EEF5;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }
        .section-title {
            color: #E8EEF5; font-size: 1.1rem; font-weight: 700; margin-top: 1.3rem; margin-bottom: 0.5rem;
        }
        .priority-box {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(22, 34, 53, 0.9));
            border: 1px solid rgba(239, 68, 68, 0.24);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-top: 0.35rem;
        }
        @media (max-width: 768px) {
            .block-container { padding-left: 0.7rem; padding-right: 0.7rem; }
            .priority-box { padding: 0.9rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Network Operations Centre")
    st.caption("AI-supported network management concept")
    st.markdown("<div class='simulated-badge'>Simulated network data</div>", unsafe_allow_html=True)

    total_sites, healthy_sites, degraded_sites, unavailable_sites, affected_customers = summary_cards()

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

    st.markdown("<div class='section-title'>Priority</div>", unsafe_allow_html=True)
    priority = priority_site(SITE_DATA)
    if priority is not None:
        priority_label = status_label(priority)
        stale_note = "Telemetry stale" if freshness_label(priority) == "Telemetry stale" else "Fresh readings"
        prio_text = (
            f"{priority['name']} ({priority['site_id']}) is the current priority. "
            f"Status: {priority_label}. {stale_note}. It affects approximately {priority['affected_customers']:,} customers. "
            f"The site is showing {priority['packet_loss_pct'] if priority['packet_loss_pct'] is not None else 'no available'} packet loss and "
            f"{priority['latency_ms'] if priority['latency_ms'] is not None else 'no available'} latency, so the operator should focus here first."
        )
        if priority["status"] == "Unavailable":
            prio_text = (
                f"{priority['name']} ({priority['site_id']}) is offline and currently the highest-priority incident. "
                f"It is affecting approximately {priority['affected_customers']:,} customers and has no available telemetry. "
                "The operator should verify power, backhaul, and radio service before restoring capacity."
            )
        st.markdown(
            f"""
            <div class='priority-box'>
                <div style='font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.08em; color:#8DA3BE;'>Most urgent site</div>
                <div style='font-size: 1.45rem; font-weight: 700; margin: 0.35rem 0; color: #E8EEF5;'>{priority['name']}</div>
                <div>{status_badge_html(priority_label)} <span style='color:#8DA3BE; margin-left:0.5rem;'>{priority['region']} · {priority['technology']}</span></div>
                <div style='margin-top:0.8rem; color: #E8EEF5; line-height:1.5;'>{prio_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No active sites available.")

    st.markdown("<div class='section-title'>Sites</div>", unsafe_allow_html=True)
    with st.sidebar:
        st.subheader("Filters")
        search_query = st.text_input("Search by site name or ID")
        region_filter = st.selectbox("Region", ["All"] + sorted({site["region"] for site in SITE_DATA}))
        technology_filter = st.selectbox("Technology", ["All"] + sorted({site["technology"] for site in SITE_DATA}))
        status_filter = st.selectbox("Status", ["All"] + ["Healthy", "Degraded", "Unavailable"])

    filtered_sites = [
        site
        for site in SITE_DATA
        if (not search_query or search_query.lower() in site["name"].lower() or search_query.lower() in site["site_id"].lower())
        and (region_filter == "All" or site["region"] == region_filter)
        and (technology_filter == "All" or site["technology"] == technology_filter)
        and (status_filter == "All" or status_label(site) == status_filter)
    ]

    filtered_sites = sorted(
        filtered_sites,
        key=lambda site: (
            status_rank(status_label(site)),
            -int(site["affected_customers"] or 0),
            site["name"],
        ),
        reverse=True,
    )

    st.caption(f"Showing {len(filtered_sites)} of {len(SITE_DATA)} sites")
    if not filtered_sites:
        st.warning("No sites match the current filters.")
        return

    table = build_dataframe(filtered_sites)
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(width="small"),
            "Latency": st.column_config.TextColumn(width="small"),
            "CPU": st.column_config.TextColumn(width="small"),
            "Availability": st.column_config.TextColumn(width="small"),
            "Packet loss": st.column_config.TextColumn(width="small"),
            "Traffic": st.column_config.TextColumn(width="small"),
            "Error rate": st.column_config.TextColumn(width="small"),
            "Affected customers": st.column_config.NumberColumn(format="%d"),
        },
    )

    selected_site_name = st.selectbox(
        "Inspect a site",
        options=[site["name"] for site in filtered_sites],
        index=0,
    )
    selected_site = next(site for site in filtered_sites if site["name"] == selected_site_name)

    site_status = status_label(selected_site)
    site_age_minutes = int((datetime.now(timezone.utc) - selected_site["last_updated"]).total_seconds() / 60)

    st.markdown("<div class='section-title'>Site inspection</div>", unsafe_allow_html=True)
    info_cols = st.columns([1.3, 2.2])
    with info_cols[0]:
        st.markdown(
            f"""
            <div style='background:#162235; border: 1px solid rgba(148,163,184,0.2); border-radius: 14px; padding:1rem; height:100%;'>
                <div style='color:#8DA3BE; font-size:0.78rem; text-transform: uppercase; letter-spacing:0.06em;'>Selected site</div>
                <div style='font-size: 1.6rem; color:#E8EEF5; font-weight:700; margin: 0.5rem 0;'>{selected_site['name']}</div>
                <div>{status_badge_html(site_status)}</div>
                <div style='margin-top: 1rem; color:#E8EEF5; line-height:1.7;'><strong>ID:</strong> {selected_site['site_id']}<br>
                <strong>Region:</strong> {selected_site['region']}<br>
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
            <div style='background:#162235; border: 1px solid rgba(148,163,184,0.2); border-radius: 14px; padding:1rem; height:100%;'>
                <div style='font-size:0.8rem; color:#8DA3BE; text-transform: uppercase; letter-spacing:0.06em;'>Operational note</div>
                <div style='margin-top:0.75rem; color:#E8EEF5; line-height:1.6;'>
                    {site_explanation(selected_site)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    metric_cols = st.columns(3)
    metric_cards = [
        ("Latency", format_metric(selected_site["latency_ms"], "ms"), "#38BDF8"),
        ("CPU utilisation", format_metric(selected_site["cpu_util_pct"], "%"), "#38BDF8"),
        ("Availability", format_metric(selected_site["availability_pct"], "%"), "#22C55E"),
        ("Packet loss", format_metric(selected_site["packet_loss_pct"], "%"), "#F59E0B"),
        ("Bandwidth utilisation", format_metric(selected_site["bandwidth_util_pct"], "%"), "#38BDF8"),
        ("Error rate", format_metric(selected_site["error_rate_ppm"], "ppm"), "#F59E0B"),
    ]

    for index, (title, value, accent) in enumerate(metric_cards):
        with metric_cols[index % 3]:
            render_metric_card(title, value, accent)


if __name__ == "__main__":
    main()
