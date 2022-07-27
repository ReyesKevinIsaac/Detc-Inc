from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/error')
def error():
    return '<div> <h1> Error, no se puede encontrar la página </h1></div>'

@app.route('/detectando')
def detector():
    from pygame import mixer
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt

    live_Camera = cv2.VideoCapture(0) # variable iniciando captura del video
    lower_bound = np.array([11,33,111])
    upper_bound = np.array([90,255,255])

    while(live_Camera.isOpened()): #leer el material de archivo en un ciclo while infinito
        ret, frame = live_Camera.read()
        frame = cv2.resize(frame,(1280,720))
        frame = cv2.flip(frame,1)
        frame_smooth = cv2.GaussianBlur(frame,(7,7),0)

        mask = np.zeros_like(frame)
        mask[0:720, 0:1280] = [255,255,255] #Ahora asigne la máscara con color blanco en formato BGR.
        img_roi = cv2.bitwise_and(frame_smooth, mask) #img1 = frame_smooth da una imagen del cuadro actual #es una matriz de valores de color black, su valor es 0 en OpenCV.
        frame_hsv = cv2.cvtColor(img_roi,cv2.COLOR_BGR2HSV) #Primero convertimos el ROI al formato HSV.

        image_binary = cv2.inRange(frame_hsv, lower_bound, upper_bound) #Ahora el paso final es detectar las llamas. Mantener la imagen de origen como video en vivo y los límites como lower_bound y upper_bound definidos anteriormente.

        check_if_fire_detected = cv2.countNonZero(image_binary)
        if int(check_if_fire_detected) >= 20000 :
            cv2.putText(frame,"Fuego detectado !",(300,60),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2)
            mixer.init()
            alarma=mixer.Sound("alarma.wav")
            mixer.Sound.play(alarma)
            

        cv2.imshow("Fire Detection",frame)
        
        if cv2.waitKey(10) == 27 :  ##Detener el video
            break

    live_Camera.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    app.run(debug=True)
