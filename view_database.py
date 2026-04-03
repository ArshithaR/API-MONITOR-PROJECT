#!/usr/bin/env python
"""
Database Viewer Script
Display database tables and their contents
"""

import sqlite3

def print_table(rows, column_names):
    """Print table with nice formatting"""
    if not rows:
        print("(No data)")
        return
    
    # Calculate column widths
    col_widths = [len(str(name)) for name in column_names]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header = " | ".join([str(name).ljust(col_widths[i]) for i, name in enumerate(column_names)])
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in rows:
        print(" | ".join([str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)]))

def view_database():
    try:
        # Try database.db first (has actual data), then api_monitor.db
        db_file = 'instance/database.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("=" * 80)
        print("DATABASE: API MONITOR PROJECT")
        print("=" * 80)
        print(f"\nTotal Tables Found: {len(tables)}\n")
        
        for table in tables:
            table_name = table[0]
            print(f"\n{'='*80}")
            print(f"TABLE: {table_name.upper()}")
            print(f"{'='*80}")
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            column_list = ', '.join([col[1] for col in columns_info])
            print(f"Columns: {column_list}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            print(f"Total Rows: {row_count}\n")
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            
            if rows:
                print_table(rows, column_names)
            else:
                print("(No data in this table)")
        
        conn.close()
        print("\n" + "=" * 80)
        print("END OF DATABASE VIEW")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_database()

if __name__ == "__main__":
    view_database()
