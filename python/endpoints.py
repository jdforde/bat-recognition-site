from flask import Flask, request
import os, cv2, smtplib, ssl
from flask_cors.decorator import cross_origin
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from imutils.video import FileVideoStream
import set_vars
from centroidtracking import Centroidtracking

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



app = Flask(__name__)
CORS(app)
class BatRecognizer:
    def __init__(self, video):
        #Constants
        self.thr1 = 12
        self.thr2 = 13
        self.frames = 60
        self.disappeartime = 10
        self.skip = 2
        
        self.ct = Centroidtracking(int(self.disappeartime))

        #Used for filtering non-bats
        self.model = tf.keras.models.load_model('python\size_1K_epochs_200')
        self.class_names = ['Bat', 'Not Bat']

        self.number_frames=0
        self.skip_amount=int(self.skip)
        self.video_name = video[video.rfind('\\')+1:]

        self.file_index = 1
        initialisationPeriod = int(self.frames)# decrease when noisy, increase when clear
        self.loadVideoStream(video)
        self.dim = None
        self.kernel = np.ones((3,3), np.uint8)
        self.tupe = self.run(initialisationPeriod)

    def stop(self):
        self.stream.stop()
        cv2.destroyAllWindows()

    def loadVideoStream(self, video):
        self.stream = FileVideoStream(video).start()

    def loadVideoFrame(self,initialization_period=False):
        #We do not skip frames for the initialization period
        if not initialization_period:
            for _ in range(self.skip_amount):
                frame = self.stream.read()
                self.number_frames+=1
                if frame is None:
                    return None, None, None
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
            frame, iCOR, frame_copy = self.loadVideoFrame()
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

    #Task for tomorrow: streamline this process (choose good size, make files go somewhere else, etc.) and UNDERSTAND EVERYTHING
    def display_mask(self):
        k = cv2.waitKey(1)
        if k == ord('q'):
            self.stop()

    def run(self, initialisationPeriod):
        t1 = float(self.thr1)
        t2 = float(self.thr2)

        assert t1 < t2

        alpha = 0.99
        beta = 0.99
        self.initialiseFilters(initialisationPeriod)

        while self.stream.more():

            self.iVAR = np.sqrt(self.iVARsq)
            THRESHOLD_ONE, THRESHOLD_TWO = self.updateThresholds(t1, t2, self.iVAR)

            frame, iCOR, copy_frame = self.loadVideoFrame()

            #Fixes crash instead of graceful Termination
            if frame is None:
                return (curCount,self.ct.getEnterExitList())


            update, freeze = self.generateMasks(iCOR, self.iBG, THRESHOLD_ONE)
            self.predict_iBG(alpha, iCOR, self.iBG, update, freeze)
            self.predict_iVAR(beta, self.iVARsq, self.iBG, iCOR, update, freeze)

            output = self.generateOutputMask(THRESHOLD_TWO, self.iBG, iCOR)
            removed_singles = cv2.erode(output, self.kernel, iterations=1)
            filled_mask = cv2.dilate(removed_singles, self.kernel, iterations=2)
            output = cv2.blur(filled_mask, (9,9))
            
            #Start of creating boundboxes around any movement from output
            #window of only 0's and ones
            clipped_output = np.clip(output,0,255)


            #Find the contours of the image
            contours,hierarchy = cv2.findContours(clipped_output.astype(np.uint8),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #create the box drawings array to hold the values
            boxdrawings = np.zeros((output.shape[0],output.shape[1],3),dtype=np.uint8)
            color = (255,255,255)
            allboxes = []
            
            #For each frame, keep a temp screenshot
            

            #Get all the contours and append them to a list
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                #draw the contour box in the boxdrawings array
                cv2.rectangle(boxdrawings, (x,y), (x+w,y+h), color, 2)
                
                #for each rect, determine likelyhood of bat from the output of the screenshot.
                #Only append bats to the allboxes to check
                
                resized_image=cv2.resize(copy_frame[int(y/1.3):int((y+h+15)/1.3),int(x/1.3):int((x+w+15)/1.3)], dsize=(180, 180), interpolation= cv2.INTER_CUBIC)
                img_array = tf.expand_dims(resized_image,0)

                predictions=self.model.predict(img_array)

                #img_array_res = keras.preprocessing.image.array_to_img(img_array)
                #img_array_res = keras.preprocessing.image.img_to_array(img_array_res)
                
                #predictions = self.model(img_array_res)
                score = tf.nn.softmax(predictions[0])
                if self.class_names[np.argmax(score)]=="Bat":
                    allboxes.append(cv2.boundingRect(contour))
                    #Draw the actual bats as different color
                    cv2.rectangle(boxdrawings, (x,y), (x+w,y+h), (255,0,0), 2)

                
                
            
            #Return the object list from the update function
            objectcentroids = self.ct.update(allboxes,self.number_frames)

            #For every object, print the location, the centroid, and it's id
            for (objectID,trackedObject) in objectcentroids.items():
                text = "ID {}".format(objectID)
                centroid=trackedObject.getCurrentLocation()
                cv2.putText(boxdrawings, text, (centroid[0], centroid[1]+10),cv2.FONT_HERSHEY_SIMPLEX, color=color,fontScale=1)
                cv2.circle(boxdrawings, (centroid[0],centroid[1]), radius=0, color=color, thickness=5)
            
            #Get the count of entered and exited objects
            curCount=self.ct.getInNOut()
            enteredText="Entered: {}".format(curCount[0])
            exitedText="Exited: {}".format(curCount[1])
            cv2.putText(boxdrawings, enteredText, (0,50),cv2.FONT_HERSHEY_SIMPLEX, color=color,fontScale=1)
            cv2.putText(boxdrawings, exitedText, (0,100),cv2.FONT_HERSHEY_SIMPLEX, color=color,fontScale=1)
            #Highlight gate, coords are bot-left, top-right
            cv2.rectangle(boxdrawings, (220,425), (485,125), color, 4)
            
            self.display_mask()


@app.route("/count")
def compute_stats():
    set_vars

    #Handling of incorrect request
    if ('name' not in request.args.keys() or 
        'date' not in request.args.keys()):
        return 'Bad Request', 400

    #Handling of video not existing
    if (not os.path.exists(os.path.join('videos', request.args['name']))):
        return 'Unable to locate video', 404
        
    try:
        if ('email' in request.args.keys()):
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Emergence Count Results for " + request.args['date']
            msg['From'] = os.environ.get('EMAIL')
            msg['To'] = request.args['email']

        try:
            answer = BatRecognizer(os.path.join('videos', request.args['name']))
            entered = str(answer.tupe[0][0])
            exited = str(answer.tupe[0][1])
            text="Here are your results from the video: " + entered + " bats entered and " + exited + " bats exited."
        except Exception as e:
            print(e)
            text="There was an error trying to process your video"
        
        if ('email' in request.args.keys()):
            msg.attach(MIMEText(text, 'plain'))
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
                server.sendmail(os.environ.get('EMAIL'), request.args['email'], msg.as_string())
        
        os.remove(os.path.join('videos', request.args['name']))

        
        return 'Email was sent!', 200
        
    except Exception as e:
        os.remove(os.path.join('videos', request.args['name']))
        return 'Error has occured!', 400

@app.route("/upload", methods=['POST'])
@cross_origin()
def upload_file():
    file = request.files['file']
    path = os.path.join('videos', file.filename)
    print(path)
    file.save(path)

    return 'Success', 200



if __name__ == '__main__':
    app.secret_key= os.urandom(24)
    app.run(debug=True, use_reloader=False)
    