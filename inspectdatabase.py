import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Select all the rows from the contact_form table
cursor.execute("SELECT * FROM contact_form")
rows = cursor.fetchall()

# Display the data in a readable format as tuples, each on a new line
if rows:
    for row in rows:
        # Display each row as a tuple
        print(f"({row[0]}, '{row[1]}', '{row[2]}', '{row[3]}')")
        print()  # Print a newline for separation between rows
else:
    print("No data available in the table.")

# Close the connection
conn.close()
