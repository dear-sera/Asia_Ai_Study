"""
3. 모델 예측 파일
"""

from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import glob

model = load_model('../models/cat_and_dog_binary_classfication.h5')  #상위폴더 아래에 있는 모델이기때문에 ..을 붙임
print(model.summary())  #모델이 잘 불러왔는지를 확인하기 위해

img_dir = '../datasets/cat_dog/'  #분류 사진의 경로를 지정

#이미지 크기 설정
image_w = 64
image_h = 64

#강아지 사진 랜덤으로 추출하기
dog_files = glob.glob(img_dir + 'dog*.jpg')  #강아지 파일의 이름을 리스트로 만듬
dog_sample = np.random.randint((len(dog_files)))  #강아지 이름 리스트 중 하나를 랜덤하게 가져온다
dog_sample_path = dog_files[dog_sample]  #강아지 이미지의 경로

#고양이 사진 랜덤으로 추출하기
cat_files = glob.glob(img_dir + 'cat*.jpg') #고양이 파일의 이름을 리스트로 만듬
cat_sample = np.random.randint((len(cat_files)))  #고양이 이름 리스트 중 하나를 랜덤하게 가져온다
cat_sample_path = cat_files[cat_sample]  #고양이 이미지의 경로

print(dog_sample_path)
print(cat_sample_path)

#경로가 에러날 수 있으니 try문 사용
try:
    #dog 데이터 전처리
    img = Image.open(dog_sample_path)  #랜덤으로 추출한 이미지 열기
    img.show()  #어떤 사진인지 확인하기
    img = img.convert('RGB')
    img = img.resize((image_w, image_h)) #이미지 크기 조정
    data = np.asarray(img)  #np형식으로 변경
    data = data / 255 #데이터 스케일링
    dog_data = data.reshape(1, 64, 64, 3)  #컬러는 3이기에 마지막으로 넣어주기, 64*64로 지정

    #cat 데이터 전처리
    img = Image.open(cat_sample_path)
    img.show()
    img = img.convert('RGB')
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    data = data / 255
    cat_data = data.reshape(1, 64, 64, 3)
except:
    print('error')

print(data.shape) #전처리과정 확인

#반올림을 하여 결과값을 예측한다 : 고양이는 0, 강아지는 1
print('dog data : ', model.predict(dog_data).round())
print('cat data : ', model.predict(cat_data).round())


