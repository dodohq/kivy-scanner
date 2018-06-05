from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import imutils 
from imutils.video import WebcamVideoStream
 
def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
    print('Points : ', obj.polygon,'\n')
  return decodedObjects
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon  
    # If the points do not form a quad, find convex hull
    if len(points) == 4 : 
      print('top left: ', points[1].x, ' ', points[1].y)
      print('bottom right: ', points[3].x, ' ', points[3].y)
      cv2.rectangle(im, (points[0].x, points[0].y), (points[2].x, points[2].y), (0,255,0), 3)
    
  # Display results 
  cv2.imshow("Results", im);
  cv2.waitKey(1);
 
   
# Main 
if __name__ == '__main__':
 
  # Read image
  # im = cv2.imread('zbar-test.jpg')

  camera = WebcamVideoStream(src=1).start()
  

  while(True): 
    frame = camera.read()
	  # resize the frame and convert it to grayscale (while still
	  # retaining 3 channels)
    frame = imutils.resize(frame, width=400)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = np.dstack([frame, frame, frame])    
    decodedObjects = decode(frame)
    display(frame, decodedObjects)
	    
  cv2.destroyAllWindows()
  camera.stop()
