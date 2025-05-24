dictionary = {'built-in-camera-1': {'pyuic': {('camera-1', 'model-1'):'pyuic5',('camera-1', 'model-2'):'pyuic6'}, 'model_loader': {('camera-1', 'model-1'): 'model 1' },
                        'signals': {'ready': {'read_register': '2000', 'read_value': '', 'write_register': '1000', 'write_value': '1'}, 
                                    'run': {'read_register': '', 'read_value': '', 'write_register': '1002', 'write_value': '1'}, 
                                    'trigger': {'read_register': '2004', 'read_value': '1', 'write_register': '', 'write_value': ''}, 
                                    'busy': {'read_register': '', 'read_value': '', 'write_register': '1006', 'write_value': '1'}}},
    'built-in-camera-2': {'pyuic': {('camera-2', 'model-1'):'pyuic5'}, 'model_loader': {('camera-1', 'model-1'): 'model 1' },
                        'signals': {'ready': {'read_register': '1000', 'read_value': '', 'write_register': '1000', 'write_value': '1'}, 
                                    'run': {'read_register': '', 'read_value': '', 'write_register': '1002', 'write_value': '1'}, 
                                    'trigger': {'read_register': '1004', 'read_value': '1', 'write_register': '', 'write_value': ''}, 
                                    'busy': {'read_register': '', 'read_value': '', 'write_register': '1006', 'write_value': '1'}}}}
# first_key = list(dictionary.keys())[1]
# print(dictionary[first_key])
address = 'DM'
trigger = 1000
print(f'{address}{trigger}')

# test = '2004'
# num_model = 2
# for key,val in t.items():
#     trigger = val['signals']['trigger']['read_register']
#     if test in trigger:
#         for (shot, model_full), pyuic5 in val['pyuic'].items():
            
#             print(shot, 'avc  ',model_full)
            # print(k[1].split('-')[0])


# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QSpinBox, QTableWidget,
#     QTableWidgetItem, QComboBox,QPushButton
# )
# import sys

# class ShotModelWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Shot and Model Table")
#         self.resize(500, 400)
#         self.num_models = 3  
#         layout = QVBoxLayout()
#         input_layout = QHBoxLayout()
#         self.shot_spinbox = QSpinBox()
#         self.shot_spinbox.setMinimum(1)
#         self.shot_spinbox.setMaximum(100)
#         self.shot_spinbox.setValue(1)
#         self.shot_spinbox.valueChanged.connect(self.generate_table)
#         input_layout.addWidget(QLabel("Number of Shots:"))
#         input_layout.addWidget(self.shot_spinbox)
#         self.table = QTableWidget()
#         self.table.setColumnCount(2)
#         self.table.setHorizontalHeaderLabels(["Num of Shot", "Num of Model"])
#         self.button = QPushButton("Add Shot")
#         self.button.clicked.connect(self.print_shots)
#         layout.addWidget(self.button)
#         layout.addLayout(input_layout)
#         layout.addWidget(self.table)
#         self.setLayout(layout)
#         self.generate_table()

#     def generate_table(self):
#         num_shots = self.shot_spinbox.value()
#         self.table.setRowCount(num_shots)

#         for row in range(num_shots):
#             shot_item = QTableWidgetItem(str(row + 1))
#             self.table.setItem(row, 0, shot_item)
#             combo = QComboBox()
#             combo.addItems([str(i + 1) for i in range(self.num_models)])
#             self.table.setCellWidget(row, 1, combo)

#     def print_shots(self):
#         row_count = self.table.rowCount()
#         col_count = self.table.columnCount()
#         row_data = {}
#         for row in range(row_count):
#             item = self.table.item(row, 0)
#             shot = item.text()
#             widget_model = self.table.cellWidget(row, 1)
#             if isinstance(widget_model, QComboBox):
#                 model = widget_model.currentText()
#             row_data[shot] = model

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ShotModelWindow()
#     window.show()
#     sys.exit(app.exec_())


def _engine(self,image,width_widget,height_widget,model_loader):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        result_model = model_loader(image_rgb, size=640, conf=0.4)
        result = result_model.pandas().xyxy[0]
        result = result[result.name.isin(model_loader.names)]
        index_ng = []
        flag = True
        for idx, row in result.iterrows():
            label_name = row.name
            confidence = float(row.confidence)
            xmin, ymin, xmax, ymax = float(row.xmin),float(row.ymin),float(row.xmax),float(row.ymax)
            width = xmax - xmin
            height = ymax - ymin
            for i in range(pyuic.model.rowCount()):
                label_item = pyuic.model.item(i, pyuic.model_column.index(self.keys_mapping[0]))
                if label_item and label_item.text().strip() == label_name:  
                    join_item = pyuic.model.item(i, pyuic.model_column.index(self.keys_mapping[1]))
                    if join_item and join_item.checkState() == Qt.Checked:
                        conf_item = int(pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[-1])).text())
                        wmin = int(pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[5])).text())
                        wmax = int(pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[6])).text())
                        hmin = int(pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[7])).text())
                        hmax = int(pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[8])).text())
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
        for i in range(pyuic.model.rowCount()):
            label_item = pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[0]))
            join_item = pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[1]))
            ok_item = pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[2]))
            ng_item = pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[3]))
            quantity_item = pyuic.model.item(i,pyuic.model_column.index(self.keys_mapping[4]))
            if join_item and join_item.checkState() == Qt.Checked:
                if ok_item and ok_item.checkState() == Qt.Checked:
                    if list_ok.count(label_item.text().strip()) != int(quantity_item.text().strip()):
                        flag = False
                if ng_item and ng_item.checkState() == Qt.Checked:
                    if label_item.text().strip() in list_ok:
                        flag = False
        
        return result_image_rgb,flag
    