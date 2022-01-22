from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist


class Centroidtracking():
    #Constructor for the centroids tracker
    def __init__(self, framesBeforeDisappeared=50):
        #variables for storing the current id index, the list of all the objects, and the count of frames
        #that a centroid has to see if it should be removed
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        #total frames that will be counted before a centroid is dropped
        self.framesBeforeDisappeared = framesBeforeDisappeared

    #Put new objects into the objects dictionary
    def register(self, centroid):
        #put centroid in our list and initialize the other values
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        #if all objects are gone, update all disappeared counters
        if len(rects)==0:
            
            #iterate over all of the objects that we have at the moment and increment their disappeared counter
            #if they go over the frame count, delete them
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.framesBeforeDisappeared:
                    self.deregister(objectID)
                
            #terminate early if this is the case and return what we currently have
            return self.objects
        
        
        #input centroids are going to be all of the rects found in the list of rectangles (rects)
        inputCentroids = np.zeros((len(rects),2),dtype="int")

        #boundingbox rect has startX,startY,width,height
        for (i,(startX,startY,width,height)) in enumerate(rects):
            
            cX = int(startX+width/2.0)
            cY = int(startY+height/2.0)
            inputCentroids[i] = (cX,cY)

        #if no objects initially, then add all that are seen
        if len(self.objects)==0:
            for i in range(0,len(inputCentroids)):
                self.register(inputCentroids[i])
        
        else:
            #get the list of the keys and values of the centroids that we currently have
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            #compute distance to each respective objectCentroid
            D = dist.cdist(np.array(objectCentroids),inputCentroids)

            #rows will be 
            rows = D.min(axis = 1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            usedRows = set()
            usedCols = set()

            for(row,col) in zip(rows,cols):
                if row in usedRows or col in usedCols:
                    continue
                
                objectID = objectIDs[row]

                self.objects[objectID] = inputCentroids[col]
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
                            self.deregister(objectID)
                else:
                    for col in unusedCols:
                        self.register(inputCentroids[col])
        return self.objects