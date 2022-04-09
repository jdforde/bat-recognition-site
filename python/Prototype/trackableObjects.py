class trackableObjects():
    def __init__(self,centroidLocation):
        self.startingLocation = centroidLocation
        self.currentLocation = centroidLocation
        self.endingLocation = (0,0)

    #update the locations
    def updateCurrentLocation(self, currentLocation):
        self.currentLocation = currentLocation

    def updateEndLocation(self):
        self.endingLocation = self.currentLocation
    
    #Return the various locations for use in centroidTracking.py
    def getStartLocation(self):
        return self.startingLocation
    
    def getEndLocation(self):
        return self.endingLocation
    
    def getCurrentLocation(self):
        return self.currentLocation
    
    def enterOrExit(self):
        #If the object starts on the outside of the rect and goes inside (enter condition)
        if self.startingLocation[0]>485 or self.startingLocation[0]<220 or self.startingLocation[1]>425 or self.startingLocation[1]<125:
            if self.endingLocation[0]<485 and self.endingLocation[0]>220 and self.endingLocation[1]<425 and self.endingLocation[1]>125:
                return 1
        
        #if the object is on the inside of the rect and leaves (exit condition)
        elif self.startingLocation[0]<485 and self.startingLocation[0]>220 and self.startingLocation[1]<425 and self.startingLocation[1]>125:
            if self.endingLocation[0]>485 or self.endingLocation[0]<220 or self.endingLocation[1]>425 or self.endingLocation[1]<125:
                return -1
        
        return 0