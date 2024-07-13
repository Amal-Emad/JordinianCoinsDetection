from ultralytics import YOLO

model = YOLO(r'C:\Users\user\Downloads\jdcoins.pt')


results = model(source=1 , show=True ,conf = 0.02,save=True)