import gpio
import time


locker_to_gpio = {'L1': 466, 'L2': 397, 'L3': 255, 'L4': 398, 'L5': 389, 'L6': 395,  
                'L7': 393, 'L8': 394, 'L9': 297, 'L10': 254, 'L11': 481, 'L12': 392} 

def unlock(locker):
  print('unlocked '+locker)
  # pin = locker_to_gpio[locker]
  pin = locker
  gpio.setup(pin, gpio.OUT)
  gpio.output(pin, 1)
  time.sleep(3)
  gpio.output(pin, 0)
  time.sleep(3)
  gpio.cleanup(pin) 
  return 0
  
  

class GPIO():
  def __init__():
    pass
    
if __name__ == "__main__": 
  while True:
    pin = input("Which pin? ")
    print(pin)
    unlock(pin)
