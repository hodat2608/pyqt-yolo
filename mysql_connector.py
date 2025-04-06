import mysql.connector

def get_connection_info(host, user, password, database, table_name):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            server_info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]

            print("MySQL Connection Information:")
            print(f"Host: {host}")
            print(f"User: {user}")
            print(f"Database: {db_name}")
            print(f"MySQL Server Version: {server_info}")
            print(f"Connection ID: {connection.connection_id}")

            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nTables in the database:")
            for table in tables:
                print(table[0])

            # Show records from the specified table
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            print(f"\nRecords in table '{table_name}':")
            for record in records:
                print(record)
            cursor.close()
            connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

import mysql.connector

def create_database_and_tables(host, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS AIVISONPRO_LINECODE")
        cursor.execute("USE AIVISONPRO_LINECODE")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ITEMS_CODE (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_line_code VARCHAR(255) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NUMS_CAMERA (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nums_camera INT,
                device_serial_number INT,
                connection_type VARCHAR(255),
                ip_address VARCHAR(255),
                item_code_id INT,
                FOREIGN KEY (item_code_id) REFERENCES ITEMS_CODE(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NUMS_MODEL (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nums_model INT,
                name_model VARCHAR(255),
                camera_id INT,
                FOREIGN KEY (camera_id) REFERENCES NUMS_CAMERA(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PARAMETERSET (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Label_Name TEXT NOT NULL,
                `Join` BOOLEAN DEFAULT FALSE,
                OK BOOLEAN DEFAULT FALSE,
                NG BOOLEAN DEFAULT FALSE,
                Quantity INT DEFAULT 0,
                Width_Min INT DEFAULT 0,
                Width_Max INT DEFAULT 0,
                Height_Min INT DEFAULT 0,
                Height_Max INT DEFAULT 0,
                Assign_Value INT DEFAULT 0,
                Confidence INT DEFAULT 0,
                model_id INT,
                FOREIGN KEY (model_id) REFERENCES NUMS_MODEL(id) ON DELETE CASCADE
            )
        """)
        
        print("Database and tables created successfully with proper foreign keys.")
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

create_database_and_tables('127.0.0.1', "root", "123456789")

