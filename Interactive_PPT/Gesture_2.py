import cv2
import numpy as np
import tkinter
import HandTracking as htm
import pynput.keyboard as Keyboard
import pynput.mouse as Mouse
import time

# Get resolution of the Monitor Screen
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

mouse = Mouse.Controller()
keyboard = Keyboard.Controller()

# wCam, hCam = 1920, 1080
wCam, hCam = 640, 480
frameR = 125

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.5)

pos = []
dist = 0
dist1 = 0
dist2 = 0
distance1 = []
distance2 = []
function1 = False
function2 = False
gesture = False
click = False
happen = False
next_time = 0
point_0_l = 0
dist_click = 0
f1_l = 0
f2_l = 0
i = 0
present_distances = []
is_present = 0
txt = 0
txt_time = 16
disp_time = 0
mouse_pressed = 0
key_pressed = 0
erased = 0
pressed_start = 0

# String
txt = 0
disp = ''

# Scale Hand for Depth
def scale(lmList):
    sq_x = 0
    sq_y = 0
    for i in [1, 5, 9, 13, 17]:
        sq_x = sq_x + (lmList[i][1] - lmList[0][1]) ** 2
        sq_y = sq_y + (lmList[i][2] - lmList[0][2]) ** 2
    size = int(np.sqrt(sq_x + sq_y))
    zoom = 1 / (size / 300)
    return zoom


# Function to get distance of fingers from thumb
def distance(lmList):
    # Global Variables
    global present_distances

    # Calling Scale Function
    zoom = scale(lmList)

    # Coordinates of fingers
    thumb1, thumb2 = lmList[4][1], lmList[4][2]
    index1, index2 = lmList[8][1], lmList[8][2]
    middle1, middle2 = lmList[12][1], lmList[12][2]
    ring1, ring2 = lmList[16][1], lmList[16][2]
    pinky1, pinky2 = lmList[20][1], lmList[20][2]

    # Distance of fingers from thumb
    hyp = np.sqrt((index1 - thumb1) ** 2 + (index2 - thumb2) ** 2
                  + (middle1 - thumb1) ** 2 + (middle2 - thumb2) ** 2
                  + (ring1 - thumb1) ** 2 + (ring2 - thumb2) ** 2
                  + (pinky1 - thumb1) ** 2 + (pinky2 - thumb2) ** 2)

    # Adjusting distance for depth
    hyp = hyp * zoom

    # Appending Distances
    present_distances.append(hyp)


# Presentation Mode On
def present_on(lmList):
    # Global Variables
    global is_present, present_distances, txt

    # Call Distance Function
    distance(lmList)

    # Press F5 on gesture
    try:
        if is_present == 0:
            if present_distances[-6] < 150:
                nxt = present_distances[-6]
                for i in present_distances[-5:-1]:
                    if i > nxt:
                        nxt = i
                    else:
                        break

                if nxt > 360:
                    txt = 'Present'
                    keyboard.press(Keyboard.Key.f5)
                    keyboard.release(Keyboard.Key.f5)
                    is_present = 1
                    time.sleep(0.5)
    except:
        pass


# Presentation Mode Off
def present_off():
    # Global Variables
    global is_present, present_distances, txt, function1 ,function2

    try:
        if is_present == 1:
            nxt = 0
            if present_distances[-6] > 360:
                nxt = present_distances[-6]
                for i in present_distances[-5:-1]:
                    if i < nxt:
                        # print(next)
                        nxt = i
                    else:
                        break

                if nxt < 150:
                    txt = 'Leave Presentation Mode'
                    keyboard.press(Keyboard.Key.esc)
                    keyboard.release(Keyboard.Key.esc)
                    keyboard.press(Keyboard.Key.esc)
                    keyboard.release(Keyboard.Key.esc)
                    is_present = 0
                    function1 = False
                    function2 = False
    except:
        pass


def cursor_hold(lmList, img):
    # Global Variable
    global frameR, width, height, mouse_pressed, key_pressed, erased, pressed_start, txt, click

    x1, y1 = lmList[8][1], lmList[8][2]
    x2, y2 = lmList[12][1], lmList[12][2]
    #click = True

    # fingers = fingers_up(lmList)
    zoom = scale(lmList)
    dist = np.sqrt((lmList[8][1] - lmList[12][1]) ** 2 + (lmList[8][2] - lmList[12][2]) ** 2)
    dist = dist * zoom

    # Index and Middle raised : Click
    if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[13][2]:
        cv2.line(img, (lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]), (255, 0, 0), 3)

        if dist < 45:
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            x3 = np.interp(x1, (frameR, cap.get(3) - frameR), (0, width))
            y3 = np.interp(y1, (frameR, cap.get(4) - frameR), (0, height))
            if mouse_pressed == 1:
                mouse.position = (x3, y3)
                mouse.press(Mouse.Button.left)

            if key_pressed == 0:
                with keyboard.pressed(Keyboard.Key.ctrl):
                    keyboard.press('p')
                    keyboard.release('p')
                key_pressed = 1
                mouse_pressed = 1
                erased = 0
                pressed_start = time.time()
                txt = 'Drawing Mode On'

        if (mouse_pressed == 1) & ((time.time() - pressed_start) > 11):
            mouse.release(Mouse.Button.left)
            mouse_pressed = 0
            txt = 'Drawing Mode Off'

        if dist > 30 or lmList[13][2] > lmList[16][2]:
            if key_pressed == 1:
                if mouse_pressed == 1:
                    mouse.release(Mouse.Button.left)
                    mouse_pressed = 0
                key_pressed = 0
                with keyboard.pressed(Keyboard.Key.ctrl):
                    keyboard.press('a')
                    keyboard.release('a')
                    txt = 'Drawing Mode Off'

def Gesture():
    global i,gesture,pos,dist,dist1,dist2,distance1,distance2,function1,function2,click,happen,next_time,point_0_l,dist_click,f1_l,f2_l,present_distances,is_present,txt,mouse_pressed,key_pressed,erased,pressed_start, txt_time, disp_time

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)
        txt = 0
        txt_time = txt_time + 1
        if len(lmList) != 0 and lmList[16][2] < lmList[0][2]:
            i += 1
            pos.append(lmList)
            dist = np.sqrt((lmList[8][1] - lmList[4][1]) ** 2 + (lmList[8][2] - lmList[4][2]) ** 2)
            distance1.append(dist)
            dist1 = np.sqrt((lmList[20][1] - lmList[4][1]) ** 2 + (lmList[20][2] - lmList[4][2]) ** 2)
            distance2.append(dist1)
            dist2 = np.sqrt((lmList[12][1] - lmList[4][1]) ** 2 + (lmList[12][2] - lmList[4][2]) ** 2)
            x1, y1 = lmList[8][1], lmList[8][2]

            # Gesture Switch
            if dist2< 20 and lmList[8][2]<lmList[6][2] and lmList[20][2]<lmList[18][2] and lmList[16][2]>lmList[13][2]:
                if gesture == False:
                    gesture = True
                    txt = 'Gesture on'
                elif gesture == True:
                    gesture = False
                    txt = 'Gesture off'
                lmList[20][2] = 480
                time.sleep(1)

            if gesture==True:

                present_on(lmList)
                present_off()

                # Function 1 Zoom
                # Fuction 1 Switch
                if len(distance1) > 5:
                    pos.pop(0)
                    distance1.pop(0)
                    if distance1[-4] < 25 and distance1[-3] < 25 and distance1[-5] < 25 and distance1[-2] < 25 and distance1[
                        -1] < 25 and lmList[0][2] < 400:
                        if function1 == False:
                            function1 = True
                            function2 = False
                            txt = 'Zoom on'
                        elif function1 == True:
                            function1 = False
                            txt = 'Zoom off'
                        time.sleep(1)

                # Fuction 1 Fuctionalities
                if function1 == True:
                    if lmList[9][2] < 400:
                        point_0 = lmList[9][2]

                        # Zoom out
                        if ((point_0 - point_0_l) > (25) and point_0_l != 0 and lmList[12][2] < lmList[11][
                            2]) and click == False and lmList[4][1] < 320:
                            txt = '-'
                            keyboard.press('-')
                            keyboard.release('-')
                            happen = True
                            time.sleep(0.5)

                        # Zoom In
                        if ((point_0_l - point_0) > (25) and point_0_l != 0 and lmList[12][2] < lmList[11][
                            2]) and click == False and lmList[4][1] > 320:
                            txt = '+'
                            keyboard.press('=')
                            keyboard.release('=')
                            happen = True
                            time.sleep(0.5)

                        if happen == False:
                            point_0_l = point_0
                        elif happen == True:
                            point_0_l = 0
                            happen = False

                        # Cursor Movements
                        if (lmList[8][2] < lmList[6][2]) and (lmList[16][2] > lmList[14][2]):
                            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)

                            # Convert Coordinates
                            x3 = np.interp(x1, (frameR, cap.get(3) - frameR), (0, width))
                            y3 = np.interp(y1, (frameR, cap.get(4) - frameR), (0, height))
                            mouse.position = (x3, y3)
                            dist_click = np.sqrt((lmList[8][1] - lmList[12][1]) ** 2 + (lmList[8][2] - lmList[12][2]) ** 2)
                            # print(dist_click)

                            if dist_click < 20:
                                if click == False:
                                    click = True
                                    mouse.press(Mouse.Button.left)
                                    txt = 'click on'
                                    time.sleep(0.25)
                                elif click == True:
                                    click = False
                                    mouse.release(Mouse.Button.left)
                                    txt = 'click off'
                                    time.sleep(0.25)

                # Function 2

                if len(distance2) > 5:
                    # pos.pop(0)
                    distance2.pop(0)
                    #cv2.line(img, (lmList[4][1], lmList[4][2]), (lmList[20][1], lmList[20][2]), (255, 0, 0), 3)
                    #print(len(distance2))

                    # Function 2 Switch
                    if distance2[-4] < 25 and distance2[-3] < 25 and distance2[-5] < 25 and distance2[-2] < 25 and distance2[
                        -1] < 25 and lmList[12][2] < lmList[11][2] and lmList[0][2] < 400:
                        if function2 == False:
                            function2 = True
                            function1 = False
                            txt = 'Pen on'
                        elif function2 == True:
                            function2 = False
                            txt = 'Pen off'
                        time.sleep(1)

                # Function 2 Functionalities
                if function2 == True:

                    # Eraser
                    if lmList[4][2] > lmList[0][2]:
                        keyboard.press('e')
                        keyboard.release('e')
                        txt = 'Erase'
                        happen = True
                        time.sleep(0.5)

                    # Cursor Movements
                    if (lmList[8][2] < lmList[6][2]) and (lmList[16][2] > lmList[13][2]):
                        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)

                        # Convert Coordinates
                        x3 = np.interp(x1, (frameR, cap.get(3) - frameR), (0, width))
                        y3 = np.interp(y1, (frameR, cap.get(4) - frameR), (0, height))
                        mouse.position = (x3, y3)
                    cursor_hold(lmList, img)

                # Slide Motion
                if lmList[8][2] < 400 and lmList[20][2] < 400 and lmList[20][2] < lmList[18][2] and function1==False :
                    f1 = lmList[12][1]
                    f2 = lmList[20][1]

                    if (f1_l - f1) > (70) and (f2_l - f2) > (70) and f1_l != 0 :
                        txt = 'Next Slide'
                        keyboard.press('n')
                        keyboard.release('n')
                        happen = True
                        time.sleep(1)

                        # elif  f1_l<320:
                    if (f1 - f1_l) > (70) and (f2 - f2_l) > (70) and f1_l != 0 :
                        txt = 'Previous Slide'
                        keyboard.press('p')
                        keyboard.release('p')
                        happen = True
                        time.sleep(1)

                    if happen == False:
                        f1_l = f1
                        f2_l = f2
                    elif happen == True:
                        f1_l = 0
                        f2_l = 0
                        happen = False


        elif len(lmList) == 0:
            f1_l = 0
            f2_l = 0
            point_0_l = 0

            # print(i,len(pos))
            # if len(pos)==5 &
            # print(function)

        # cv2.imshow('Img', img)
        # cv2.waitKey(20)
        if txt_time > 1000:
            txt_time = 16
            disp_time = 0

        if txt != 0:
            disp = txt
            disp_time = txt_time

        if disp_time >= (txt_time - 15):
            cv2.putText(img, disp, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

