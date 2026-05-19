import sqlite3
from pathlib import Path

# SQLite database path (from config default)
db_path = "./inventory.db"
db_full_path = Path(db_path)

print(f"Database path: {db_full_path}")
print(f"Database exists: {db_full_path.exists()}")
print("-" * 50)

if db_full_path.exists():
    conn = sqlite3.connect(str(db_full_path))
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    expected_tables = [
        "user",
        "role",
        "product",
        "inventory",
        "salesorder",
        "purchaseorder",
        "stocktransaction",
    ]

    print("Expected tables:")
    for table in expected_tables:
        print(f"  - {table}")

    print("\n" + "-" * 50)
    print("Actual tables in database:")

    if tables:
        actual_table_names = [t[0] for t in tables]
        for table in actual_table_names:
            print(f"  ✓ {table}")
    else:
        print("  ✗ No tables found!")

    print("\n" + "-" * 50)
    print("Status:")

    actual_table_names = [t[0] for t in tables]
    missing_tables = [t for t in expected_tables if t not in actual_table_names]

    if not missing_tables:
        print("✓ All expected tables exist!")
    else:
        print(f"✗ Missing tables: {', '.join(missing_tables)}")

    conn.close()
else:
    print("✗ Database file does not exist!")
    print(f"  Expected at: {db_full_path.absolute()}")
