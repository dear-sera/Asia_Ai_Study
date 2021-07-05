import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2
import time

form_window = uic.loadUiType('./mainWidget.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.path = None
        self.setupUi(self)
        self.model = load_model('../models/cat_and_dog_binary_classfication.h5')

        self.btn_select.clicked.connect(self.predict_image)

    def predict_image(self):
        capture = cv2.VideoCapture(0)  # 비디오 캡쳐 기능, 0은 내 노트북 카메라 번호(기본이 0)

        # 캡쳐 사이즈 설정
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        flag = True
        while flag:
            ret, frame = capture.read()  # 읽을 때마다 캡쳐함
            cv2.imshow("VideoFrame", frame)  # frame = 캡쳐된 이미지
            time.sleep(0.5)  # 딜레이함수, 0.05초마다 멈춘다
            print('cature')
            cv2.imwrite('./imgs/capture.png', frame)

            key = cv2.waitKey(33)  # waitKey= 33sec마다 키를 누르는 것
            if key == 27:  # 27 = esc버튼 = 버튼을 누르면 false가 되어 종료가 된다
                flag = False

            pixmap = QPixmap('./imgs/capture.png')
            self.lbl_image.setPixmap(pixmap)

            try:
                img = Image.open('./imgs/capture.png')
                img = img.convert('RGB')
                img = img.resize((64,64))
                data = np.asarray(img)
                data = data / 255
                data = data.reshape(1,64,64,3)
            except:
                  print('error')
            predict_value = self.model.predict(data)
            if predict_value > 0.5:
                self.lbl_predict.setText('이 이미지는 ' +
                   str((predict_value[0][0] * 100).round()) + '% 확률로 Dog입니다.')
            else:
                self.lbl_predict.setText('이 이미지는 ' +
                   str(((1 - predict_value[0][0]) * 100).round()) + '% 확률로 Cat입니다.')
        capture.release()  # 카메라를 잡고있지 못하게 놔주는 것 (에러가 나면 계속 카메라를 잡고있는다)
        cv2.destroyAllWindows()  # 지정된 윈도우 파괴

app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())