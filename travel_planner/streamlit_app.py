import html
import os
from typing import Any

import httpx
import streamlit as st


DEFAULT_API_BASE_URL = "http://localhost:8000"
# Three agents run in parallel, then the planner runs, so a request can take a while.
REQUEST_TIMEOUT = httpx.Timeout(180.0, connect=10.0)

EXAMPLE_TRIPS = {
    "🗼 Paris": (
        "I want to spend 4 days in Paris. I love museums and art, want to try "
        "classic French food, and have a medium budget."
    ),
    "🏝️ Bali": (
        "7 days in Bali for a relaxing beach holiday with some temples and rice "
        "terraces. I like street food and have a low budget."
    ),
    "🏔️ Swiss Alps": (
        "5 days in the Swiss Alps in winter. I want scenic train rides, hiking or "
        "skiing and cozy mountain restaurants. High budget."
    ),
    "🍣 Tokyo": (
        "6 days in Tokyo. I'm into food markets, ramen, anime shops and modern "
        "architecture. Medium budget."
    ),
}

BUDGET_ICONS = {
    "Accommodation": "🏨",
    "Food": "🍽️",
    "Transportation": "🚆",
    "Activities": "🎟️",
    "Total": "💰",
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Nunito:wght@400;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stTextArea textarea, button {
    font-family: 'Nunito', sans-serif;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1F3A4D;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0E7490 0%, #2A9D8F 45%, #F4A261 85%, #E76F51 100%);
    border-radius: 22px;
    padding: 2.6rem 2.4rem 2.2rem;
    color: #ffffff;
    margin-bottom: 1.6rem;
    box-shadow: 0 12px 30px rgba(14, 116, 144, 0.25);
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "✈";
    position: absolute;
    right: 2rem;
    top: 0.8rem;
    font-size: 6rem;
    opacity: 0.18;
    transform: rotate(-20deg);
}
.hero h1 {
    color: #ffffff !important;
    font-size: 2.6rem;
    margin: 0 0 0.4rem 0;
    padding: 0;
}
.hero p {
    font-size: 1.1rem;
    margin: 0;
    max-width: 640px;
    opacity: 0.95;
}
.hero .agents {
    margin-top: 1.1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.hero .agent-chip {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 999px;
    padding: 0.25rem 0.85rem;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Boarding pass for the thread ID */
.boarding-pass {
    display: flex;
    background: #ffffff;
    border: 1px solid #E8DCCB;
    border-radius: 16px;
    overflow: hidden;
    margin: 0.4rem 0 1.2rem;
    box-shadow: 0 6px 18px rgba(31, 58, 77, 0.08);
}
.boarding-pass .stub {
    background: #E76F51;
    color: #ffffff;
    padding: 1rem 1.2rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    display: flex;
    align-items: center;
    font-size: 0.85rem;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
}
.boarding-pass .body {
    padding: 0.9rem 1.3rem;
    border-left: 2px dashed #E8DCCB;
    flex: 1;
    min-width: 0;
}
.boarding-pass .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8A7A66;
}
.boarding-pass .value {
    font-family: monospace;
    font-size: 0.95rem;
    color: #1F3A4D;
    word-break: break-all;
}
.boarding-pass .request {
    margin-top: 0.5rem;
    font-size: 0.95rem;
    color: #1F3A4D;
}

/* Budget metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #E8DCCB;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    box-shadow: 0 4px 12px rgba(31, 58, 77, 0.05);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem;
}
.stTabs [data-baseweb="tab"] {
    background: #F3E9DC;
    border-radius: 999px;
    padding: 0.4rem 1rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #2A9D8F;
    color: #ffffff !important;
}

/* Form card */
[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #E8DCCB;
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
}

.footer-note {
    text-align: center;
    color: #8A7A66;
    font-size: 0.85rem;
    margin-top: 2rem;
}
</style>
"""


class APIError(Exception):
    pass


def api_base_url() -> str:
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def request_json(method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    url = f"{api_base_url()}{path}"
    try:
        response = httpx.request(
            method,
            url,
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except httpx.TimeoutException as exc:
        raise APIError(
            "Planning took too long and the request timed out. Please try again."
        ) from exc
    except httpx.RequestError as exc:
        raise APIError(
            f"Could not connect to the API at {api_base_url()}. "
            "Check that FastAPI is running and API_BASE_URL is correct."
        ) from exc

    if not response.is_success:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise APIError(f"API returned HTTP {response.status_code}: {detail}")

    try:
        data = response.json()
    except ValueError as exc:
        raise APIError("The API returned an invalid JSON response.") from exc

    if not isinstance(data, dict):
        raise APIError("The API returned a response in an unexpected format.")
    return data


def create_plan(user_request: str) -> dict[str, Any]:
    return request_json(
        "POST",
        "/api/travel-plan",
        json={"request": user_request},
    )


def load_plan(thread_id: str) -> dict[str, Any]:
    return request_json("GET", f"/api/travel-plan/{thread_id}")


def use_example(text: str) -> None:
    st.session_state.trip_request = text


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Where to next?</h1>
            <p>Tell us about your dream trip. A team of AI travel agents will scout the
            sights, find the best local food and estimate your budget, then put it all
            together into one day-by-day itinerary.</p>
            <div class="agents">
                <span class="agent-chip">🗺️ Destination scout</span>
                <span class="agent-chip">🍜 Food guide</span>
                <span class="agent-chip">💶 Budget analyst</span>
                <span class="agent-chip">🧳 Trip planner</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_boarding_pass(thread_id: str, user_request: str) -> None:
    st.markdown(
        f"""
        <div class="boarding-pass">
            <div class="stub">BOARDING PASS</div>
            <div class="body">
                <div class="label">Trip ID — save it to open this plan later</div>
                <div class="value">{html.escape(thread_id)}</div>
                <div class="label" style="margin-top:0.6rem;">Your request</div>
                <div class="request">{html.escape(user_request)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def parse_budget(budget_info: str) -> tuple[list[tuple[str, str]], str]:
    # The budget agent returns "Key: value" lines, e.g. "Food: 250.0 EUR".
    items: list[tuple[str, str]] = []
    notes = ""
    for line in budget_info.splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        if key == "Notes":
            notes = value
        else:
            items.append((key, value))
    return items, notes


def render_budget(budget_info: str) -> None:
    items, notes = parse_budget(budget_info)
    if not items:
        st.markdown(budget_info)
        return

    columns = st.columns(len(items))
    for column, (key, value) in zip(columns, items):
        icon = BUDGET_ICONS.get(key, "•")
        column.metric(f"{icon} {key}", value)

    if notes:
        st.markdown(f"**📝 Assumptions:** {notes}")


def render_agent_output(text: str | None, empty_message: str) -> None:
    if text:
        st.markdown(text)
    else:
        st.info(empty_message)


def render_plan(plan: dict[str, Any]) -> None:
    if plan.get("final_plan"):
        st.success("🌴 Your itinerary is ready. Bon voyage!")
    else:
        st.warning("This trip was never finished. Please plan it again.")

    tab_plan, tab_destination, tab_food, tab_budget = st.tabs(
        ["🧳 Itinerary", "🗺️ Sights", "🍜 Food", "💶 Budget"]
    )

    with tab_plan:
        st.caption("From the trip planner, who combines everything into one itinerary.")
        render_agent_output(plan.get("final_plan"), "The itinerary isn't ready yet.")

    with tab_destination:
        st.caption("From the destination scout: attractions and activities.")
        render_agent_output(
            plan.get("destination_info"), "No sightseeing ideas yet."
        )

    with tab_food:
        st.caption("From the food guide: local dishes, restaurants and markets.")
        render_agent_output(plan.get("food_info"), "No food recommendations yet.")

    with tab_budget:
        st.caption("From the budget analyst: estimated costs for the whole trip.")
        budget_info = plan.get("budget_info")
        if budget_info:
            render_budget(budget_info)
        else:
            st.info("No budget estimate yet.")


def main() -> None:
    st.set_page_config(page_title="Travel Planner", page_icon="✈️", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if "active_thread_id" not in st.session_state:
        st.session_state.active_thread_id = ""
    if "plan" not in st.session_state:
        st.session_state.plan = None
    if "trip_request" not in st.session_state:
        st.session_state.trip_request = ""

    with st.sidebar:
        st.markdown("## 🧭 Travel journal")
        st.caption("Open a trip you planned before using its trip ID.")
        recovery_id = st.text_input(
            "Trip ID",
            value=st.session_state.active_thread_id,
            key="recovery_thread_id",
        )
        if st.button("📖 Open trip", use_container_width=True):
            thread_id = recovery_id.strip()
            if not thread_id:
                st.warning("Enter a trip ID.")
            else:
                try:
                    with st.spinner("Finding your trip..."):
                        plan = load_plan(thread_id)
                    st.session_state.active_thread_id = thread_id
                    st.session_state.plan = plan
                    st.success("Trip loaded.")
                except APIError as exc:
                    st.error(str(exc))
                    if "404" in str(exc):
                        st.info("No trip with this ID was found in the database.")

        st.divider()
        with st.expander("⚙️ API settings"):
            st.code(api_base_url())
            st.caption("Set API_BASE_URL in the environment to use another API server.")

    render_hero()

    st.markdown("### 🌍 Need inspiration?")
    example_columns = st.columns(len(EXAMPLE_TRIPS))
    for column, (label, text) in zip(example_columns, EXAMPLE_TRIPS.items()):
        column.button(
            label,
            on_click=use_example,
            args=(text,),
            use_container_width=True,
        )

    with st.form("travel_request_form"):
        user_request = st.text_area(
            "✍️ Describe your trip",
            key="trip_request",
            height=140,
            placeholder=(
                "For example: I want to spend 4 days in Paris. I like museums, "
                "good local food and have a medium budget."
            ),
        )
        st.caption(
            "Include the destination, number of days, your interests and your budget level."
        )
        submitted = st.form_submit_button("✈️ Plan my trip", type="primary")

    if submitted:
        if len(user_request.strip()) < 10:
            st.warning("Tell us a bit more about your trip before submitting.")
        else:
            try:
                with st.spinner(
                    "🧳 Your travel agents are scouting sights, tasting food and "
                    "crunching numbers. This can take up to a minute..."
                ):
                    plan = create_plan(user_request.strip())
                thread_id = plan.get("thread_id")
                if not isinstance(thread_id, str) or not thread_id:
                    raise APIError("The API response did not include a valid thread ID.")
                st.session_state.active_thread_id = thread_id
                st.session_state.plan = plan
            except APIError as exc:
                st.error(str(exc))

    plan = st.session_state.plan
    thread_id = st.session_state.active_thread_id
    if plan and thread_id:
        st.divider()
        st.header("Your trip")
        render_boarding_pass(thread_id, st.session_state.plan.get("user_request", ""))
        render_plan(st.session_state.plan)

    st.markdown(
        '<div class="footer-note">Recommendations and prices are AI-generated '
        "estimates. Check opening hours and current prices before you travel.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
