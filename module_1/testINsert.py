import mysql.connector
from mysql.connector import Error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_3.main_thread import intermediate_layer

def create_database_and_tables(cursor):
    """Tạo cơ sở dữ liệu và các bảng"""
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS NQDVNHT_M1000")
        cursor.execute("USE NQDVNHT_M1000")
        
        # Tạo các bảng
        tables = [
            """CREATE TABLE IF NOT EXISTS ITEMS_CODE (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_line_code VARCHAR(255) NOT NULL UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS NUMS_CAMERA (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nums_camera INT,
                device_type VARCHAR(255),
                device_serial INT,
                connection_type VARCHAR(255),
                ip_address VARCHAR(255),
                item_code_id INT,
                FOREIGN KEY (item_code_id) REFERENCES ITEMS_CODE(id) ON DELETE CASCADE,
                UNIQUE KEY unique_camera (nums_camera, item_code_id)
            )""",
            """CREATE TABLE IF NOT EXISTS NUMS_MODEL (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nums_model INT,
                camera_id INT,
                FOREIGN KEY (camera_id) REFERENCES NUMS_CAMERA(id) ON DELETE CASCADE,
                UNIQUE KEY unique_model (nums_model, camera_id)
            )""",
            """CREATE TABLE IF NOT EXISTS PARAMETERSET (
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
            )"""
        ]
        
        for table in tables:
            cursor.execute(table)
    except Error as e:
        print(f"Lỗi khi tạo bảng: {e}")
        raise

def insert_item_code(cursor, connection, item_code):
    """Chèn item code và trả về ID"""
    try:
        cursor.execute("""
            INSERT IGNORE INTO ITEMS_CODE (name_line_code)
            VALUES (%s)
        """, (item_code,))
        connection.commit()
        
        cursor.execute("""
            SELECT id FROM ITEMS_CODE 
            WHERE name_line_code = %s
        """, (item_code,))
        
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"Lỗi khi chèn item code {item_code}: {e}")
        connection.rollback()
        return None

def insert_camera_data(cursor, connection, camera_data, item_code_id):
    """Chèn dữ liệu camera"""
    try:
        for index, camera in enumerate(camera_data.get("camera_tabs", []), 1):
            cursor.execute("""
                INSERT IGNORE INTO NUMS_CAMERA (
                    nums_camera, device_type, device_serial, 
                    connection_type, ip_address, item_code_id
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                index,
                camera.get("camera_type", "Unknown"),
                camera.get("serial", "0"),
                camera.get("port", "Unknown"),
                camera.get("ip_address", "Unknown"),
                item_code_id
            ))
            
            # Lấy ID của camera vừa chèn
            cursor.execute("""
                SELECT id FROM NUMS_CAMERA 
                WHERE nums_camera = %s AND item_code_id = %s
            """, (index, item_code_id))
            
            camera_result = cursor.fetchone()
            if camera_result:
                camera_id = camera_result[0]
                
                # Chèn dữ liệu model
                for model_index in range(1, int(camera.get("model_count", "0")) + 1):
                    cursor.execute("""
                        INSERT IGNORE INTO NUMS_MODEL (nums_model, camera_id)
                        VALUES (%s, %s)
                    """, (model_index, camera_id))
        
        connection.commit()
        return True
    except Error as e:
        print(f"Lỗi khi chèn dữ liệu camera: {e}")
        connection.rollback()
        return False

def _main():
    dataset_device = {
        'DEDEN': {'device_name': 'NQDVNHT_M100', 'camera_tabs': [
            {'camera_type': 'STC - Stviewer', 'ip_address': '192.168.1.1', 'port': 'Enthernet', 'serial': '25332', 'model_count': 2}, 
            {'camera_type': 'STC - Stviewer', 'ip_address': '192.168.1.1', 'port': 'Enthernet', 'serial': '56325', 'model_count': 2}
        ]},
        'DETRANG': {'device_name': 'NQDVNHT_M100', 'camera_tabs': [
            {'camera_type': 'HIK - MVS', 'ip_address': '192.168.1.1', 'port': 'USB', 'serial': '64323', 'model_count': 2}, 
            {'camera_type': 'HIK - MVS', 'ip_address': '192.168.1.1', 'port': 'USB', 'serial': '52353', 'model_count': 2}
        ]}
    }

    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456789',
            port=3306,
            database='NQDVNHT_M100'
        )
        
        # Tạo con trỏ
        cursor = connection.cursor()
        
        # Tạo cơ sở dữ liệu và bảng
        create_database_and_tables(cursor)
        
        # Lặp qua từng item code
        for item_code, device_data in dataset_device.items():
            # Chèn item code và lấy ID
            item_code_id = insert_item_code(cursor, connection, item_code)
            
            if item_code_id is not None:
                # Chèn dữ liệu camera
                if not insert_camera_data(cursor, connection, device_data, item_code_id):
                    print(f"Không thể chèn dữ liệu cho {item_code}")
    
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
    finally:
        # Đóng kết nối
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Kết nối MySQL đã đóng")

def main():

    # try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456789',
            port=3306,
            database='NQDVNHT_M100'
        )
        item_code = 'DEDEN'
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id FROM ITEMS_CODE 
            WHERE name_line_code = %s
        """, (item_code,))
        result = cursor.fetchone()[0]
        cursor.execute("""
            SELECT * FROM NUMS_CAMERA 
            WHERE item_code_id = %s
        """, (result,))

        result1 = cursor.fetchall()
        print(result1)

def open_pyuic6(item_code,database,connection):
        pyuic6_instance = intermediate_layer(item_code,database,connection)
class link:
    def __init__(self):
        self.connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='123456789',
                port=3306,
                database='NQTAMSATF'
            )
        self.database ='NQTAMSATF'
        self.item_code = 'TAMSATF'

from PyQt5 import QtWidgets
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    connect = link()
    item_code = connect.item_code
    database = connect.database
    window = intermediate_layer(item_code, database, connect)
    sys.exit(app.exec_())

