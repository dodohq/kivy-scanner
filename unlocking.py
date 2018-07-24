import gpio
import time


locker_to_gpio = {'L1': 430, 'L2': 389, 'L3': 398, 'L4': 393, 'L5': 394, 'L6': 297,  
                'L7': 396, 'L8': 397, 'L9': 255, 'L10': 392, 'L11': 481, 'L12': 254} 

pins = [430, 389, 398, 393, 394, 297, 396, 397, 255,392, 481, 254]
def unlock(locker):
  print('unlocked '+str(locker))
  # pin = locker_to_gpio[locker]
  pin = str(locker)
  gpio.setup(pin, gpio.OUT)
  gpio.output(pin, 1)
  time.sleep(1)
  gpio.output(pin, 0)
  time.sleep(1)
  gpio.cleanup(pin) 
  return 0
  
  

class GPIO():
  def __init__():
    pass
    
if __name__ == "__main__": 
  while 1:
    pin = input("Which pin? ")
    print(pin)
    unlock(pin)

  for pin in pins:
    print(pins.index(pin))
    unlock(pin)
