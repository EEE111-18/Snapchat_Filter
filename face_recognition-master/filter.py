import cv2
import face_recognition
head = cv2.imread('head.png', -1)
cheek = cv2.imread('cheek.png', -1)
head = cv2.cvtColor(head, cv2.COLOR_BGR2BGRA)
cheek = cv2.cvtColor(cheek, cv2.COLOR_BGR2BGRA)
cam = cv2.VideoCapture(0)

def Overlay(frame,filterr,w_offset,h_offset):
    filterr_h,filterr_w,filterr_ = filterr.shape
    frame_h,frame_w,frame_ = frame.shape
    for i in range(0, filterr_h):
        for j in range(0, filterr_w):
            if filterr[i,j][3]!= 0:
                frame[h_offset+i, w_offset+j] = filterr[i][j]
    return frame
while (cam.isOpened()):
    ret, frame = cam.read()
    face_locations = face_recognition.face_locations(frame)
    face_landmarks = face_recognition.face_landmarks(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    for e in face_landmarks:
        cheek_w = (e['left_eye'][0][0])-30 
        cheek_h = (e['left_eye'][2][1])+20
        cheek_filterr = cv2.resize(cheek, (50+(int(e['right_eye'][3][0]) - int(e['left_eye'][0][0])), (30+((int(e['left_eye'][4][1]) + int(e['left_eye'][5][1]))//2) - ((int(e['left_eye'][1][1]) + int(e['left_eye'][2][1]))//2))))
        head_w = (e['left_eye'][0][0])-70
        head_h = (e['left_eye'][2][1])-120
        head_filterr = cv2.resize(head, (160+(int(e['right_eye'][3][0]) - int(e['left_eye'][0][0])), (80+((int(e['left_eye'][4][1]) + int(e['left_eye'][5][1]))//2) - ((int(e['left_eye'][1][1]) + int(e['left_eye'][2][1]))//2))))
        Overlay (frame, head_filterr, head_w, head_h)
        Overlay (frame, cheek_filterr, cheek_w, cheek_h)
    cv2.imshow("Video", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
