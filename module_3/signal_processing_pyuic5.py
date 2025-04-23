
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import Error
class SignalTableHelper:
    def __init__(self, table_widget):
        self.table = table_widget
        self.rows = {
            'ready': 0,
            'run': 1,
            'trigger': 2,
            'busy': 3,
            'gate': 4,
            'complete': 5,
            'reset': 6,
            'reset_counter': 7
        }
        self.columns = {
            'variable': 0,
            'address': 1,
            'read_register': 2,
            'read_value': 3,
            'write_register': 4,
            'write_value': 5
        }

    def get_value(self, signal_name, column_name):
        row = self.rows.get(signal_name.lower())
        col = self.columns.get(column_name.lower())
        if row is not None and col is not None:
            item = self.table.item(row, col)
            return item.text() if item else ''
        return None

    def set_value(self, signal_name, column_name, value):
        row = self.rows.get(signal_name.lower())
        col = self.columns.get(column_name.lower())
        if row is not None and col is not None:
            self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))


class DataProcessSignal:

    def __init__(self,uic):
        self.uic = uic
        self.signal_table = SignalTableHelper(self.uic.tableWidget)

    def save_values_signal(self, cursor, connect_db, camera_id):
        try:
            cursor.execute("""
                INSERT IGNORE INTO MODE_AUTO (mode_name, camera_id)
                VALUES (%s, %s)
            """, (self.uic.comboBox_mode_auto.currentText(), camera_id))

            cursor.execute("""
                SELECT id FROM MODE_AUTO 
                WHERE mode_name = %s AND camera_id = %s
            """, (self.uic.comboBox_mode_auto.currentText(), camera_id))
            result = cursor.fetchone()

            if result:
                mode_auto_id = result[0]
                for signal_name in self.signal_table.rows.keys():
                    variable_name = self.signal_table.get_value(signal_name, 'variable')
                    address = self.signal_table.get_value(signal_name, 'address')
                    read_register = self.signal_table.get_value(signal_name, 'read_register')
                    read_value = self.signal_table.get_value(signal_name, 'read_value')
                    write_register = self.signal_table.get_value(signal_name, 'write_register')
                    write_value = self.signal_table.get_value(signal_name, 'write_value')

                    cursor.execute("""
                        INSERT INTO MODE_AUTO_SIGNAL (
                            signal_name, variable_name, address, read_register, 
                            read_value, write_register, write_value, mode_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        signal_name,
                        variable_name if variable_name else None,
                        address if address else None,
                        read_register if read_register else None,
                        read_value if read_value else None,
                        write_register if write_register else None,
                        write_value if write_value else None,
                        mode_auto_id
                    ))

                connect_db.connection.commit()
        except Error as e:
            connect_db.connection.rollback()
            QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")

        except Exception as e:
            connect_db.connection.rollback()
            QMessageBox.critical(None, "Lỗi không xác định", str(e))

    def load_values_from_db(self,cursor,camera_id):
        mode_name = self.uic.comboBox_mode_auto.currentText()
        cursor.execute("""
            SELECT id FROM MODE_AUTO
            WHERE mode_name = %s AND camera_id = %s
        """, (mode_name, camera_id))
        result = cursor.fetchone()
        if result:
            mode_auto_id = result[0]
            cursor.execute("""
                SELECT signal_name, variable_name, address, read_register, 
                    read_value, write_register, write_value
                FROM MODE_AUTO_SIGNAL
                WHERE mode_id = %s
            """, (mode_auto_id,))
            rows = cursor.fetchall()
            for row in rows:
                signal_name = row[0].lower()
                for i, column_name in enumerate(self.signal_table.columns.keys()):
                    value = row[i + 1]
                    if value is not None:
                        self.signal_table.set_value(signal_name, column_name, value)

    