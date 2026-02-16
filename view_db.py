import sqlite3
import pandas as pd

# Change this if your DB file name is different
conn = sqlite3.connect("music_store.db")

# See all tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:\n", tables)

# Example: View first 10 rows of Invoices
df = pd.read_sql("SELECT * FROM Invoices LIMIT 10;", conn)
print("\nInvoices Preview:\n")
print(df)

conn.close()
