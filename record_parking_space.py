import cv2
import pickle
import tkinter as tk


class mark_park():
    def __init__(self,park="new_park_plot"):
        self.park=park
        self.width, self.height = 107, 48
        try:
            with open(park, 'rb') as f:
                self.pos_list = pickle.load(f)
        except:
            self.pos_list = []


    def mouseClick(self,events, x, y, flags, params,):
        if events == cv2.EVENT_LBUTTONDOWN:
            self.pos_list.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(self.pos_list):
                x1, y1 = pos
                if x1 < x < x1 + self.width and y1 < y < y1 + self.height:
                    self.pos_list.pop(i)

        with open(self.park, 'wb') as f:
            pickle.dump(self.pos_list, f)

    def mark_the_park(self,image):
        while True:
            img = cv2.imread(image)
            for pos in self.pos_list:
                cv2.rectangle(img, pos, (pos[0] + self.width, pos[1] + self.height), (255, 0, 255), 2)

            cv2.imshow("Image", img)
            cv2.setMouseCallback("Image", self.mouseClick)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    park=mark_park()
    park.mark_the_park("park_img.png")


