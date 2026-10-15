
import json
import re
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# METRICMIND CONFIGURATION
# =====================================================

CUBE_URL = "http://localhost:4000/cubejs-api/v1/load"
CUBE = "metricmind_sales"

st.set_page_config(
    page_title="MetricMind | BI Engine",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

DATE = f"{CUBE}.order_date"

COLORS = [
    "#4776A8", "#F28E2B", "#45A765", "#D9535D",
    "#A77BA8", "#61AAA3", "#D6B83F", "#E58DAD",
    "#9B7967", "#7773C8",
]

PAGES = ["Overview", "Explore Data", "Ask MetricMind", "Data Table"]


# =====================================================
# CUSTOM THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #F5FAF6 !important;
    color: #20392A !important;
}

.block-container {
    max-width: 1600px;
    padding: 1.5rem 2rem 3rem;
}

h1, h2, h3, h4 {
    color: #174D32 !important;
    font-weight: 850 !important;
}

p, label, li {
    color: #20392A;
}

/* SIDEBAR */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #D5E7D9;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p {
    color: #174D32 !important;
}

.brand-card {
    background: linear-gradient(135deg, #174D32, #45A765);
    border-radius: 18px;
    padding: 22px 17px;
    margin: 8px 0 24px;
}

.brand-card h2 {
    color: #FFFFFF !important;
    font-size: 27px !important;
    margin-bottom: 5px;
}

.brand-card p {
    color: #FFFFFF !important;
    font-size: 12px;
    letter-spacing: 1px;
}

.sidebar-note {
    background: #EFF8F1;
    border: 1px solid #D5E7D9;
    border-radius: 14px;
    padding: 15px;
    margin-top: 22px;
}

.sidebar-note p {
    color: #52685A !important;
    font-size: 13px;
    line-height: 1.7;
}

/* HEADER */
.hero {
    background: linear-gradient(115deg, #174D32, #23864B, #55A96E);
    padding: 27px 30px;
    border-radius: 19px;
    margin-bottom: 22px;
    box-shadow: 0 7px 22px rgba(23,77,50,.09);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 2.15rem !important;
    margin: 0;
}

.hero p {
    color: #FFFFFF !important;
    margin: 8px 0 0;
}

/* KPI CARDS */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E7D9;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 13px rgba(23,77,50,.04);
}

div[data-testid="stMetricLabel"] {
    color: #52685A !important;
    font-weight: 750 !important;
}

div[data-testid="stMetricValue"] {
    color: #23864B !important;
    font-weight: 850 !important;
}

/* INPUTS AND DROPDOWNS */
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label,
[data-testid="stMultiSelect"] label {
    color: #174D32 !important;
    font-weight: 800 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #174D32 !important;
    border: 1px solid #A9D4B5 !important;
    border-radius: 11px !important;
    min-height: 44px;
}

[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #174D32 !important;
    -webkit-text-fill-color: #174D32 !important;
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

[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: #173D29 !important;
    -webkit-text-fill-color: #173D29 !important;
    caret-color: #23864B !important;
    border: 1.5px solid #8BC69D !important;
    border-radius: 11px !important;
    min-height: 46px;
    font-size: 16px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #63796A !important;
    -webkit-text-fill-color: #63796A !important;
    opacity: 1 !important;
}

/* BUTTONS */
.stButton > button,
.stFormSubmitButton > button {
    background: #23864B !important;
    color: #FFFFFF !important;
    border: 1px solid #23864B !important;
    border-radius: 11px !important;
    min-height: 43px;
    font-weight: 800 !important;
}

.stButton > button p,
.stFormSubmitButton > button p {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #174D32 !important;
}

[data-testid="stDownloadButton"] button {
    background: #DDF5E3 !important;
    color: #174D32 !important;
    border: 1px solid #A9D4B5 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

[data-testid="stDownloadButton"] button p {
    color: #174D32 !important;
}

/* CHARTS AND TABLES */
[data-testid="stPlotlyChart"],
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E7D9;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-color: #D5E7D9 !important;
    border-radius: 16px;
}

.section-title {
    color: #174D32;
    font-size: 1.6rem;
    font-weight: 900;
    margin: 23px 0 13px;
}

/* ANSWER PANEL */
.answer-card {
    background: linear-gradient(135deg, #FFFFFF, #EAF7ED);
    border: 1px solid #B9DEC4;
    border-left: 6px solid #23864B;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}

.answer-card h3 {
    color: #174D32 !important;
    margin: 0 0 6px;
}

.answer-card p {
    color: #52685A !important;
    margin: 0;
}

.footer {
    color: #63796A;
    font-size: 12px;
    text-align: center;
    padding-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

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


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )


def to_numeric(df, column):
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def fmt(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return "N/A"


def style_chart(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial", color="#20392A", size=13),
        colorway=COLORS,
        height=height,
        margin=dict(l=25, r=25, t=40, b=35),
        legend=dict(
            bgcolor="#FFFFFF",
            font=dict(color="#20392A", size=12),
        ),
    )

    fig.update_xaxes(
        color="#20392A",
        tickfont=dict(color="#20392A", size=12),
        title_font=dict(color="#174D32"),
        gridcolor="#E1EBE4",
        linecolor="#CBDACF",
    )

    fig.update_yaxes(
        color="#20392A",
        tickfont=dict(color="#20392A", size=12),
        title_font=dict(color="#174D32"),
        gridcolor="#E1EBE4",
        linecolor="#CBDACF",
    )

    return fig


def csv_download(df, filename, label="Download CSV"):
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
    )


def show_answer(answer):
    st.markdown("""
    <div class="answer-card">
        <h3>MetricMind Insights</h3>
        <p>Results from your business data</p>
    </div>
    """, unsafe_allow_html=True)

    text = str(answer).strip()

    # Format common grouped responses as a readable table.
    if ":" in text:
        title, remainder = text.split(":", 1)

        pattern = (
            r"([A-Za-z][A-Za-z0-9 &()_./-]*?):\s*"
            r"(-?\d[\d,]*(?:\.\d+)?)"
        )

        matches = list(re.finditer(pattern, remainder))

        if matches:
            st.markdown(f"**{title.strip()}**")

            result_df = pd.DataFrame([
                {
                    "Group": match.group(1).strip(),
                    "Value": match.group(2),
                }
                for match in matches
            ])

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True,
            )
            return

    st.markdown(text.replace("\n", "  \n"))


def month_label(value):
    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return str(value)

    return parsed.strftime("%b %Y")


def get_monthly_revenue():
    rows = get_data(
        [MEASURES["Revenue"]],
        time_dimensions=[{
            "dimension": DATE,
            "granularity": "month",
        }],
    )

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Cube commonly returns keys ending in ".month".
    date_col = next(
        (
            column for column in df.columns
            if column.startswith(DATE)
        ),
        None,
    )

    revenue_col = MEASURES["Revenue"]

    if not date_col or revenue_col not in df.columns:
        return pd.DataFrame()

    df["Month"] = df[date_col].apply(month_label)
    df["Revenue"] = pd.to_numeric(
        df[revenue_col], errors="coerce"
    )

    df = df.dropna(subset=["Revenue"])

    return df[["Month", "Revenue"]]


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>MetricMind</h1>
    <p>Business Intelligence Engine | Explore. Analyze. Decide.</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR ONLY NAVIGATION
# No extra horizontal navigation bar
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <h2>MetricMind</h2>
        <p>BUSINESS INTELLIGENCE ENGINE</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### NAVIGATION")

    for page_name in PAGES:
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page_name
                else "secondary"
            ),
        ):
            st.session_state.page = page_name
            st.rerun()

    st.markdown("""
    <div class="sidebar-note">
        <h4>MetricMind Workspace</h4>
        <p>
            Explore business performance, compare metrics,
            ask questions and export results.
        </p>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page


# =====================================================
# APPLICATION PAGES
# =====================================================

try:

    # -------------------------------------------------
    # OVERVIEW
    # -------------------------------------------------

    if page == "Overview":
        section("Executive Overview")

        rows = get_data(list(MEASURES.values()))

        if rows:
            values = rows[0]
            cols = st.columns(4)

            for col, name in zip(
                cols,
                ["Revenue", "Profit", "Orders", "Average Margin"],
            ):
                value = values.get(MEASURES[name])

                if name == "Orders":
                    try:
                        display = f"{float(value):,.0f}"
                    except (ValueError, TypeError):
                        display = "N/A"
                else:
                    display = fmt(value)

                col.metric(name, display)

        section("Business Performance")

        left, right = st.columns(2)

        with left:
            st.markdown("### Monthly Revenue Trend")

            monthly_df = get_monthly_revenue()

            if not monthly_df.empty:
                st.dataframe(
                    monthly_df,
                    use_container_width=True,
                    hide_index=True,
                )

                fig = px.line(
                    monthly_df,
                    x="Month",
                    y="Revenue",
                    markers=True,
                    color_discrete_sequence=[COLORS[2]],
                )
                fig.update_traces(
                    line=dict(width=3),
                    marker=dict(size=8),
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )
            else:
                st.info(
                    "No monthly results returned. "
                    "Check the order-date dimension in Cube."
                )

        with right:
            st.markdown("### Revenue by Product Category")

            rows = get_data(
                [MEASURES["Revenue"]],
                [DIMENSIONS["Product Category"]],
            )

            df = pd.DataFrame(rows)

            if not df.empty:
                df = to_numeric(df, MEASURES["Revenue"])

                fig = px.pie(
                    df,
                    names=DIMENSIONS["Product Category"],
                    values=MEASURES["Revenue"],
                    hole=0.42,
                    color_discrete_sequence=COLORS,
                )

                fig.update_traces(
                    textinfo="percent+label",
                    textposition="inside",
                    textfont=dict(color="#FFFFFF", size=12),
                    marker=dict(
                        line=dict(color="#FFFFFF", width=2)
                    ),
                )

                st.plotly_chart(
                    style_chart(fig, 400),
                    use_container_width=True,
                )

        section("Profit by Country")

        rows = get_data(
            [MEASURES["Profit"]],
            [DIMENSIONS["Country"]],
        )

        df = pd.DataFrame(rows)

        if not df.empty:
            df = to_numeric(df, MEASURES["Profit"])
            df = df.sort_values(MEASURES["Profit"])

            fig = px.bar(
                df,
                x=MEASURES["Profit"],
                y=DIMENSIONS["Country"],
                orientation="h",
                color=DIMENSIONS["Country"],
                color_discrete_sequence=COLORS,
            )
            fig.update_layout(showlegend=False)

            st.plotly_chart(
                style_chart(fig, max(380, len(df) * 35)),
                use_container_width=True,
            )

            csv_download(
                df,
                "metricmind_profit.csv",
                "Download Profit Report",
            )


    # -------------------------------------------------
    # EXPLORE DATA
    # -------------------------------------------------

    elif page == "Explore Data":
        section("Interactive Data Explorer")

        st.write(
            "Compare business metrics, discover top performers "
            "and visualize your data in different ways."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            metric = st.selectbox(
                "Select Business Metric",
                list(MEASURES.keys()),
            )

        with col2:
            dimension = st.selectbox(
                "Group Results By",
                list(DIMENSIONS.keys()),
            )

        with col3:
            chart_type = st.selectbox(
                "Visualization",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Area Chart",
                    "Pie Chart",
                    "Donut Chart",
                ],
            )

        rows = get_data(
            [MEASURES[metric]],
            [DIMENSIONS[dimension]],
        )

        df = pd.DataFrame(rows)

        if not df.empty:
            metric_col = MEASURES[metric]
            dim_col = DIMENSIONS[dimension]

            df = to_numeric(df, metric_col)
            df = df.dropna(subset=[metric_col])
            df = df.sort_values(metric_col, ascending=False)

            if df.empty:
                st.info("No numeric results are available.")
            else:
                section("Quick Insights")

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    f"Total {metric}",
                    fmt(df[metric_col].sum()),
                )
                c2.metric(
                    f"Average {metric}",
                    fmt(df[metric_col].mean()),
                )
                c3.metric(
                    "Top Performer",
                    str(df.iloc[0][dim_col]),
                )
                c4.metric(
                    "Lowest Performer",
                    str(df.iloc[-1][dim_col]),
                )

                section("Primary Analysis")

                if chart_type == "Bar Chart":
                    fig = px.bar(
                        df,
                        x=dim_col,
                        y=metric_col,
                        color=dim_col,
                        text_auto=".2s",
                        color_discrete_sequence=COLORS,
                    )
                    fig.update_layout(showlegend=False)

                elif chart_type == "Line Chart":
                    fig = px.line(
                        df,
                        x=dim_col,
                        y=metric_col,
                        markers=True,
                        color_discrete_sequence=[COLORS[0]],
                    )
                    fig.update_traces(
                        line=dict(width=3),
                        marker=dict(size=8),
                    )

                elif chart_type == "Area Chart":
                    fig = px.area(
                        df,
                        x=dim_col,
                        y=metric_col,
                        color_discrete_sequence=[COLORS[2]],
                    )

                else:
                    fig = px.pie(
                        df,
                        names=dim_col,
                        values=metric_col,
                        hole=0.48 if chart_type == "Donut Chart" else 0,
                        color_discrete_sequence=COLORS,
                    )
                    fig.update_traces(
                        textinfo="percent+label",
                        textposition="inside",
                        textfont=dict(color="#FFFFFF", size=12),
                        marker=dict(
                            line=dict(color="#FFFFFF", width=2)
                        ),
                    )

                st.plotly_chart(
                    style_chart(fig, 450),
                    use_container_width=True,
                )

                section("Performance Comparison")

                left, right = st.columns(2)

                with left:
                    st.markdown("### Top Five Performers")

                    top_df = df.head(5).sort_values(metric_col)

                    fig = px.bar(
                        top_df,
                        x=metric_col,
                        y=dim_col,
                        orientation="h",
                        color=dim_col,
                        text_auto=".2s",
                        color_discrete_sequence=COLORS,
                    )
                    fig.update_layout(showlegend=False)

                    st.plotly_chart(
                        style_chart(fig, 320),
                        use_container_width=True,
                    )

                with right:
                    st.markdown("### Value Distribution")

                    fig = px.histogram(
                        df,
                        x=metric_col,
                        nbins=min(10, max(3, len(df))),
                        color_discrete_sequence=[COLORS[1]],
                    )

                    st.plotly_chart(
                        style_chart(fig, 320),
                        use_container_width=True,
                    )

                section("Detailed Results")

                search = st.text_input(
                    "Search Results",
                    placeholder=f"Search {dimension.lower()}...",
                    key="explore_search",
                )

                view_df = df.copy()

                if search.strip():
                    mask = view_df[dim_col].astype(str).str.contains(
                        search.strip(),
                        case=False,
                        na=False,
                        regex=False,
                    )
                    view_df = view_df[mask]

                display_df = view_df.rename(columns={
                    dim_col: dimension,
                    metric_col: metric,
                })

                st.caption(
                    f"Showing {len(display_df)} of {len(df)} rows"
                )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                )

                csv_download(
                    display_df,
                    "metricmind_exploration.csv",
                    "Download Exploration Results",
                )

                section("Additional Metric Comparison")

                other_metrics = [
                    name for name in MEASURES if name != metric
                ]

                extra_metrics = st.multiselect(
                    "Choose additional metrics",
                    other_metrics,
                    default=[
                        "Profit" if metric != "Profit" else "Revenue"
                    ],
                )

                if extra_metrics:
                    extra_rows = get_data(
                        [MEASURES[name] for name in extra_metrics],
                        [dim_col],
                    )

                    extra_df = pd.DataFrame(extra_rows)

                    if not extra_df.empty:
                        rename_map = {dim_col: dimension}

                        for name in extra_metrics:
                            rename_map[MEASURES[name]] = name

                        extra_df = extra_df.rename(
                            columns=rename_map
                        )

                        for name in extra_metrics:
                            extra_df = to_numeric(extra_df, name)

                        st.dataframe(
                            extra_df,
                            use_container_width=True,
                            hide_index=True,
                        )

                        fig = px.bar(
                            extra_df,
                            x=dimension,
                            y=extra_metrics,
                            barmode="group",
                            color_discrete_sequence=COLORS,
                        )

                        st.plotly_chart(
                            style_chart(fig, 380),
                            use_container_width=True,
                        )

        else:
            st.info("No data is available for this selection.")


    # -------------------------------------------------
    # ASK METRICMIND
    # -------------------------------------------------

    elif page == "Ask MetricMind":
        section("Ask MetricMind")

        st.write(
            "Ask a question about your business data in plain English."
        )

        examples = [
            "What is our total revenue?",
            "What is our total profit?",
            "How many orders do we have?",
            "Show revenue by country",
            "Show profit by category",
            "Show monthly revenue",
        ]

        section("Suggested Questions")

        cols = st.columns(2)

        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(
                    example,
                    key=f"ask_example_{i}",
                    use_container_width=True,
                ):
                    st.session_state.ask_question = example

        question = st.text_input(
            "Your Business Question",
            key="ask_question",
            placeholder="Example: Show revenue by country",
        )

        if st.button(
            "Analyze Question",
            key="analyze_question",
        ):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                try:
                    from ai_agent import ask_metricmind

                    with st.spinner("Analyzing your question..."):
                        answer = ask_metricmind(question.strip())

                    show_answer(answer)

                except requests.RequestException:
                    st.error(
                        "Cannot connect to Cube. "
                        "Check that Cube is running."
                    )

                except Exception as error:
                    st.error("Could not analyze this question.")
                    st.code(str(error))

        st.caption(
            "Answers depend on the metrics and question patterns "
            "currently supported by the Python assistant."
        )


    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------

    elif page == "Data Table":
        section("Business Data Table")

        st.write(
            "Search, inspect and export grouped business results."
        )

        col1, col2 = st.columns(2)

        with col1:
            metric = st.selectbox(
                "Select Metric",
                list(MEASURES.keys()),
                key="table_metric",
            )

        with col2:
            dimension = st.selectbox(
                "Group By",
                list(DIMENSIONS.keys()),
                key="table_dimension",
            )

        rows = get_data(
            [MEASURES[metric]],
            [DIMENSIONS[dimension]],
        )

        df = pd.DataFrame(rows)

        if not df.empty:
            df = df.rename(columns={
                DIMENSIONS[dimension]: dimension,
                MEASURES[metric]: metric,
            })

            search = st.text_input(
                "Search Table",
                placeholder="Search by country, category or value...",
                key="table_search",
            )

            if search.strip():
                mask = df.astype(str).apply(
                    lambda col: col.str.contains(
                        search.strip(),
                        case=False,
                        na=False,
                        regex=False,
                    )
                ).any(axis=1)

                df = df[mask].copy()

            st.caption(f"{len(df)} matching rows")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            csv_download(
                df,
                "metricmind_data.csv",
                "Export Table to CSV",
            )

        else:
            st.info("No data is available for this selection.")


except requests.RequestException as error:
    st.error(
        "Cannot connect to Cube. Start Cube and try again."
    )
    st.code(str(error))

except Exception as error:
    st.error("MetricMind encountered an error.")
    st.code(str(error))

st.markdown("""
<div class="footer">
    METRICMIND | BUSINESS INTELLIGENCE ENGINE
</div>
""", unsafe_allow_html=True)
