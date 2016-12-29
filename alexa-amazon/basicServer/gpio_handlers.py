"""
/*
 * Custom handlers for the BBB
 *
 */
"""
import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P9_12", GPIO.OUT)

def alexaHandler(client, userdata, message):
    print "Received payload: " + str(message.payload.decode())
    # Assume only 1 and 0 are send here.
    if message.payload == "1":
        GPIO.output("P9_12", GPIO.HIGH)
        print "Turned christmas tree On"
    elif message.payload == "0":
        GPIO.output("P9_12", GPIO.LOW)
        print "Turned christmas tree Off"

def cleanUp():
    GPIO.cleanup()
