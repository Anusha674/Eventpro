"""
Fix all placeholder password hashes in the database.
Run this ONCE after setting up the database with seed_data.sql.

Admin:     username=admin,     password=admin123
Customers: all use              password=password123
"""
import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config

conn = mysql.connector.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME
)
cursor = conn.cursor()

# Fix admin password
admin_hash = generate_password_hash('admin123')
cursor.execute("UPDATE Admin SET Password = %s WHERE Username = 'admin'", (admin_hash,))
print("[OK] Admin password fixed -> username: admin | password: admin123")

# Fix all customer passwords
customer_hash = generate_password_hash('password123')
cursor.execute("UPDATE Customer SET Password = %s", (customer_hash,))
print("[OK] All customer passwords fixed -> password: password123")

# Show customer emails for reference
cursor.execute("SELECT Email FROM Customer ORDER BY C_ID")
emails = cursor.fetchall()
print("")
print("Customer login emails:")
for email in emails:
    print(f"  - {email[0]}")

conn.commit()
conn.close()
print("")
print("All passwords fixed! You can now log in.")
