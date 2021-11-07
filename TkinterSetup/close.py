import cv2
from PIL import ImageTk, Image
import numpy as np
def current_running_process(cap,lmain):
	cv2.destroyAllWindows()
	cap.release()
	image = np.zeros((568, 728, 3), np.uint8)
	image[:] =(200,200,200)
	cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
	img = Image.fromarray(cv2image)
	imgtk = ImageTk.PhotoImage(image=img)
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	return