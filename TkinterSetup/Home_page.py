from tkinter import *
import numpy as np
import cv2
import yaml
from PIL import ImageTk, Image
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import close
import warnings
warnings.filterwarnings("ignore")

#Global Varible declaration starts
image_file_path = 'images/parking_lot_1.png'
data_file_path  = 'data/coordinates_1.yml'
video_file_path = 'videos/parking_lot_1.mp4'
index = 1
#Global Varible declaration ends

def btn_clicked(a):
    global index,cap,lmain
    
    print("Button {} Clicked".format(a))
    if a=='Close':
        close.current_running_process(cap,lmain)
    elif a=='Configure':
        if image_file_path is not None:
            with open(data_file_path, "w+") as points:
                generator = CoordinatesGenerator(image_file_path, points, COLOR_RED)
                generator.generate()
        else:
            print('Image path is incorrect:)')
    elif a=='Parking':
        try:
            with open(data_file_path, "r") as data:
                cap = cv2.VideoCapture(video_file_path)
                points = yaml.load(data)
                print(points)
                detector = MotionDetector(points, 1,lmain,cap)
                detector.detect_motion()
        except:
            pass
        
    else:
        cap = cv2.VideoCapture(0)
        video_stream(1)


window = Tk()
#window.state("zoomed")
window.geometry("1217x725")
window.configure(bg = "#ffffff")

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 856,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge",
    )
canvas.place(x = 0, y = 0)

canvas.create_rectangle(0, 0, 380, 856, fill='#00203F')
img0 = PhotoImage(file = f"Button/home_page/ParkingLot.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_clicked('Parking'),
    relief = "flat")

b0.place(
    x = 87, y = 62,
    width = 200,
    height = 238)

 

img11 = PhotoImage(file = f"Button/home_page/Entry.png")
b11 = Button(
    image = img11,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_clicked('License'),
    relief = "flat")


b11.place(
    x = 87, y = 405,
    width = 200,
    height = 238)

img12 = PhotoImage(file = f"Button/home_page/close.png")
b12 = Button(
    image = img12,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_clicked('Close'),
    relief = "flat")


b12.place(
    x = 759, y = 623,
    width = 77,
    height = 76)

img13 = PhotoImage(file = f"Button/home_page/Configure.png")
b13 = Button(
    image = img13,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_clicked('Configure'),
    relief = "flat")


b13.place(
    x = 434, y = 642,
    width = 217,
    height = 38)


lmain = Label(canvas)
lmain.grid()
lmain.place(x = 434, y = 40, width=728,height=568)
image = np.zeros((590, 750, 3), np.uint8)
image[:] =(200,200,200)
cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
img = Image.fromarray(cv2image)
imgtk = ImageTk.PhotoImage(image=img)
lmain.imgtk = imgtk
lmain.configure(image=imgtk)

# Capture from camera
cap = cv2.VideoCapture(0)
# function for video streaming
def video_stream(index):
    try:
        if index == 1:
            _, frame = cap.read()
            frame = cv2.resize(frame, (728, 568))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, lambda:video_stream(1))
        else:
            cap.release()
            cv2.destroyAllWindows()
            image = np.zeros((568, 728, 3), np.uint8)
            image[:] =(255,255,255)
            cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)

    except :
            pass
window.resizable(False, False)
window.mainloop()