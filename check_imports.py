print("Checking what's in app.database module...")

try:
    import app.database as db_module
    print("\nAvailable attributes in database module:")
    for attr in dir(db_module):
        if not attr.startswith('_'):
            print(f"  - {attr}")

    # Try to see what specific variables exist
    if hasattr(db_module, 'db'):
        print("\n✓ Found 'db' object")
        if hasattr(db_module.db, 'database'):
            print("  - db.database exists")

    if hasattr(db_module, 'database'):
        print("\n✓ Found 'database' object")

    if hasattr(db_module, 'motor_client'):
        print("\n✓ Found 'motor_client' object")

    if hasattr(db_module, 'get_sync_database'):
        print("\n✓ Found 'get_sync_database' function")

except Exception as e:
    print(f"\nError importing: {e}")
