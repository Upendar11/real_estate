"""
Day 2 - SQL Project 2: Order-Payment Data Quality and Reconciliation
Educational video covering data quality, validation, and reconciliation concepts
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *

E = StoryEp(2, "Order-Payment Reconciliation")

# Intro
E.intro([
    "Understand the business problem",
    "Learn data quality validation",
    "Master reconciliation techniques",
    "Build trustworthy financial reports"
], say_hello="Welcome to Day 2 of SQL Mastery! Today we're solving a real-world data quality challenge.")

# ========================================
# CHAPTER 1: THE BUSINESS PROBLEM
# ========================================
E.chapter("The Business Challenge")

E.story("Finance Team's Nightmare", [
    ("N", "An e-commerce company is facing serious data issues", 
     "An e-commerce company is facing serious data issues"),
    ("M", "Finance has discovered multiple problems in our payment data", 
     "Finance has discovered multiple problems in our payment data", "point"),
    ("A", "That sounds concerning! What kind of problems?", 
     "That sounds concerning! What kind of problems?", "think")
])

E.bullets("Data Quality Problems Discovered", [
    ("Duplicate payments appearing in the system", 
     "Duplicate payments appearing in the system", "red"),
    ("Successful orders missing their payments", 
     "Successful orders missing their payments", "red"),
    ("Payment amounts don't match order totals", 
     "Payment amounts don't match order totals", "orange"),
    ("Payments referencing non-existent orders", 
     "Payments referencing non-existent orders", "red"),
    ("Invalid records entering financial reports", 
     "Invalid records entering financial reports", "orange"),
    ("Daily books cannot be closed with confidence", 
     "Daily books cannot be closed with confidence", "red")
])

E.add("business_impact", [
    B("These issues have serious business consequences!", [
        T("Business Impact"),
        card(200, 180, 880, "Without clean data:\n• Revenue reports are inaccurate\n• Payment reconciliation fails\n• Financial audits are at risk\n• Business decisions are compromised", 
             "red", fs=22, minh=140)
    ], acts=[
        A("server", "server_rack", (0.0, 180, 380, {"pop": 1})),
        A("alert", "stamp_error", (0.3, 900, 350, {"pop": 1}))
    ], sfx=[("buzz", 0.3)], host="stand")
])

# ========================================
# CHAPTER 2: THE DATA SOURCES
# ========================================
E.chapter("Understanding the Data")

E.story("Two Data Sources", [
    ("N", "We have two main data sources to work with", 
     "We have two main data sources to work with"),
    ("M", "First, the orders table from our sales platform", 
     "First, the orders table from our sales platform", "point"),
    ("A", "And the payments table from the payment processor?", 
     "And the payments table from the payment processor?", "happy")
])

E.tables("Orders Table Structure", [
    ("orders", 
     ["Column", "Type", "Purpose"],
     [["order_id", "INTEGER", "Unique order ID"],
      ["customer_id", "VARCHAR", "Customer ID"],
      ["order_timestamp", "TIMESTAMP", "When ordered"],
      ["quantity", "INTEGER", "Items ordered"],
      ["unit_price", "DECIMAL", "Price per item"],
      ["order_status", "VARCHAR", "Order state"],
      ["updated_at", "TIMESTAMP", "Last update"]],
     "The orders table tracks every customer purchase")
])

E.tables("Payments Table Structure", [
    ("payments",
     ["Column", "Type", "Purpose"],
     [["payment_record_id", "INTEGER", "Record ID"],
      ["payment_id", "VARCHAR", "Payment ID"],
      ["order_id", "INTEGER", "Links to order"],
      ["payment_timestamp", "TIMESTAMP", "When paid"],
      ["payment_amount", "DECIMAL", "Amount paid"],
      ["payment_status", "VARCHAR", "Payment state"],
      ["updated_at", "TIMESTAMP", "Last update"]],
     "The payments table tracks all payment attempts")
])

E.add("data_flow", [
    B("Data flows from two independent systems", [
        T("System Architecture"),
        text(250, 160, "Sales Platform", 22, "blue"),
        text(640, 160, "Payment Processor", 22, "green"),
        text(640, 480, "Finance Database", 22, "violet")
    ], acts=[
        A("sales", "laptop_blue", (0.0, 180, 200, {"pop": 1})),
        A("payment", "monitor_green", (0.3, 560, 200, {"pop": 1})),
        A("db", "server_rack", (0.6, 580, 320, {"pop": 1}))
    ], host="point")
])

# ========================================
# CHAPTER 3: SAMPLE DATA WITH PROBLEMS
# ========================================
E.chapter("Examining Real Data")

E.tables("Sample Orders Data", [
    ("orders",
     ["order_id", "customer_id", "quantity", "unit_price", "status"],
     [["2001", "C101", "2", "50.00", "COMPLETED"],
      ["2002", "C102", "1", "120.00", "COMPLETED"],
      ["2003", "C103", "3", "30.00", "CANCELLED"],
      ["2004", "NULL", "1", "75.00", "COMPLETED"],
      ["2005", "C105", "-2", "40.00", "COMPLETED"],
      ["2006", "C106", "2", "NULL", "COMPLETED"]],
     "Can you spot the data quality issues here?", {"3": "orange", "4": "red", "5": "red"})
])

E.add("spot_issues", [
    B("Let me highlight the problems in the orders!", [
        T("Order Data Issues")
    ], acts=[
        A("issue1", "stamp_null", (0.0, 200, 250, {"pop": 1})),
        A("issue2", "stamp_error", (0.3, 500, 250, {"pop": 1})),
        A("issue3", "stamp_error", (0.6, 800, 250, {"pop": 1}))
    ], sfx=[("ding", 0.0), ("ding", 0.3), ("ding", 0.6)])
])

E.bullets("Orders Data Issues Found", [
    ("Order 2004: Missing customer_id (NULL)", 
     "Order 2004 has a missing customer I D", "red"),
    ("Order 2005: Negative quantity (-2)", 
     "Order 2005 has a negative quantity of minus 2", "red"),
    ("Order 2006: Missing unit_price (NULL)", 
     "Order 2006 has a missing unit price", "red"),
    ("Order 2003: Cancelled but has a payment", 
     "Order 2003 is cancelled but has a payment", "orange")
])

E.tables("Sample Payments Data", [
    ("payments",
     ["record_id", "payment_id", "order_id", "amount", "status"],
     [["1", "PAY-501", "2001", "100.00", "SUCCESS"],
      ["2", "PAY-501", "2001", "100.00", "SUCCESS"],
      ["3", "PAY-502", "2002", "100.00", "SUCCESS"],
      ["4", "PAY-503", "2003", "90.00", "SUCCESS"],
      ["5", "PAY-504", "9999", "45.00", "SUCCESS"],
      ["6", "PAY-505", "2004", "75.00", "FAILED"],
      ["7", "PAY-505", "2004", "75.00", "SUCCESS"]],
     "The payments table has even more issues!", {"1": "orange", "2": "orange", "4": "orange", "5": "red"})
])

E.bullets("Payments Data Issues Found", [
    ("PAY-501: Duplicate payment records", 
     "Payment 501 appears twice as duplicates", "orange"),
    ("PAY-502: Amount mismatch (100 vs 120)", 
     "Payment 502 amount is 100 but order expects 120", "orange"),
    ("PAY-503: Payment for cancelled order", 
     "Payment 503 is for a cancelled order", "orange"),
    ("PAY-504: Orphan payment (order 9999 doesn't exist)", 
     "Payment 504 references non-existent order 9999", "red"),
    ("PAY-505: Failed then succeeded (need latest)", 
     "Payment 505 has both failed and successful versions", "blue")
])

# ========================================
# CHAPTER 4: THE SOLUTION APPROACH
# ========================================
E.chapter("Building the Solution")

E.story("Step-by-Step Strategy", [
    ("N", "We'll solve this with a structured six-step approach", 
     "We'll solve this with a structured six step approach"),
    ("M", "Each step validates, cleans, or reconciles the data", 
     "Each step validates, cleans, or reconciles the data", "point"),
    ("A", "And we never silently discard bad records!", 
     "And we never silently discard bad records!", "happy")
])

E.flow("Six-Step Solution", [
    ("Step 1:\nValidate\nOrders", "Validate all orders against quality rules", "green"),
    ("Step 2:\nQuarantine\nBad Orders", "Store invalid orders with rejection reasons", "orange"),
    ("Step 3:\nDeduplicate\nPayments", "Keep latest version of each payment", "blue"),
    ("Step 4:\nQuarantine\nBad Payments", "Store invalid payments separately", "orange"),
    ("Step 5:\nReconcile\nOrder-Payment", "Match orders with their payments", "violet"),
    ("Step 6:\nDaily\nSummary", "Create financial summary report", "teal")
])

# ========================================
# CHAPTER 5: VALIDATION AND QUARANTINE
# ========================================
E.chapter("Validation and Quarantine")

E.bullets("Order Validation Rules", [
    ("order_id must not be NULL", 
     "order I D must not be null", "blue"),
    ("customer_id must not be NULL", 
     "customer I D must not be null", "blue"),
    ("quantity must be greater than zero", 
     "quantity must be greater than zero", "blue"),
    ("unit_price must be greater than zero", 
     "unit price must be greater than zero", "blue"),
    ("order_status must be in approved set", 
     "order status must be in approved set", "blue"),
    ("Calculate expected_amount = quantity × unit_price", 
     "Calculate expected amount equals quantity times unit price", "green")
])

E.code("validated_orders CTE", '''
-- Step 1: Validate Orders
WITH validated_orders AS (
  SELECT
    order_id,
    customer_id,
    order_timestamp,
    quantity,
    unit_price,
    order_status,
    quantity * unit_price AS expected_amount,
    updated_at
  FROM orders
  WHERE order_id IS NOT NULL
    AND customer_id IS NOT NULL
    AND quantity > 0
    AND unit_price > 0
    AND order_status IN ('COMPLETED', 'PENDING', 'CANCELLED')
)''', [
    (22, "We apply all validation rules in the WHERE clause", None),
    (23, "Only records passing ALL rules make it through", None)
])

E.add("validation_visual", [
    B("Think of validation as a quality gate", [
        T("Validation Process"),
        text(280, 180, "6 Orders In", 24, "blue"),
        text(640, 300, "Quality Gate", 24, "orange"),
        text(920, 420, "3 Valid Out", 24, "green")
    ], acts=[
        A("input", "cube_blue", (0.0, 240, 230, {"pop": 1})),
        A("gate", "router", (0.3, 560, 350, {"pop": 1})),
        A("output", "cube_green", (0.6, 880, 470, {"pop": 1}))
    ], host="point")
])

# ========================================
# STEP 2 - QUARANTINE BAD ORDERS (continued in same chapter)
# ========================================

E.story("Never Lose Bad Data", [
    ("N", "Invalid records must be preserved, not deleted", 
     "Invalid records must be preserved, not deleted"),
    ("M", "We quarantine them with explicit rejection reasons", 
     "We quarantine them with explicit rejection reasons", "point"),
    ("A", "This helps us investigate and fix upstream issues!", 
     "This helps us investigate and fix upstream issues!", "happy")
])

E.code("order_quarantine CTE", '''
-- Step 2: Quarantine Invalid Orders
order_quarantine AS (
  SELECT
    order_id,
    customer_id,
    quantity,
    unit_price,
    order_status,
    CASE
      WHEN order_id IS NULL THEN 'Missing order_id'
      WHEN customer_id IS NULL THEN 'Missing customer_id'
      WHEN quantity <= 0 THEN 'Invalid quantity'
      WHEN unit_price <= 0 THEN 'Invalid unit_price'
      WHEN order_status NOT IN ('COMPLETED', 'PENDING', 'CANCELLED')
        THEN 'Invalid order_status'
      ELSE 'Unknown issue'
    END AS rejection_reason,
    CURRENT_TIMESTAMP AS rejected_at
  FROM orders
  WHERE order_id IS NULL
     OR customer_id IS NULL
     OR quantity <= 0
     OR unit_price <= 0
     OR order_status NOT IN ('COMPLETED', 'PENDING', 'CANCELLED')
)''', [
    (20, "We capture the FIRST rejection reason found", None),
    (21, "Alternative: capture ALL reasons in comma-separated list", None)
])

E.bullets("Quarantine Design Decision", [
    ("Option A: One row per order, combined reasons", 
     "Option A, one row per order with combined reasons", "blue"),
    ("Option B: Multiple rows per order, one per failure", 
     "Option B, multiple rows per order, one per failure", "blue"),
    ("We choose Option A for simpler analysis", 
     "We choose option A for simpler analysis", "green"),
    ("Document your choice in production code!", 
     "Always document your choice in production code!", "orange")
])

# ========================================
# CHAPTER 6: PAYMENT PROCESSING
# ========================================
E.chapter("Payment Processing")

E.story("The Duplicate Problem", [
    ("N", "Payment systems often create duplicate records", 
     "Payment systems often create duplicate records"),
    ("A", "Why do duplicates happen?", 
     "Why do duplicates happen?", "think"),
    ("M", "Retries, system issues, or versioning can cause them", 
     "Retries, system issues, or versioning can cause them", "point")
])

E.add("duplicate_example", [
    B("Payment PAY-501 appears twice in our data!", [
        T("Duplicate Detection"),
        card(200, 180, 880, "payment_record_id=1: PAY-501, updated_at: 09:10\npayment_record_id=2: PAY-501, updated_at: 09:12\n\nWhich one should we keep?", 
             "orange", fs=20, minh=100)
    ], acts=[
        A("dup1", "stamp_6rows", (0.0, 200, 380, {"pop": 1})),
        A("dup2", "stamp_6rows", (0.2, 600, 380, {"pop": 1}))
    ], sfx=[("buzz", 0.0), ("buzz", 0.2)])
])

E.bullets("Deduplication Strategy", [
    ("Keep the LATEST version by updated_at timestamp", 
     "Keep the latest version by updated at timestamp", "green"),
    ("Use payment_record_id as tie-breaker", 
     "Use payment record I D as tie breaker", "blue"),
    ("This ensures deterministic results", 
     "This ensures deterministic results", "green"),
    ("ROW_NUMBER() makes this easy!", 
     "Row number function makes this easy!", "teal")
])

E.code("latest_payments CTE", '''
-- Step 3: Deduplicate Payments
latest_payments AS (
  SELECT
    payment_id,
    order_id,
    payment_amount,
    payment_status,
    payment_timestamp,
    updated_at
  FROM (
    SELECT *,
      ROW_NUMBER() OVER (
        PARTITION BY payment_id
        ORDER BY updated_at DESC, payment_record_id DESC
      ) AS rn
    FROM payments
  ) ranked
  WHERE rn = 1
)''', [
    (11, "ROW_NUMBER partitions by payment_id", None),
    (12, "We order by updated_at DESC to get latest first", None),
    (13, "Then payment_record_id DESC breaks ties", None),
    (16, "Filter rn = 1 keeps only the latest version", None)
])

E.add("dedup_visual", [
    B("Deduplication keeps one record per payment ID", [
        T("Deduplication Result"),
        text(250, 180, "2 Duplicates", 22, "red"),
        text(640, 300, "ROW_NUMBER()", 22, "blue"),
        text(920, 420, "1 Latest", 22, "green")
    ], acts=[
        A("before", "stamp_6rows", (0.0, 200, 240, {"pop": 1})),
        A("process", "cpu_chip", (0.4, 590, 350, {"pop": 1})),
        A("after", "stamp_ok", (0.7, 870, 470, {"pop": 1}))
    ], sfx=[("ding", 0.7)], host="happy")
])

# ========================================
# STEP 4 - QUARANTINE BAD PAYMENTS (continued in same chapter)
# ========================================

E.bullets("Payment Validation Rules", [
    ("payment_amount must be positive", 
     "payment amount must be positive", "blue"),
    ("payment_status must be valid", 
     "payment status must be valid", "blue"),
    ("order_id must exist in orders table", 
     "order I D must exist in orders table", "blue"),
    ("Detect orphan payments early!", 
     "Detect orphan payments early!", "orange")
])

E.code("payment_quarantine CTE", '''
-- Step 4: Quarantine Invalid Payments
payment_quarantine AS (
  SELECT
    p.payment_id,
    p.order_id,
    p.payment_amount,
    p.payment_status,
    CASE
      WHEN p.payment_amount IS NULL OR p.payment_amount <= 0
        THEN 'Invalid payment amount'
      WHEN p.payment_status NOT IN ('SUCCESS', 'FAILED', 'PENDING')
        THEN 'Invalid payment status'
      WHEN p.order_id NOT IN (SELECT order_id FROM orders)
        THEN 'Orphan payment - order does not exist'
      ELSE 'Unknown issue'
    END AS rejection_reason,
    CURRENT_TIMESTAMP AS rejected_at
  FROM latest_payments p
  WHERE p.payment_amount IS NULL
     OR p.payment_amount <= 0
     OR p.payment_status NOT IN ('SUCCESS', 'FAILED', 'PENDING')
     OR p.order_id NOT IN (SELECT order_id FROM orders)
)''', [
    (15, "The subquery checks if order_id exists", None),
    (16, "This catches orphan payments like PAY-504", None)
])

E.warn("Common Payment Issues", [
    ("Orphan Payment: PAY-504 references order 9999 (doesn't exist)", 
     "Orphan Payment, payment 504 references order 9999 which doesn't exist"),
    ("Never convert NULL amounts to zero!", 
     "Never convert null amounts to zero!"),
    ("Case sensitivity matters: 'success' ≠ 'SUCCESS'", 
     "Case sensitivity matters, lowercase success is not equal to uppercase success")
])

# ========================================
# CHAPTER 7: RECONCILIATION
# ========================================
E.chapter("Reconciliation")

E.story("Matching Orders and Payments", [
    ("N", "Now we match completed orders with their payments", 
     "Now we match completed orders with their payments"),
    ("M", "We use LEFT JOIN to find missing payments", 
     "We use left join to find missing payments", "point"),
    ("A", "Why not INNER JOIN?", 
     "Why not inner join?", "think")
])

E.compare("JOIN Type Comparison", [
    ("INNER JOIN", "Only returns matched orders\nHides missing payments\nLoses critical data!", "red",
     "Inner join only returns matched orders, hides missing payments, and loses critical data!"),
    ("LEFT JOIN", "Returns all completed orders\nShows missing payments as NULL\nReveals data quality issues!", "green",
     "Left join returns all completed orders, shows missing payments as null, and reveals data quality issues!")
])

E.code("order_payment_reconciliation", '''
-- Step 5: Reconcile Orders with Payments
order_payment_reconciliation AS (
  SELECT
    o.order_id,
    o.customer_id,
    o.expected_amount,
    p.total_payment AS successful_payment_amount,
    CASE
      WHEN p.total_payment IS NULL THEN 'MISSING_PAYMENT'
      WHEN p.payment_count > 1 THEN 'MULTIPLE_SUCCESSFUL_PAYMENTS'
      WHEN p.total_payment = o.expected_amount THEN 'MATCHED'
      ELSE 'AMOUNT_MISMATCH'
    END AS reconciliation_status,
    COALESCE(o.expected_amount - p.total_payment, o.expected_amount)
      AS difference_amount
  FROM validated_orders o
  LEFT JOIN (
    SELECT
      order_id,
      SUM(payment_amount) AS total_payment,
      COUNT(*) AS payment_count
    FROM latest_payments
    WHERE payment_status = 'SUCCESS'
    GROUP BY order_id
  ) p ON o.order_id = p.order_id
  WHERE o.order_status = 'COMPLETED'
)''', [
    (7, "NULL payment means order has no successful payment", None),
    (8, "Multiple payments might indicate data issues", None),
    (9, "Exact match is ideal case", None),
    (11, "COALESCE handles NULL payments gracefully", None),
    (14, "LEFT JOIN from orders reveals missing payments", None)
])

E.add("reconciliation_visual", [
    B("Reconciliation produces four possible statuses", [
        T("Reconciliation Outcomes"),
        text(180, 180, "MATCHED", 20, "green"),
        text(420, 180, "AMOUNT_MISMATCH", 18, "orange"),
        text(700, 180, "MISSING_PAYMENT", 18, "red"),
        text(980, 180, "MULTIPLE_PAYMENTS", 16, "violet")
    ], acts=[
        A("s1", "stamp_ok", (0.0, 140, 240, {"pop": 1})),
        A("s2", "stamp_error", (0.25, 370, 240, {"pop": 1})),
        A("s3", "stamp_rejected", (0.5, 650, 240, {"pop": 1})),
        A("s4", "stamp_6rows", (0.75, 940, 240, {"pop": 1}))
    ], sfx=[("ding", 0.0)])
])

E.tables("Reconciliation Results", [
    ("reconciliation",
     ["order_id", "expected", "paid", "status", "diff"],
     [["2001", "100.00", "100.00", "MATCHED", "0.00"],
      ["2002", "120.00", "100.00", "AMOUNT_MISMATCH", "20.00"],
      ["2004", "75.00", "NULL", "MISSING_PAYMENT", "75.00"]],
     "Order 2001 is perfect, 2002 is short, 2004 is missing!", {"0": "green", "1": "orange", "2": "red"})
])

# ========================================
# CHAPTER 8: SUMMARY AND BEST PRACTICES
# ========================================
E.chapter("Summary and Best Practices")

E.story("Creating the Summary Report", [
    ("N", "Finance needs a daily summary to close the books", 
     "Finance needs a daily summary to close the books"),
    ("M", "We aggregate all reconciliation results", 
     "We aggregate all reconciliation results", "point"),
    ("A", "This is what management sees every day!", 
     "This is what management sees every day!", "happy")
])

E.code("daily_finance_summary", '''
-- Step 6: Daily Financial Summary
SELECT
  CAST(order_timestamp AS DATE) AS business_date,
  COUNT(*) AS completed_order_count,
  SUM(expected_amount) AS expected_order_revenue,
  SUM(successful_payment_amount) AS successful_payment_total,
  SUM(CASE WHEN reconciliation_status = 'MATCHED' THEN 1 ELSE 0 END)
    AS matched_order_count,
  SUM(CASE WHEN reconciliation_status = 'AMOUNT_MISMATCH' THEN 1 ELSE 0 END)
    AS mismatched_order_count,
  SUM(CASE WHEN reconciliation_status = 'MISSING_PAYMENT' THEN 1 ELSE 0 END)
    AS missing_payment_count,
  SUM(CASE WHEN reconciliation_status != 'MATCHED'
      THEN difference_amount ELSE 0 END)
    AS unreconciled_amount
FROM order_payment_reconciliation
GROUP BY CAST(order_timestamp AS DATE)
ORDER BY business_date DESC;''', [
    (4, "Conditional aggregation counts each status", None),
    (13, "Unreconciled amount shows total discrepancy", None),
    (15, "Group by date for daily summaries", None)
])

E.tables("Sample Daily Summary", [
    ("summary",
     ["business_date", "completed", "expected", "paid", "matched", "issues"],
     [["2026-10-04", "2", "220.00", "200.00", "1", "1"],
      ["2026-10-05", "1", "75.00", "75.00", "1", "0"]],
     "This is the trustworthy report finance needs!", {"0": "orange", "1": "green"})
])

# ========================================
# KEY CONCEPTS REVIEW (continued in same chapter)
# ========================================

E.bullets("Critical Data Quality Principles", [
    ("Never silently discard bad records", 
     "Never silently discard bad records", "red"),
    ("Always quarantine with explicit reasons", 
     "Always quarantine with explicit reasons", "orange"),
    ("Deduplicate before reconciliation", 
     "Deduplicate before reconciliation", "blue"),
    ("Use LEFT JOIN to reveal missing data", 
     "Use left join to reveal missing data", "blue"),
    ("Handle NULLs explicitly with COALESCE", 
     "Handle nulls explicitly with coalesce", "blue"),
    ("Create audit trails for investigations", 
     "Create audit trails for investigations", "green")
])

E.compare("Anti-Patterns vs Best Practices", [
    ("Anti-Pattern", "Converting NULL to 0\nUsing INNER JOIN only\nDeleting bad records\nIgnoring duplicates", "red",
     "Anti patterns include converting null to zero, using inner join only, deleting bad records, and ignoring duplicates"),
    ("Best Practice", "Quarantine invalid data\nUSE LEFT JOIN\nPreserve with reasons\nDeduplicate deterministically", "green",
     "Best practices include quarantining invalid data, using left join, preserving records with reasons, and deduplicating deterministically")
])

# Practice exercise
E.practice(1,
    "What happens if we use INNER JOIN instead of LEFT JOIN?",
    '''-- Wrong approach
SELECT o.order_id, p.payment_amount
FROM validated_orders o
INNER JOIN payments p ON o.order_id = p.order_id

-- This HIDES orders with missing payments!
-- We lose critical data quality information.
-- Always use LEFT JOIN when checking for missing data.''',
    [
        (6, "Inner join only shows orders that HAVE payments", 
         "Inner join only shows orders that have payments"),
        (7, "Missing payments become invisible to the business", 
         "Missing payments become invisible to the business"),
        (8, "This is a dangerous data quality blind spot!", 
         "This is a dangerous data quality blind spot!")
    ],
    total=1,
    atitle="Practice 1: Why LEFT JOIN Matters"
)

# Memory hook
E.hook("LEFT reveals what's missing",
       "What SQL pattern helps you find missing payments?",
       "Use LEFT JOIN starting from orders to reveal NULL payments! Never use INNER JOIN when you need to detect missing data.",
       "LEFT JOIN = Find Missing")

# ========================================
# EDGE CASES TO CONSIDER (continued in same chapter)
# ========================================

E.bullets("Additional Scenarios to Handle", [
    ("Split payments: One order, multiple successful payments", 
     "Split payments, one order with multiple successful payments", "orange"),
    ("Refunds: Negative payment amounts", 
     "Refunds represented as negative payment amounts", "orange"),
    ("Late payments: Payment arrives next day", 
     "Late payments that arrive the next day", "orange"),
    ("Status changes: Payment later becomes REFUNDED", 
     "Status changes where a payment later becomes refunded", "orange"),
    ("Penny differences: Rounding in different systems", 
     "Penny differences due to rounding in different systems", "blue"),
    ("Case sensitivity: 'success' vs 'SUCCESS'", 
     "Case sensitivity issues with lowercase success versus uppercase", "red")
])

E.flow("Handling Split Payments", [
    ("Order\n$100", "Customer places one order", "blue"),
    ("Payment 1\n$60", "First partial payment", "green"),
    ("Payment 2\n$40", "Second partial payment", "green"),
    ("SUM = $100\nMATCHED", "Sum of payments equals order amount", "teal")
], note=("Our solution already handles this with SUM()!", 
         "Our solution already handles this with sum function!"))

E.add("computer_reconciliation", [
    B("Modern systems use automated reconciliation daily", [
        T("Production System Architecture"),
        text(200, 160, "Daily ETL", 20, "blue"),
        text(500, 160, "Validation", 20, "orange"),
        text(780, 160, "Reconciliation", 18, "green"),
        text(960, 160, "Alerts", 20, "red")
    ], acts=[
        A("etl", "server_rack", (0.0, 160, 220, {"pop": 1})),
        A("validate", "cpu_chip", (0.3, 460, 240, {"pop": 1})),
        A("reconcile", "ram_stick", (0.5, 710, 240, {"pop": 1})),
        A("alert", "router", (0.7, 930, 240, {"pop": 1}))
    ], host="point")
])

# ========================================
# INTERVIEW INSIGHTS (continued in same chapter)
# ========================================

E.story("Common Interview Questions", [
    ("N", "These concepts come up frequently in data engineering interviews", 
     "These concepts come up frequently in data engineering interviews"),
    ("A", "What should I focus on?", 
     "What should I focus on?", "think"),
    ("M", "Understand the WHY behind each design decision", 
     "Understand the why behind each design decision", "point")
])

E.bullets("Top Interview Questions", [
    ("Q: Why quarantine instead of delete?", 
     "Question, why quarantine instead of delete?", "blue"),
    ("A: Enables root cause analysis and system fixes", 
     "Answer, enables root cause analysis and system fixes", "green"),
    ("Q: Why deduplicate before reconciliation?", 
     "Question, why deduplicate before reconciliation?", "blue"),
    ("A: Prevents double-counting and inflated totals", 
     "Answer, prevents double counting and inflated totals", "green"),
    ("Q: How does INNER JOIN hide problems?", 
     "Question, how does inner join hide problems?", "blue"),
    ("A: It drops unmatched orders, losing visibility", 
     "Answer, it drops unmatched orders, losing visibility", "green")
])

E.bullets("Key Technical Concepts", [
    ("CTEs: Break complex queries into logical steps", 
     "C T Es break complex queries into logical steps", "teal"),
    ("Window Functions: Enable deduplication with ROW_NUMBER", 
     "Window functions enable deduplication with row number", "teal"),
    ("LEFT JOIN: Reveals missing relationships", 
     "Left join reveals missing relationships", "teal"),
    ("COALESCE: Handles NULL values explicitly", 
     "Coalesce handles null values explicitly", "teal"),
    ("Conditional Aggregation: Counts by status in one query", 
     "Conditional aggregation counts by status in one query", "teal")
])

# ========================================
# OUTRO
# ========================================
E.outro([
    ("You learned data quality validation and quarantine patterns", 
     "You learned data quality validation and quarantine patterns"),
    ("You mastered payment deduplication with ROW_NUMBER", 
     "You mastered payment deduplication with row number"),
    ("You built order-payment reconciliation with LEFT JOIN", 
     "You built order payment reconciliation with left join"),
    ("You created a trustworthy daily financial summary", 
     "You created a trustworthy daily financial summary"),
    ("Tomorrow: We'll tackle slowly changing dimensions!", 
     "Tomorrow we'll tackle slowly changing dimensions!")
], "Day 3: Slowly Changing Dimensions")

E.build()
