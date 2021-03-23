# стрельба по мишеням в will to live11
from mss import mss
import pydirectinput
import time
import numpy as np
import cv2 as cv
import os
import pynput
import random

# Обрабатываем файлы (проверяем как работает наш тимплейт)
def sc(file):
    img_rgb = cv.imread("c:/project/screen/"+file)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('c:/project/template.jpg', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        x = int(pt[0])
        y = int(pt[1])
#        cv.imshow("win",img_rgb)
#        cv.imwrite("c:/res.jpg", img_rgb)
        print(x, y)

def mss_test(template):
#    mon_width=1920
#    mon_height=1080
    mon_width=1080
    mon_height=1920

    with mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            img = np.array(sct.grab(monitor))
            #img = sct.grab(monitor)
            #img = cv.imread('c:/project/screen/001.jpg', 0)
            img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            w_img = img.shape[1] # ширина
            h_img = img.shape[0] # длинна картинки
            w_template = template.shape[1] # длинна
            h_template = template.shape[0] # ширина темплейта
            print("W_H image:"+str(w_img),str(h_img))
            print("W_H teplate:"+str(w_template),str(h_template))
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            threshold = 0.61  # 0.55 для mishen, 0.65 для человека
            print('Best position and val %s' % str(max_val), str(max_loc[1]),str(max_loc[0]))
            w=max_loc[0] #+(w_template/2)
            h=max_loc[1] #+(h_template/2)

            if max_val >= threshold:
                print("found")

                w_move = (int(w) - int((w_img)/2));
                h_move = int(h - ((h_img - 20) / 2))  # -15 для того чтобы прицелился ниже, в центр мишени
                if w_move>0:
                    w_move=w_move*1.27 # для медленных пушек w_move=w_move*1.28
                elif w_move>0 and w_move<200:
                    w_move=(w_move*1.27)+40 #
                elif w_move<0:
                    w_move=w_move*1.17 # для снайперок w_move=w_move*1.17
                elif w_move<0 and w_move<200:
                    w_move=(w_move*1.17)+40 # для снайперок w_move=w_move*1.17

                print("move na:" + str(w_move), str(h_move))
                pydirectinput.move(int(w_move/2),int(h_move/2))
                time.sleep(0.07) # +random.uniform(0.01,0.05)
                pydirectinput.click()  # Стреляем
                shooting=int(random.randrange(1,50,1))
                if shooting>47:
                    time.sleep(0.20)  # +random.uniform(0.01,0.05)
                      #  pydirectinput.click()
                else:
                    print("no randome here")
                time.sleep(1.2) #+random.uniform(0.01,0.05)
                # После выстрела двигаем прицел вниз
                pydirectinput.move(0+random.randrange(-40,40,10),30+random.randrange(-10,20,10))
                time.sleep(0.02)
            # Если не нашли мишень, то
            else:
                print("not found")
                pydirectinput.move(0 + random.randrange(-160,160, 40), 15 + random.randrange(-5, 30, 1)) # сдвинуть чуток
                time.sleep(0.01)
            # Сделано сдвинуть на центр мишени

            #

#            if cv.waitKey(25) & 0xFF == ord("q"):
#                cv.destroyAllWindows()


def main():
    dir="c:/project/screen/"
    template = cv.imread('c:/project/template.jpg', 0)
#   template = cv.imread('c:/project/template.jpg', cv.IMREAD_UNCHANGED)
    time.sleep(1)
    reloadCount=0 # счётчик
    reloadTime=6
    while "a":
            reloadCount=reloadCount+1
            time.sleep(0.01)
            if reloadCount>6:
                pydirectinput.press('r')
                time.sleep(reloadTime)
                reloadCount = 0
                pydirectinput.rightClick()  # переходим в режим прицеливания
                time.sleep(1)
            mss_test(template)
        # mss_test()

# обрабатываем файлы проверяя наш тимплейт
#    for file in os.listdir(dir):
#        print(file)
#       file="001.jpg"
#        sc(file)



# запуск главного цикла
if __name__ == '__main__':
    main()

