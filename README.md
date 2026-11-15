# fabric-demo-sql-e2e

End-to-end Microsoft Fabric demo — Bronze → Silver → Gold medallion pipeline with notebook-generated sales data.

## What this demo does

Runs a complete medallion architecture inside a single Fabric workspace using only notebooks and a Lakehouse. No external data sources, no credentials, no gateway — fully self-contained and reproducible.

| Layer | Notebook | What it does |
|-------|----------|--------------|
| Bronze | `NB_Bronze_Ingestion` | Generates 500 synthetic sales orders (10 customers, 5 products, 3 regions, 4 statuses) and writes them as a raw Delta table |
| Silver | `NB_Silver_Transform` | Cleans types, adds calculated fields (LineTotal, OrderYear, OrderQuarter, OrderMonth), filters out cancelled orders |
| Gold | `NB_Gold_Aggregates` | Creates three business-ready aggregate tables for reporting |

## Gold tables

| Table | Use case |
|-------|----------|
| `gold_revenue_by_customer` | Customer leaderboard, top accounts |
| `gold_revenue_by_region_quarter` | Trend lines, regional comparison over time |
| `gold_product_performance` | Product mix, best sellers, avg quantity per order |

## Workspace structure

```
Demo - SQL Server End to End/
├── 01_Source_Files/
├── 02_Lakehouse/         → LH_SalesOrders
├── 03_Notebooks/         → NB_Bronze_Ingestion, NB_Silver_Transform, NB_Gold_Aggregates
├── 04_Semantic_Model/    → SM_SalesOrders
├── 05_Reports/           → RPT_SalesOrders
├── 06_App/
├── 07_Governance/
└── 99_Scratch/
```

## How to run

1. Create a Fabric workspace and a Lakehouse (`LH_SalesOrders`)
2. Run `NB_Bronze_Ingestion` → writes `bronze_sales_orders` (500 rows)
3. Run `NB_Silver_Transform` → writes `silver_sales_orders` (~450 rows, cancelled excluded)
4. Run `NB_Gold_Aggregates` → writes 3 gold tables
5. Create a semantic model from the Lakehouse tables
6. Build a Power BI report

## Prerequisites

- Microsoft Fabric workspace (trial or paid)
- No API keys, gateways, or external dependencies

## Data schema

The Bronze table contains:

| Column | Type | Example |
|--------|------|---------|
| OrderID | int | 1 |
| OrderDate | date | 2024-01-15 |
| CustomerName | string | Contoso Ltd |
| Product | string | Widget A |
| Quantity | int | 50 |
| UnitPrice | decimal | 12.99 |
| Region | string | APAC |
| Status | string | Completed |

Silver adds: `LineTotal`, `OrderYear`, `OrderQuarter`, `OrderMonth`

## Naming conventions

| Prefix | Item type |
|--------|-----------|
| `NB_` | Notebook |
| `LH_` | Lakehouse |
| `SM_` | Semantic Model |
| `RPT_` | Report |
| `PL_` | Pipeline |

## Author

Ivy Fiecas — AI Solutions Developer / Associate Consultant, Data & AI @ SoftwareOne
