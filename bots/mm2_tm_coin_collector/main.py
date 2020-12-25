from utils import robloxControl as rc
from games.mm2 import mm2_coinDetector
import matplotlib.pyplot as plt
from games.mm2.mm2_policy import *
import cv2
from datetime import datetime
import os
import time
plot = True
save = False
if __name__ == '__main__':
    plt.ion()


    h = rc.getHandleByTitle('Roblox')
    plt.figure(1)
    hfig1 = rc.getHandleByTitle('Figure 1')

    # save file info
    foldername = r'C:\Users\ctawo\PycharmProjects\autoclicker\mm2\\' + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    os.mkdir(foldername)
    filename =  foldername + r'\img_%04d.png'
    debugIm = foldername + r'\dbg_img_%04d.png'
    i = 0

    # coin templates
    tt = r'C:\Users\ctawo\PycharmProjects\autoclicker\mm2\dcoin%d.png'
    templates = [tt % i for i in [1,3,5]]
    coinDetector = mm2_coinDetector.CoinDetector_tm(templates)
    img = rc.captureWindow(h, convert='GBR', save=filename % i)
    while True:
        starttime = time.time()
        if save:
            img = rc.captureWindow(h, convert='GBR', save = filename%i)
        else:
            img = rc.captureWindow(h, convert='GBR', save=None)
        durationCapture = time.time()-starttime
        x,y = coinDetector.findCoins(img)
        durationDetect = time.time()-starttime-durationCapture
        xc, yc = [0.5, 0.75]
        xn = np.array(x)/img.shape[1]
        yn = np.array(y)/img.shape[0]
        dx, dy, direction = policy_async(xn, yn, xc, yc)

        durationPolicy = time.time()-starttime - durationCapture - durationDetect
        duration = time.time() - starttime
        if plot:
            plt.clf()
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.plot(int(x*img.shape[1]), int(y*img.shape[0]), 'x', 'white')
            if x.size >0 and y.size>0:
                plt.plot(np.median(x), np.median(y), 'o', 'white')
            plt.plot(xc*img.shape[1], yc*img.shape[0], 'x', 'red')
            plt.title('%d, %1.2f, %1.2f, %s duration:cap %1.2f, dect %1.2f, pol %1.2f, wtot %1.2f'%(len(x), dx, dy, direction,
                                                                          durationCapture, durationDetect, durationPolicy, duration) )
            rc.moveWindow(hfig1, 1000, 0, 800, 800)  # next to roblox screen
            plt.pause(0.0001)
            if save:
                plt.savefig(debugIm % i)
                i += 1
        else:
            print('%d, %1.2f, %1.2f, %s duration:%1.2f'%(len(x), dx, dy, direction, duration))




