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

from pyspark.sql.functions import col, sum, count, round, avg

# Revenue by Customer
df_customer = (
    spark.read.table("silver_sales_orders")
    .groupBy("CustomerName")
    .agg(
        count("OrderID").alias("TotalOrders"),
        sum("Quantity").alias("TotalUnits"),
        round(sum("LineTotal"), 2).alias("TotalRevenue"),
        round(avg("LineTotal"), 2).alias("AvgOrderValue")
    )
    .orderBy(col("TotalRevenue").desc())
)
df_customer.write.format("delta").mode("overwrite").saveAsTable("gold_revenue_by_customer")
print("gold_revenue_by_customer written.")
df_customer.show()

# Revenue by Region and Quarter
df_region_quarter = (
    spark.read.table("silver_sales_orders")
    .groupBy("Region", "OrderYear", "OrderQuarter")
    .agg(
        count("OrderID").alias("TotalOrders"),
        round(sum("LineTotal"), 2).alias("TotalRevenue")
    )
    .orderBy("OrderYear", "OrderQuarter", "Region")
)
df_region_quarter.write.format("delta").mode("overwrite").saveAsTable("gold_revenue_by_region_quarter")
print("gold_revenue_by_region_quarter written.")
df_region_quarter.show()

# Product Performance
df_product = (
    spark.read.table("silver_sales_orders")
    .groupBy("Product")
    .agg(
        count("OrderID").alias("TotalOrders"),
        sum("Quantity").alias("TotalUnits"),
        round(sum("LineTotal"), 2).alias("TotalRevenue"),
        round(avg("Quantity"), 0).alias("AvgQtyPerOrder")
    )
    .orderBy(col("TotalRevenue").desc())
)
df_product.write.format("delta").mode("overwrite").saveAsTable("gold_product_performance")
print("gold_product_performance written.")
df_product.show()

print("All Gold tables written.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
