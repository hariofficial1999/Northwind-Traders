# 🌐 Northwind Business Performance Insights Dashboard

> **A futuristic, interactive Business Intelligence dashboard built with Streamlit & Plotly**  
> Dark glassmorphism theme · Neon blue/cyan glow · Real-time filtering · AI-powered insights

---

## 📌 Project Overview

This project is a **full-featured BI dashboard** built using Python and Streamlit, powered by the classic **Northwind Traders dataset**. It delivers executive-level analytics across Sales, Customers, Products, Employees, and Logistics — all in a stunning dark-themed, glassmorphism UI.

---

## 🖥️ Dashboard Preview

| Section | Description |
|---|---|
| 🎛️ Sidebar Filters | 6 interactive filters with Select All toggles |
| 📊 KPI Cards | 5 key performance indicators with neon glow |
| 📈 Sales Analytics | Monthly trend + Top 10 products |
| 🗂️ Category & Geography | Donut chart, Country bar, Employee performance |
| 🚚 Logistics | Quarterly revenue + Shipping delay by carrier |
| 🔍 Customer Intel | Bubble scatter — Orders vs Revenue |
| 💡 Insights | 6 dynamic AI-generated business recommendations |

---

## 🚀 Quick Start

### 1. Clone / Navigate to the project folder

```bash
cd "d:\Intern Project\Northwind Traders"
```

### 2. Install dependencies

```bash
pip install streamlit pandas plotly
```

### 3. Run the dashboard

```bash
streamlit run dashboard.py
```

### 4. Open in browser

```
http://localhost:8501
```

---

## 📁 Project Structure

```
Northwind Traders/
│
├── dashboard.py              ← Main Streamlit dashboard app
├── northwind_cleaned.csv     ← Cleaned & merged dataset (primary source)
├── northwind_traders.csv     ← Raw Northwind dataset
├── categories.csv            ← Product categories
├── customers.csv             ← Customer master data
├── employees.csv             ← Employee records
├── orders.csv                ← Order headers
├── order_details.csv         ← Order line items
├── products.csv              ← Product catalogue
├── shippers.csv              ← Shipping carriers
├── Data.ipynb                ← Data exploration notebook
├── northwind.ipynb           ← Analysis notebook
├── Copy of data_dictionary.csv ← Column reference guide
└── README.md                 ← This file
```

---

## 🎛️ Sidebar Filters

The left sidebar contains **6 interactive filters**, each with:

- ☑️ **Select All checkbox** (on the left) — tick to instantly select/deselect all values
- 📋 **Multiselect dropdown** — pre-filled with all values by default
- 🔵 **Live badge** — shows `selected / total` count with colour indicator  
  - 🟢 Green = all selected &nbsp; 🟡 Yellow = partial selection
- 📊 **Summary card** at the bottom showing active filter counts

| # | Filter | Column Used |
|---|---|---|
| 1 | 📅 Year | `order_year` |
| 2 | 🌍 Country | `customer_country` |
| 3 | 📦 Category | `categoryName` |
| 4 | 👤 Employee | `employee_name` |
| 5 | 🚚 Shipper | `shipper_name` |
| 6 | 🏷️ Product Name | `productName` |

> **Fail-safe:** If all items in a filter are cleared, it automatically reverts to **all values** — the dashboard never shows blank data.

---

## 📊 KPI Cards

| KPI | Metric | Description |
|---|---|---|
| 💰 Total Revenue | `SUM(line_total)` | All-time gross sales value |
| 📦 Total Orders | `COUNT DISTINCT(orderID)` | Unique orders placed |
| 👥 Total Customers | `COUNT DISTINCT(customerID)` | Active customer accounts |
| 🎯 Avg Order Value | `Revenue / Orders` | Average revenue per order |
| 🚚 Avg Ship Delay | `MEAN(ship_delay_days)` | Average days past schedule |

---

## 📈 Charts & Visualisations

### Row 1 — Sales Analytics
| Chart | Type | Insight |
|---|---|---|
| Monthly Sales Trend | Area + Line | Revenue movement over time |
| Top 10 Products | Horizontal Bar | Best-performing SKUs by revenue |

### Row 2 — Category, Geography & Team
| Chart | Type | Insight |
|---|---|---|
| Category-wise Revenue | Donut | Share of revenue by product category |
| Revenue by Country | Vertical Bar | Top 12 markets by gross sales |
| Sales by Employee | Horizontal Bar | Individual rep performance |

### Row 3 — Logistics & Quarterly
| Chart | Type | Insight |
|---|---|---|
| Quarterly Revenue | Grouped Bar | Year-over-year quarterly comparison |
| Shipping Delay by Carrier | Horizontal Bar | Average delay per shipper |

### Row 4 — Customer Intelligence
| Chart | Type | Insight |
|---|---|---|
| Customer Segmentation | Bubble Scatter | Orders vs Revenue per customer |

---

## 💡 Business Insights (Auto-generated)

The dashboard dynamically computes 6 data-driven business recommendations:

1. **📦 Product Portfolio** — Top-grossing product & bundling strategy
2. **🗂️ Category Concentration** — Category revenue share & diversification advice
3. **🌍 Geographic Expansion** — Top market identification & growth opportunities
4. **👤 Sales Team Excellence** — Top performer spotlight & peer-mentoring strategy
5. **🚚 Logistics Optimisation** — Worst-delay carrier & SLA improvement tips
6. **📈 Revenue Growth Strategy** — AOV analysis & upselling recommendations

---

## 🎨 Design System

| Element | Style |
|---|---|
| Theme | Dark glassmorphism |
| Primary colour | `#00c8ff` (Neon Cyan) |
| Secondary colour | `#38bdf8` (Sky Blue) |
| Accent | `#34d399` (Emerald Green) |
| Background | `radial-gradient(#0d1b2a → #000814)` |
| Font | Inter (Google Fonts) |
| Charts | Plotly with transparent dark backgrounds |
| Cards | `rgba` glass effect + neon border glow |

---

## 🗃️ Dataset Reference

The primary file used is **`northwind_cleaned.csv`** — a fully merged, enriched dataset.

### Key Columns

| Column | Description |
|---|---|
| `orderID` | Unique order identifier |
| `productID` | Product identifier |
| `productName` | Name of the product |
| `categoryName` | Product category |
| `customerID` | Customer identifier |
| `customer_company` | Customer company name |
| `customer_country` | Customer's country |
| `employee_name` | Sales representative name |
| `shipper_name` | Shipping carrier |
| `orderDate` | Date order was placed |
| `shippedDate` | Date order was shipped |
| `line_total` | Revenue for that line item |
| `ship_delay_days` | Days between required and shipped date |
| `order_year` | Extracted year from orderDate |
| `order_month` | Extracted month from orderDate |
| `order_quarter` | Extracted quarter from orderDate |
| `is_shipped` | Boolean — whether order was shipped |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `streamlit` | ≥ 1.30 | Web application framework |
| `pandas` | ≥ 2.0 | Data loading & transformation |
| `plotly` | ≥ 5.18 | Interactive charts & visualisations |
| `python` | ≥ 3.9 | Core language |

---

## ⚙️ Configuration

No `.env` or config files are needed. The app reads directly from `northwind_cleaned.csv` in the same directory.

To change the data source, update line in `dashboard.py`:

```python
df = pd.read_csv("northwind_cleaned.csv")   # ← change path here
```

---

## 🔧 Troubleshooting

| Issue | Fix |
|---|---|
| `FileNotFoundError` for CSV | Run `streamlit run dashboard.py` from the project folder |
| Charts not showing | Ensure `plotly` is installed: `pip install plotly` |
| Blank dashboard | All filters cleared — click any "All" checkbox to restore |
| Port already in use | Run on a different port: `streamlit run dashboard.py --server.port 8502` |
| `use_container_width` warning | Harmless deprecation warning — does not affect functionality |

---

## 👨‍💻 Author

**Northwind BI Dashboard**  
Built as an Internship Project using the Northwind Traders sample dataset.

- 🛠️ Built with: Python · Streamlit · Plotly · Pandas  
- 🎨 Design: Dark BI Theme · Glassmorphism · Neon Glow  
- 📅 Year: 2026

---

## 📜 License

This project is for educational / internship purposes.  
The Northwind dataset is a sample dataset originally provided by Microsoft.

---

*"Turning raw data into business decisions — one chart at a time."* 🚀
