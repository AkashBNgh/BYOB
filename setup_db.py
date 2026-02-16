import sqlite3

def create_dummy_db():
    conn = sqlite3.connect('music_store.db')
    cursor = conn.cursor()

    # Create a table named 'Invoices' to match the PDF context
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invoices (
            InvoiceId INTEGER PRIMARY KEY,
            BillingCountry TEXT,
            Total REAL
        )
    ''')

    # Insert sample data (Data from your PDF source)
    data = [
        ('Argentina', 37.62),
        ('Australia', 37.62),
        ('Austria', 42.62),
        ('Belgium', 37.62),
        ('Brazil', 190.10),
        ('Canada', 303.96),
        ('Chile', 46.62),
        ('USA', 500.00),
        ('Germany', 150.00)
    ]
    
    cursor.executemany('INSERT INTO Invoices (BillingCountry, Total) VALUES (?, ?)', data)
    
    conn.commit()
    print("Database 'music_store.db' created successfully with dummy data.")
    conn.close()

if __name__ == "__main__":
    create_dummy_db()