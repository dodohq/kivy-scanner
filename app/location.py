import gpsd
 
# Listen on port 2947 (gpsd) of localhost
session = gpsd.connect(host="localhost", port=2947)

while True:
  try:  
    packet = gpsd.get_current()
    print(packet)
    print(packet.position())
      
  except KeyError: 
    pass
  except KeyboardInterrupt:
    quit()
  except StopIteration: 
    session = None
    print("GPSD has terminated")
    
