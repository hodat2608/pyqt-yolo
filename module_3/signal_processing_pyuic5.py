
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import Error
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QTableWidget,
    QTableWidgetItem, QComboBox
)


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
            'address': 0,
            'read_register': 1,
            'read_value_on': 2,
            'read_value_off': 3,
            'write_register': 4,
            'write_value_on': 5,
            'write_value_off': 6
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

    def save_mode_auto(self, cursor, connect_db, item_code_id):
        camera_name = self.uic.comboBox_camera.currentText()
        cursor.execute("""
                    SELECT id FROM NUMS_CAMERA 
                    WHERE item_code_id = %s AND nums_camera = %s
                """, (item_code_id, camera_name))
            
        result_camera_id = cursor.fetchone() 
        if (camera_id := result_camera_id[0] if result_camera_id else None):
            mode_name = self.uic.comboBox_mode_auto.currentText()
            cursor.execute("""
                SELECT id FROM MODE_AUTO 
                WHERE mode_name = %s AND camera_id = %s
            """, (mode_name, camera_id))
            result = cursor.fetchone()
            if not result:
                cursor.execute("""
                    INSERT INTO MODE_AUTO (mode_name, camera_id)
                    VALUES (%s, %s)
                """, (mode_name, camera_id))
                connect_db.connection.commit()
                cursor.execute("""
                    SELECT id FROM MODE_AUTO 
                    WHERE mode_name = %s AND camera_id = %s
                """, (mode_name, camera_id))
                result = cursor.fetchone()

        return result[0] if result else None

    def save_values_signal_to_db(self, cursor,connect_db,item_code_id):
        mode_auto_id = None
        if (mode_auto_id := self.save_mode_auto(cursor, connect_db, item_code_id)):
            try:
                cursor.execute("""
                    DELETE FROM MODE_AUTO_SIGNAL WHERE mode_id = %s
                """, (mode_auto_id,))
                for signal_name in self.signal_table.rows.keys():
                    address = self.signal_table.get_value(signal_name, 'address')
                    read_register = self.signal_table.get_value(signal_name, 'read_register')
                    read_value_on = self.signal_table.get_value(signal_name, 'read_value_on')
                    read_value_off = self.signal_table.get_value(signal_name, 'read_value_off')
                    write_register = self.signal_table.get_value(signal_name, 'write_register')
                    write_value_on = self.signal_table.get_value(signal_name, 'write_value_on')
                    write_value_off = self.signal_table.get_value(signal_name, 'write_value_off')

                    cursor.execute("""
                        INSERT INTO MODE_AUTO_SIGNAL (
                            signal_name, address, read_register, 
                            read_value_on, read_value_off, write_register, write_value_on, write_value_off, mode_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        signal_name,
                        address if address else None,
                        read_register if read_register else None,
                        read_value_on if read_value_on else None,
                        read_value_off if read_value_off else None,
                        write_register if write_register else None,
                        write_value_on if write_value_on else None,
                        write_value_off if write_value_off else None,
                        mode_auto_id
                    ))
                connect_db.connection.commit()
                QMessageBox.information(None, "Thành công", "Lưu thành công mode auto!")

            except Error as e:
                connect_db.connection.rollback()
                QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")

            except Exception as e:
                connect_db.connection.rollback()
                QMessageBox.critical(None, "Lỗi không xác định", str(e))

    def load_values_signals_from_db(self,cursor,camera_id):
        mode_name = self.uic.comboBox_mode_auto.currentText()
        cursor.execute("""
            SELECT id FROM MODE_AUTO
            WHERE mode_name = %s AND camera_id = %s
        """, (mode_name, camera_id))

        if result := cursor.fetchone():
            mode_auto_id = result[0]
            cursor.execute("""
                SELECT signal_name, address, read_register, 
                read_value_on, read_value_off, write_register, write_value_on, write_value_off
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
        
        return mode_auto_id if result else None

    def get_table_params(self):
        dict_params = {}
        dict_params['ready']= {}
        dict_params['ready']['address'] = self.signal_table.get_value('ready', 'address')
        dict_params['ready']['read_register'] = self.signal_table.get_value('ready', 'read_register')
        dict_params['ready']['read_value_on'] = self.signal_table.get_value('ready', 'read_value_on')
        dict_params['ready']['read_value_off'] = self.signal_table.get_value('ready', 'read_value_off')
        dict_params['ready']['write_register'] = self.signal_table.get_value('ready', 'write_register')
        dict_params['ready']['write_value_on'] = self.signal_table.get_value('ready', 'write_value_on')
        dict_params['ready']['write_value_off'] = self.signal_table.get_value('ready', 'write_value_off')
        
        dict_params['run'] = {}
        dict_params['run']['address'] = self.signal_table.get_value('run', 'address')
        dict_params['run']['read_register'] = self.signal_table.get_value('run', 'read_register')
        dict_params['run']['read_value_on'] = self.signal_table.get_value('run', 'read_value_on')
        dict_params['run']['read_value_off'] = self.signal_table.get_value('run', 'read_value_off')
        dict_params['run']['write_register'] = self.signal_table.get_value('run', 'write_register')
        dict_params['run']['write_value_on'] = self.signal_table.get_value('run', 'write_value_on')
        dict_params['run']['write_value_off'] = self.signal_table.get_value('run', 'write_value_off')

        dict_params['trigger'] = {}
        dict_params['trigger']['address'] = self.signal_table.get_value('trigger', 'address')
        dict_params['trigger']['read_register'] = self.signal_table.get_value('trigger', 'read_register')
        dict_params['trigger']['read_value_on'] = self.signal_table.get_value('trigger', 'read_value_on')
        dict_params['trigger']['read_value_off'] = self.signal_table.get_value('trigger', 'read_value_off')
        dict_params['trigger']['write_register'] = self.signal_table.get_value('trigger', 'write_register')
        dict_params['trigger']['write_value_on'] = self.signal_table.get_value('trigger', 'write_value_on')
        dict_params['trigger']['write_value_off'] = self.signal_table.get_value('trigger', 'write_value_off')

        dict_params['busy'] = {}
        dict_params['busy']['address'] = self.signal_table.get_value('busy', 'address')
        dict_params['busy']['read_register'] = self.signal_table.get_value('busy', 'read_register')
        dict_params['busy']['read_value_on'] = self.signal_table.get_value('busy', 'read_value_on')
        dict_params['busy']['read_value_off'] = self.signal_table.get_value('busy', 'read_value_off')
        dict_params['busy']['write_register'] = self.signal_table.get_value('busy', 'write_register')
        dict_params['busy']['write_value_on'] = self.signal_table.get_value('busy', 'write_value_on')
        dict_params['busy']['write_value_off'] = self.signal_table.get_value('busy', 'write_value_off')

        dict_params['gate'] = {}
        dict_params['gate']['address'] = self.signal_table.get_value('gate', 'address')
        dict_params['gate']['read_register'] = self.signal_table.get_value('gate', 'read_register')
        dict_params['gate']['read_value_on'] = self.signal_table.get_value('gate', 'read_value_on')
        dict_params['gate']['read_value_off'] = self.signal_table.get_value('gate', 'read_value_off')
        dict_params['gate']['write_register'] = self.signal_table.get_value('gate', 'write_register')
        dict_params['gate']['write_value_on'] = self.signal_table.get_value('gate', 'write_value_on')
        dict_params['gate']['write_value_off'] = self.signal_table.get_value('gate', 'write_value_off')

        dict_params['complete'] = {}
        dict_params['complete']['address'] = self.signal_table.get_value('complete', 'address')
        dict_params['complete']['read_register'] = self.signal_table.get_value('complete', 'read_register')
        dict_params['complete']['read_value_on'] = self.signal_table.get_value('complete', 'read_value_on')
        dict_params['complete']['read_value_off'] = self.signal_table.get_value('complete', 'read_value_off')
        dict_params['complete']['write_register'] = self.signal_table.get_value('complete', 'write_register')
        dict_params['complete']['write_value_on'] = self.signal_table.get_value('complete', 'write_value_on')
        dict_params['complete']['write_value_off'] = self.signal_table.get_value('complete', 'write_value_off')
        
        dict_params['reset'] = {}
        dict_params['reset']['address'] = self.signal_table.get_value('reset', 'address')
        dict_params['reset']['read_register'] = self.signal_table.get_value('reset', 'read_register')
        dict_params['reset']['read_value_on'] = self.signal_table.get_value('reset', 'read_value_on')
        dict_params['reset']['read_value_off'] = self.signal_table.get_value('reset', 'read_value_off')
        dict_params['reset']['write_register'] = self.signal_table.get_value('reset', 'write_register')
        dict_params['reset']['write_value_on'] = self.signal_table.get_value('reset', 'write_value_on')
        dict_params['reset']['write_value_off'] = self.signal_table.get_value('reset', 'write_value_off')

        dict_params['reset_counter'] = {}
        dict_params['reset_counter']['address'] = self.signal_table.get_value('reset_counter', 'address')
        dict_params['reset_counter']['read_register'] = self.signal_table.get_value('reset_counter', 'read_register')
        dict_params['reset_counter']['read_value_on'] = self.signal_table.get_value('reset_counter', 'read_value_on')
        dict_params['reset_counter']['read_value_off'] = self.signal_table.get_value('reset_counter', 'read_value_off')
        dict_params['reset_counter']['write_register'] = self.signal_table.get_value('reset_counter', 'write_register')
        dict_params['reset_counter']['write_value_on'] = self.signal_table.get_value('reset_counter', 'write_value_on')
        dict_params['reset_counter']['write_value_off'] = self.signal_table.get_value('reset_counter', 'write_value_off')

        return dict_params
    

    def save_shotxmodel_to_db(self,cursor,connect_db,item_code_id):
        mode_auto_id = None
        if mode_auto_id := self.save_mode_auto(cursor, connect_db, item_code_id):
            try: 
                cursor.execute("""
                    DELETE FROM SHOTXMODEL WHERE mode_id = %s
                """, (mode_auto_id,))

                row_count = self.uic.tableWidget_shotxmodel.rowCount()
                col_count = self.uic.tableWidget_shotxmodel.columnCount()
                list_insert = []

                for row in range(row_count):
                    row_data = {}
                    for col in range(col_count):
                        item = self.uic.tableWidget_shotxmodel.item(row, col)
                        if item is not None:
                            row_data[col] = item.text()
                        else:
                            widget = self.uic.tableWidget_shotxmodel.cellWidget(row, col)
                            if isinstance(widget, QComboBox):
                                row_data[col] = widget.currentText()
                    if row_data:
                        list_insert.append(row_data)
                if list_insert:
                    insert_query = """
                        INSERT INTO SHOTXMODEL (shot, no_of_model, mode_id)
                        VALUES (%s, %s, %s)
                    """
                    for row in list_insert:
                        shot = int(row.get(0, 0)) 
                        no_of_model = int(row.get(1, 0))  
                        cursor.execute(insert_query, (shot, no_of_model, mode_auto_id))
                    connect_db.connection.commit()
                    QMessageBox.information(None, "Thành công", "Lưu thành công shot link model!")

            except Error as e:
                connect_db.connection.rollback()
                QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")

            except Exception as e:
                connect_db.connection.rollback()
                QMessageBox.critical(None, "Lỗi không xác định", str(e))

    def load_shotxmodel_from_db(self,cursor,mode_auto_id):
        
        query = """
            SELECT shot,no_of_model
            FROM SHOTXMODEL
            WHERE mode_id = %s
            ORDER BY shot ASC
        """
        cursor.execute(query, (mode_auto_id,))
        if results:=cursor.fetchall():
            self.uic.tableWidget_shotxmodel.setRowCount(len(results))
            for row_index, (shot, no_of_model) in enumerate(results):
                shot_item = QTableWidgetItem(str(shot))
                self.uic.tableWidget_shotxmodel.setItem(row_index,0,shot_item)
                combo = QComboBox()
                combo.addItems([str(i + 1) for i in range(10)])
                combo.setCurrentText(str(no_of_model))
                self.uic.tableWidget_shotxmodel.setCellWidget(row_index, 1, combo)

    def dict_shotxmodel(self):
        row_count = self.uic.tableWidget_shotxmodel.rowCount()
        row_data = {}
        for row in range(row_count):
            item = self.uic.tableWidget_shotxmodel.item(row,0)
            shot = item.text()
            widget_model = self.uic.tableWidget_shotxmodel.cellWidget(row, 1)
            if isinstance(widget_model, QComboBox):
                model = widget_model.currentText()
            row_data[shot] = model

        return row_count,row_data
    