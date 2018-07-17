import gpio
import time


locker_to_gpio = {'L1': 466, 'L2': 397, 'L3': 255, 'L4': 398, 'L5': 298, 'L6': 389,  
                'L7': 395, 'L8': 388, 'L9': 393, 'L10': 394, 'L11': 467, 'L12': 297} 

def unlock(locker):
  pin = locker_to_gpio[locker]
  gpio.setup(pin, gpio.OUT)
  gpio.output(pin, 1)
  time.sleep(5)
  return 0
  
  

