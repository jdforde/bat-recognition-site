from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist
from trackableObjects import trackableObjects


class Centroidtracking():
    #Constructor for the centroids tracker
    def __init__(self, framesBeforeDisappeared=50):
        #variables for storing the current id index, the list of all the objects, and the count of frames
        #that a centroid has to see if it should be removed
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        
        #running count of the entered and exited bats
        self.entered=0
        self.exited=0

        self.enterexitList=[]
        #total frames that will be counted before a tackable object is dropped default is 50 frames
        self.framesBeforeDisappeared = framesBeforeDisappeared

    #Put new objects into the objects dictionary
    def register(self, centroidinfo):
        #put trackable object in our list and initialize the other values
        self.objects[self.nextObjectID] = trackableObjects(centroidinfo)
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID,timestamp):
        self.objects[objectID].updateEndLocation()
        if self.objects[objectID].enterOrExit()==1:
            self.entered+=1
            self.enterexitList.append(("Entered",timestamp))
        elif self.objects[objectID].enterOrExit()==-1:
            self.exited+=1
            self.enterexitList.append(("Exited",timestamp))
            
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects,timestamp):
        #if all objects are gone, update all disappeared counters
        if len(rects)==0:
            
            #iterate over all of the objects that we have at the moment and increment their disappeared counter
            #if they go over the frame count, delete them
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.framesBeforeDisappeared:
                    self.deregister(objectID,timestamp)
                
            #terminate early if this is the case and return the current list
            return self.objects
        
        
        #input centroids are going to be all of the rects found in the list of rectangles (rects)
        inputCentroids = np.zeros((len(rects),2),dtype="int")

        #boundingbox rect has startX,startY,width,height
        for (i,(startX,startY,width,height)) in enumerate(rects):
            
            cX = int(startX+width/2.0)
            cY = int(startY+height/2.0)
            inputCentroids[i] = (cX,cY)

        #if no objects initially, then add all that are seen to the list
        if len(self.objects)==0:
            for i in range(0,len(inputCentroids)):
                self.register(inputCentroids[i])
        

        #Otherwise, we have to calculate the distance to see which objects are closer.
        else:
            #get the list of the keys and values of the centroids that we currently have
            objectIDs = list(self.objects.keys())
            #Extract the objects from the current Objects List
            objectList = list(self.objects.values())
            objectCentroids=[]
            for idx,object in enumerate(objectList):
                objectCentroids.append(objectList[idx].getCurrentLocation())
            
            #compute Euclidian distance to each respective inputcentroid and return that list to D
            #D will be a list of lists that contain the euclidean distances between
            D = dist.cdist(np.array(objectCentroids),inputCentroids)

            #Get the row of the minimum value for all inputs
            rows = D.min(axis = 1).argsort()

            #col will be the row with the minimum value
            cols = D.argmin(axis=1)[rows]
            
            #Keep track of which has been used
            usedRows = set()
            usedCols = set()

            for(row,col) in zip(rows,cols):

                #If we used the tuple before, we'll skip it
                if row in usedRows or col in usedCols:
                    continue
                
                objectID = objectIDs[row]

                self.objects[objectID].updateCurrentLocation(inputCentroids[col])
                self.disappeared[objectID]=0

                usedRows.add(row)
                usedCols.add(col)

            unusedRows=set(range(0,D.shape[0])).difference(usedRows)
            unusedCols=set(range(0,D.shape[1])).difference(usedCols)

            if D.shape[0]>=D.shape[1]:
                for row2 in unusedRows:
                    objectID = objectIDs[row2]
                    self.disappeared[objectID]+=1
                    if self.disappeared[objectID]>self.framesBeforeDisappeared:
                        self.deregister(objectID,timestamp)
            else:
                for col2 in unusedCols:
                    self.register(inputCentroids[col2])
        return self.objects


    def getInNOut(self):
        return (self.entered,self.exited)

    def getEnterExitList(self):
        return self.enterexitList