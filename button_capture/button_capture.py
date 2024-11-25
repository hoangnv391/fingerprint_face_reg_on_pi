import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

button1_GPIO_pin = 26    # position follow on Raspberry Pi Pinout Mapping
GPIO.setup(button1_GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button2_GPIO_pin = 5    # position follow on Raspberry Pi Pinout Mapping
GPIO.setup(button2_GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(1)

try:
    while True:
        button1_state = GPIO.input(button1_GPIO_pin)
        button2_state = GPIO.input(button2_GPIO_pin)
        
        if button1_state == GPIO.HIGH:
            print("Button 1 not pressed")
        else:
            print("Button 1 pressed")
        
        if button2_state == GPIO.HIGH:
            print("Button 2 not pressed")
        else:
            print("Button 2 pressed")
            
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    GPIO.cleanup()
