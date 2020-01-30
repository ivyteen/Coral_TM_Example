from gpio_rgb import LED
import os
import sys

def main(arg):
    led_index = int(arg)
    if led_index < 1 or led_index > 3:
        print("Out of index")
        return
 
    ledCont=LED()    
    # 1: RED
    # 2: GREEN
    # 3: BLUE
    if led_index == 1:
        ledCont.setLedOn(LED.RED)
    elif led_index == 2:
        ledCont.setLedOn(LED.GREEN)
    elif led_index == 3:
        ledCont.setLedOn(LED.BLUE)
    else:
        pass
        

if __name__ == '__main__':
    main(sys.argv[1])
