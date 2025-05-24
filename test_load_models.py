# list = [{'Label Name': 'mat1', 'Join': '125335', 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'mat2', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'mat3', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'mat4', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'tu_dien', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'mat5', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'mat6', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'chau_dien', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'keo_dinh_chau', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'di_vat', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}, {'Label Name': 'dithuong', 'Join': True, 'OK': False, 'NG': False, 'Quantity': '0', 'Width Min': '0', 'Width Max': '0', 'Height Min': '0', 'Height Max': '0', 'Assign Value': '0', 'Confidence': '0'}]
# label_name = 'mat1'
# for i in list:
#     if i['Label Name'] == label_name:
#         print(i['Join'])
#         break

t = '[0]%USB%MV-CA023-10UC%02DA4201734'

port = t.split('%')[1]
chModeName = t.split('%')[2]
strSerialNumber = t.split('%')[3]
print(port,chModeName,strSerialNumber)




# import sys,os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from PyQt5 import QtCore, QtGui, QtWidgets
# from core.core import *

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     device = Initial_Device(MainWindow,ui)
#     ui.setupUi(MainWindow)
#     ui.pushButton_find_device.clicked.connect(device.enum_devices)
#     ui.pushButton_Connect_Device.clicked.connect(device.open_device)
#     ui.pushButton_set_load.clicked.connect(device.user_set_load)
#     ui.pushButton_set_save.clicked.connect(device.set_param)
#     ui.radioButton_check_continous.clicked.connect(device.set_continue_mode)
#     ui.pushButton_start_stream.clicked.connect(device.start_grabbing)
#     ui.pushButton_stop_stream.clicked.connect(device.stop_grabbing)
#     MainWindow.show()
#     sys.exit(app.exec_())