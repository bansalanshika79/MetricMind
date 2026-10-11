
import requests

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
        return "Try asking about revenue, profit, orders, margin, or quantity."

    query = {"measures": [measure]}

    
    try:
        response = requests.get(
            CUBE_URL,
            params={"query": __import__("json").dumps(query)},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        value = data["data"][0][measure]
        return f"Total Revenue: {value}"

    except requests.RequestException as error:
        return f"Could not connect to Cube: {error}"

    

if __name__ == "__main__":
    print("MetricMind Business Assistant")
    while True:
        question = input("\nAsk a business question (or type exit): ")
        if question.lower() == "exit":
            break
        print(ask_metricmind(question))
