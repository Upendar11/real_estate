# Episode 2: Order-Payment Reconciliation

## Intro

Welcome to Day 2 of SQL Mastery! Today we're solving a real-world data quality challenge. In this episode: Understand the business problem; Learn data quality validation; Master reconciliation techniques; Build trustworthy financial reports.

## Chapter1

Part one. The Business Challenge.

## Story

An e-commerce company is facing serious data issues Finance has discovered multiple problems in our payment data That sounds concerning! What kind of problems?

## Bullets

Duplicate payments appearing in the system Successful orders missing their payments Payment amounts don't match order totals Payments referencing non-existent orders Invalid records entering financial reports Daily books cannot be closed with confidence

## Business Impact

These issues have serious business consequences!

## Chapter2

Part two. Understanding the Data.

## Story

We have two main data sources to work with First, the orders table from our sales platform And the payments table from the payment processor?

## Tables

The orders table tracks every customer purchase

## Tables

The payments table tracks all payment attempts

## Data Flow

Data flows from two independent systems

## Chapter3

Part three. Examining Real Data.

## Tables

Can you spot the data quality issues here?

## Spot Issues

Let me highlight the problems in the orders!

## Bullets

Order 2004 has a missing customer I D Order 2005 has a negative quantity of minus 2 Order 2006 has a missing unit price Order 2003 is cancelled but has a payment

## Tables

The payments table has even more issues!

## Bullets

Payment 501 appears twice as duplicates Payment 502 amount is 100 but order expects 120 Payment 503 is for a cancelled order Payment 504 references non-existent order 9999 Payment 505 has both failed and successful versions

## Chapter4

Part four. Building the Solution.

## Story

We'll solve this with a structured six step approach Each step validates, cleans, or reconciles the data And we never silently discard bad records!

## Flow

Validate all orders against quality rules Store invalid orders with rejection reasons Keep latest version of each payment Store invalid payments separately Match orders with their payments Create financial summary report

## Chapter5

Part five. Validation and Quarantine.

## Bullets

order I D must not be null customer I D must not be null quantity must be greater than zero unit price must be greater than zero order status must be in approved set Calculate expected amount equals quantity times unit price

## Code

We apply all validation rules in the WHERE clause Only records passing ALL rules make it through

## Validation Visual

Think of validation as a quality gate

## Story

Invalid records must be preserved, not deleted We quarantine them with explicit rejection reasons This helps us investigate and fix upstream issues!

## Code

We capture the FIRST rejection reason found Alternative: capture ALL reasons in comma-separated list

## Bullets

Option A, one row per order with combined reasons Option B, multiple rows per order, one per failure We choose option A for simpler analysis Always document your choice in production code!

## Chapter6

Part six. Payment Processing.

## Story

Payment systems often create duplicate records Why do duplicates happen? Retries, system issues, or versioning can cause them

## Duplicate Example

Payment PAY-501 appears twice in our data!

## Bullets

Keep the latest version by updated at timestamp Use payment record I D as tie breaker This ensures deterministic results Row number function makes this easy!

## Code

ROW_NUMBER partitions by payment_id We order by updated_at DESC to get latest first Then payment_record_id DESC breaks ties Filter rn = 1 keeps only the latest version

## Dedup Visual

Deduplication keeps one record per payment ID

## Bullets

payment amount must be positive payment status must be valid order I D must exist in orders table Detect orphan payments early!

## Code

The subquery checks if order_id exists This catches orphan payments like PAY-504

## Mistakes

Orphan Payment, payment 504 references order 9999 which doesn't exist Never convert null amounts to zero! Case sensitivity matters, lowercase success is not equal to uppercase success

## Chapter7

Part seven. Reconciliation.

## Story

Now we match completed orders with their payments We use left join to find missing payments Why not inner join?

## Compare

Inner join only returns matched orders, hides missing payments, and loses critical data! Left join returns all completed orders, shows missing payments as null, and reveals data quality issues!

## Code

NULL payment means order has no successful payment Multiple payments might indicate data issues Exact match is ideal case COALESCE handles NULL payments gracefully LEFT JOIN from orders reveals missing payments

## Reconciliation Visual

Reconciliation produces four possible statuses

## Tables

Order 2001 is perfect, 2002 is short, 2004 is missing!

## Chapter8

Part eight. Summary and Best Practices.

## Story

Finance needs a daily summary to close the books We aggregate all reconciliation results This is what management sees every day!

## Code

Conditional aggregation counts each status Unreconciled amount shows total discrepancy Group by date for daily summaries

## Tables

This is the trustworthy report finance needs!

## Bullets

Never silently discard bad records Always quarantine with explicit reasons Deduplicate before reconciliation Use left join to reveal missing data Handle nulls explicitly with coalesce Create audit trails for investigations

## Compare

Anti patterns include converting null to zero, using inner join only, deleting bad records, and ignoring duplicates Best practices include quarantining invalid data, using left join, preserving records with reasons, and deduplicating deterministically

## Practice1 Q

Practice 1 of 1. What happens if we use INNER JOIN instead of LEFT JOIN? Pause the video and write your query.

## Practice1 A

Inner join only shows orders that HAVE payments Missing payments become invisible to the business This is a dangerous data quality blind spot!

## Hook

Memory hook: LEFT reveals what's missing

## Quiz1

Quick quiz! Question one. What SQL pattern helps you find missing payments? Pause and think. Use LEFT JOIN starting from orders to reveal NULL payments! Never use INNER JOIN when you need to detect missing data.

## Bullets

Split payments, one order with multiple successful payments Refunds represented as negative payment amounts Late payments that arrive the next day Status changes where a payment later becomes refunded Penny differences due to rounding in different systems Case sensitivity issues with lowercase success versus uppercase

## Flow

Customer places one order First partial payment Second partial payment Sum of payments equals order amount Our solution already handles this with sum function!

## Computer Reconciliation

Modern systems use automated reconciliation daily

## Story

These concepts come up frequently in data engineering interviews What should I focus on? Understand the why behind each design decision

## Bullets

Question, why quarantine instead of delete? Answer, enables root cause analysis and system fixes Question, why deduplicate before reconciliation? Answer, prevents double counting and inflated totals Question, how does inner join hide problems? Answer, it drops unmatched orders, losing visibility

## Bullets

C T Es break complex queries into logical steps Window functions enable deduplication with row number Left join reveals missing relationships Coalesce handles null values explicitly Conditional aggregation counts by status in one query

## Outro

Let's recap. You learned data quality validation and quarantine patterns You mastered payment deduplication with row number You built order payment reconciliation with left join You created a trustworthy daily financial summary Tomorrow we'll tackle slowly changing dimensions! Next time: Day 3: Slowly Changing Dimensions. See you there!

