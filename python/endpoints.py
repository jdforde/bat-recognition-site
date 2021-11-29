from flask import Flask, request
import os, cv2, smtplib, ssl
import numpy as np
import tensorflow as tf
from imutils.video import FileVideoStream
import set_vars

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#
# This file represents the various endpoints that our front-end will call with documentation
#

app = Flask(__name__)


#BatRecognizer is modificatin of rs.py. thr1 = 12 thr2 = 13, frames = 40, and no screenshotting capabilities
class BatRecognizer:

    def __init__(self, video, skp=1):
        self.skip_amount = skp

        self.model = tf.keras.models.load_model('python\size_1K_epochs_200') #make sure to download this model's folder
        self.loadVideoStream(video)
        self.dim = None
        self.kernel = np.ones((3,3), np.uint8)
        self.run()

    def stop(self):
        self.stream.stop()
        cv2.destroyAllWindows()

    def loadVideoStream(self, video):
        self.stream = FileVideoStream(video).start()

    def loadVideoFrame(self, initialization_period=False):
        #We do not skip frames for the initialization period
        if not initialization_period:
            for _ in range(self.skip_amount):
                frame = self.stream.read()
                if frame is None:
                    return None, None, None
        else:
            frame = self.stream.read()

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

    def predict_iVAR(self, beta, iVARsq, iBG, iCOR, update_BG_mask, freeze_BG_mask):
        update_BG_mask = update_BG_mask*(beta*iVARsq + (1-beta)*np.square(iCOR - iBG))
        freeze_BG_mask = freeze_BG_mask*iVARsq
        self.iVARsq = update_BG_mask + freeze_BG_mask
        self.iVARsq.astype('float16')


    def generateOutputMask(self, THRESHOLD_TWO, iBG, iCOR):
        absiRES = abs(iBG - iCOR)

        MOVING_mask = np.clip(absiRES, a_min=THRESHOLD_TWO, a_max=1)
        MOVING_mask = (MOVING_mask - THRESHOLD_TWO)*255
        return MOVING_mask

    def display_mask(self, output, overlay=False):
        k = cv2.waitKey(1)
        if k == ord('q'):
            self.stop()

    def run(self):
        t1 = float(12)
        t2 = float(13)

        assert t1 < t2

        alpha = 0.99
        beta = 0.99
        self.initialiseFilters(40)


        while self.stream.more():

            self.iVAR = np.sqrt(self.iVARsq)
            THRESHOLD_ONE, THRESHOLD_TWO = self.updateThresholds(t1, t2, self.iVAR)

            frame, iCOR, copy_frame = self.loadVideoFrame()

            if frame is None:
                break
            
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
            cv2.imshow("INPUT", frame_uint8)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                if (w*h) > 1000:
                    resized_image = cv2.resize(copy_frame[int(y/1.3):int((y+h+15)/1.3), int(x/1.3):int((x+w+15)/1.3)], dsize=(180, 180), interpolation= cv2.INTER_CUBIC)
                    img_array = tf.expand_dims(resized_image, 0)
                    predictions = self.model.predict(img_array)

                    score = tf.nn.softmax(predictions[0])
                    print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(['Bat', 'Not Bat'][np.argmax(score)], 100 * np.max(score)))

            self.display_mask(output, frame)

"""
request: http://localhost:5000/youtube/?link=<link>
this wants:
video name (will assume video is placed in videos folder)
email
date of recording
response: none
error codes:
^update information above to be valid

"""
@app.route("/download/")
def compute_stats():
    set_vars

    #Handling of incorrect request
    if ('name' not in request.args.keys() or 
        'date' not in request.args.keys()):
        return 'Bad Request', 400

    #Handling of video not existing
    if (not os.path.exists(os.path.join('videos', request.args['name']))):
        return 'Unable to locate video', 404

    if ('email' in request.args.keys()):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Emergence Count Results for " + request.args['date']
        msg['From'] = os.environ.get('EMAIL')
        msg['To'] = request.args['email']

    try:
        count = BatRecognizer(os.path.join('videos', request.args['name']), 4)
        text="Here are your results from the video: "
    except:
        text="There was an error trying to process your video"
    
    if ('email' in request.args.keys()):
        msg.attach(MIMEText(text, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
            server.sendmail(os.environ.get('EMAIL'), request.args['email'], msg.as_string())

    return count, 200

app.run()