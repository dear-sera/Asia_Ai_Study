"""
3. 모델 예측 파일
"""

from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import glob

model = load_model('../models/horse_and_human_binary_classfication.h5')  #상위폴더 아래에 있는 모델이기때문에 ..을 붙임
print(model.summary())  #모델이 잘 불러왔는지를 확인하기 위해

img_dir = '../datasets/horse_or_human/'  #분류 사진의 경로를 지정

#이미지 크기 설정
image_w = 64
image_h = 64

#말 사진 랜덤으로 추출해보기
horse_files = glob.glob(img_dir + 'horse*.png')  #glob 모듈의 glob 함수는 사용자가 제시한 조건에 맞는 파일명을 리스트 형식으로 반환한다
horse_sample = np.random.randint((len(horse_files)))  #리스트 중 하나를 랜덤으로 가져온다
horse_sample_path = horse_files[horse_sample]

#사람 사진 랜덤으로 추출해보기
human_files = glob.glob(img_dir + 'human*.png')
human_sample = np.random.randint((len(human_files)))
human_sample_path = human_files[human_sample]

#랜덤 이미지 경로 출력해보기
print(horse_sample_path)
print(human_sample_path)

#경로가 에러날 수 있으니 try문 사용
try:
    #horse 이미지 전처리
    img = Image.open(horse_sample_path)   #랜덤으로 추출한 이미지 열기
    img.show()
    img = img.convert('RGB')
    img = img.resize((image_w, image_h))
    data = np.asarray(img)  #np형식으로 변경
    data = data/ 255  #데이터 스케일링
    horse_data = data.reshape(1, 64, 64, 3)

    #human 이미지 전처리
    img = Image.open(human_sample_path)
    img.show()
    img = img.convert('RGB')
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    data = data / 255
    human_data = data.reshape(1, 64, 64, 3)
except:
    print('error')

print(data.shape) #전처리과정 확인

#반올림으로 결과 값을 예측한다. 말이면 0, 사람이면 1
print('horse predict : ', model.predict(horse_data).round())
print('human predict : ', model.predict(human_data).round())