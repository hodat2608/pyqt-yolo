
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                             QFrame, QComboBox, QScrollArea, QMessageBox, QSpinBox,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox)
import logging

class Connect2Mysql:

    def __init__(self,ui_connection_sql,ui_mainwindow,uicmin):
        self.ui_mainwindow = ui_mainwindow
        self.ui_connection_sql = ui_connection_sql
        self.uicmin = uicmin
        self.connection = None
        self.cursor = None
        logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
    
    def show_connection_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("MySQL Workbench")
        msg.setText("Successfully made the MySQL connection")
        msg.setInformativeText(
            "Information related to this connection:\n\n"
            "Host: 127.0.0.1\n"
            "Port: 3306\n"
            "User: root\n"
            "SSL: enabled with TLS_AES_128_GCM_SHA256\n\n"
            "A successful MySQL connection was made with\n"
            "the parameters defined for this connection."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def connect_to_mysql(self):

        if not self.ui_connection_sql.lineEdit_hostname.text():
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập hostname!")
            return
        if not self.ui_connection_sql.lineEdit_username.text():
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập username!")
            return
        if not self.ui_connection_sql.lineEdit_password.text():
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập password!")
            return
        if not self.ui_connection_sql.lineEdit_port.text():
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập port!")
            return
        
        hostname = self.ui_connection_sql.lineEdit_hostname.text()
        username = self.ui_connection_sql.lineEdit_username.text()
        password = self.ui_connection_sql.lineEdit_password.text()
        port     = self.ui_connection_sql.lineEdit_port.text()

        try:
            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                port=int(port) if port else 3306 
            )
            if self.connection.is_connected():
                self.show_connection_success()
                self.uicmin.pushButton.setEnabled(True)
            else:
                QMessageBox.warning(None, "Lỗi", "Không thể kết nối đến MySQL.")
        except Error as e:
            QMessageBox.critical(None, "Lỗi kết nối", f"Lỗi: {str(e)}")

    def create_item_code_device(self):
        if not self.uicmin.lineEdit_name_devic.text():
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập tên thiết bị!")
            return
        reply = QMessageBox.question(
            None, "Xác nhận", f"Xác nhận tên thiết bị: {self.uicmin.lineEdit_name_devic.text()}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.uicmin.lineEdit_name_devic.text()}")
                self.cursor.execute(f"USE {self.uicmin.lineEdit_name_devic.text()}")
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
                    """CREATE TABLE IF NOT EXISTS WEIGHTS (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        Weight_Path TEXT NOT NULL,
                        Weight_Used_Path TEXT NOT NULL,
                        Conf_Value INT DEFAULT 0,
                        Size_Value INT DEFAULT 0,
                        model_id INT,
                        FOREIGN KEY (model_id) REFERENCES NUMS_MODEL(id) ON DELETE CASCADE
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
                    )""",
                    """CREATE TABLE IF NOT EXISTS MODE_AUTO (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        mode_name VARCHAR(255) NOT NULL,
                        camera_id INT NOT NULL,
                        UNIQUE (mode_name, camera_id),
                        FOREIGN KEY (camera_id) REFERENCES NUMS_CAMERA(id) ON DELETE CASCADE
                    )""",
                    """CREATE TABLE IF NOT EXISTS MODE_AUTO_SIGNAL (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        signal_name VARCHAR(255) NOT NULL,
                        variable_name VARCHAR(255),
                        address VARCHAR(255),
                        read_register VARCHAR(255),
                        read_value VARCHAR(255),
                        write_register VARCHAR(255),
                        write_value VARCHAR(255),
                        mode_id INT NOT NULL,
                        FOREIGN KEY (mode_id) REFERENCES MODE_AUTO(id) ON DELETE CASCADE
                    )""",
                ]
                
                for table in tables:
                    self.cursor.execute(table)
                QMessageBox.information(None,"Succesfull dll","Thiết lập dữ liệu thành công")
                self.uicmin.spinBox_num_itemcode.setEnabled(True)
            except mysql.connector.Error as error:
                QMessageBox.critical(None, "Error", f"Lỗi query: {str(error)}")
                logging.error(f"Lỗi {error}")
                raise

    def insert_item_code(self,item_code):
        try:
            self.cursor.execute("""
                INSERT IGNORE INTO ITEMS_CODE (name_line_code)
                VALUES (%s)
            """, (item_code,))
            self.connection.commit()
            
            self.cursor.execute("""
                SELECT id FROM ITEMS_CODE 
                WHERE name_line_code = %s
            """, (item_code,))
            
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            self.connection.rollback()
            return None

    def insert_camera_data(self,camera_data,item_code_id):
        try:
            for index, camera in enumerate(camera_data.get("camera_tabs", []), 1):
                self.cursor.execute("""
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

                self.cursor.execute("""
                    SELECT id FROM NUMS_CAMERA 
                    WHERE nums_camera = %s AND item_code_id = %s
                """, (index, item_code_id))
                
                camera_result = self.cursor.fetchone()
                if camera_result:
                    camera_id = camera_result[0]
                    for model_index in range(1, int(camera.get("model_count", "0")) + 1):
                        self.cursor.execute("""
                            INSERT IGNORE INTO NUMS_MODEL (nums_model, camera_id)
                            VALUES (%s, %s)
                        """, (model_index, camera_id))
            
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            return False

    def commitment(self):
        try:
            for item_code, device_data in self.ui_mainwindow.list_item_code.items():
                item_code_id = self.insert_item_code(item_code)
                if item_code_id is not None:
                    if not self.insert_camera_data(device_data, item_code_id):
                        QMessageBox.critical(None, "Error", f"Không thể chèn dữ liệu cho {item_code}")
        except Error as e:
            QMessageBox.critical(None, "Error", f"Lỗi kết nối MySQL: {e}")
        finally:
            if self.connection.is_connected():
                # self.cursor.close()
                # self.connection.close()
                QMessageBox.information(None,"Succesfull","Thiết lập thành công")