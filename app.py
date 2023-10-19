from flask import Flask, render_template, request, redirect, url_for, Response
import requests
import cv2
import numpy as np


app = Flask(__name__)

def detect_and_label_mud(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_mud = np.array([0, 30, 50])  
    upper_mud = np.array([30, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_mud, upper_mud)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "mud", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    return frame

"""def generate_webcam():
    #video from webcam

    cap = cv2.VideoCapture(0)  

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        mud_detection_result = detect_and_label_mud(frame)
        ret, buffer = cv2.imencode('.jpg', mud_detection_result)
        if not ret:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()
    """


# function to generate video frames from ESP32-CAM
def generate_module():
    while True:
        try:
            response = requests.get('http://<ESP32-CAM_IP>:<PORT>/video', stream=True)
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=1024):
                    frame = cv2.imdecode(np.frombuffer(chunk, dtype=np.uint8), cv2.IMREAD_COLOR)
                    mud_detection_result = detect_and_label_mud(frame)
                    _, buffer = cv2.imencode('.jpg', mud_detection_result)
                    if not ret:
                        continue
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                print('Error fetching video frames from ESP32-CAM')
        except Exception as e:
            print(f'Error: {e}')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_webcam(),mimetype='multipart/x-mixed-replace; boundary=frame')


def send_command(command):
    nodeMCU_ip = "NodeMCU_IP_Address"
    url = f"http://{nodeMCU_ip}/{command}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "Command sent successfully."
        else:
            return "Failed to send command."
    except Exception as e:
        return str(e)

@app.route('/control/<command>')
def control(command):
    result = send_command(command)
    return result

    
if __name__ == '__main__':
    app.run(debug=True)
