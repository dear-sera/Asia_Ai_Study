"""
2. 모델 생성 파일
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping
import  matplotlib.pyplot as plt

#데이터 불러와서 데이터 갯수 확인하기
X_train, X_test, Y_train, Y_test = np.load('../datasets/binary_image_data.npy', allow_pickle=True)  #allow_pickle=True로 줘야 array타입으로 불러와진다 (안하면 문자열로 읽힌다)
print('X_train shape :', X_train.shape)
print('X_test shape :', X_test.shape)
print('Y_train shape :', Y_train.shape)
print('Y_test shape :', Y_test.shape)

#모델 생성
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(64, 64, 3), padding='same', activation='relu'))  #컬러라서 3
model.add(MaxPool2D(pool_size=(2, 2)))  #이미지 사이즈 (32, 32)으로 변경, 사이즈가 64라서 padding은 적지 않아도 된다
model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))  #이미지 사이즈 (16, 16)으로 변경
model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))  #3번의 MaxPool2D를 거쳐서 이미지는 (8, 8)사이즈가 된다
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))  #이진분류기는 sigmoid

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_accuracy', patience=7)  #학습 시 정확도를 봤을 때 더 이상 오르지 않는 것이 7횟수가 넘었다면 멈춤
model.summary()

#모델학습
fit_hist = model.fit(X_train, Y_train, batch_size=64, epochs=100, validation_split=0.15, callbacks=[early_stopping]) #callbacks으로 EarlyStopping가져옴
model.save('../models/cat_and_dog_binary_classfication.h5')

score = model.evaluate(X_test, Y_test)
print('Evaluation loss :', score[0])
print('Evaluation accuracy :', score[1])

plt.plot(fit_hist.history['loss'], label='loss')
plt.plot(fit_hist.history['val_loss'], label='val_loss')
plt.legend()
plt.show()


plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()



