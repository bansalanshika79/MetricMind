
import json
import re
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# ================= CONFIGURATION =================

CUBE_URL = "http://localhost:4000/cubejs-api/v1/load"
CUBE = "metricmind_sales"

st.set_page_config(
    page_title="MetricMind | BI Engine",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = [
    "#4E79A7", "#F28E2B", "#59A14F", "#E15759",
    "#B07AA1", "#76B7B2", "#EDC948", "#FF9DA7",
    "#9C755F", "#6B6ECF",
]

MEASURES = {
    "Revenue": f"{CUBE}.total_revenue",
    "Profit": f"{CUBE}.total_profit",
    "Orders": f"{CUBE}.total_orders",
    "Average Margin": f"{CUBE}.average_margin",
    "Quantity": f"{CUBE}.total_quantity",
}

DIMENSIONS = {
    "Country": f"{CUBE}.country",
    "Product Category": f"{CUBE}.product_category",
    "Customer Segment": f"{CUBE}.customer_segment",
    "Brand": f"{CUBE}.brand",
    "Membership Status": f"{CUBE}.membership_status",
}

DATE_DIMENSION = f"{CUBE}.order_date"

# ================= DESIGN =================

st.markdown("""
<style>
.stApp {
    background: #F5FAF6 !important;
    color: #20392A !important;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #174D32 !important;
    font-weight: 850 !important;
}

p, label, li, [data-testid="stCaptionContainer"] {
    color: #20392A;
}

.section-title {
    color: #174D32 !important;
    font-size: 1.65rem;
    font-weight: 900;
    margin: 22px 0 14px;
}

/* HEADER */
.hero {
    background: linear-gradient(120deg, #174D32, #23864B, #55A96E);
    padding: 30px 32px;
    border-radius: 20px;
    margin-bottom: 25px;
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: 2.25rem !important;
    font-weight: 900 !important;
    margin: 0 0 8px;
}
.hero p {
    color: #FFFFFF !important;
    font-size: 1.05rem;
    margin: 0;
}

/* SIDEBAR */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] section {
    background: #FFFFFF !important;
}
[data-testid="stSidebar"] {
    border-right: 1px solid #D5E7D9;
}
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #174D32 !important;
}
.brand-card {
    background: linear-gradient(135deg, #174D32, #45A765);
    border-radius: 18px;
    padding: 22px 17px;
    margin: 8px 0 25px;
}
.brand-mark {
    background: #FFFFFF;
    color: #174D32;
    border-radius: 13px;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: 900;
    margin-bottom: 14px;
}
.brand-card h2 {
    color: #FFFFFF !important;
    font-size: 26px !important;
    margin: 0 0 6px;
}
.brand-card p {
    color: #FFFFFF !important;
    font-size: 12px;
    letter-spacing: 1px;
    margin: 0;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 48px;
    background: #F4FAF5 !important;
    color: #174D32 !important;
    border: 1px solid #D5E7D9 !important;
    border-radius: 12px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .stButton > button p {
    color: #174D32 !important;
    font-weight: 800 !important;
}
.sidebar-footer {
    background: #F0FAF2;
    border: 1px solid #D5E7D9;
    border-radius: 15px;
    padding: 16px;
    margin-top: 24px;
}
.sidebar-footer h4 {
    color: #174D32 !important;
}
.sidebar-footer p {
    color: #52685A !important;
    font-size: 13px;
    line-height: 1.7;
}

/* KPI CARDS */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E7D9;
    padding: 20px;
    border-radius: 16px;
}
div[data-testid="stMetricLabel"] {
    color: #52685A !important;
    font-weight: 750 !important;
}
div[data-testid="stMetricValue"] {
    color: #23864B !important;
    font-weight: 850 !important;
}

/* WHITE DROPDOWNS */
[data-testid="stSelectbox"] label {
    color: #174D32 !important;
    font-weight: 850 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #174D32 !important;
    border: 1px solid #A9D4B5 !important;
    border-radius: 12px !important;
    min-height: 45px;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #174D32 !important;
    -webkit-text-fill-color: #174D32 !important;
    font-weight: 700 !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"],
li[role="option"] {
    background: #FFFFFF !important;
    color: #174D32 !important;
}
li[role="option"] * {
    color: #174D32 !important;
    -webkit-text-fill-color: #174D32 !important;
}
li[role="option"]:hover {
    background: #DDF5E3 !important;
}

/* QUESTION INPUT — HIGH CONTRAST */
[data-testid="stTextInput"] label {
    color: #174D32 !important;
    font-weight: 850 !important;
}
[data-testid="stTextInput"] input,
[data-testid="stForm"] input {
    background: #FFFFFF !important;
    color: #173D29 !important;
    -webkit-text-fill-color: #173D29 !important;
    caret-color: #23864B !important;
    border: 2px solid #8BC69D !important;
    border-radius: 12px !important;
    min-height: 48px;
    font-size: 16px !important;
    font-weight: 600 !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #64796B !important;
    -webkit-text-fill-color: #64796B !important;
    opacity: 1 !important;
}

/* BUTTONS */
.stButton > button,
.stFormSubmitButton > button {
    background: #23864B !important;
    color: #FFFFFF !important;
    border: 1px solid #23864B !important;
    border-radius: 11px !important;
    min-height: 44px;
    font-weight: 800 !important;
}
.stButton > button p,
.stFormSubmitButton > button p {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}
[data-testid="stDownloadButton"] button {
    background: #DDF5E3 !important;
    color: #174D32 !important;
    border: 1px solid #A9D4B5 !important;
    border-radius: 11px !important;
    font-weight: 800 !important;
}
[data-testid="stDownloadButton"] button p {
    color: #174D32 !important;
}

/* WHITE TABLES AND FORMS */
[data-testid="stDataFrame"],
[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E7D9;
    border-radius: 14px;
    overflow: hidden;
}
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E7D9;
    border-radius: 16px;
    padding: 20px;
}

/* ANSWER CARD */
.answer-card {
    background: linear-gradient(135deg, #FFFFFF, #EAF7ED);
    border: 1px solid #B9DEC4;
    border-left: 6px solid #23864B;
    border-radius: 18px;
    padding: 22px;
    margin: 10px 0 15px;
    box-shadow: 0 8px 22px rgba(23, 77, 50, 0.07);
}
.answer-title {
    color: #174D32;
    font-size: 22px;
    font-weight: 900;
}
.answer-subtitle {
    color: #52685A;
    font-size: 13px;
    margin-top: 5px;
}
hr {
    border-color: #D5E7D9;
}
</style>
""", unsafe_allow_html=True)


# ================= DATA FUNCTIONS =================

def get_data(measures, dimensions=None, time_dimensions=None):
    query = {"measures": measures}

    if dimensions:
        query["dimensions"] = dimensions
    if time_dimensions:
        query["timeDimensions"] = time_dimensions

    response = requests.get(
        CUBE_URL,
        params={"query": json.dumps(query)},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("data", [])


def money(value):
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def numeric(df, column):
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            color="#20392A",
            size=14,
        ),
        height=height,
        margin=dict(l=25, r=25, t=35, b=35),
        colorway=COLORS,
        legend=dict(
            font=dict(color="#20392A", size=13),
            bgcolor="#FFFFFF",
        ),
    )

    # Force all chart text and axis labels to dark colors.
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E1EBE4",
        color="#20392A",
        tickfont=dict(color="#20392A", size=12),
        title_font=dict(color="#174D32", size=14),
        zerolinecolor="#CBDACF",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E1EBE4",
        color="#20392A",
        tickfont=dict(color="#20392A", size=12),
        title_font=dict(color="#174D32", size=14),
        zerolinecolor="#CBDACF",
    )
    return fig


def display_answer(answer):
    if answer is None or not str(answer).strip():
        st.info("No answer was returned.")
        return

    text = str(answer).strip()

    if ":" in text:
        title, remainder = text.split(":", 1)

        if any(word in title.lower() for word in [
            " by ", "category", "country", "month", "segment", "brand"
        ]):
            st.markdown(f"**{title.strip()}**")

            pattern = re.compile(
                r"([A-Za-z][A-Za-z0-9 &()_./-]*?):\s*"
                r"(-?\d[\d,]*(?:\.\d+)?)"
            )
            matches = list(pattern.finditer(remainder))

            if matches:
                rows = []
                for match in matches:
                    label = match.group(1).strip(" :")
                    value = match.group(2).replace(",", "")

                    try:
                        value = f"{float(value):,.2f}"
                    except ValueError:
                        pass

                    rows.append({
                        "Category / Group": label,
                        "Value": value,
                    })

                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                )
                return

    st.markdown(text.replace("\n", "  \n"))


# ================= SIDEBAR =================

if "metricmind_page" not in st.session_state:
    st.session_state.metricmind_page = "Overview"

with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <div class="brand-mark">M</div>
        <h2>MetricMind</h2>
        <p>BUSINESS INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### NAVIGATION")

    navigation = [
        ("▦", "Overview"),
        ("◈", "Explore Data"),
        ("✦", "Ask MetricMind"),
        ("▤", "Data Table"),
    ]

    for symbol, page_name in navigation:
        if st.button(
            f"{symbol}   {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.metricmind_page == page_name
                else "secondary"
            ),
        ):
            st.session_state.metricmind_page = page_name
            st.rerun()

    st.markdown("""
    <div class="sidebar-footer">
        <h4>Data Platform</h4>
        <p>
            PostgreSQL → dbt<br>
            Cube → Python
        </p>
        <p>
            Your workspace for exploring performance
            and discovering business insights.
        </p>
        <p><b>MetricMind · BI Engine</b></p>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.metricmind_page

st.markdown("""
<div class="hero">
    <h1>MetricMind BI Engine</h1>
    <p>Explore performance, understand trends, and turn business data
    into better decisions.</p>
</div>
""", unsafe_allow_html=True)


# ================= PAGE CONTENT =================

try:

    # ---------------- OVERVIEW ----------------
    if page == "Overview":
        section("Executive Overview")

        data = get_data(list(MEASURES.values()))

        if data:
            values = data[0]
            cols = st.columns(4)

            for col, name in zip(
                cols, ["Revenue", "Profit", "Orders", "Average Margin"]
            ):
                value = values.get(MEASURES[name])

                if value is None:
                    shown = "N/A"
                elif name in ("Revenue", "Profit"):
                    shown = money(value)
                elif name == "Average Margin":
                    shown = f"{float(value):.2f}"
                else:
                    shown = f"{float(value):,.0f}"

                col.metric(name, shown)

        section("Revenue and Profit Analysis")
        left, right = st.columns(2)

        with left:
            st.markdown("### Monthly Revenue Trend")

            monthly = get_data(
                [MEASURES["Revenue"]],
                time_dimensions=[{
                    "dimension": DATE_DIMENSION,
                    "granularity": "month",
                }],
            )
            df = pd.DataFrame(monthly)

            if not df.empty and DATE_DIMENSION in df:
                df = numeric(df, MEASURES["Revenue"])
                fig = px.line(
                    df,
                    x=DATE_DIMENSION,
                    y=MEASURES["Revenue"],
                    markers=True,
                    color_discrete_sequence=[COLORS[0]],
                    labels={
                        DATE_DIMENSION: "Month",
                        MEASURES["Revenue"]: "Revenue",
                    },
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=7))
                st.plotly_chart(
                    chart_layout(fig),
                    use_container_width=True,
                )
            else:
                st.info("No monthly revenue data available.")

        with right:
            st.markdown("### Revenue by Product Category")

            data = get_data(
                [MEASURES["Revenue"]],
                [DIMENSIONS["Product Category"]],
            )
            df = pd.DataFrame(data)

            if not df.empty:
                df = numeric(df, MEASURES["Revenue"])
                fig = px.pie(
                    df,
                    names=DIMENSIONS["Product Category"],
                    values=MEASURES["Revenue"],
                    hole=0.45,
                    color_discrete_sequence=COLORS,
                )
                fig.update_traces(
                    textinfo="percent+label",
                    textposition="inside",
                    textfont=dict(color="#FFFFFF", size=12),
                )
                fig.update_layout(
                    paper_bgcolor="#FFFFFF",
                    font=dict(color="#20392A", size=13),
                    height=380,
                    legend=dict(font=dict(color="#20392A")),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category revenue data available.")

        section("Profit by Country")

        data = get_data(
            [MEASURES["Profit"]],
            [DIMENSIONS["Country"]],
        )
        df = pd.DataFrame(data)

        if not df.empty:
            df = numeric(df, MEASURES["Profit"])
            df = df.sort_values(MEASURES["Profit"])

            fig = px.bar(
                df,
                x=MEASURES["Profit"],
                y=DIMENSIONS["Country"],
                orientation="h",
                color=DIMENSIONS["Country"],
                color_discrete_sequence=COLORS,
                labels={
                    MEASURES["Profit"]: "Profit",
                    DIMENSIONS["Country"]: "Country",
                },
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(
                chart_layout(fig, max(380, len(df) * 35)),
                use_container_width=True,
            )

            export = df.rename(columns={
                DIMENSIONS["Country"]: "Country",
                MEASURES["Profit"]: "Profit",
            })
            st.download_button(
                "Download Profit Report (CSV)",
                export.to_csv(index=False).encode("utf-8"),
                "metricmind_profit_report.csv",
                "text/csv",
            )

    # ---------------- EXPLORE DATA ----------------
    elif page == "Explore Data":
        section("Interactive Data Explorer")

        left, right = st.columns(2)

        with left:
            metric = st.selectbox(
                "Select Business Metric",
                list(MEASURES.keys()),
            )

        with right:
            dimension = st.selectbox(
                "Group Results By",
                list(DIMENSIONS.keys()),
            )

        data = get_data([MEASURES[metric]], [DIMENSIONS[dimension]])
        df = pd.DataFrame(data)

        if not df.empty:
            metric_col = MEASURES[metric]
            dimension_col = DIMENSIONS[dimension]

            df = numeric(df, metric_col)
            df = df.sort_values(metric_col, ascending=False)

            shown = df.rename(columns={
                dimension_col: dimension,
                metric_col: metric,
            })

            section("Data Results")
            st.dataframe(
                shown,
                use_container_width=True,
                hide_index=True,
            )

            section("Visualization Settings")
            chart = st.selectbox(
                "Choose Chart Type",
                ["Bar Chart", "Line Chart", "Pie Chart", "Area Chart"],
            )

            labels = {
                dimension_col: dimension,
                metric_col: metric,
            }

            if chart == "Bar Chart":
                fig = px.bar(
                    df,
                    x=dimension_col,
                    y=metric_col,
                    color=dimension_col,
                    color_discrete_sequence=COLORS,
                    labels=labels,
                )
                fig.update_layout(showlegend=False)

            elif chart == "Line Chart":
                fig = px.line(
                    df,
                    x=dimension_col,
                    y=metric_col,
                    markers=True,
                    color_discrete_sequence=[COLORS[0]],
                    labels=labels,
                )
                fig.update_traces(line=dict(width=3))

            elif chart == "Area Chart":
                fig = px.area(
                    df,
                    x=dimension_col,
                    y=metric_col,
                    color_discrete_sequence=[COLORS[2]],
                    labels=labels,
                )

            else:
                fig = px.pie(
                    df,
                    names=dimension_col,
                    values=metric_col,
                    hole=0.4,
                    color_discrete_sequence=COLORS,
                )
                fig.update_traces(
                    textinfo="percent+label",
                    textposition="inside",
                    textfont=dict(color="#FFFFFF"),
                )

            st.plotly_chart(
                chart_layout(fig),
                use_container_width=True,
            )

            st.download_button(
                "Download Current Data (CSV)",
                shown.to_csv(index=False).encode("utf-8"),
                "metricmind_data.csv",
                "text/csv",
            )
        else:
            st.info("No data found for this selection.")

    # ---------------- ASK METRICMIND ----------------
    elif page == "Ask MetricMind":
        section("Ask MetricMind")
        st.write("Ask a business question in plain English.")

        examples = [
            "What is our total revenue?",
            "What is our total profit?",
            "How many orders do we have?",
            "Show revenue by country",
            "Show profit by category",
        ]

        st.markdown("### Try a suggested question")
        cols = st.columns(2)

        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(
                    example,
                    key=f"example_{i}",
                    use_container_width=True,
                ):
                    st.session_state.ask_question = example

        # Separate input widget from the form to avoid stale values.
        question = st.text_input(
            "Your Business Question",
            key="ask_question",
            placeholder="Example: Show revenue by country",
        )

        submitted = st.button(
            "Analyze Question",
            key="analyze_question",
            use_container_width=False,
        )

        if submitted:
            if not question.strip():
                st.warning("Type a business question before analyzing.")
            else:
                try:
                    from ai_agent import ask_metricmind

                    with st.spinner("Analyzing your question..."):
                        answer = ask_metricmind(question.strip())

                    st.markdown("""
                    <div class="answer-card">
                        <div class="answer-title">MetricMind Insights</div>
                        <div class="answer-subtitle">
                            Results based on your business data
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    display_answer(answer)

                except requests.RequestException:
                    st.error(
                        "Could not reach Cube. Make sure Cube is running "
                        "at http://localhost:4000."
                    )
                except Exception as error:
                    st.error("Unable to analyze this question.")
                    st.code(str(error))

        st.caption(
            "The current Python assistant uses predefined question patterns."
        )

    # ---------------- DATA TABLE ----------------
    elif page == "Data Table":
        section("Business Data Table")
        st.write("View, search, and download your business data.")

        left, right = st.columns(2)

        with left:
            metric = st.selectbox(
                "Metric",
                list(MEASURES.keys()),
                key="table_metric",
            )

        with right:
            dimension = st.selectbox(
                "Group By",
                list(DIMENSIONS.keys()),
                key="table_dimension",
            )

        data = get_data(
            [MEASURES[metric]],
            [DIMENSIONS[dimension]],
        )
        df = pd.DataFrame(data)

        if not df.empty:
            df = df.rename(columns={
                DIMENSIONS[dimension]: dimension,
                MEASURES[metric]: metric,
            })

            st.markdown("### Find Data")
            search_col, clear_col = st.columns([5, 1])

            with search_col:
                search = st.text_input(
                    "Search",
                    placeholder=f"Type a {dimension.lower()} name or value...",
                    key="business_table_search",
                    label_visibility="collapsed",
                )

            with clear_col:
                if st.button(
                    "Clear Search",
                    use_container_width=True,
                    key="clear_table_search",
                ):
                    st.session_state.business_table_search = ""
                    st.rerun()

            if search.strip():
                mask = df.astype(str).apply(
                    lambda column: column.str.contains(
                        search.strip(),
                        case=False,
                        na=False,
                        regex=False,
                    )
                ).any(axis=1)
                filtered = df[mask].copy()
            else:
                filtered = df.copy()

            st.markdown("### Results")
            st.caption(
                f"{len(filtered)} results found out of {len(df)} total rows."
            )

            if filtered.empty:
                st.info(
                    "No matching results. Try another search or clear "
                    "the search box to see all data."
                )
            else:
                st.dataframe(
                    filtered,
                    use_container_width=True,
                    hide_index=True,
                )

            st.download_button(
                "Export Results to CSV",
                data=filtered.to_csv(index=False).encode("utf-8"),
                file_name="metricmind_business_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No data available for this selection.")

except requests.RequestException as error:
    st.error(
        "Cannot connect to Cube. Make sure Cube is running at "
        "http://localhost:4000."
    )
    st.code(str(error))

except Exception as error:
    st.error("MetricMind encountered an error.")
    st.code(str(error))
