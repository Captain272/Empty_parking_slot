import cv2
import pickle
import cvzone
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import PIL.Image, PIL.ImageTk


parking_video=""
park_pos_file=""
posList=None
width, height = 107, 48
def checkParkingSpace(imgPro,img):
    global posList
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)


        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
def main_task():
    global parking_video
    global park_pos_file
    global posList
    cap = cv2.VideoCapture(parking_video)
    with open(park_pos_file, 'rb') as f:
        posList = pickle.load(f)
    while True:

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkParkingSpace(imgDilate,img)
        cv2.imshow("Image", img)
        cv2.imshow("ImageBlur", imgBlur)
        cv2.imshow("ImageThres", imgMedian)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break

window = Tk()
window.title('Parking space monitering')
window.geometry("700x500")

bg= Image.open("parking.jpg")

def on_resize(event):
    image = bg.resize((event.width, event.height), Image.ANTIALIAS)
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)



def browseFiles1():
    global parking_video
    filename = filedialog.askopenfilename(initialdir = "Users/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.mp4*"),
													("all files",
														"*.*")))
    label_file_explorer.configure(text="File Opened: "+filename)
    # inp = blur.get(1.0, "end-1c")    
    parking_video=filename
    print(filename)


def browseFiles2():
    global park_pos_file
    filename = filedialog.askopenfilename(initialdir = "Users/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.*"),
													("all files",
														"*.*")))
    label_file_explorer.configure(text="File Opened: "+filename)
    # inp = blur.get(1.0, "end-1c")
    park_pos_file=filename
    print(filename)
    main_task()



											


l = Label(window)
l.place(x=0, y=0, relwidth=1, relheight=1)
l.bind('<Configure>', on_resize) 



label_file_explorer = Label(window,
							text = "This is the tool built for monitering the empty parking spaces \n-------------------------------\n Steps to use the application \n-------------------------------\n 1)If you are using a new parking lot then record the co-ordinates of the parking spots (use Right click of the mouse). \n 2) After recording the co-ordinates choose the video file that is to be monitired \n 3) choose the file in which co-ordinates are being saved \n \n ESC - to close the window",
							width = 105, height = 9,
							fg = "blue")


button_explore1 = Button(window,text = "Step-1) Select the video file to moniter.", width=55, height=2, command = browseFiles1)
button_explore2 = Button(window,text = "Step-2) Select saved position file and start monitering.", width=55, height=2, command = browseFiles2)
button_exit = Button(window,
					text = "Exit", width=15, height=2, command = exit)




label_file_explorer.grid(column = 0, row = 1,pady=10)
button_explore1.grid(column = 0, row = 3,sticky="w",pady=10,padx=180)
button_explore2.grid(column = 0, row = 4,sticky="w",pady=10,padx=180)
button_exit.grid(column = 0,row = 7,sticky="w",pady=10,padx=180)

window.mainloop()






