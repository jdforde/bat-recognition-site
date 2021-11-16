import cv2
import argparse
import numpy as np
from imutils.video import FileVideoStream
import sys, os, time
import tensorflow as tf
import keras as keras

class main:

    def __init__(self,args):
        self.screenshot = True if(args.screenshot) else False
        self.number_frames = 0
        self.skip_amount = int(args.skip)
        self.video_name = args.video[args.video.rfind('\\')+1:]

        self.model = tf.keras.models.load_model('python\size_1K_epochs_200') #make sure to download this model's folder

        if (self.screenshot):
            if (not os.path.isdir(args.screenshot)):
                print("ERROR: path specified is not a directory")
                sys.exit(1)

        self.file_index = 1
        initialisationPeriod = int(args.frames)# decrease when noisy, increase when clear
        self.loadVideoStream(args)
        self.dim = None
        self.kernel = np.ones((3,3), np.uint8)
        self.run(initialisationPeriod, args)

    def stop(self):
        self.stream.stop()
        cv2.destroyAllWindows()

    def loadVideoStream(self, args):
        self.stream = FileVideoStream(args.video).start()

    def loadVideoFrame(self, initialization_period=False):
        #We do not skip frames for the initialization period
        if not initialization_period:
            for _ in range(self.skip_amount):
                frame = self.stream.read()
                self.number_frames+=1
                if frame is None:
                    return None, None
        else:
            frame = self.stream.read()
            self.number_frames+=1

        if frame is not None:
            copy_frame = frame.copy()
            self.h, self.w, _ = frame.shape #NoneType has no attribute 'shape'
            if self.dim is None:
                scale_percent = 130 # percent of original size
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                self.dim = (width, height)
            frame = cv2.resize(frame, self.dim, interpolation=cv2.INTER_AREA)
            if frame is None:
                self.stop()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = frame/255
            frame.astype('float16')
            iCOR = self.correctImage(frame)
            return frame, iCOR, copy_frame
        else:
            return None, None, None

    def correctImage(self, frame):
        try:
            SAT = self.invNPix * frame
            iCOR = frame - SAT
        except:
            self.nR, self.nC, *_ = frame.shape
            self.invNPix = 1/(self.nR*self.nC)
            SAT = self.invNPix * frame
            iCOR = frame - SAT
        return iCOR

    def initialiseFilters(self, initialisationPeriod):
        for self.n in range(initialisationPeriod):
            frame, iCOR, frame_copy = self.loadVideoFrame(True)
            self.initialiseBackgroundFilter(iCOR)
            self.initialiseVarianceFilter(frame, iCOR)
        self.iBG = self.rollingAvg_iCOR
        self.iVARsq = self.rollingAvg_iVARsq

    def initialiseBackgroundFilter(self, iCOR):
        try:
            self.rollingAvg_iCOR = self.rollingAvg_iCOR + (iCOR - self.rollingAvg_iCOR)/self.n
        except:
            self.rollingAvg_iCOR = iCOR
            self.rollingAvg_iCOR.astype('float16')

    def initialiseVarianceFilter(self, frame, iCOR):
        try:
            self.rollingAvg_iVARsq = self.rollingAvg_iVARsq + (np.square(self.rollingAvg_iCOR -frame) - self.rollingAvg_iVARsq)/self.n
        except:
            self.rollingAvg_iVARsq = np.square(self.rollingAvg_iCOR-frame)
            self.rollingAvg_iVARsq.astype('float16')

    def updateThresholds(self, t1, t2, iVAR):
        T1 = t1*iVAR
        T2 = t2*iVAR
        return T1, T2

    def generateMasks(self, iCOR, iBG, THRESHOLD_ONE):
        iRES = iCOR - iBG
        absiRES = np.abs(iRES)
        temp = THRESHOLD_ONE - absiRES
        temp = np.clip(temp, a_min=0, a_max=255)
        update_BG_mask = cv2.threshold(temp, 0, 1, cv2.THRESH_BINARY_INV)[1]
        freeze_update_BG_mask = cv2.threshold(temp, 0, 1, cv2.THRESH_BINARY)[1]
        return update_BG_mask, freeze_update_BG_mask

    def predict_iBG(self, alpha, iCOR, iBG, update_BG_mask, freeze_BG_mask):
        update_BG_mask = update_BG_mask*(alpha*iBG + (1-alpha)*iCOR)
        freeze_BG_mask = freeze_BG_mask*iBG
        self.iBG = update_BG_mask + freeze_BG_mask
        self.iBG.astype('float16')
        if not self.screenshot:
            cv2.imshow("self.iBG", self.iBG)

    def predict_iVAR(self, beta, iVARsq, iBG, iCOR, update_BG_mask, freeze_BG_mask):
        update_BG_mask = update_BG_mask*(beta*iVARsq + (1-beta)*np.square(iCOR - iBG))
        freeze_BG_mask = freeze_BG_mask*iVARsq
        self.iVARsq = update_BG_mask + freeze_BG_mask
        self.iVARsq.astype('float16')

        if not self.screenshot:
            cv2.imshow("iVARsq", self.iVARsq)

    def generateOutputMask(self, THRESHOLD_TWO, iBG, iCOR):
        absiRES = abs(iBG - iCOR)
        temp = absiRES - THRESHOLD_TWO

        MOVING_mask = np.clip(absiRES, a_min=THRESHOLD_TWO, a_max=1)
        MOVING_mask = (MOVING_mask - THRESHOLD_TWO)*255
        return MOVING_mask

    def display_mask(self, output, overlay=False):
        if not self.screenshot:
            cv2.imshow("MASK", output)
        k = cv2.waitKey(1)
        if k == ord('q'):
            self.stop()

    def run(self, initialisationPeriod, args):
        t1 = float(args.thr1)
        t2 = float(args.thr2)

        assert t1 < t2

        alpha = 0.99
        beta = 0.99
        self.initialiseFilters(initialisationPeriod)

        #each frame takes about .05 seconds to process
        while self.stream.more():

            self.iVAR = np.sqrt(self.iVARsq)
            THRESHOLD_ONE, THRESHOLD_TWO = self.updateThresholds(t1, t2, self.iVAR)

            frame, iCOR, copy_frame = self.loadVideoFrame()

            #Fixes issue of program crashing at the end instead of gracefully exiting
            if frame is None:
                print(self.number_frames)
                break
            
            
            if not self.screenshot:
                cv2.imshow("INPUT", frame)

            update, freeze = self.generateMasks(iCOR, self.iBG, THRESHOLD_ONE)
            self.predict_iBG(alpha, iCOR, self.iBG, update, freeze)
            self.predict_iVAR(beta, self.iVARsq, self.iBG, iCOR, update, freeze)

            output = self.generateOutputMask(THRESHOLD_TWO, self.iBG, iCOR)
            removed_singles = cv2.erode(output, self.kernel, iterations=1)
            filled_mask = cv2.dilate(removed_singles, self.kernel, iterations=2)
            output = cv2.blur(filled_mask, (9,9))

            clipped_output = np.clip(output, 0, 255)
            contours, hierarchy = cv2.findContours(clipped_output.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            frame_uint8 = (frame*255).astype(np.uint8)

            for contour in contours:
                    (x, y, w, h) = cv2.boundingRect(contour)
                   
                    if (w*h) > 1000:
                        if self.screenshot:
                            file_location = os.path.join(args.screenshot, self.video_name + "_" + str(self.file_index) + ".png")
                            print("Writing file", file_location)
                            cv2.imwrite(file_location, frame_uint8[y+15:y+h+15, x+15:x+w+15]) #adding wiggle room of 15px to screenshot
                            self.file_index +=1


                        resized_image = cv2.resize(copy_frame[int(y/1.3):int((y+h+15)/1.3), int(x/1.3):int((x+w+15)/1.3)], dsize=(180, 180), interpolation= cv2.INTER_CUBIC)
                        img_array = tf.expand_dims(resized_image, 0)
                        input()
                        predictions = self.model.predict(img_array)

                        score = tf.nn.softmax(predictions[0])
                        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(['Bat', 'Not Bat'][np.argmax(score)], 100 * np.max(score)))
            if self.screenshot:
                cv2.imshow("INPUT", frame_uint8)

            self.display_mask(output, frame)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('video', help='path to IR video')
    argparser.add_argument('thr1', help='Estimation threshold')
    argparser.add_argument('thr2', help='Output sensitivity')
    argparser.add_argument('frames', help='Number of frames used to train the background')
    #-sc is used to generate screenshots for model creation and training
    argparser.add_argument('-sc', '--screenshot', help='Optional, takes screenshots of moving objects, specify absolute directory', default="")
    argparser.add_argument('-skp', '--skip', help='Number of frames desired to skip. For example, -skp 4 means for every frame we analyze, skip the following 3.', default=1)


    args = argparser.parse_args()
    start_time = time.time()
    main(args)
    print("Total processing time:", str(time.time() - start_time))