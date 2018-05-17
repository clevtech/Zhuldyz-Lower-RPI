from gpiozero import LED
import time

motor1 = LED(23)
motor2 = LED(24)

motor1.on()
motor2.on()

time.sleep(2)

motor1.off()
motor2.on()

time.sleep(2)

motor1.off()
motor2.off()
