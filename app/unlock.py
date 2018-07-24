import gpio
import time


locker_to_gpio = {'L1': 430, 'L2': 389, 'L3': 398, 'L4': 393, 'L5': 394, 'L6': 297,  
                'L7': 396, 'L8': 397, 'L9': 255, 'L10': 392, 'L11': 481, 'L12': 254} 

def unlock(locker):
  pin = str(locker_to_gpio[locker])
  gpio.setup(pin, gpio.OUT)
  gpio.output(pin, 1)
  time.sleep(5)
  gpio.output(pin, 0)
 # gpio.cleanup(pin)
  return 0
  
  

