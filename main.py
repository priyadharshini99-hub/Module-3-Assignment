# ==========================================
# MAIN APPLICATION
# Part 5 – Execution Flow
# ==========================================

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():

    print("=" * 50)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 50)

    # ---------------- STEP 1 ----------------
    print("\n[1/10] Reading sales data...")
    raw_lines = read_sales_data("data/sales_data.txt")

    if not raw_lines:
        print("❌ No data found. Exiting.")
        return

    print("✓ Successfully read data")

    # ---------------- STEP 2 ----------------
    print("\n[2/10] Parsing & cleaning data...")
    transactions = parse_transactions(raw_lines)
    print(f"✓ Parsed {len(transactions)} records")

    # ---------------- STEP 3 ----------------
    print("\n[3/10] Filter options:")
    regions = set(t['Region'] for t in transactions)
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]

    print("Regions:", regions)
    print("Amount Range:",
          min(amounts), "to", max(amounts))

    apply_filter = input("Do you want to filter data? (y/n): ").lower()

    region = None
    min_amt = None
    max_amt = None

    if apply_filter == "y":
        region = input("Enter region (or press Enter to skip): ") or None

        min_amt = input("Enter minimum amount (or press Enter): ")
        max_amt = input("Enter maximum amount (or press Enter): ")

        min_amt = float(min_amt) if min_amt else None
        max_amt = float(max_amt) if max_amt else None

    # ---------------- STEP 4 ----------------
    print("\n[4/10] Validating transactions...")
    valid_tx, invalid_count, summary = validate_and_filter(
        transactions,
        region,
        min_amt,
        max_amt
    )

    print("✓ Validation complete")

    # ---------------- STEP 5 ----------------
    print("\n[5/10] Performing analysis...")

    total_revenue = calculate_total_revenue(valid_tx)
    region_stats = region_wise_sales(valid_tx)
    top_products = top_selling_products(valid_tx)
    customers = customer_analysis(valid_tx)
    daily_trend = daily_sales_trend(valid_tx)

    print("✓ Analysis complete")

    # ---------------- STEP 6 ----------------
    print("\n[6/10] Fetching product data from API...")
    api_products = fetch_all_products()

    # ---------------- STEP 7 ----------------
    print("\n[7/10] Enriching sales data...")
    mapping = create_product_mapping(api_products)
    enriched = enrich_sales_data(valid_tx, mapping)

    matched = sum(1 for t in enriched if t['API_Match'])
    print(f"✓ Enriched {matched}/{len(enriched)} transactions")

    # ---------------- STEP 8 ----------------
    print("\n[8/10] Saving enriched data...")
    save_enriched_data(enriched)

    # ---------------- STEP 9 ----------------
    print("\n[9/10] Generating report...")
    generate_sales_report(valid_tx, enriched)

    # ---------------- STEP 10 ----------------
    print("\n[10/10] Process Complete!")
    print("Files created:")
    print("→ data/enriched_sales_data.txt")
    print("→ output/sales_report.txt")
    print("=" * 50)


if __name__ == "__main__":
    main()
