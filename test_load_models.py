import torch
model = torch.hub.load('./yolov5','custom', path=r"C:\gui_part\models_pt\cam1\model1\NQDVNHT_M100_CAMERA_1_2025-02-05.pt", source='local',force_reload =False)

label = model.names
for label in label.values():
    print(label)