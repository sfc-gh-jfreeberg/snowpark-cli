# Example Python script that uses the injected Snowpark session

# The 'session' variable is automatically available when run with snowpark-cli
# No need to import or create the session manually

def main():
    # Use the session to query Snowflake
    print("Current database:", session.get_current_database())
    print("Current schema:", session.get_current_schema())
    print("Current warehouse:", session.get_current_warehouse())
    
    # Example: Create a simple DataFrame
    df = session.create_dataframe([
        [1, "Alice", 25],
        [2, "Bob", 30],
        [3, "Charlie", 35]
    ], schema=["id", "name", "age"])
    
    print("\nSample DataFrame:")
    df.show()
    
    # Example: Run a SQL query
    result = session.sql("SELECT CURRENT_VERSION()").collect()
    print(f"\nSnowflake version: {result[0][0]}")

if __name__ == "__main__":
    main()
