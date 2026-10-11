
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
    "date": f"{CUBE}.order_date",
}


def ask_metricmind(question):
    question = question.lower().strip()

    # Identify the business metric
    if "revenue" in question or "sales" in question:
        measure = MEASURES["revenue"]
        metric_name = "Revenue"

    elif "profit" in question:
        measure = MEASURES["profit"]
        metric_name = "Profit"

    elif "order" in question:
        measure = MEASURES["orders"]
        metric_name = "Orders"

    elif "margin" in question:
        measure = MEASURES["margin"]
        metric_name = "Average Margin"

    elif "quantity" in question:
        measure = MEASURES["quantity"]
        metric_name = "Quantity"

    else:
        return (
            "Try asking about revenue, profit, orders, "
            "margin, or quantity."
        )

    # Identify the grouping dimension
    if "country" in question:
        dimension = DIMENSIONS["country"]
        group_name = "Country"

    elif "category" in question:
        dimension = DIMENSIONS["category"]
        group_name = "Product Category"

    elif any(word in question for word in ["monthly", "month", "trend"]):
        dimension = DIMENSIONS["date"]
        group_name = "Month"

    else:
        dimension = None
        group_name = None

    # Build the Cube query
    query = {"measures": [measure]}

    if dimension:
        query["dimensions"] = [dimension]

    # Request results from Cube
    try:
        response = requests.get(
            CUBE_URL,
            params={"query": json.dumps(query)},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()["data"]

        if not data:
            return "No results found."

        if dimension:
            results = []

            for row in data:
                label = row.get(dimension, "Unknown")
                value = row.get(measure, "N/A")
                results.append(f"{label}: {value}")

            return f"{metric_name} by {group_name}:\n" + "\n".join(results)

        value = data[0].get(measure, "N/A")
        return f"Total {metric_name}: {value}"

    except (requests.RequestException, KeyError, IndexError) as error:
        return f"Could not retrieve results: {error}"


if __name__ == "__main__":
    print("=== MetricMind Business Assistant ===")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a business question: ")

        if question.lower().strip() == "exit":
            print("Goodbye!")
            break

        print(ask_metricmind(question))
