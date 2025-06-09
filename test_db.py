import pymysql
from tabulate import tabulate

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'a',
    'database': 'amazon',
    'charset': 'utf8'
}

try:
    # Establish connection
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    # Get all tables in the database
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if not tables:
        print("No tables found in the database.")
    else:
        print("\nTables in the database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Display contents of each table
        for table in tables:
            table_name = table[0]
            print(f"\nContents of table '{table_name}':")
            
            # Get column names
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            
            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Display using tabulate for better formatting
            if rows:
                print(tabulate(rows, headers=columns, tablefmt="grid"))
            else:
                print("(Empty table)")
    
except pymysql.Error as e:
    print(f"Error: {e}")
    
finally:
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()