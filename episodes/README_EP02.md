# Episode 2: SQL Order-Payment Reconciliation

## 🎬 Video Overview

**Title**: Day 2 - SQL Project 2: Order-Payment Data Quality and Reconciliation  
**Duration**: ~7.9 minutes (estimated)  
**Difficulty**: Intermediate  
**Topics**: Data Quality, Validation, Reconciliation, SQL Best Practices

---

## 📚 What This Video Teaches

### Business Problem
An e-commerce company faces critical data quality issues:
- Duplicate payments in the system
- Successful orders missing their payments
- Payment amounts that don't match order totals
- Payments referencing non-existent orders
- Invalid records entering financial reports

### Learning Objectives
By the end of this video, you'll understand:

1. **Data Quality Validation**
   - How to validate orders and payments
   - When and why to quarantine bad records
   - How to preserve rejected records with explicit reasons

2. **Payment Deduplication**
   - Using ROW_NUMBER() for deterministic deduplication
   - Choosing the latest version with tie-breakers
   - Handling duplicate payment records

3. **Reconciliation Techniques**
   - Why LEFT JOIN reveals missing data
   - How to match orders with payments
   - Detecting four reconciliation statuses (MATCHED, AMOUNT_MISMATCH, MISSING_PAYMENT, MULTIPLE_PAYMENTS)

4. **Financial Reporting**
   - Creating trustworthy daily summaries
   - Using conditional aggregation
   - Building audit trails

---

## 🎭 Video Structure

### Chapter 1: The Business Challenge (3 scenes)
- Finance team's nightmare
- Data quality problems discovered
- Business impact visualization

### Chapter 2: Understanding the Data (4 scenes)
- Orders and payments table structures
- System architecture
- Data flow visualization
- **Characters used**: laptop_blue, monitor_green, server_rack

### Chapter 3: Examining Real Data (4 scenes)
- Sample orders with issues highlighted
- Sample payments with problems
- Visual identification of data quality issues
- **Characters used**: stamp_null, stamp_error

### Chapter 4: Building the Solution (2 scenes)
- Six-step solution strategy
- Process flow visualization

### Chapter 5: Validation and Quarantine (8 scenes)
- Order validation rules
- validated_orders CTE implementation
- Quality gate visualization
- Order quarantine design
- Quarantine decision patterns
- **Characters used**: cube_blue, router, cube_green

### Chapter 6: Payment Processing (8 scenes)
- The duplicate problem explained
- Deduplication strategy with ROW_NUMBER()
- latest_payments CTE
- Payment validation rules
- payment_quarantine CTE
- Common payment issues
- **Characters used**: stamp_6rows, cpu_chip, stamp_ok

### Chapter 7: Reconciliation (6 scenes)
- Matching orders and payments
- INNER JOIN vs LEFT JOIN comparison
- order_payment_reconciliation CTE
- Four reconciliation statuses explained
- Reconciliation results visualization
- **Characters used**: stamp_ok, stamp_error, stamp_rejected

### Chapter 8: Summary and Best Practices (16 scenes)
- Daily financial summary query
- Sample summary report
- Key concepts review
- Anti-patterns vs best practices
- Practice exercise on JOIN types
- Memory hook
- Edge cases (split payments, refunds, late payments)
- Production system architecture
- Interview-ready answers
- Technical concepts summary
- **Characters used**: server_rack, cpu_chip, ram_stick, router

---

## 💻 SQL Techniques Covered

### Window Functions
```sql
ROW_NUMBER() OVER (
  PARTITION BY payment_id
  ORDER BY updated_at DESC, payment_record_id DESC
) AS rn
```
Used for deterministic payment deduplication.

### CTEs (Common Table Expressions)
- validated_orders
- order_quarantine
- latest_payments
- payment_quarantine
- order_payment_reconciliation

### LEFT JOIN Pattern
```sql
FROM validated_orders o
LEFT JOIN (
  SELECT order_id, SUM(payment_amount) AS total_payment
  FROM latest_payments
  WHERE payment_status = 'SUCCESS'
  GROUP BY order_id
) p ON o.order_id = p.order_id
```
Reveals missing payments (NULL values).

### COALESCE for NULL Handling
```sql
COALESCE(o.expected_amount - p.total_payment, o.expected_amount)
  AS difference_amount
```

### Conditional Aggregation
```sql
SUM(CASE WHEN reconciliation_status = 'MATCHED' THEN 1 ELSE 0 END)
  AS matched_order_count
```

### CASE Statements
```sql
CASE
  WHEN p.total_payment IS NULL THEN 'MISSING_PAYMENT'
  WHEN p.payment_count > 1 THEN 'MULTIPLE_SUCCESSFUL_PAYMENTS'
  WHEN p.total_payment = o.expected_amount THEN 'MATCHED'
  ELSE 'AMOUNT_MISMATCH'
END AS reconciliation_status
```

---

## 🎨 Visual Elements

### Characters Featured
- **Mira** (mentor) - Explains complex concepts with pointer
- **Asha** (student) - Asks questions and learns
- **Pip** (penguin host) - Bottom-right companion
- **Computer components**: laptop_blue, monitor_green, server_rack, cpu_chip, ram_stick, router
- **Stamps**: stamp_null, stamp_error, stamp_ok, stamp_rejected, stamp_6rows
- **Cubes**: cube_blue, cube_green (data visualization)

### Color Coding
- **Green**: Valid data, success, matched records
- **Red**: Critical errors, rejected records
- **Orange**: Warnings, mismatches, issues
- **Blue**: Information, processes
- **Violet**: Reconciliation status
- **Teal**: Technical concepts

---

## 📊 Expected Learning Outcomes

### From Sample Data
Students will verify that:
- PAY-501 appears once after deduplication (was duplicated)
- Order 2001 reconciles as MATCHED (100.00 = 100.00)
- Order 2002 is AMOUNT_MISMATCH with 20.00 difference (120.00 expected, 100.00 paid)
- Payment PAY-504 is quarantined as orphan (references non-existent order 9999)
- Latest PAY-505 version is SUCCESS (after FAILED attempt)
- Order 2003 doesn't contribute to revenue (CANCELLED status)
- Orders 2004, 2005, 2006 fail validation rules

### Key Principles Learned
1. **Never silently discard bad records** - Always quarantine with reasons
2. **Deduplicate before reconciliation** - Prevents double-counting
3. **Use LEFT JOIN** - Reveals missing relationships
4. **Handle NULLs explicitly** - With COALESCE, never convert to 0
5. **Create audit trails** - For investigation and debugging

---

## 🎯 Interview Preparation

### Key Questions Answered
1. Why quarantine instead of delete?
   - Enables root cause analysis and system fixes

2. Why deduplicate before reconciliation?
   - Prevents double-counting and inflated totals

3. How does INNER JOIN hide problems?
   - Drops unmatched orders, losing visibility of missing payments

4. What is an orphan record?
   - A payment referencing a non-existent order (or vice versa)

5. Should NULL monetary values become zero?
   - No! This masks data quality issues

---

## 🚀 How to Generate the Video

### Prerequisites
```bash
# Ensure videogen is set up
./setup.sh
```

### Generate Scenes
```bash
# Run the episode script
python3 episodes/ep02_sql_order_payment_reconciliation.py
```

This creates:
- 58 Excalidraw scene files in `series_out/ep02/`
- `plan.json` with timing and narration
- `script.md` with full transcript

### Render Video (if render tools available)
```bash
cd render
./run_video.sh 2
```

This produces:
- `OUT/final/ep02.mp4` - Complete video with narration
- `OUT/final/ep02.srt` - Subtitle file

---

## 🎤 Narration Features

### Female Voice Narrator
- **Voice**: Piper TTS `en_US-amy-medium`
- **Age range**: 21-25 years old
- **Tone**: Clear, friendly, approachable
- **Style**: Educational, conversational

### Speaking Time
- **Total**: ~7.9 minutes
- **Words**: 1,112 spoken words
- **Scenes**: 58 visual scenes
- **Beats**: 156 narration beats

---

## 📁 Generated Files

```
series_out/ep02/
├── 00_intro.excalidraw                    # Introduction with agenda
├── 01_chapter1.excalidraw                 # Chapter 1: Business Challenge
├── 02_story.excalidraw                    # Finance team's nightmare
├── 03_bullets.excalidraw                  # Data quality problems
├── 04_business_impact.excalidraw          # Business consequences
├── 05_chapter2.excalidraw                 # Chapter 2: Data sources
├── 06_story.excalidraw                    # Two data sources
├── 07_tables.excalidraw                   # Orders table structure
├── 08_tables.excalidraw                   # Payments table structure
├── 09_data_flow.excalidraw                # System architecture
├── 10_chapter3.excalidraw                 # Chapter 3: Sample data
├── 11_tables.excalidraw                   # Sample orders
├── 12_spot_issues.excalidraw              # Issues highlighted
├── 13_bullets.excalidraw                  # Orders issues list
├── 14_tables.excalidraw                   # Sample payments
├── 15_bullets.excalidraw                  # Payments issues list
├── 16_chapter4.excalidraw                 # Chapter 4: Solution
├── 17_story.excalidraw                    # Strategy overview
├── 18_flow.excalidraw                     # Six-step solution
├── 19_chapter5.excalidraw                 # Chapter 5: Validation
├── 20_bullets.excalidraw                  # Validation rules
├── 21_code.excalidraw                     # validated_orders CTE
├── 22_validation_visual.excalidraw        # Quality gate
├── 23_story.excalidraw                    # Quarantine importance
├── 24_code.excalidraw                     # order_quarantine CTE
├── 25_bullets.excalidraw                  # Quarantine design
├── 26_chapter6.excalidraw                 # Chapter 6: Payments
├── 27_story.excalidraw                    # Duplicate problem
├── 28_duplicate_example.excalidraw        # PAY-501 example
├── 29_bullets.excalidraw                  # Deduplication strategy
├── 30_code.excalidraw                     # latest_payments CTE
├── 31_dedup_visual.excalidraw             # Dedup visualization
├── 32_bullets.excalidraw                  # Payment validation
├── 33_code.excalidraw                     # payment_quarantine CTE
├── 34_mistakes.excalidraw                 # Common issues
├── 35_chapter7.excalidraw                 # Chapter 7: Reconciliation
├── 36_story.excalidraw                    # Matching strategy
├── 37_compare.excalidraw                  # INNER vs LEFT JOIN
├── 38_code.excalidraw                     # Reconciliation CTE
├── 39_reconciliation_visual.excalidraw    # Four statuses
├── 40_tables.excalidraw                   # Results sample
├── 41_chapter8.excalidraw                 # Chapter 8: Summary
├── 42_story.excalidraw                    # Finance summary
├── 43_code.excalidraw                     # Summary query
├── 44_tables.excalidraw                   # Summary report
├── 45_bullets.excalidraw                  # Key principles
├── 46_compare.excalidraw                  # Anti-patterns vs best
├── 47_practice1_q.excalidraw              # Practice question
├── 48_practice1_a.excalidraw              # Practice answer
├── 49_hook.excalidraw                     # Memory hook
├── 50_quiz1.excalidraw                    # Quiz pause
├── 51_bullets.excalidraw                  # Edge cases
├── 52_flow.excalidraw                     # Split payments
├── 53_computer_reconciliation.excalidraw  # Production systems
├── 54_story.excalidraw                    # Interview prep
├── 55_bullets.excalidraw                  # Interview questions
├── 56_bullets.excalidraw                  # Technical concepts
├── 57_outro.excalidraw                    # Outro and next steps
├── plan.json                              # Video plan
└── script.md                              # Full transcript
```

---

## 🎓 Educational Design

### Pedagogical Approach
1. **Problem First**: Start with real business pain
2. **Show Don't Tell**: Visualize data and processes
3. **Build Understanding**: Step-by-step from basics to complex
4. **Practice**: Interactive exercise with pause
5. **Reinforce**: Memory hooks and summaries
6. **Prepare**: Interview-ready explanations

### Learning Styles Addressed
- **Visual**: Diagrams, flowcharts, color-coded tables
- **Auditory**: Clear female narration with conversational tone
- **Kinesthetic**: Practice exercise (students code along)
- **Reading/Writing**: Code examples, bullet points, tables

### Retention Techniques
- **Memory Hook**: "LEFT reveals what's missing"
- **Practice Exercise**: Why LEFT JOIN matters
- **Repetition**: Key concepts repeated in different contexts
- **Visualization**: Computer components represent abstract concepts
- **Storytelling**: Mira and Asha dialogue format

---

## 💡 Tips for Students

### Before Watching
1. Have a SQL environment ready for practice
2. Review basic SQL (SELECT, WHERE, JOIN)
3. Understand what CTEs are (or learn during video)

### During Watching
1. Pause at practice exercises
2. Try to spot data issues before they're revealed
3. Code along with the SQL examples
4. Take notes on the "why" behind decisions

### After Watching
1. Implement the solution with your own data
2. Test the edge cases mentioned
3. Review the interview questions
4. Try the stretch challenge (data quality summary)

---

## 🔗 Related Resources

### From This Project
- **QUICK_START.md** - Get started with videogen
- **CHARACTER_SHOWCASE.md** - All characters used
- **ENHANCEMENTS.md** - Technical documentation

### Next Episodes
- **Episode 3**: Slowly Changing Dimensions (mentioned in outro)

---

## 🎉 Summary

This educational video demonstrates:
- ✅ Real-world data quality challenges
- ✅ SQL best practices for validation and reconciliation
- ✅ Visual explanations with colorful characters
- ✅ Professional female narrator
- ✅ Interview preparation
- ✅ Production-ready patterns
- ✅ 58 beautifully crafted scenes
- ✅ ~7.9 minutes of comprehensive learning

**Perfect for**: Data engineers, SQL developers, analysts learning data quality, interview preparation

**Difficulty**: Intermediate (requires basic SQL knowledge)

**Value**: Production-ready code patterns + theoretical understanding + interview prep

---

Created with ❤️ using the enhanced videogen toolkit with vibrant colors and female narration!
