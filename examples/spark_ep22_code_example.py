import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from course import *
from gen import text, box, line
from gen2 import T, merge
from course import card

E = Episode(22, "The Medallion Architecture")
E.intro(["Bronze, silver and gold layers", "The complete lakehouse", "Hands-on: a customer demographics pipeline", "SQL analytics on the gold table"])

E.chapter("Bronze, silver, gold")
E.bullets("What is the medallion architecture?", [
    ("The lakehouse is about unification: the best of different technologies in one place.", "The lakehouse is all about unification: combining the best elements of different technologies in one place."),
    ("The medallion architecture: a popular design pattern with BRONZE, SILVER and GOLD layers, enabled by Delta Lake.",
     "The medallion architecture is a popular data design pattern, with bronze, silver and gold layers, ultimately enabled by Delta Lake.", "orange"),
    ("It organises lakehouse data step by step, improving structure and quality at each layer, for batch and streaming alike.",
     "It organises data in a lakehouse step by step, improving the structure and quality of data at each layer, each with its own purpose, while unifying batch and streaming."),
])
layers = [("Bronze", "bronze", "Raw data, as it arrived. No transformations, no business rules. The landing zone."),
          ("Silver", "silver", "Cleaned and normalised: standard dates/times, naming standards, de-duplicated, quality-checked. “Just enough.”"),
          ("Gold", "gold", "Business-level aggregates: star schema, snowflake schema, or any model your consumers need. The single source of truth.")]
E.add("medals", [
    B("Data flows through three layers, each one more refined than the last.", [
        T("Bronze → Silver → Gold"), box(50, 120, 190, 120, "sources:\nCSV · JSON\n· DB", "grey", fs=20)]),
    B("Bronze holds the raw data from the sources, ingested without any transformations or business rules. It's the landing zone, so its tables match the source systems exactly.", [
        line([(245, 180), (300, 180)], sw=3), card(310, 110, 260, f"{layers[0][0]}: {layers[0][2]}", layers[0][1], fs=20, minh=200)[0]],
      acts=[A("c1", "cube_grey", (0.2, 150, 330, {"pop": 1}), (0.6, 440, 360, {"whoosh": 1}))]),
    B("Silver cleans and normalises it: standard formats for dates and times, the company's column naming standard, de-duplication, and quality checks that drop bad rows. "
      "With a just-enough philosophy: enough detail with the least effort, to stay agile.", [
        line([(575, 180), (630, 180)], sw=3), card(640, 110, 260, f"{layers[1][0]}: {layers[1][2]}", layers[1][1], fs=20, minh=200)[0]],
      acts=[A("c2", "cube_blue", (0.2, 440, 360, {"pop": 1}), (0.6, 770, 360, {"whoosh": 1}))]),
    B("Gold creates business-level aggregates, using a Kimball star schema, an Inmon snowflake schema, or any model that fits the business. The final transformations and quality rules "
      "make it high-quality, reliable data: the single source of truth for the organisation.", [
        line([(905, 180), (960, 180)], sw=3), card(970, 110, 250, f"{layers[2][0]}: {layers[2][2]}", layers[2][1], fs=20, minh=200)[0]],
      acts=[A("c3", "cube_orange", (0.2, 770, 360, {"pop": 1}), (0.6, 1095, 360, {"whoosh": 1}))], sfx=[("chime", 0.9)]),
])
E.bullets("Bronze keeps the source format", [
    ("CSV source → stored in Bronze as CSV · JSON → JSON", "One detail about bronze: the source format is kept. A CSV source is stored in bronze as CSV, and JSON stays JSON."),
    ("A database table → usually lands as Parquet or AVRO.", "Data extracted from a database table typically lands in bronze as Parquet or AVRO files."),
])
E.add("medal_animals", [
    B("Think of it as a squirrel sorting its harvest: everything goes into the bronze pile, the good nuts are cleaned into the silver pile, and only the best become the gold reserve.", [
        T("Raw → clean → business-ready"), box(60, 180, 300, 260, "", "bronze", fill="hachure"), text(210, 190, "bronze", 30, "bronze", align="center"),
        box(460, 180, 300, 260, "", "silver", fill="hachure"), text(610, 190, "silver", 30, "silver", align="center"),
        box(860, 180, 300, 260, "", "gold", fill="hachure"), text(1010, 190, "gold", 30, "gold", align="center")],
      acts=[A("sq", "squirrel", (0.05, 210, 560, {"pop": 1}), (0.45, 610, 560, {"walk": 1, "whoosh": 1}), (0.85, 1010, 560, {"walk": 1}))] +
           [A(f"n{i}", "cube_grey", (0.05, 120 + i * 60, 400, {"pop": 1})) for i in range(4)] +
           [A(f"m{i}", "cube_blue", (0.45, 550 + i * 60, 400, {"pop": 1})) for i in range(3)] +
           [A("g0", "cube_orange", (0.85, 990, 400, {"pop": 1}))], sfx=[("ding", 0.9)], host="happy"),
])

E.chapter("The complete lakehouse")
E.flow("The complete lakehouse", [
    ("Sources: batch & streaming", "Once the medallion architecture is in place on Delta Lake, you see the full benefits of the lakehouse. Data arrives from batch and streaming sources...", "grey"),
    ("Bronze · Silver · Gold on Delta Lake", "...flows through bronze, silver and gold, all stored as Delta tables...", "orange"),
    ("BI & reporting", "...and serves business intelligence and reporting...", "blue"),
    ("Data science & ML", "...as well as data science and machine learning, all from one reliable source of truth.", "violet"),
])

E.chapter("Hands-on: customer demographics")
E.code("Bronze: land the raw CSV", '''from pyspark.sql import SparkSession
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("CustomerDemographics").getOrCreate()

# bronze layer
bronzePath = "/mnt/delta/customers/bronze/"

bronzeDF = spark.read.format("csv") \\
    .option("header", "true") \\
    .option("inferSchema", "true") \\
    .load("dbfs:/databricks-datasets/retail-org/customers/customers.csv")

bronzeDF.write.mode("overwrite").format("delta").save(bronzePath)''', [
    (4, "Let's build a customer demographics pipeline. Imports, and a SparkSession called CustomerDemographics. You'll also need functions like col, trim, upper, initcap, desc, rank, when, "
        "count and collect_list from pyspark.sql.functions."),
    (7, "The bronze layer lives at mnt, delta, customers, bronze."),
    (12, "Read the raw customers CSV from the Databricks sample datasets, with a header and inferred schema."),
    (14, "And write it, unchanged, as a Delta table at the bronze path. Note: here bronze is stored as Delta rather than CSV, a common practical choice.", "bronze: raw customers (Delta)"),
])
E.code("Silver: clean and standardise", '''# silver layer
silverPath = "/mnt/delta/customers/silver/"

silverDF = spark.read.format("delta").load(bronzePath) \\
    .withColumn("customer_name", initcap(trim(col("customer_name")))) \\
    .withColumn("state", upper(trim(col("state")))) \\
    .withColumn("city", initcap(trim(col("city")))) \\
    .fillna({"tax_code": "UNKNOWN"}) \\
    .dropDuplicates(["customer_id"])

silverDF.write.mode("overwrite").format("delta").save(silverPath)''', [
    (4, "Silver: read bronze back."),
    (7, "Standardise the text: trim spaces and capitalise customer names and cities, and uppercase the state codes."),
    (8, "Fill missing tax codes with UNKNOWN."),
    (9, "Remove duplicate customers by customer_id."),
    (11, "Write the clean data to the silver path.", "silver: clean, unique customers"),
])
E.add("silver_before_after", [
    B("Here's what silver does to one messy row.", [
        T("Silver, before and after"),
        E.table_els(60, 140, ["customer_name", "state", "city", "tax_code"], [["  jOHN smith ", " ca", "los angeles ", "null"]], [260, 120, 220, 160], rh=54, fs=20, color="bronze"),
        line([(420, 260), (420, 320)], sw=3),
        E.table_els(60, 330, ["customer_name", "state", "city", "tax_code"], [["John Smith", "CA", "Los Angeles", "UNKNOWN"]], [260, 120, 220, 160], rh=54, fs=20, color="silver")],
      sfx=[("ding", 0.7)]),
])
E.code("Silver: enrich", '''# Read silver data
silverDF = spark.read.format("delta").load(silverPath)

# Example transformation: Rank customers by state based on their tax_code frequency
windowSpec = Window.partitionBy("state").orderBy(desc("tax_code"))
rankedDF = silverDF.withColumn("rank", rank().over(windowSpec))

# Add a 'customer_age_group' column based on arbitrary age logic for demonstration
enrichedDF = rankedDF.withColumn("customer_age_group", when(col("tax_id").substr(-1, 1) % 2 == 0, "Even").otherwise("Odd"))

enrichedDF.write.mode("overwrite").option("overwriteSchema", "true").format("delta").save(silverPath)''', [
    (2, "Next, enrich the silver data. Read it back."),
    (6, "A window function: within each state, order by tax_code descending, and add a rank column. The comment says frequency, but this actually ranks by the tax code value itself."),
    (10, "Add a demo column, customer_age_group: Even if the last digit of tax_id is even, otherwise Odd. Purely for demonstration."),
    (13, "Overwrite silver, with overwriteSchema true, because we added new columns.", "silver: + rank + customer_age_group"),
])
E.code("Gold: business aggregates", '''# Gold Layer
goldPath = "/mnt/delta/customers/gold/"

goldDF = spark.read.format("delta").load(silverPath) \\
    .groupBy("state", "customer_age_group") \\
    .agg(count("*").alias("total_customers"),
         collect_list("customer_name").alias("sample_customers")) \\
    .orderBy("state", "total_customers")

goldDF.write.mode("overwrite").format("delta").save(goldPath)''', [
    (2, "Gold: business-ready aggregates."),
    (8, "Group by state and age group. Count the customers, and collect a list of their names. Order by state and total."),
    (10, "Write it to the gold path.", "state | customer_age_group | total_customers | sample_customers"),
])

E.chapter("SQL analytics on gold")
E.code("Register the gold table", '''CREATE DATABASE customer;
USE customer;

CREATE TABLE customer_gold
SELECT *
FROM delta.`/mnt/delta/customers/gold/`;

SElECT * FROM customer_gold;''', [
    (2, "Analysts can now use SQL. Create and use a customer database."),
    (6, "Create a customer_gold table from the gold Delta folder. The notes have a stray backtick at the end of this line; remove it, and you may need AS before SELECT."),
    (8, "And query it.", "all gold rows"),
])
E.code("Business questions", '''SELECT state, total_customers
FROM customer_gold
ORDER BY total_customers DESC
LIMIT 10;

SELECT state, SUM(total_customers) AS customers_in_state
FROM customer_gold
GROUP BY state
ORDER BY customers_in_state DESC;

SELECT state, total_customers
FROM customer_gold
WHERE total_customers < 50 -- Assuming cities with less than 50 customers are underrepresented
ORDER BY total_customers;''', [
    (4, "The ten largest state and age-group groups."),
    (9, "Total customers per state, biggest first."),
    (14, "And under-represented groups: fewer than fifty customers. The comment says cities, but the table is grouped by state.", "states ranked by customers"),
])

E.quiz([
    ("Which layer holds raw data exactly as the source sent it?", "Bronze, the landing zone.", "Bronze"),
    ("Where do de-duplication and standard formats happen?", "In silver, which cleans and normalises the data.", "Silver"),
    ("Which layer is the single source of truth for business users?", "Gold, with business-level aggregates.", "Gold"),
])
E.outro([
    ("Bronze = raw landing zone · Silver = clean & conformed · Gold = business aggregates", "Bronze is raw, silver is clean, gold is business-ready."),
    ("Each layer improves structure and quality, for batch and streaming", "Each layer improves structure and quality."),
    ("Pipeline: read CSV → Delta bronze → trim/case/fill/dedupe → rank & enrich → group & aggregate", "Our pipeline went from raw CSV, through cleaning and enrichment, to aggregates."),
    ("SQL on gold: top groups · totals per state · under-represented groups", "And SQL on gold answers business questions."),
], "Parquet, One Big Table and Spark Optimization")
E.build()
