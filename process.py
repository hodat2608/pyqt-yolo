
import torch

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from layout_congfiguration_model import Ui_MainWindow

class process:
    def __init__(self,uic):
        self.model = None
        self.model1 = None
        self.file_path = None
        self.uic = uic

    def browse_file(self):
            print('ssss')
            options = QtWidgets.QFileDialog.Options()
            self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Chọn file",
                "",
                "PyTorch Model (*.pt);;Tất cả các file (*)",
                options=options
            )
            if self.file_path:
                print(f"Đã chọn file: {self.file_path}")

    def load_model(self):
        self.model1 = torch.hub.load('./levu','custom', path=self.file_path, source='local',force_reload =False)
        self.populateTable()
    
    def populateTable(self):
        """Thêm dữ liệu mẫu vào model"""
        for label in self.model1.names:
            row_items = []
            for col in range(11): 
                item = QStandardItem()
                if col == 0: 
                    item.setText(str(label))
                    item.setTextAlignment(Qt.AlignCenter)
                elif col in [1, 2, 3]:
                    item.setCheckable(True)
                    item.setCheckState(Qt.Checked)
                else:  
                    item.setText("0")
                    item.setTextAlignment(Qt.AlignCenter)
                row_items.append(item)
            self.uic.model.appendRow(row_items)

    def save_data(self):  
        print(self.uic.spinBox.value())
        print('size img',self.uic.comboBox_3.currentText()) 
        print('cmer',self.uic.comboBox_6.currentText()) 
        print('model',self.uic.comboBox_4.currentText()) 

    def event_clock(self, camera_id, model_id, dict, tabWidget, ui_instances):
        """ Cập nhật dữ liệu từ database vào các widget của model trong camera """

        # 🔍 Tìm vị trí của tab "Camera X"
        camera_tab_index = -1
        for i, j in enumerate(dict):
            if j[1] == camera_id:
                camera_tab_index = i
                print('camera_tab_index',camera_tab_index)
                break

        if camera_tab_index != -1:
            # Đặt tab widget tới "Camera X"
            tabWidget.setCurrentIndex(camera_tab_index)

            # Lấy tab widget bên trong "Camera X"
            inner_tab_widget = tabWidget.widget(camera_tab_index).findChild(QtWidgets.QTabWidget)

            if inner_tab_widget:
                # 🔍 Tìm tab "Model Y"
                model_tab_index = model_id - 1  # Vì index bắt đầu từ 0
                if model_tab_index < inner_tab_widget.count():
                    inner_tab_widget.setCurrentIndex(model_tab_index)

                    # 📌 Lấy UI instance từ dictionary
                    ui_instance = ui_instances.get((camera_id, model_id))

                    if ui_instance:
                        # 🗄️ Giả lập dữ liệu từ database
                        db_data = {
                            "spinBox": 99,
                            "comboBox_3": "768",
                            "comboBox_6": "3",
                            "comboBox_4": "2"
                        }
                        # 🎯 Cập nhật giá trị từ database vào UI
                        ui_instance.spinBox.setValue(db_data["spinBox"])
                        ui_instance.comboBox_3.setCurrentText(db_data["comboBox_3"])
                        ui_instance.comboBox_6.setCurrentText(db_data["comboBox_6"])
                        ui_instance.comboBox_4.setCurrentText(db_data["comboBox_4"])

                        print(f"✅ Cập nhật thành công cho Model {model_id} trong Camera {camera_id}")
                    else:
                        print(f"❌ Không tìm thấy UI instance của Model {model_id} trong Camera {camera_id}")
                else:
                    print(f"❌ Model {model_id} không tồn tại trong Camera {camera_id}")
            else:
                print(f"❌ Không tìm thấy inner tab widget trong Camera {camera_id}")
        else:
            print(f"❌ Không tìm thấy Camera {camera_id}")


# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QHeaderView
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     uic = process(ui)
#     ui.setupUi(MainWindow)
#     ui.pushButton.clicked.connect(uic.browse_file)
#     ui.pushButton_2.clicked.connect(uic.load_model)
#     MainWindow.show()
#     sys.exit(app.exec_())
