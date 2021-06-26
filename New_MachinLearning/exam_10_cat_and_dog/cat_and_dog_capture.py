import time
import cv2

capture = cv2.VideoCapture(0)  #비디오 캡쳐 기능, 0은 내 노트북 카메라 번호(기본이 0)

#캡쳐 사이즈 설정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
flag = True
while flag:
    ret, frame = capture.read()  #읽을 때마다 캡쳐함
    cv2.imshow("VideoFrame", frame)  #frame = 캡쳐된 이미지
    time.sleep(0.05)  #딜레이함수, 0.05초마다 멈춘다
    print('cature')
    key = cv2.waitKey(33)  #waitKey= 33sec마다 키를 누르는 것
    if key == 27:  #27 = esc버튼 = 버튼을 누르면 false가 되어 종료가 된다
        flag = False

capture.release()  #카메라를 잡고있지 못하게 놔주는 것 (에러가 나면 계속 카메라를 잡고있는다)
cv2.destroyAllWindows()  #지정된 윈도우 파괴