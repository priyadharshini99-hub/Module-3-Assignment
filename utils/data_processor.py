# ==========================================
# Data Processor Module
# Task 1.2 + Task 1.3 + Part 2 + Task 4.1
# ==========================================

from datetime import datetime
from collections import defaultdict


# =================================================
# TASK 1.2 – PARSE & CLEAN RAW DATA
# =================================================

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        # ---------- CLEANING ----------
        pname = pname.replace(',', '')
        qty = qty.replace(',', '')
        price = price.replace(',', '')

        try:
            qty = int(qty)
            price = float(price)
        except:
            continue

        record = {
            'TransactionID': tid,
            'Date': date,
            'ProductID': pid,
            'ProductName': pname,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cid,
            'Region': region
        }

        transactions.append(record)

    return transactions


# =================================================
# TASK 1.3 – VALIDATION & FILTERING
# =================================================

def validate_and_filter(transactions, region=None,
                        min_amount=None, max_amount=None):

    valid = []
    invalid = 0

    # ---------------- VALIDATION ----------------
    for tx in transactions:
        try:
            if tx['Quantity'] <= 0:
                raise
            if tx['UnitPrice'] <= 0:
                raise
            if not tx['TransactionID'].startswith('T'):
                raise
            if not tx['ProductID'].startswith('P'):
                raise
            if not tx['CustomerID'].startswith('C'):
                raise
            if not tx['Region']:
                raise
        except:
            invalid += 1
            continue

        valid.append(tx)

    total = len(transactions)

    # ---------------- SUMMARY OUTPUT ----------------
    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    # ---------------- DISPLAY OPTIONS ----------------
    regions = set(t['Region'] for t in valid)
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid]

    print("Available regions:", regions)
    print("Transaction amount range:",
          min(amounts), "to", max(amounts))

    # ---------------- FILTERING ----------------
    filtered = valid.copy()

    summary = {
        'total_input': total,
        'invalid': invalid
    }

    if region:
        filtered = [t for t in filtered if t['Region'] == region]
        print("After region filter:", len(filtered))
        summary['filtered_by_region'] = len(filtered)

    if min_amount:
        filtered = [t for t in filtered
                    if t['Quantity'] * t['UnitPrice'] >= min_amount]

    if max_amount:
        filtered = [t for t in filtered
                    if t['Quantity'] * t['UnitPrice'] <= max_amount]

    print("After amount filter:", len(filtered))

    summary['filtered_by_amount'] = len(filtered)
    summary['final_count'] = len(filtered)

    return filtered, invalid, summary


# =================================================
# PART 2 – DATA PROCESSING & ANALYTICS
# =================================================

def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx['Quantity'] * tx['UnitPrice']
    return round(total, 2)


def region_wise_sales(transactions):
    region_data = {}
    grand_total = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx['Region']
        amount = tx['Quantity'] * tx['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    for region in region_data:
        sales = region_data[region]['total_sales']
        region_data[region]['percentage'] = round(
            (sales / grand_total) * 100, 2
        )

    region_data = dict(
        sorted(region_data.items(),
               key=lambda x: x[1]['total_sales'],
               reverse=True)
    )

    return region_data


def top_selling_products(transactions, n=5):
    product_data = {}

    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        revenue = qty * tx['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0
            }

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['quantity'],
        reverse=True
    )

    result = []
    for product, values in sorted_products[:n]:
        result.append(
            (product,
             values['quantity'],
             round(values['revenue'], 2))
        )

    return result


def customer_analysis(transactions):
    customer_data = {}

    for tx in transactions:
        cid = tx['CustomerID']
        amount = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']

        if cid not in customer_data:
            customer_data[cid] = {
                'total_spent': 0,
                'purchase_count': 0,
                'products': set()
            }

        customer_data[cid]['total_spent'] += amount
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products'].add(product)

    final = {}

    for cid, data in customer_data.items():
        final[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(
                data['total_spent'] / data['purchase_count'], 2
            ),
            'products_bought': list(data['products'])
        }

    final = dict(
        sorted(final.items(),
               key=lambda x: x[1]['total_spent'],
               reverse=True)
    )

    return final


def daily_sales_trend(transactions):
    trend = {}

    for tx in transactions:
        date = tx['Date']
        amount = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in trend:
            trend[date] = {
                'total_revenue': 0,
                'transaction_count': 0,
                'customers': set()
            }

        trend[date]['total_revenue'] += amount
        trend[date]['transaction_count'] += 1
        trend[date]['customers'].add(customer)

    final = {}

    for date, data in trend.items():
        final[date] = {
            'total_revenue': round(data['total_revenue'], 2),
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }

    final = dict(sorted(final.items()))

    return final


# =================================================
# TASK 4.1 – GENERATE TEXT REPORT
# =================================================

def generate_sales_report(transactions,
                          enriched_transactions,
                          output_file="output/sales_report.txt"):

    from datetime import datetime
    from collections import defaultdict

    with open(output_file, "w", encoding="utf-8") as f:

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # =================================================
        # HEADER
        # =================================================
        f.write("=" * 44 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 44 + "\n\n")

        # =================================================
        # OVERALL SUMMARY
        # =================================================
        total_revenue = sum(
            t['Quantity'] * t['UnitPrice']
            for t in transactions
        )

        avg_order = total_revenue / len(transactions)

        dates = sorted(t['Date'] for t in transactions)

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {len(transactions)}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {dates[0]} to {dates[-1]}\n\n")

        # =================================================
        # REGION PERFORMANCE
        # =================================================
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write("Region | Total Sales | % of Total | Transactions\n")

        region_data = defaultdict(lambda: {"sales": 0, "count": 0})

        for t in transactions:
            amt = t['Quantity'] * t['UnitPrice']
            region_data[t['Region']]['sales'] += amt
            region_data[t['Region']]['count'] += 1

        region_data = dict(
            sorted(region_data.items(),
                   key=lambda x: x[1]['sales'],
                   reverse=True)
        )

        for r, v in region_data.items():
            pct = (v['sales'] / total_revenue) * 100
            f.write(
                f"{r} | ₹{v['sales']:,.2f} | {pct:.2f}% | {v['count']}\n"
            )

        f.write("\n")

        # =================================================
        # TOP 5 PRODUCTS
        # =================================================
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank | Product | Quantity | Revenue\n")

        prod = defaultdict(lambda: {"qty": 0, "rev": 0})

        for t in transactions:
            name = t['ProductName']
            prod[name]["qty"] += t['Quantity']
            prod[name]["rev"] += t['Quantity'] * t['UnitPrice']

        sorted_prod = sorted(
            prod.items(),
            key=lambda x: x[1]['qty'],
            reverse=True
        )[:5]

        for i, (p, v) in enumerate(sorted_prod, 1):
            f.write(
                f"{i} | {p} | {v['qty']} | ₹{v['rev']:,.2f}\n"
            )

        f.write("\n")

        # =================================================
        # TOP 5 CUSTOMERS
        # =================================================
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank | CustomerID | Total Spent | Orders\n")

        cust = defaultdict(lambda: {"spent": 0, "count": 0})

        for t in transactions:
            cid = t['CustomerID']
            amt = t['Quantity'] * t['UnitPrice']
            cust[cid]["spent"] += amt
            cust[cid]["count"] += 1

        sorted_cust = sorted(
            cust.items(),
            key=lambda x: x[1]['spent'],
            reverse=True
        )[:5]

        for i, (c, v) in enumerate(sorted_cust, 1):
            f.write(
                f"{i} | {c} | ₹{v['spent']:,.2f} | {v['count']}\n"
            )

        f.write("\n")

        # =================================================
        # DAILY SALES TREND
        # =================================================
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write("Date | Revenue | Transactions | Customers\n")

        trend = defaultdict(lambda: {"rev": 0, "count": 0, "cust": set()})

        for t in transactions:
            d = t['Date']
            amt = t['Quantity'] * t['UnitPrice']
            trend[d]["rev"] += amt
            trend[d]["count"] += 1
            trend[d]["cust"].add(t['CustomerID'])

        for d in sorted(trend):
            v = trend[d]
            f.write(
                f"{d} | ₹{v['rev']:,.2f} | {v['count']} | {len(v['cust'])}\n"
            )

        f.write("\n")

        # =================================================
        # PRODUCT PERFORMANCE ANALYSIS
        # =================================================
        best_day = max(trend.items(), key=lambda x: x[1]["rev"])

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(
            f"Best Selling Day: {best_day[0]} "
            f"(₹{best_day[1]['rev']:,.2f} in {best_day[1]['count']} transactions)\n"
        )

        # low performing products
        prod_sorted_low = sorted(
            prod.items(),
            key=lambda x: x[1]["qty"]
        )[:5]

        f.write("Low Performing Products:\n")
        for p, v in prod_sorted_low:
            f.write(
                f"{p} - Qty: {v['qty']}, Revenue: ₹{v['rev']:,.2f}\n"
            )

        f.write("\n")

        # =================================================
        # API ENRICHMENT SUMMARY
        # =================================================
        matched = sum(
            1 for t in enriched_transactions
            if t.get("API_Match")
        )

        total = len(enriched_transactions)
        rate = (matched / total) * 100

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Products Enriched: {matched}/{total}\n")
        f.write(f"Success Rate: {rate:.1f}%\n")

        if matched == total:
            f.write("All products were enriched successfully.\n")

        f.write("-- Final sales report generated successfully --")

    print("✓ Report generated:", output_file)
