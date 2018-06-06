from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import imutils 
from imutils.video import WebcamVideoStream
 
class Scanner():
  def __init__(self, src=1):
    self.camera = WebcamVideoStream(src=src).start()
    self.code = ''
    
  def __decode(self, im): 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
      self.code = obj.data
    return decodedObjects
  
  # Display barcode and QR code location  
  def display(self, im, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects: 
      points = decodedObject.polygon  
      if len(points) == 4 : 
        cv2.rectangle(im, (points[0].x, points[0].y), (points[2].x, points[2].y), (0,255,0), 3)
    return im

  def decoded(self):
    if not self.code:
      return False
    else:
      return self.code
 
  def cv2_call(self):
    while(True): 
      frame = camera.read()
      # resize the frame and convert it to grayscale (while still
      # retaining 3 channels)
      frame = imutils.resize(frame, width=400)
      #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #frame = np.dstack([frame, frame, frame])    
      decodedObjects = self.__decode(frame)
      self.display(frame, decodedObjects)
      cv2.imshow("Results", im)
      cv2.waitKey(1)
	    
    cv2.destroyAllWindows()
    camera.stop()
    
  def callback(self):
    frame = self.camera.read()
    frame = imutils.resize(frame, width=400)
    decodedObjects = self.__decode(frame)
    image = self.display(frame, decodedObjects)
    return image
    
  def exit(self):
    self.camera.stop()

if __name__ == "__main__":
  s = Scanner()
  s.call()
  print(s.decoded)
