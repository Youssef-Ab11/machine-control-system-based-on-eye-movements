import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
from gaze_tracking import GazeTracking
import threading
import json
import pyautogui
import pyglet
import mediapipe as mp
import os
import math


global sounds
sounds = True

global mouseSpeed
mouseSpeed = 10

global state
state = ""

global mouth_ratio
mouth_ratio = 0

global mouth_coord_up
mouth_coord_up = []

global mouth_coord_down
mouth_coord_down = []

global T
T = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

app = Flask(__name__)
socketio = SocketIO(app)

gaze = GazeTracking()
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

left_sound = pyglet.media.load("./sounds/Left_sound.mp3", streaming=False)
right_sound = pyglet.media.load("./sounds/Right_sound.mp3", streaming=False)
up_sound = pyglet.media.load("./sounds/Up_sound.mp3", streaming=False)
down_sound = pyglet.media.load("./sounds/Down_sound.mp3", streaming=False)
left_click_sound = pyglet.media.load(
    "./sounds/Left_click_sound.mp3", streaming=False)
right_click_sound = pyglet.media.load(
    "./sounds/Right_click_sound.mp3", streaming=False)
start_sound = pyglet.media.load("./sounds/start_sound.mp3", streaming=False)
stop_sound = pyglet.media.load("./sounds/stop_sound.mp3", streaming=False)

pyautogui.FAILSAFE = False


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def generate_frames():

    global mouth_coord_down
    global mouth_coord_up
    global mouth_ratio
    global T

    global state
    pTime = 0
    C = 0

    while True:
        _, frame = webcam.read()
        width_f, height_f, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                upper_point_left = faceLms.landmark[82]
                upper_point_center = faceLms.landmark[13]
                upper_point_right = faceLms.landmark[312]
                lower_point_left = faceLms.landmark[87]
                lower_point_center = faceLms.landmark[14]
                lower_point_right = faceLms.landmark[317]

                distance_left = math.hypot(int((upper_point_left.x * width_f) - (lower_point_left.x * height_f)), int(
                    (upper_point_left.y * width_f) - (lower_point_left.y * height_f)))

                distance_center = math.hypot(int((upper_point_center.x * width_f) - (lower_point_center.x * height_f)), int(
                    (upper_point_center.y * width_f) - (lower_point_center.y * height_f)))

                distance_right = math.hypot(math.pow(int((upper_point_right.x * width_f) - (
                    lower_point_right.x * height_f)), int((upper_point_right.y * width_f) - (lower_point_right.y * height_f))))

                mouth_coord_up.append(int(upper_point_center.x * width_f))
                mouth_coord_up.append(int(upper_point_center.y * height_f))

                mouth_coord_down.append(int(lower_point_center.x * width_f))
                mouth_coord_down.append(int(lower_point_center.y * height_f))

                mouth_ratio = int(
                    (distance_left + distance_center + distance_right) / 3)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if mouth_ratio >= 108 and T == False:
            if C % 5 == 0:
                T = True
                start_sound.play()
            C = C+1

        elif mouth_ratio >= 108 and T == True:
            if C % 5 == 0:
                T = False
                stop_sound.play()
            C = C+1
        if T == True:

            global mouseSpeed

            if gaze.is_right():
                text = "Right"
                pyautogui.moveRel((mouseSpeed, 0))
                if C % 5 == 0:
                    right_sound.play()
                C = C+1
            elif gaze.is_left():
                text = "Left"
                pyautogui.moveRel((mouseSpeed * -1, 0))
                if C % 5 == 0:
                    left_sound.play()
                C = C+1
            elif gaze.is_up():
                text = "Up"
                pyautogui.moveRel((0, mouseSpeed * -1))
                if C % 5 == 0:
                    up_sound.play()
                C = C+1
            elif gaze.is_down():
                text = "Down"
                pyautogui.moveRel((0, mouseSpeed))
                if C % 5 == 0:
                    down_sound.play()
                C = C+1
            elif gaze.is_center():
                text = "Center"
            else:
                text = "Not detected"

        if T == False:
            if(gaze.is_right_blinking() == False) and (gaze.is_left_blinking() == True):
                text = "Right click"
                pyautogui.rightClick()
                if C % 5 == 0:
                    right_click_sound.play()
                C = C+1
            elif (gaze.is_right_blinking() == True) and (gaze.is_left_blinking() == False):
                text = "Left click"
                pyautogui.doubleClick()
                if C % 5 == 0:
                    left_click_sound.play()
                C = C+1

        if text == state:
            mouseSpeed = mouseSpeed + 0
        else:
            mouseSpeed = 10

        state = text

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, f'FPS: {int(fps)}', (400, 450),
                    cv2.FONT_HERSHEY_DUPLEX, 1.6, (43, 44, 46), 2)

        cv2.putText(frame, text, (80, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 1.6, (43, 44, 46), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def getEyeCoordinates():
    global state
    while True:
        _, frame = webcam.read()
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        gaze.refresh(frame)

        if cv2.waitKey(1) == ord('o'):
            break

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil),
                    (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil),
                    (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("GazeTracking", frame)

        return json.dumps({"right_pupil": str(gaze.pupil_left_coords()), "left_pupil": str(gaze.pupil_right_coords()), "state": str(state)})


def emitCoordinates():
    socketio.emit('coordinates', getEyeCoordinates())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video/')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Start')
def Start():
    print('EyeGaze is launching...')
    os.system('python app.py')
    return "started"


@app.route('/Stop')
def Stop():
    print('EyeGaze is stopping...')
    os.system('taskkill -f -im python*')
    return "stopped"


@socketio.on('connect')
def sendEyeCoordinates():
    print('Connected...')
    set_interval(emitCoordinates, 1)


if __name__ == "__main__":
    socketio.run(app)
