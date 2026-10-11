
import requests
import json

CUBE_URL = "http://localhost:4000/cubejs-api/v1/load"

MEASURES = {
    "revenue": "metricmind_sales.total_revenue",
    "profit": "metricmind_sales.total_profit",
    "orders": "metricmind_sales.total_orders",
    "margin": "metricmind_sales.average_margin",
    "quantity": "metricmind_sales.total_quantity",
}


def ask_metricmind(question):
    question = question.lower()

    if "revenue" in question or "sales" in question:
        measure = MEASURES["revenue"]
    elif "profit" in question:
        measure = MEASURES["profit"]
    elif "order" in question:
        measure = MEASURES["orders"]
    elif "margin" in question:
        measure = MEASURES["margin"]
    elif "quantity" in question:
        measure = MEASURES["quantity"]
    else:
        return "Ask about revenue, profit, orders, margin, or quantity."

    if "country" in question:
        dimension = "metricmind_sales.country"
    elif "category" in question:
        dimension = "metricmind_sales.product_category"
    else:
        dimension = None

    if dimension:
        query = {
            "measures": [measure],
            "dimensions": [dimension]
        }
    else:
        query = {"measures": [measure]}

    try:
        response = requests.get(
            CUBE_URL,
            params={"query": json.dumps(query)},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if dimension:
            rows = data["data"]
            return "\n".join(
                f"{row[dimension]}: {row[measure]}"
                for row in rows
            )

        value = data["data"][0][measure]
        return f"Result: {value}"

    except (requests.RequestException, KeyError, IndexError) as error:
        return f"Could not retrieve results: {error}"


if __name__ == "__main__":
    print("MetricMind Business Assistant")
    while True:
        question = input("\nAsk a business question (or type exit): ")
        if question.lower() == "exit":
            break
        print(ask_metricmind(question))
