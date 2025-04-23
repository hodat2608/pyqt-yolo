
import torch
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                             QFrame, QComboBox, QScrollArea, QMessageBox, QSpinBox,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from module_3.layout_configuration_options import Ui_MainWindow
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QStandardItem
from mysql.connector import Error
import cv2, numpy as np
from module_3.layout_configuration_options_ver_2 import COLUMN_MAPPING
import time
class CheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data(Qt.CheckStateRole)
        if value is not None:
            checkbox_style_option = QStyleOptionButton()
            checkbox_style_option.state |= QStyle.State_Enabled
            if int(value) == Qt.Checked:
                checkbox_style_option.state |= QStyle.State_On
            else:
                checkbox_style_option.state |= QStyle.State_Off

            checkbox_rect = self.parent().style().subElementRect(QStyle.SE_CheckBoxIndicator, checkbox_style_option, None)
            checkbox_style_option.rect = QRect(
                option.rect.x() + option.rect.width() // 2 - checkbox_rect.width() // 2,
                option.rect.y() + option.rect.height() // 2 - checkbox_rect.height() // 2,
                checkbox_rect.width(),
                checkbox_rect.height()
            )
            self.parent().style().drawControl(QStyle.CE_CheckBox, checkbox_style_option, painter)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            current_value = index.data(Qt.CheckStateRole)
            new_value = Qt.Unchecked if current_value == Qt.Checked else Qt.Checked
            model.setData(index, new_value, Qt.CheckStateRole)
        return True
    
    
class Process_Model:

    def __init__(self,uic):
        self.model = None
        self.file_path = None
        self.uic = uic
        self.list_layer = []
        self.list_layer_save = []
        self.keys_mapping = list(COLUMN_MAPPING.keys())
        self.file_path_detect = None
        self.model_loader = None

    def browse_file(self):
            options = QtWidgets.QFileDialog.Options()
            self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Chọn file",
                "",
                "PyTorch Model (*.pt);;Tất cả các file (*)",
                options=options
            )
            if self.file_path:
                self.uic.lineEdit.setText(self.file_path)

    def browse_file_detect(self):
        options = QtWidgets.QFileDialog.Options()
        self.file_path_detect, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Chọn file",
            "",
            "Hình ảnh (*.jpg *.png *.bmp);;Tất cả các file (*)",
            options=options
        )
        if self.file_path_detect:
            size = self.uic.label_5.size()
            width, height = size.width(), size.height()
            self.uic.lineEdit_2.setText(self.file_path_detect)

            image = cv2.imread(self.file_path_detect)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (width, height))

            qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.uic.label_5.setPixmap(pixmap)

    def detect_img(self):
        if not self.file_path_detect:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng chọn file trước.")
            return
        t1 = time.time()
        size = self.uic.label_5.size()
        width_widget, height_widget = size.width(), size.height()
        image = cv2.imread(self.file_path_detect) 
        result_image_rgb,flag = self.engine(image,width_widget,height_widget)
        if flag:
            cv2.putText(result_image_rgb, 'RESULT:OK',(10, 50),cv2.FONT_HERSHEY_COMPLEX,  0.5,(0,255,0),1)
        else:
            cv2.putText(result_image_rgb, 'RESULT:NG',(10, 50),cv2.FONT_HERSHEY_COMPLEX,  0.5,(0,0,255),1)
        t2 = time.time()
        cv2.putText(result_image_rgb, f"Time: {t2-t1:.3f} s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        qimage = QtGui.QImage(result_image_rgb.data, result_image_rgb.shape[1], result_image_rgb.shape[0], result_image_rgb.strides[0], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        self.uic.label_5.setPixmap(pixmap)

    def save_parameter_before_load_weight(self):
        model = self.uic.model
        model_column = self.uic.model_column
        label_col_index = model_column.index(self.keys_mapping[0])
        for row in range(model.rowCount()): 
            label_item = model.item(row, label_col_index)
            if label_item is None:
                continue
            label_text = label_item.text().strip()
            row_data = {}
            for col in range(model.columnCount()): 
                item = model.item(row, col)
                if item is not None:
                    if item.isCheckable():
                        value = item.checkState() == Qt.Checked
                    else:
                        value = item.text()
                    row_data[model_column[col]] = value
            row_data[self.keys_mapping[0]] = label_text
            self.list_layer.append(row_data)

    def load_model(self):
        if not self.file_path:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng chọn file trước.")
            return
        if self.file_path.endswith('.pt'):
            self.model = torch.hub.load('./levu','custom', path=self.file_path, source='local',force_reload =False)
            self.populateTable()
    
    def populateTable(self):
        self.uic.model.removeRows(0, self.uic.model.rowCount())
        for label in self.model.names:
            row_items = []
            checkbox_delegate = CheckboxDelegate(self.uic.tableView)
            for col_name in [self.keys_mapping[1], self.keys_mapping[2], self.keys_mapping[3]]:
                col_index = self.uic.model_column.index(col_name)
                self.uic.tableView.setItemDelegateForColumn(col_index, checkbox_delegate)

            for col in range(len(self.uic.model_column)): 
                item = QStandardItem()
                if col == self.uic.model_column.index(self.keys_mapping[0]): 
                    item.setText(str(label))
                    item.setTextAlignment(Qt.AlignCenter)
                elif col in [self.uic.model_column.index(self.keys_mapping[1]),\
                            self.uic.model_column.index(self.keys_mapping[2]),\
                            self.uic.model_column.index(self.keys_mapping[3])]:
                    item.setCheckable(True)
                    item.setCheckState(Qt.Unchecked)
                else:  
                    item.setText("0")
                    item.setTextAlignment(Qt.AlignCenter)
                row_items.append(item)
            self.uic.model.appendRow(row_items)

    def save_values_injection_safe(self, cursor, connector):
        try:
            row_count = self.uic.model.rowCount()
            col_count = self.uic.model.columnCount()
            list_insert = []
            for row in range(row_count):
                row_data = {}
                is_empty_row = True
                for col in range(col_count):
                    header = self.uic.model_column[col] 
                    item = self.uic.model.item(row, col)
                    if item is not None:
                        if item.isCheckable():
                            value = item.checkState() == Qt.Checked
                        else:
                            value = item.text().strip()
                            if value:
                                is_empty_row = False
                        row_data[header] = value
                    else:
                        row_data[header] = None
                if not is_empty_row:
                    list_insert.append(row_data)
            cursor.execute("""
                SELECT id FROM NUMS_MODEL
                WHERE camera_id = %s AND nums_model = %s
            """, (self.uic.comboBox_6.currentText(), self.uic.comboBox_4.currentText()))

            result = cursor.fetchone()
            if not result:
                raise ValueError("Không tìm thấy model_id tương ứng.")

            model_id = result[0]
            weight_path = self.uic.lineEdit.text().strip()
            conf = self.uic.spinBox.value()
            size = self.uic.comboBox_3.currentText()
            
            if weight_path and weight_path.endswith('.pt'):
                cursor.execute("""
                    INSERT IGNORE INTO WEIGHTS 
                    (Weight_Path, Conf_Value, Size_Value, model_id)
                    VALUES (%s, %s, %s, %s)
                """, (weight_path, conf, size, model_id))

            cursor.execute(
                    f"DELETE FROM PARAMETERSET WHERE model_id = %s",
                    (model_id,),
                )

            if list_insert:
                param_fields = list(COLUMN_MAPPING.values())
                sql = f"""
                    INSERT IGNORE INTO PARAMETERSET 
                    ({', '.join(param_fields)}, model_id)
                    VALUES ({', '.join(['%s'] * (len(param_fields) + 1))})
                """

                for row_dict in list_insert:
                    values = [row_dict.get(ui_col, None) for ui_col in COLUMN_MAPPING.keys()]
                    values.append(model_id)
                    cursor.execute(sql, values)

                connector.connection.commit()
            QMessageBox.information(None, "Thành công", "Lưu thông số thành công")

        except Error as e:
            connector.connection.rollback()
            QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")

        except Exception as e:
            connector.connection.rollback()
            QMessageBox.critical(None, "Lỗi không xác định", str(e))

    def load_data_injection_safe(self):
        model = self.uic.model
        model_column = self.uic.model_column
        label_col_index = model_column.index(self.keys_mapping[0])

        for row in range(model.rowCount()):
            label_item = model.item(row, label_col_index)
            if label_item is None:
                continue
            label_text = label_item.text().strip()
            for param_dict in self.list_layer:
                if param_dict[self.keys_mapping[0]] == label_text:
                    for col, col_name in enumerate(model_column):
                        value = param_dict.get(col_name)
                        item = QStandardItem()
                        if col == label_col_index:
                            item.setText(label_text)
                            item.setTextAlignment(Qt.AlignCenter)
                        elif col_name in [self.keys_mapping[1], self.keys_mapping[2], self.keys_mapping[3]]:
                            item.setCheckable(True)
                            item.setCheckState(Qt.Checked if value else Qt.Unchecked)
                        else:
                            item.setText(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                        model.setItem(row, col, item)
            
    def assign_values(self,model,camera,code):  
        self.uic.comboBox_5.addItem(str(code))
        self.uic.comboBox_6.addItem(str(camera))
        self.uic.comboBox_4.addItem(str(model))

    def load_parameter_injection_safe(self, camera_id, model, cursor, connect_db, tabWidget, ui_instances):
        try:
            weight_path = None
            cursor.execute("""
                SELECT Weight_Path, Conf_Value, Size_Value
                FROM WEIGHTS
                WHERE model_id = (SELECT id FROM NUMS_MODEL WHERE camera_id = %s AND nums_model = %s)
            """, (camera_id, model))
            result = cursor.fetchone()
            if result:
                weight_path, conf_value, size_value = result
                self.uic.lineEdit.setText(weight_path)
                self.uic.spinBox.setValue(conf_value)
                self.uic.comboBox_3.setCurrentText(str(size_value))
                
        except Error as e:
            connect_db.connection.rollback()
            QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")
            return

        if weight_path and weight_path.endswith('.pt'):
            self.model_loader = torch.hub.load('./levu', 'custom', path=weight_path, source='local', force_reload=False)

        try:
            reverse_column_map = {v: k for k, v in COLUMN_MAPPING.items()}

            db_columns = list(COLUMN_MAPPING.values())

            cursor.execute(f"""
                SELECT {', '.join(db_columns)}
                FROM PARAMETERSET
                WHERE model_id = (SELECT id FROM NUMS_MODEL WHERE camera_id = %s AND nums_model = %s)
            """, (camera_id, model))
            result = cursor.fetchall()
            if result:
                self.uic.model.removeRows(0, self.uic.model.rowCount())
                for label_name in self.model_loader.names:
                    for row_data in result:
                        if row_data[db_columns.index(list(COLUMN_MAPPING.values())[0])] == label_name:
                            row_items = []
                            checkbox_delegate = CheckboxDelegate(self.uic.tableView)
                            for col_name in [self.keys_mapping[1], self.keys_mapping[2], self.keys_mapping[3]]:
                                col_index = self.uic.model_column.index(col_name)
                                self.uic.tableView.setItemDelegateForColumn(col_index, checkbox_delegate)

                            for ui_col in self.uic.model_column:
                                db_col = COLUMN_MAPPING[ui_col]
                                db_value = row_data[db_columns.index(db_col)]

                                item = QStandardItem()
                                if ui_col == self.keys_mapping[0]:
                                    item.setText(str(label_name))
                                    item.setTextAlignment(Qt.AlignCenter)
                                elif ui_col in [self.keys_mapping[1], self.keys_mapping[2], self.keys_mapping[3]]:
                                    item.setCheckable(True)
                                    item.setCheckState(Qt.Checked if db_value else Qt.Unchecked)
                                else:
                                    item.setText(str(db_value))
                                    item.setTextAlignment(Qt.AlignCenter)

                                row_items.append(item)

                            self.uic.model.appendRow(row_items)
            self.save_parameter_before_load_weight()
        except Error as e:
            connect_db.connection.rollback()
            QMessageBox.critical(None, "Lỗi", f"MySQL Error: {e}")

        except Exception as e:
            connect_db.connection.rollback()
            QMessageBox.critical(None, "Lỗi không xác định", str(e))

    def engine(self,image,width_widget,height_widget):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        result_model = self.model_loader(image_rgb, size=640, conf=0.4)
        result = result_model.pandas().xyxy[0]
        result = result[result.name.isin(self.model_loader.names)]
        index_ng = []
        flag = True
        for idx, row in result.iterrows():
            label_name = row.name
            confidence = float(row.confidence)
            xmin, ymin, xmax, ymax = float(row.xmin),float(row.ymin),float(row.xmax),float(row.ymax)
            width = xmax - xmin
            height = ymax - ymin
            for i in range(self.uic.model.rowCount()):
                label_item = self.uic.model.item(i, self.uic.model_column.index(self.keys_mapping[0]))
                if label_item and label_item.text().strip() == label_name:  
                    join_item = self.uic.model.item(i, self.uic.model_column.index(self.keys_mapping[1]))
                    if join_item and join_item.checkState() == Qt.Checked:
                        conf_item = int(self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[-1])).text())
                        wmin = int(self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[5])).text())
                        wmax = int(self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[6])).text())
                        hmin = int(self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[7])).text())
                        hmax = int(self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[8])).text())
                        if (confidence < (conf_item/100) or 
                            width < wmin or width > wmax or 
                            height < hmin or height > hmax):
                            result.drop(idx, inplace=True, axis=0)
                            index_ng.append(idx)
                    else:
                        if label_item and label_item.text().strip() == label_name:  
                            result.drop(idx, inplace=True, axis=0)
                            index_ng.append(idx)
        list_ok = list(result.name)
        result_image = np.squeeze(result_model.render(index_ng))
        result_image_rgb = cv2.resize(result_image, (width_widget, height_widget), interpolation=cv2.INTER_AREA)
        for i in range(self.uic.model.rowCount()):
            label_item = self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[0]))
            join_item = self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[1]))
            ok_item = self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[2]))
            ng_item = self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[3]))
            quantity_item = self.uic.model.item(i,self.uic.model_column.index(self.keys_mapping[4]))
            if join_item and join_item.checkState() == Qt.Checked:
                if ok_item and ok_item.checkState() == Qt.Checked:
                    if list_ok.count(label_item.text().strip()) != int(quantity_item.text().strip()):
                        flag = False
                if ng_item and ng_item.checkState() == Qt.Checked:
                    if label_item.text().strip() in list_ok:
                        flag = False
        
        return result_image_rgb,flag
    

    def print_tb_signal(self):
        self.uic.tabWidget.setCurrentIndex(0)
        self.uic.tabWidget_2.setCurrentIndex(0)
        self.uic.tabWidget_3.setCurrentIndex(0)
        self.uic.tabWidget_4.setCurrentIndex(0)

    def read_register_from_txt(self,filepath):
        with open(filepath, 'r') as file:
            line = file.readline().strip()
            if '=' in line:
                register, value = line.split('=')
                register = register.strip()
                value = int(value.strip())
                return register, value
            else:
                raise ValueError("File format is invalid")  
            