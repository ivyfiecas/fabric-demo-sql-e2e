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

from pyspark.sql.functions import col, year, month, quarter

df_silver = (
    spark.read.table("bronze_sales_orders")
    .withColumn("LineTotal", col("Quantity") * col("UnitPrice"))
    .withColumn("OrderYear", year("OrderDate"))
    .withColumn("OrderQuarter", quarter("OrderDate"))
    .withColumn("OrderMonth", month("OrderDate"))
    .filter(col("Status") != "Cancelled")
    .orderBy("OrderDate")
)

df_silver.write.format("delta").mode("overwrite").saveAsTable("silver_sales_orders")
print(f"Silver table written with {df_silver.count()} rows (cancelled orders excluded).")
df_silver.show(20)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
