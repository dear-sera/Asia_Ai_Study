"""
1. 데이터 전처리. 이미지 파일을 바이너리로 train, test 나눠 저장
"""

from PIL import Image
import glob
import numpy as np
from sklearn.model_selection import train_test_split

img_dir = '../datasets/cat_dog/'  #..는 상위폴더를 뜻함, 사진 폴더 경로 지정
categories = ['cat', 'dog']  #이미지 카테고리

image_w = 64  #이미지의 폭
image_h = 64  #이미지의 높이

pixel = image_h * image_w * 3 #픽셀의 갯수, 높이 * 폭 * 3컬러

# image, label 저장할 변수 초기화
X = []
Y = []
files = None

# 카테고리별 반복(2회), 첫 for문은 cat이 들어감 , idx = 인덱스번호가 들어감(cat은 0, dog는 1)
for idx, category in enumerate(categories):  #enumerate= 자료형을 입력받으면 인덱스 값을 포함하는 enumerate 객체를 돌려줘서, cat, dog를 하나씩 돌려준다
    files = glob.glob(img_dir + category + '*.jpg')  # 경로 내 해당 카테고리로 시작하는 파일 경로 리스트
    for i, f in enumerate(files):  # 각 경로명마다 반복, 파일의 경로를 받는다(f가 경로)
        # 파일 관련 작업이므로 try-except 사용
        try:
            # 이미지를 열어 RGB로 바꾸고 resize
            img = Image.open(f)  #Image=이미지 처리 패키지
            img = img.convert('RGB')  #이미지를 RGB(칼라모드)로 바꿔준다
            img = img.resize((image_w, image_h))  #이미지 크기를 64 * 64 픽셀로 지정
            # image와 label을 숫자로 저장
            data = np.asarray(img)
            X.append(data)  #asarray한 데이터 넣어주기
            Y.append(idx)   # 라벨 인덱스가 들어간다
            if i % 300 == 0:  #코드 진행사항을 보기 위해서 넣어준 것(300개 당 한 번씩 출력)
                print(category, ':', f)
        except:
            print(category, i, '번째에서 에러')

# ndarray로 변환
X = np.array(X)
Y = np.array(Y)

#스케일링, Y는 0, 1 둘 중 하나로 들어가서 따로 스케일링 하지 않는다
X = X / 255
print(X[0])
print(Y[0:5])
# train, test 나눔
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)

# 파일로 저장, 다른 파일에서 읽어서 실행할 수 있도록
xy = (X_train, X_test, Y_train, Y_test)
np.save('../datasets/binary_image_data.npy', xy)