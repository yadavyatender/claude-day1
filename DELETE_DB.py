import os
import sys

db_file = "gold_rates.db"

# First, check if file exists
if os.path.exists(db_file):
    try:
        # Try to delete it
        os.remove(db_file)
        print(f"✓ Successfully deleted: {db_file}")
    except PermissionError:
        print(f"✗ Permission denied - file is locked")
        print(f"  Close any programs using {db_file} and try again")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
else:
    print(f"✓ Database file doesn't exist")

print(f"\n✓ Ready for fresh database creation")
print(f"✓ Run: python main.py")
