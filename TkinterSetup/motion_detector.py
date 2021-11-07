import cv2 as open_cv
import numpy as np
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE
from datetime import datetime
from PIL import ImageTk, Image
import warnings
warnings.filterwarnings("ignore")
# firebase = firebase.FirebaseApplication("https://parkinglotdetection-default-rtdb.firebaseio.com/",None)


class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1
    def __init__(self, coordinates, start_frame, lmain,cap):
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []
        self.capture = cap
        self.coordinates_points = None
        self.count=0
        self.times = None
        self.statuses = None
        self.lmain = lmain
        self.prev = {'Slot_1':None,'Slot_2':None,'Slot_3':None,'Slot_4':None,'Slot_5':None,'Slot_6':None,'Slot_7':None,'Slot_8':None}

    def detect_motion(self):
        self.capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)
        self.coordinates_points = self.coordinates_data
        for p in self.coordinates_points:
            coordinates = self._coordinates(p)
            rect = open_cv.boundingRect(coordinates)
            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
 
            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)
    

        self.statuses = [False] * len(self.coordinates_points)
        self.times = [None] * len(self.coordinates_points)
        self.start_cam()
    def start_cam(self):
            a=[]
            result, frame = self.capture.read()
            #if frame is None:
            #    break
            if frame is None:
                print(True)
                self.capture.set(open_cv.CAP_PROP_POS_FRAMES, 1)
                result, frame = self.capture.read()
                

            try:
                blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            
                grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
                new_frame = frame.copy()
    
                position_in_seconds = self.capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0
                list_status = {}
                for index, c in enumerate(self.coordinates_points):
                    status = self.__apply(grayed, index, c)
    
                    list_status[index+1] = status
                    # print(status,' --> ',index+1)
                    if self.times[index] is not None and self.same_status(self.statuses, index, status):
                        self.times[index] = None
                        continue
    
                    if self.times[index] is not None and self.status_changed(self.statuses, index, status):
                        if position_in_seconds - self.times[index] >= MotionDetector.DETECT_DELAY:
                            self.statuses[index] = status
                            self.times[index] = None
                        continue
    
                    if self.times[index] is None and self.status_changed(self.statuses, index, status):
                        self.times[index] = position_in_seconds
                
                if self.count ==100:
                    self.count=0
                    # for i,j in list_status.items():
                    #      if self.prev['Slot_'+str(i)] != str(j):
                    #          result = firebase.put('parkinglotdetection-default-rtdb/empty_spaces/-MgZwjfetdxodVLdq4RM','Slot_'+str(i),str(j))
                    #          self.prev['Slot_'+str(i)]=str(j)
                    print('Updated')
                else:
                    self.count+=1
    
                for index, p in enumerate(self.coordinates_points):
                    coordinates = self._coordinates(p)
                    color = COLOR_GREEN if self.statuses[index] else COLOR_BLUE
                    if self.statuses[index]:
                        a.append(index)
                        a=list(dict.fromkeys(a))
                        
                    elif self.statuses[index]==False and index in a:
                        a.remove(index)
                    draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
                
                new_frame = open_cv.resize(new_frame, (728, 568))
                cv2image = open_cv.cvtColor(new_frame, open_cv.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(1, lambda:self.start_cam())
            except:
                pass
    
        
    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)


        rect = self.bounds[index]

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)


        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
