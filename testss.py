t = {'built-in-camera-1': {'pyuic': {('camera-1', 'model-1'):'pyuic5'}, 'model_loader': {('camera-1', 'model-1'): 'model 1' },
                        'signals': {'ready': {'read_register': '2000', 'read_value': '', 'write_register': '1000', 'write_value': '1'}, 
                                    'run': {'read_register': '', 'read_value': '', 'write_register': '1002', 'write_value': '1'}, 
                                    'trigger': {'read_register': '2004', 'read_value': '1', 'write_register': '', 'write_value': ''}, 
                                    'busy': {'read_register': '', 'read_value': '', 'write_register': '1006', 'write_value': '1'}}},
    'built-in-camera-2': {'pyuic': {('camera-2', 'model-1'):'pyuic5'}, 'model_loader': {('camera-1', 'model-1'): 'model 1' },
                        'signals': {'ready': {'read_register': '1000', 'read_value': '', 'write_register': '1000', 'write_value': '1'}, 
                                    'run': {'read_register': '', 'read_value': '', 'write_register': '1002', 'write_value': '1'}, 
                                    'trigger': {'read_register': '1004', 'read_value': '1', 'write_register': '', 'write_value': ''}, 
                                    'busy': {'read_register': '', 'read_value': '', 'write_register': '1006', 'write_value': '1'}}}}

test = '2004'
num_model = 2
for key,val in t.items():
    trigger = val['signals']['trigger']['read_register']
    if test in trigger:
        for k,v in val['pyuic'].items():
            shot = k[0]
            model = k[1].split('-')[0]
            num_model = k[1].split('-')[1]
            total = (shot,f'{model}-{num_model}')
            print(total)
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

