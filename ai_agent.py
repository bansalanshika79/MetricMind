
import json
import requests

CUBE_URL = "http://localhost:4000/cubejs-api/v1/load"
CUBE = "metricmind_sales"

MEASURES = {
    "revenue": f"{CUBE}.total_revenue",
    "profit": f"{CUBE}.total_profit",
    "orders": f"{CUBE}.total_orders",
    "margin": f"{CUBE}.average_margin",
    "quantity": f"{CUBE}.total_quantity",
}

DIMENSIONS = {
    "country": f"{CUBE}.country",
    "category": f"{CUBE}.product_category",
    "brand": f"{CUBE}.brand",
    "segment": f"{CUBE}.customer_segment",
    "membership": f"{CUBE}.membership_status",
}

DATE = f"{CUBE}.order_date"


def run_query(measures, dimensions=None, time_dimensions=None, order=None):
    query = {"measures": measures}

    if dimensions:
        query["dimensions"] = dimensions

    if time_dimensions:
        query["timeDimensions"] = time_dimensions

    if order:
        query["order"] = order

    response = requests.get(
        CUBE_URL,
        params={"query": json.dumps(query)},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("data", [])


def number(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def format_number(value):
    return f"{value:,.2f}"


def ask_metricmind(question):
    q = question.lower().strip()

    if not q:
        return "Please enter a business question."

    # Identify the metric
    if any(word in q for word in ["margin", "profitability"]):
        metric = "margin" if "margin" in q else "profit"
    elif any(word in q for word in ["profit", "profitable"]):
        metric = "profit"
    elif any(word in q for word in ["order", "orders"]):
        metric = "orders"
    elif any(word in q for word in ["quantity", "units", "items sold"]):
        metric = "quantity"
    elif any(word in q for word in [
        "revenue", "sales", "selling", "turnover"
    ]):
        metric = "revenue"
    else:
        return (
            "I couldn't identify the metric. Try asking about "
            "sales, revenue, profit, orders, margin, or quantity."
        )

    # Identify grouping
    dimension_name = None

    if any(word in q for word in ["country", "countries", "nation"]):
        dimension_name = "country"
    elif any(word in q for word in ["category", "categories"]):
        dimension_name = "category"
    elif "brand" in q:
        dimension_name = "brand"
    elif any(word in q for word in ["segment", "customer group"]):
        dimension_name = "segment"
    elif "membership" in q:
        dimension_name = "membership"

    # Detect average, ranking, and time trends
    average = any(word in q.split() for word in ["average", "avg", "mean"])
    highest = any(word in q for word in [
        "highest", "top", "best", "maximum", "most"
    ])
    lowest = any(word in q for word in [
        "lowest", "bottom", "worst", "minimum", "least"
    ])
    monthly = any(word in q for word in [
        "monthly", "month", "trend", "over time"
    ])

    # Calculate average sales as revenue divided by order count.
    # This is average revenue per order, not average line-item value.
    if average and metric == "revenue":
        measures = [
            MEASURES["revenue"],
            MEASURES["orders"],
        ]
        dimensions = (
            [DIMENSIONS[dimension_name]]
            if dimension_name else None
        )

        data = run_query(measures, dimensions)

        if not data:
            return "No data was returned."

        results = []

        for row in data:
            revenue = number(row.get(MEASURES["revenue"]))
            orders = number(row.get(MEASURES["orders"]))
            average_sales = revenue / orders if orders else 0

            if dimension_name:
                label = row.get(
                    DIMENSIONS[dimension_name], "Unknown"
                )
                results.append({
                    "label": label,
                    "value": average_sales,
                })
            else:
                return (
                    "Average sales per order: "
                    f"{format_number(average_sales)} "
                    f"(Revenue: {format_number(revenue)}, "
                    f"Orders: {orders:,.0f})"
                )

        results.sort(key=lambda item: item["value"], reverse=True)

        if highest:
            results = results[:1]
        elif lowest:
            results = results[-1:]

        title = "Average Revenue per Order"
        return title + ":\n" + "\n".join(
            f"{item['label']}: {format_number(item['value'])}"
            for item in results
        )

    # Prepare normal metric query
    measure = MEASURES[metric]
    measures = [measure]
    dimensions = (
        [DIMENSIONS[dimension_name]]
        if dimension_name else None
    )
    time_dimensions = None

    if monthly:
        dimensions = None
        time_dimensions = [{
            "dimension": DATE,
            "granularity": "month",
        }]

    order = None

    if dimensions and (highest or lowest):
        order = {
            measure: "desc" if highest else "asc"
        }

    data = run_query(
        measures,
        dimensions,
        time_dimensions,
        order,
    )

    if not data:
        return "No results found for this question."

    metric_label = {
        "revenue": "Revenue",
        "profit": "Profit",
        "orders": "Orders",
        "margin": "Average Margin",
        "quantity": "Quantity",
    }[metric]

    # Overall total
    if not dimensions and not time_dimensions:
        value = number(data[0].get(measure))
        return f"Total {metric_label}: {format_number(value)}"

    # Grouped results
    if dimensions:
        results = []

        for row in data:
            label = row.get(DIMENSIONS[dimension_name], "Unknown")
            value = number(row.get(measure))
            results.append((label, value))

        results.sort(key=lambda item: item[1], reverse=True)

        if highest:
            results = results[:1]
        elif lowest:
            results = results[:1] if not order else results[:1]

        title = f"{metric_label} by {dimension_name.title()}"

        if highest:
            title = f"Highest {metric_label}"
        elif lowest:
            title = f"Lowest {metric_label}"

        return title + ":\n" + "\n".join(
            f"{label}: {format_number(value)}"
            for label, value in results
        )

    # Monthly results
    if time_dimensions:
        date_key = DATE + ".month"
        results = []

        for row in data:
            label = row.get(date_key, "Unknown")
            value = number(row.get(measure))
            results.append((label, value))

        return f"Monthly {metric_label}:\n" + "\n".join(
            f"{label}: {format_number(value)}"
            for label, value in results
        )

    return "I couldn't generate a result for that question."


if __name__ == "__main__":
    print("MetricMind Business Assistant")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a business question: ")

        if question.strip().lower() == "exit":
            break

        try:
            print(ask_metricmind(question))
        except requests.RequestException as error:
            print(f"Cube connection error: {error}")
