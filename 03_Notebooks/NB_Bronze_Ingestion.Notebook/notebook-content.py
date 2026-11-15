# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5c388b16-7174-4f0e-a7c0-0315dba73b9a",
# META       "default_lakehouse_name": "LH_SalesOrders",
# META       "default_lakehouse_workspace_id": "0482fdfe-a4fc-4233-addb-2ed8217ba008",
# META       "known_lakehouses": [
# META         {
# META           "id": "5c388b16-7174-4f0e-a7c0-0315dba73b9a"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS bronze_sales_orders")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import random
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType, DateType
from decimal import Decimal

customers = ["Contoso Ltd", "Northwind Traders", "Adventure Works", "Fabrikam Inc", "Tailwind Toys", "Woodgrove Bank", "Alpine Ski House", "Bellows College", "Munson's Pickles", "VanArsdel Ltd"]
products = [("Widget A", Decimal("12.99")), ("Widget B", Decimal("8.50")), ("Widget C", Decimal("5.25")), ("Widget D", Decimal("22.00")), ("Widget E", Decimal("15.75"))]
regions = ["APAC", "EMEA", "Americas"]
statuses = ["Completed", "Pending", "Cancelled", "Returned"]

random.seed(42)
rows = []
start_date = datetime(2023, 1, 1)

for i in range(1, 501):
    order_date = start_date + timedelta(days=random.randint(0, 729))
    customer = random.choice(customers)
    product, base_price = random.choice(products)
    quantity = random.randint(5, 300)
    region = random.choice(regions)
    status = random.choices(statuses, weights=[70, 15, 10, 5])[0]
    rows.append((i, order_date.date(), customer, product, quantity, base_price, region, status))

schema = StructType([
    StructField("OrderID", IntegerType()),
    StructField("OrderDate", DateType()),
    StructField("CustomerName", StringType()),
    StructField("Product", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("UnitPrice", DecimalType(10,2)),
    StructField("Region", StringType()),
    StructField("Status", StringType())
])

df_bronze = spark.createDataFrame(rows, schema)
df_bronze.write.format("delta").mode("overwrite").saveAsTable("bronze_sales_orders")
print(f"Bronze table written with {df_bronze.count()} rows.")
df_bronze.show(20)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
