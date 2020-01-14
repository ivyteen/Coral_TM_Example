from gpio_led import LED
import os
import sys

def main(arg):
    led_index = int(arg)
    if led_index < 1 or led_index > 4:
        print("Out of index")
        return
    
    ledCont=LED()    
    # 1: RED
    # 2: GREEN
    # 3: BLUE
    # 4: YELLOW

    ledCont.setOnlyLED(led_index)



if __name__ == '__main__':
    main(sys.argv[1])
