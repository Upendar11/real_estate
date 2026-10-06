import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *

E = StoryEp(1, "What Is SQL? The Language of the Data City")
E.intro(["The dashboard that looked too good", "SQL, databases, tables, rows and columns", "The five families of SQL commands",
         "The keywords you will use most, and your first query"],
        say_hello="Hi! I'm Pip, and welcome to SQL for Data Engineers. In this course we follow Asha, a curious student, and Mira, her mentor, "
                  "on the journey from writing SQL that runs, to building data people can trust. Episode one: What is SQL? The language of the data city.")

E.chapter("The dashboard that looked too good")
E.story("The opening scene", [
    ("N", "Asha's first dashboard says Northstar Market's revenue DOUBLED overnight. The team celebrates.",
     "Asha's first dashboard says Northstar Market's revenue doubled overnight. The whole team celebrates."),
    ("M", "What does one row mean?", "Mira asks one question. What does one row mean?", "point"),
    ("A", "One sale?", "Asha guesses: one sale?", "think"),
    ("M", "Show me the joins.", "Mira says: show me the joins."),
])
items = [[1, "Keyboard"], [1, "Mouse"]]
pays = [[1, "card A"], [1, "card B"], [1, "voucher"]]
joined = [[1, i[1], p[1]] for i in items for p in pays]
E.add("fanout", [
    B("Here's what happened. One order had two items...", [T("One order, 2 items × 3 payments"),
        E.table_els(60, 130, ["order_id", "item"], items, [130, 160], rh=42, fs=20, color="blue")]),
    B("...and three payments.", [E.table_els(60, 300, ["order_id", "payment"], pays, [130, 160], rh=42, fs=20, color="orange")]),
    B("A careless join matched every item with every payment. Two times three: six rows! The business did not grow. The query multiplied the evidence.", [
        line([(380, 290), (480, 290)], sw=3),
        E.table_els(500, 130, ["order_id", "item", "payment"], joined, [130, 160, 160], rh=42, fs=20, color="red")],
      acts=[A("st", "stamp_6rows", (0.55, 960, 520, {"pop": 1}))], sfx=[("buzz", 0.5)]),
])
E.bullets("Mira's three questions", [
    ("1. What does ONE ROW represent?", "Mira writes three questions on the whiteboard. One: what does one row represent?", "blue"),
    ("2. Which rows BELONG?", "Two: which rows belong?", "orange"),
    ("3. What answer does the BUSINESS need?", "Three: what answer does the business need? These questions will return in every lesson.", "green"),
    ("This course: from SQL that RUNS → to data people can TRUST.", "This is the journey from writing SQL that runs, to building data that people can trust.", "violet"),
])

E.chapter("The language of the data city")
E.story("Welcome to the data city", [
    ("N", "Asha enters a city of warehouses.", "Asha enters a city of warehouses."),
    ("M", "SQL is how we ask precise questions, and define the rules of this city.",
     "Mira explains: SQL is how we ask precise questions, and define the rules of this city.", "point"),
])
E.add("city", [
    B("Each warehouse is a database.", [T("The data city"), box(60, 120, 330, 470, "", "grey", fill="hachure"), text(225, 130, "Warehouse = DATABASE", 22, "grey", align="center")]),
    B("Each labelled shelf is a table.", [box(90, 180, 270, 170, "", "blue"), text(225, 188, "Shelf = TABLE: customers", 20, "blue", align="center"),
                                          box(90, 380, 270, 170, "", "blue"), text(225, 388, "Shelf = TABLE: orders", 20, "blue", align="center")]),
    B("Each stored record is a row, and each property is a column.", [
        E.table_els(460, 150, ["id", "name", "email"], [[1, "Asha", "asha@example.com"], [2, "Ben", "ben@example.com"], [3, "Chen", "chen@example.com"]],
                    [70, 120, 260], rh=46, fs=20, color="blue", hl={1: "orange"}),
        text(470, 360, "← one ROW = one record (Ben)", 22, "orange"), text(600, 410, "↑ each COLUMN = one property", 22, "blue")]),
])
E.compare("Who does what?", [
    ("SQL", "The LANGUAGE. Structured Query Language: the standard language for managing relational databases.", "blue",
     "Let's separate four words people mix up. SQL, Structured Query Language, is the language: the standard way to talk to relational databases. "
     "Just like we use English or Hindi to communicate with each other, SQL is how we communicate with a database."),
    ("DBMS", "The SYSTEM that manages storage, access and execution of queries.", "orange",
     "A DBMS, a database management system, manages storage, access, and the execution of your queries."),
    ("PostgreSQL", "A DBMS: a powerful open-source relational database system.", "green",
     "PostgreSQL is one such DBMS: a powerful open-source relational database. It's the one we use in this course."),
    ("pgAdmin", "A CLIENT interface: a window you use to send SQL to the server.", "violet",
     "And pgAdmin is a client interface, the window you type SQL into."),
])
E.compare("Why SQL matters to a data engineer", [
    ("Retrieve", "Query data based on criteria, so it is accessible and easy to find.", "blue",
     "Data engineering means collecting, transforming and storing data so it's easy to analyse. SQL lets you retrieve specific data by querying it with criteria."),
    ("Manipulate", "Add, update and delete data, so it stays accurate and up to date.", "orange",
     "It lets you manipulate data: add, delete or update it, keeping it accurate and up to date."),
    ("Manage", "Create tables, define relationships, set security permissions.", "green",
     "And it lets you manage databases: create tables, define relationships between them, and set permissions, so data stays organised and secure."),
])
E.bullets("A query is a business question made executable", [
    ("Pipelines retrieve, transform, load, validate and expose data. All of it speaks SQL.",
     "In a data pipeline, you retrieve, transform, load, validate, and expose data. SQL is involved at every step.", "blue"),
    ("“Which customers bought last month?” → SELECT … FROM … WHERE …",
     "A business question like: which customers bought last month? becomes a precise, runnable query.", "green"),
])

E.chapter("The five families of SQL commands")
E.tables("SQL command families", [
    ("", ["Family", "What it controls", "Commands", "Career use"], [
        ["DDL", "Structure", "CREATE, ALTER, DROP", "Create & migrate schemas"],
        ["DML", "Rows", "INSERT, UPDATE, DELETE", "Load & correct records"],
        ["DQL (retrieval)", "Reading", "SELECT", "Explore & serve datasets"],
        ["DCL", "Access", "GRANT, REVOKE", "Give permissions"],
        ["TCL", "Transaction boundaries", "BEGIN, COMMIT, ROLLBACK", "Publish changes together"]],
     "SQL commands come in families. D D L, data definition, controls structure: CREATE, ALTER, DROP. D M L, data manipulation, controls rows: INSERT, UPDATE, DELETE. "
     "Retrieval, often called D Q L, is SELECT. D C L controls access with GRANT and REVOKE. And T C L sets transaction boundaries: BEGIN, COMMIT, ROLLBACK. "
     "These categories are teaching conventions; some materials also put SELECT under D M L."),
], fs=20, rh=46)
E.flow("Four different actions", [
    ("Structure\nDDL", "Picture them as four different actions. Building or changing the shelves: structure.", "blue"),
    ("Rows\nDML", "Putting boxes on, changing them, or taking them off: rows.", "orange"),
    ("Access\nDCL", "Deciding who holds a key to the warehouse: access.", "green"),
    ("Commit\nTCL", "And deciding when a group of changes becomes final: transactions.", "violet"),
])
E.code("DDL: define the structure", '''-- CREATE TABLE statement to create a new table with columns and data types
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
);

-- ALTER TABLE statement to add a new column to an existing table
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);

-- DROP TABLE statement to remove a table from the database
DROP TABLE customers;''', [
    (6, "D D L defines structure. CREATE TABLE builds a customers table with an integer id as primary key, and a name and email of up to fifty characters."),
    (9, "ALTER TABLE adds a new phone column to the existing table.", "customers now has: id, name, email, phone"),
    (12, "And DROP TABLE removes the table, structure and data, from the database.", "table customers is gone"),
])
E.code("DML: work with the rows", '''-- INSERT statement to add new data to a table
INSERT INTO customers (name, email) VALUES ('John Doe', 'johndoe@email.com');

-- UPDATE statement to modify existing data in a table
UPDATE customers SET email = 'new@email.com' WHERE name = 'John Doe';

-- DELETE statement to remove data from a table
DELETE FROM customers WHERE name = 'John Doe';''', [
    (2, "D M L manipulates rows. INSERT adds a new row: John Doe with his email."),
    (5, "UPDATE changes existing data: set John Doe's email to new at email dot com."),
    (8, "DELETE removes rows: here, John Doe's row."),
])
E.warn("Debugging scene: why did that INSERT fail?", [
    ("The original table has id INT PRIMARY KEY with no default. The INSERT omits id → ERROR: null value in column \"id\".",
     "Careful! Against that customers table, the INSERT fails. The id is an integer primary key with no default, and the insert leaves it out, so Postgres refuses a null id."),
    ("Fix: give the id a generator, e.g. GENERATED ALWAYS AS IDENTITY (or SERIAL), or supply the id yourself.",
     "The fix: let the database generate the id, using GENERATED ALWAYS AS IDENTITY, or SERIAL, or supply the id yourself."),
])
E.code("DCL: control access (corrected for PostgreSQL)", '''-- The original notes show MySQL-style syntax (does NOT run in PostgreSQL):
--   CREATE USER 'new_user' IDENTIFIED BY 'password';

-- PostgreSQL:
CREATE USER new_user WITH PASSWORD 'example_only';
GRANT SELECT, INSERT, UPDATE ON customers TO new_user;''', [
    (2, "D C L controls access. The original notes show CREATE USER, quote new user, IDENTIFIED BY. That's MySQL-style syntax and does not run in Postgres."),
    (5, "In Postgres, write CREATE USER new_user WITH PASSWORD. A user is really a role that can log in. And a password in a teaching example is not how you manage real credentials."),
    (6, "Then GRANT gives the new user permission to SELECT, INSERT and UPDATE on customers. Object grants also need access to the database and schema.", "new_user can read, add and change customers"),
])
E.code("TCL: transaction boundaries", '''-- BEGIN TRANSACTION statement to start a new transaction
BEGIN TRANSACTION;

-- COMMIT statement to save changes made during a transaction
COMMIT;

-- ROLLBACK statement to undo changes made during a transaction
ROLLBACK;''', [
    (2, "T C L manages transactions. BEGIN TRANSACTION starts a unit of work."),
    (5, "COMMIT saves the changes made during the transaction."),
    (8, "ROLLBACK undoes the uncommitted changes instead. We'll see a full example with ACID in episode nine."),
])

E.chapter("Keywords and your first query")
E.bullets("80% of the work with 20% of the keywords", [
    ("SELECT · FROM · WHERE · JOIN", "SQL has hundreds of keywords, but about fifteen to twenty do eighty percent of the work. SELECT retrieves data. FROM names the table. WHERE filters. JOIN combines tables.", "blue"),
    ("GROUP BY · ORDER BY · HAVING", "GROUP BY groups rows. ORDER BY sorts them. HAVING filters grouped data.", "orange"),
    ("INSERT · UPDATE · DELETE", "INSERT, UPDATE and DELETE change rows.", "green"),
    ("CREATE · ALTER · DROP", "CREATE makes a database, table or view. ALTER changes an object's structure. DROP deletes one.", "violet"),
    ("Aggregates MIN · MAX · AVG · COUNT  ·  JOINS INNER · LEFT · FULL", "Aggregation functions like MIN, MAX, AVG and COUNT summarise. Joins, inner, left and full, combine tables.", "teal"),
    ("CASE statement · Window functions RANK · DENSE_RANK · ROW_NUMBER", "CASE adds conditional logic, and window functions like RANK, DENSE_RANK and ROW_NUMBER number and rank rows.", "yellow"),
])
E.code("Your first table and query", '''CREATE TABLE customers_intro (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);
INSERT INTO customers_intro (name, email)
VALUES ('Asha', 'asha@example.com');
SELECT name, email FROM customers_intro;''', [
    (5, "Now Asha writes her first table. CREATE builds the shelf. The id is generated automatically as an identity, so we never have to supply it."),
    (7, "INSERT adds a record: Asha and her email. The generated identity supplies the required id."),
    (8, "SELECT projects the columns we ask for: name and email. FROM names the source.", "name | email\nAsha | asha@example.com"),
])
E.code("Basic SELECT and WHERE", '''SELECT * FROM table_name;
-- or
SELECT col_1, col_2, col_3 FROM table_name;

-- Example
SELECT * FROM customers;
SELECT CustomerID, City, Country FROM customers;

-- WHERE filters rows, e.g. customers in New York
SELECT * FROM customers WHERE City = 'New York';''', [
    (3, "The basic patterns. SELECT star returns every column. Or list the columns you need: col one, col two, col three. These are templates, not real tables."),
    (7, "For example: everything from customers, or just CustomerID, City and Country."),
    (10, "And WHERE filters rows by a condition: here, only customers whose city is New York.", "only the New York rows"),
])
E.hook("Structure, rows, access, commit.", "Which command changes the table itself?",
       "ALTER. It changes the table's structure. UPDATE only changes the values in its rows.", "ALTER (UPDATE changes row values)")
E.outro([
    ("SQL = the language · PostgreSQL = the DBMS · pgAdmin = a client", "SQL is the language, PostgreSQL the database system, pgAdmin a client."),
    ("DDL structure · DML rows · DQL reading · DCL access · TCL transactions", "Five families: structure, rows, reading, access, and transactions."),
    ("Ask Mira's 3 questions: one row? which rows? what answer?", "And always ask Mira's three questions."),
], "Installation: open the workshop before using the tools")
E.build()
