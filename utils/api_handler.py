# ==========================================
# API Handler Module
# Part 3 – API Integration
# ==========================================

import requests


# ---------------- TASK 3.1 (a) ----------------
# Fetch ALL products

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("API request failed")
            return []

        data = response.json()
        print("✓ Products fetched from API")
        return data.get("products", [])

    except Exception as e:
        print("Error calling API:", e)
        return []


# ---------------- TASK 3.1 (b) ----------------
# Create product mapping

def create_product_mapping(api_products):
    """
    Maps ProductID to API details
    Returns: dictionary
    """

    mapping = {}

    for p in api_products:
        pid = f"P{p['id']}"   # Convert 1 → P1

        mapping[pid] = {
            'category': p.get('category'),
            'brand': p.get('brand'),
            'rating': p.get('rating')
        }

    return mapping


# ---------------- TASK 3.2 (a) ----------------
# Enrich sales data

def enrich_sales_data(transactions, product_mapping):
    """
    Adds API info to transactions
    """

    enriched = []

    for tx in transactions:
        pid = tx['ProductID']
        tx_copy = tx.copy()

        if pid in product_mapping:
            api = product_mapping[pid]

            tx_copy['API_Category'] = api['category']
            tx_copy['API_Brand'] = api['brand']
            tx_copy['API_Rating'] = api['rating']
            tx_copy['API_Match'] = True
        else:
            tx_copy['API_Category'] = None
            tx_copy['API_Brand'] = None
            tx_copy['API_Rating'] = None
            tx_copy['API_Match'] = False

        enriched.append(tx_copy)

    return enriched


# ---------------- TASK 3.2 (b) ----------------
# Save enriched data (PIPE format)

def save_enriched_data(enriched,
                       filename="data/enriched_sales_data.txt"):

    headers = [
        "TransactionID","Date","ProductID","ProductName",
        "Quantity","UnitPrice","CustomerID","Region",
        "API_Category","API_Brand","API_Rating","API_Match"
    ]

    with open(filename, "w") as f:

        f.write("|".join(headers) + "\n")

        for tx in enriched:
            row = [
                str(tx.get("TransactionID")),
                str(tx.get("Date")),
                str(tx.get("ProductID")),
                str(tx.get("ProductName")),
                str(tx.get("Quantity")),
                str(tx.get("UnitPrice")),
                str(tx.get("CustomerID")),
                str(tx.get("Region")),
                str(tx.get("API_Category")),
                str(tx.get("API_Brand")),
                str(tx.get("API_Rating")),
                str(tx.get("API_Match"))
            ]

            f.write("|".join(row) + "\n")

    print("✓ Enriched data saved:", filename)
