"""
4. 이미지를 직접 선택해 예측률 알아보기(GUI)

터미널에서 designer을 쳐서 QtDesigner을 실행하여 mainWidget.ui를 만들기, 이 Qt를 이용해서 실행
"""
import sys
from PyQt5.QtWidgets import *  #* = 하위 모듈 모두 컴파일 하는 것
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

form_window = uic.loadUiType('./mainWidget.ui')[0]  #QtDesigner에서 직접 만든 창을 가져오기(ui 파일 로드)

#화면을 띄우는데 사용되는 Class 선언(# QWidget과 ui 파일을 상속받은 클래스)
class Exam(QWidget, form_window):  #ui창 실행시키기
    def __init__(self):
        super().__init__()   #super()는 상속받은 부모 클래스를 의미 (부모 생성자 실행)
        self.path = None
        self.setupUi(self)
        self.model = load_model('../models/cat_and_dog_binary_classfication.h5')

        self.btn_select.clicked.connect(self.predict_image)  #아래 predict_image 함수를 연결하는 것, btn_select(내가 설정한 이름)버튼을 눌렀을 때 실행되게 연결하는 것

    def predict_image(self):
        self.path = QFileDialog.getOpenFileName(  #QFileDialog를 여는 것, "Open file"=QFileDialog의 이름, 그 다음''는 지정 경로, 그 다음 ''는 파일형태를 적은 것 대로 고를 수 있게 해준다
            self,
            "Open file", 'C:\work\python\AI_exam\datasets\cat_dog',
            "Image Files(*.jpg);;All Files(*.*);;Text Files(*.txt)"
        )
        print(self.path)  #경로를 출력해주는 데 튜블로 나온다(처음 건 경로, 두번째껀 파일형태),  # 윈도우 file chooser 사용해 이미지 파일 선택 / (경로, 선택 타입) 튜플 반환
        if self.path[0]:  #경로를 받았을 때만 데이터를 선택할 수 있게
            #QPixmap이란, PyQt에서 이미지를 보여줄 때 사용하는 객체로 위에 사진에 있는 포맷들을 지원하는 객체, 위젯이 없어서 자체적으로 생선한 label로 이미지를 표현
            pixmap = QPixmap(self.path[0])  #경로를 pixmap형태로 바꿔줌
            self.lbl_image.setPixmap(pixmap)  #지정한 라벨(lbl_image)에 지정한 이미지로 바꿔줌

            #이미지 전처리
            try:
                img = Image.open(self.path[0])  #이미지 경로 지정
                img = img.convert('RGB')
                img = img.resize((64, 64))
                data = np.asarray(img)
                data = data / 255
                data = data.reshape(1, 64, 64, 3)
            except:
                print('error')

            predict_value = self.model.predict(data)
            if predict_value > 0.5: #0.5보다 크면 dog
                #지정된 라벨(lbl_predict)에 setText(Text Object에 텍스트를 선언 하는 메서드)를 넣어준다
                self.lbl_predict.setText('이 이미지는 ' +
                str((predict_value[0][0] * 100).round()) + '% 확률로 Dog입니다.')
            else:
                self.lbl_predict.setText('이 이미지는 ' +
                str(((1 - predict_value[0][0]) * 100).round()) + '% 확률로 Cat입니다.')


#QApplication : 프로그램을 실행시켜주는 클래스
app = QApplication(sys.argv)
mainWindow = Exam()  #클래스의 변수
mainWindow.show()  #프로그램 화면을 보여줌
sys.exit((app.exec_()))  #프로그램을 작동시키는 코드, exit를 쓰면 프로그램 종료 시 0을 리턴한다
