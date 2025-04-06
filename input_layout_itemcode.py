import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                             QFrame, QComboBox, QScrollArea, QMessageBox, QSpinBox,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap

class StyleHelper:
    @staticmethod
    def get_style():
        return """
        QMainWindow {
            background-color: #f0f2f5;
        }
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background-color: white;
            border-radius: 5px;
        }
        QTabBar::tab {
            background-color: #e6e6e6;
            border: 1px solid #cccccc;
            border-bottom-color: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 12px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
        }
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3a76d8;
        }
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        QLineEdit, QSpinBox, QComboBox {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px;
            background-color: white;
        }
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #4a86e8;
        }
        QLabel {
            color: #333333;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
        }
        QTableWidget {
            border: 1px solid #cccccc;
            border-radius: 4px;
            gridline-color: #e6e6e6;
        }
        QHeaderView::section {
            background-color: #e6e6e6;
            padding: 6px;
            border: 1px solid #cccccc;
            font-weight: bold;
        }
        """

class CameraForm(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Tạo group box cho mỗi camera
        groupBox = QGroupBox(f"Camera {self.index + 1}")
        groupLayout = QGridLayout()
        
        # Tên camera
        groupLayout.addWidget(QLabel("Tên camera:"), 0, 0)
        self.camera_name = QLineEdit()
        self.camera_name.setPlaceholderText("Nhập tên camera")
        groupLayout.addWidget(self.camera_name, 0, 1)
        
        # Loại kết nối
        groupLayout.addWidget(QLabel("Cổng kết nối:"), 1, 0)
        self.connection_type = QComboBox()
        self.connection_type.addItems(["USB", "Ethernet", "HDMI", "Wi-Fi", "Bluetooth"])
        groupLayout.addWidget(self.connection_type, 1, 1)
        
        # Số lượng model
        groupLayout.addWidget(QLabel("Số lượng model:"), 2, 0)
        self.model_count = QSpinBox()
        self.model_count.setRange(1, 100)
        self.model_count.setValue(1)
        self.model_count.valueChanged.connect(self.update_models)
        groupLayout.addWidget(self.model_count, 2, 1)
        
        # Container cho các model
        self.models_container = QWidget()
        self.models_layout = QVBoxLayout(self.models_container)
        self.models_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo các model ban đầu
        self.model_inputs = []
        self.update_models(1)
        
        # Thêm container vào layout
        groupLayout.addWidget(self.models_container, 3, 0, 1, 2)
        
        groupBox.setLayout(groupLayout)
        layout.addWidget(groupBox)
        self.setLayout(layout)
    
    def update_models(self, count):
        # Xóa các model hiện tại
        while self.models_layout.count():
            item = self.models_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.model_inputs = []
        
        # Tạo các model mới
        for i in range(count):
            model_frame = QFrame()
            model_layout = QHBoxLayout(model_frame)
            model_layout.setContentsMargins(0, 0, 0, 0)
            
            model_label = QLabel(f"Model {i + 1}:")
            model_input = QLineEdit()
            model_input.setPlaceholderText(f"Nhập tên model {i + 1}")
            
            model_layout.addWidget(model_label)
            model_layout.addWidget(model_input)
            
            self.models_layout.addWidget(model_frame)
            self.model_inputs.append(model_input)
    
    def get_data(self):
        models = [input.text() for input in self.model_inputs]
        return {
            "camera_name": self.camera_name.text(),
            "connection_type": self.connection_type.currentText(),
            "models": models
        }

class ProductCodeForm(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.camera_forms = []
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Group box cho thông tin mã hàng
        groupBox = QGroupBox(f"Mã hàng {self.index + 1}")
        groupLayout = QGridLayout()
        
        # Tên mã hàng
        groupLayout.addWidget(QLabel("Tên mã hàng:"), 0, 0)
        self.product_code = QLineEdit()
        self.product_code.setPlaceholderText("Nhập tên mã hàng")
        groupLayout.addWidget(self.product_code, 0, 1)
        
        # Số lượng camera
        groupLayout.addWidget(QLabel("Số lượng camera:"), 1, 0)
        self.camera_count = QSpinBox()
        self.camera_count.setRange(1, 100)
        self.camera_count.setValue(1)
        self.camera_count.valueChanged.connect(self.update_cameras)
        groupLayout.addWidget(self.camera_count, 1, 1)
        
        groupBox.setLayout(groupLayout)
        layout.addWidget(groupBox)
        
        # Scroll area cho các camera
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.cameras_container = QWidget()
        self.cameras_layout = QVBoxLayout(self.cameras_container)
        self.cameras_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo các camera ban đầu
        self.update_cameras(1)
        
        self.scroll.setWidget(self.cameras_container)
        layout.addWidget(self.scroll)
        
        self.setLayout(layout)
    
    def update_cameras(self, count):
        # Lưu dữ liệu camera hiện tại
        current_data = []
        for form in self.camera_forms:
            if form.camera_name.text() or form.connection_type.currentIndex() > 0:
                current_data.append(form.get_data())
        
        # Xóa các camera hiện tại
        while self.cameras_layout.count():
            item = self.cameras_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.camera_forms = []
        
        # Tạo các camera mới
        for i in range(count):
            camera_form = CameraForm(i)
            self.cameras_layout.addWidget(camera_form)
            self.camera_forms.append(camera_form)
        
        # Khôi phục dữ liệu
        for i, data in enumerate(current_data):
            print(i,'data',data)
            if i < len(self.camera_forms):
                self.camera_forms[i].camera_name.setText(data["camera_name"])
                index = self.camera_forms[i].connection_type.findText(data["connection_type"])
                if index >= 0:
                    self.camera_forms[i].connection_type.setCurrentIndex(index)
                
                model_count = len(data["models"])
                self.camera_forms[i].model_count.setValue(model_count)
                
                for j, model in enumerate(data["models"]):
                    if j < len(self.camera_forms[i].model_inputs):
                        self.camera_forms[i].model_inputs[j].setText(model)
    
    def get_data(self):
        cameras = [form.get_data() for form in self.camera_forms]
        return {
            "product_code": self.product_code.text(),
            "cameras": cameras
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product_code_forms = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Hệ thống Quản lý Thiết bị")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(StyleHelper.get_style())
        
        # Widget chính
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Header
        header_layout = QHBoxLayout()
        
        logo_label = QLabel()
        # Thêm logo nếu có
        # logo_label.setPixmap(QPixmap("logo.png").scaled(64, 64, Qt.KeepAspectRatio))
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("HỆ THỐNG QUẢN LÝ THIẾT BỊ")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label, 1)
        
        main_layout.addLayout(header_layout)
        
        # Form thông tin máy
        machine_group = QGroupBox("Thông tin máy")
        machine_layout = QGridLayout()
        
        machine_layout.addWidget(QLabel("Tên máy:"), 0, 0)
        self.machine_name = QLineEdit()
        self.machine_name.setPlaceholderText("Nhập tên máy (VD: NQAI)")
        machine_layout.addWidget(self.machine_name, 0, 1)
        
        machine_layout.addWidget(QLabel("Số lượng mã hàng:"), 1, 0)
        self.product_code_count = QSpinBox()
        self.product_code_count.setRange(1, 100)
        self.product_code_count.setValue(1)
        self.product_code_count.valueChanged.connect(self.update_product_codes)
        machine_layout.addWidget(self.product_code_count, 1, 1)
        
        machine_group.setLayout(machine_layout)
        main_layout.addWidget(machine_group)
        
        # Tab widget cho các mã hàng
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(True)
        
        # Tạo tab ban đầu
        self.update_product_codes(1) 
        
        main_layout.addWidget(self.tab_widget)
        
        # Nút lưu và xem thông tin
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Lưu thông tin")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)
        
        self.view_button = QPushButton("Xem thông tin")
        self.view_button.setIcon(QIcon.fromTheme("document-open"))
        self.view_button.clicked.connect(self.view_data)
        button_layout.addWidget(self.view_button)
        
        self.clear_button = QPushButton("Xóa tất cả")
        self.clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        self.clear_button.clicked.connect(self.clear_data)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        self.setCentralWidget(main_widget)
    
    def update_product_codes(self, count):
        # Lưu dữ liệu mã hàng hiện tại
        current_data = []
        for form in self.product_code_forms:
            if form.product_code.text():
                current_data.append(form.get_data())
        
        # Xóa các tab hiện tại
        self.tab_widget.clear()
        self.product_code_forms = []
        
        # Tạo các tab mới
        for i in range(count):
            product_code_form = ProductCodeForm(i)
            self.tab_widget.addTab(product_code_form, f"Mã hàng {i + 1}")
            self.product_code_forms.append(product_code_form)
        
        print('current_data',current_data)
        # Khôi phục dữ liệu
        for i, data in enumerate(current_data):
            if i < len(self.product_code_forms):
                self.product_code_forms[i].product_code.setText(data["product_code"])
                camera_count = len(data["cameras"])
                self.product_code_forms[i].camera_count.setValue(camera_count)
                
                for j, camera_data in enumerate(data["cameras"]):
                    if j < len(self.product_code_forms[i].camera_forms):
                        camera_form = self.product_code_forms[i].camera_forms[j]
                        camera_form.camera_name.setText(camera_data["camera_name"])
                        index = camera_form.connection_type.findText(camera_data["connection_type"])
                        if index >= 0:
                            camera_form.connection_type.setCurrentIndex(index)
                        
                        model_count = len(camera_data["models"])
                        camera_form.model_count.setValue(model_count)
                        
                        for k, model in enumerate(camera_data["models"]):
                            if k < len(camera_form.model_inputs):
                                camera_form.model_inputs[k].setText(model)
    
    def save_data(self):
        # Kiểm tra dữ liệu trước khi lưu
        if not self.machine_name.text():
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tên máy!")
            return
        
        data = {
            "machine_name": self.machine_name.text(),
            "product_codes": []
        }
        
        for form in self.product_code_forms:
            if form.product_code.text():
                product_code_data = form.get_data()
                data["product_codes"].append(product_code_data)
        
        if not data["product_codes"]:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập ít nhất một mã hàng!")
            return
        
        # Đoạn code này có thể được mở rộng để lưu dữ liệu vào file hoặc database
        print("Dữ liệu đã lưu:", data)
        
        QMessageBox.information(self, "Thông báo", "Lưu thông tin thành công!")
    
    def view_data(self):
        # Tạo cửa sổ mới để hiển thị dữ liệu
        self.data_window = QMainWindow(self)
        self.data_window.setWindowTitle("Thông tin chi tiết")
        self.data_window.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Header
        machine_info = QLabel(f"Thông tin máy: {self.machine_name.text()}")
        machine_info.setFont(QFont("Arial", 14, QFont.Bold))
        machine_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(machine_info)
        
        # Tạo tab widget để hiển thị các mã hàng
        tab_widget = QTabWidget()
        
        for i, form in enumerate(self.product_code_forms):
            if not form.product_code.text():
                continue
                
            product_data = form.get_data()
            
            # Tab cho mỗi mã hàng
            product_tab = QWidget()
            product_layout = QVBoxLayout(product_tab)
            
            # Tiêu đề mã hàng
            product_title = QLabel(f"Mã hàng: {product_data['product_code']}")
            product_title.setFont(QFont("Arial", 12, QFont.Bold))
            product_layout.addWidget(product_title)
            
            # Bảng thông tin camera
            table = QTableWidget()
            table.setRowCount(len(product_data["cameras"]))
            table.setColumnCount(4)  # Camera, Kết nối, Số model, Chi tiết model
            
            table.setHorizontalHeaderLabels(["Tên camera", "Cổng kết nối", "Số lượng model", "Chi tiết model"])
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            
            for row, camera_data in enumerate(product_data["cameras"]):
                table.setItem(row, 0, QTableWidgetItem(camera_data["camera_name"]))
                table.setItem(row, 1, QTableWidgetItem(camera_data["connection_type"]))
                table.setItem(row, 2, QTableWidgetItem(str(len(camera_data["models"]))))
                
                models_text = ", ".join(camera_data["models"])
                table.setItem(row, 3, QTableWidgetItem(models_text))
            
            product_layout.addWidget(table)
            
            tab_widget.addTab(product_tab, product_data["product_code"])
        
        layout.addWidget(tab_widget)
        
        # Nút đóng
        close_button = QPushButton("Đóng")
        close_button.clicked.connect(self.data_window.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        self.data_window.setCentralWidget(central_widget)
        self.data_window.show()
    
    def clear_data(self):
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa tất cả dữ liệu?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.machine_name.clear()
            self.product_code_count.setValue(1)
            self.update_product_codes(1)
            QMessageBox.information(self, "Thông báo", "Đã xóa tất cả dữ liệu!")

class ExportDialog(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Xuất dữ liệu")
        self.setMinimumSize(600, 500)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Tab widget cho các định dạng xuất
        tab_widget = QTabWidget()
        
        # Tab cho xuất CSV
        csv_tab = QWidget()
        csv_layout = QVBoxLayout(csv_tab)
        
        csv_info = QLabel("Dữ liệu sẽ được xuất ra file CSV với các cột: Máy, Mã hàng, Camera, Kết nối, Models")
        csv_layout.addWidget(csv_info)
        
        csv_preview = QLabel("Xem trước:")
        csv_layout.addWidget(csv_preview)
        
        csv_text = QTableWidget()
        csv_text.setRowCount(5)
        csv_text.setColumnCount(5)
        csv_text.setHorizontalHeaderLabels(["Máy", "Mã hàng", "Camera", "Kết nối", "Models"])
        csv_text.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        csv_layout.addWidget(csv_text)
        
        export_csv_button = QPushButton("Xuất CSV")
        csv_layout.addWidget(export_csv_button, alignment=Qt.AlignRight)
        
        tab_widget.addTab(csv_tab, "CSV")
        
        # Tab cho xuất JSON
        json_tab = QWidget()
        json_layout = QVBoxLayout(json_tab)
        
        json_info = QLabel("Dữ liệu sẽ được xuất ra file JSON theo cấu trúc phân cấp")
        json_layout.addWidget(json_info)
        
        json_text = QLineEdit()
        json_text.setReadOnly(True)
        json_layout.addWidget(json_text)
        
        export_json_button = QPushButton("Xuất JSON")
        json_layout.addWidget(export_json_button, alignment=Qt.AlignRight)
        
        tab_widget.addTab(json_tab, "JSON")
        
        layout.addWidget(tab_widget)
        
        # Nút đóng
        close_button = QPushButton("Đóng")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  