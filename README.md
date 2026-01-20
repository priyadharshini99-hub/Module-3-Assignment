# Sales Analytics System  
Assignment Module 3 – Sales Data Processing, Analysis & Reporting Using Python

---

## 1. Project Overview

This project has been developed as part of Assignment Module 3 of the data analytics program.

The Sales Analytics System is a Python-based application that demonstrates:

- File handling & encoding management  
- Data cleaning & validation  
- Business analytics  
- API integration  
- Automated report generation  

The system reads raw sales transaction data, resolves data quality issues, performs structured sales analysis, enriches data using an external API, and generates a professional sales analytics report.

---

## 2. Dataset Used

### 2.1 Input Dataset

File:  
data/sales_data.txt

Format: Pipe-separated (|) text file

Schema:  
TransactionID | Date | ProductID | ProductName | Quantity | UnitPrice | CustomerID | Region

Sample Record:  
T018|2024-12-29|P107|USB Cable|8|173|C009|South

---

### 2.2 Data Quality Issues Handled

The dataset intentionally contains real-world issues:

- Product names with commas  
- Numeric values with commas  
- Missing fields  
- Zero / negative values  
- Invalid ID formats  

All issues are automatically detected and handled.

---

## 3. Project Folder Structure

sales-analytics-system/
│
│── main.py  
│   → Main execution file  
│
│── README.md  
│   → Project documentation  
│
│── requirements.txt  
│   → Dependencies  
│
├── utils/  
│   ├── file_handler.py  
│   ├── data_processor.py  
│   └── api_handler.py  
│
├── data/  
│   ├── sales_data.txt  
│   └── enriched_sales_data.txt  
│
├── output/  
│   └── sales_report.txt  

---

## 4. System Workflow

1. Data ingestion with encoding handling  
2. Data cleaning & validation  
3. Business analytics  
4. API integration  
5. Data enrichment  
6. Report generation  

Entire flow is fully automated.

---

## 5. API Used

DummyJSON Products API

Endpoint:  
https://dummyjson.com/products?limit=100

Used fields:

- Title  
- Category  
- Brand  
- Rating  

---

## 6. Project Execution

Step 1 – Install dependencies

pip install -r requirements.txt

Step 2 – Run application

python main.py

---

## 7. Output Files

data/enriched_sales_data.txt  
→ Enriched dataset  

output/sales_report.txt  
→ Final analytics report  

---

## 8. Conclusion

This project successfully implements a complete analytics pipeline and meets all objectives of Assignment Module 3.

It demonstrates:

- Clean modular design  
- Automated processing  
- Real API integration  
- Professional reporting  

---

Developed by  
Priyadharshini G
