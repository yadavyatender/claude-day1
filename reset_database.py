import os

# Delete old database to recreate with new schema
db_file = "gold_rates.db"

if os.path.exists(db_file):
    try:
        os.remove(db_file)
        print(f"✓ Deleted old database: {db_file}")
        print("✓ New database will be created with AED-only schema on next run")
    except Exception as e:
        print(f"✗ Error deleting database: {e}")
else:
    print(f"Database file not found: {db_file}")

print("\nRun: python main.py")
print("This will create a fresh database with the new AED-only schema!")
