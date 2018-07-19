import gpio
import time


locker_to_gpio = {'L1': 466, 'L2': 397, 'L3': 255, 'L4': 398, 'L5': 481, 'L6': 389,  
                'L7': 395, 'L8': 392, 'L9': 393, 'L10': 394, 'L11': 254, 'L12': 297} 

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
