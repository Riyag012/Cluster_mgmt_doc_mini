from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date
import time

#  Initialize Spark Session

# Minikube
# spark = SparkSession.builder.appName("DataAnalysis").getOrCreate()

#Docker
spark = SparkSession.builder \
    .appName("DataAnalysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()


customers_df = spark.read.parquet("/app/data/customers.parquet")
transactions_df = spark.read.parquet("/app/data/transactions.parquet")

print("--- Original Transactions Schema ---")
transactions_df.printSchema()

transactions_with_date = transactions_df.withColumn("date", to_date(col("date")))

print("\n--- Transactions Schema After Date Conversion ---")
transactions_with_date.printSchema()


# --- Now, run your analysis on the corrected DataFrame ---
print("\n--- Using DataFrame API ---")
# Find the total amount spent on 'Entertainment' in 2018
entertainment_2018_df = transactions_with_date \
    .filter((col("expense_type") == "Entertainment") & (year(col("date")) == 2018)) \
    .groupBy("cust_id") \
    .agg({"amt": "sum"}) \
    .withColumnRenamed("sum(amt)", "total_entertainment_spend")

print("Total Entertainment Spend in 2018:")
entertainment_2018_df.show(5)
time.sleep(300)
spark.stop()