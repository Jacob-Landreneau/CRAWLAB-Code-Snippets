#! /usr/bin/env python

##########################################################################################
# BBB_MotorLimitSwitches.py
#
# Basic use of interrupts limit switches on the BeagleBone Black to start/stop 
# a motor using the SparkFun TB6612FNG breakout board
#    http://sfe.io/p9457
#
# Requires - Adafruit BeagleBone IO Python library
#
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/03/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import time
import sys

class motor(object):
    """ Convenience class for controlling a motor
    
    Arguments
      ControlPin1 : the x01 pin 
      ControlPin2 : the x02 pin
      PWMpin : the PWM pin
      STBYpin : the STBY (standby) pin on the board
      
    Other atributes
      isRunning : Boolean describing if motor is running or not
      speed : current speed of the motor
      direction : current direction the motor is running 
                  =None if the motor is not currently moving
                  
    """
    def __init__(self, ControlPin1, ControlPin2, PWMpin, STBYpin):
        self.ControlPin1 = ControlPin1
        self.ControlPin2 = ControlPin2
        self.PWMpin = PWMpin
        self.STBYpin = STBYpin
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0
        
        # Set up the GPIO pins as output
        GPIO.setup(self.STBYpin, GPIO.OUT)
        GPIO.setup(self.ControlPin1, GPIO.OUT)
        GPIO.setup(self.ControlPin2, GPIO.OUT)


    def start(self, speed, direction):
        """ method to start a motor 
    
        Arguments:
          speed : speed of the motor 0-100 (as percentage of max)
          direction : CW or CCW, for clockwise or counterclockwise
        """
        
        # Standby pin should go high to enable motion
        GPIO.output(self.STBYpin, GPIO.HIGH)
    
        # x01 and x02 have to be opposite to move, toggle to change direction
        if direction in ('cw','CW','clockwise'):
            GPIO.output(self.ControlPin1, GPIO.LOW)
            GPIO.output(self.ControlPin2, GPIO.HIGH)
        elif direction in ('ccw','CCW','counterclockwise'):
            GPIO.output(self.ControlPin1, GPIO.HIGH)
            GPIO.output(self.ControlPin2, GPIO.LOW)
        else:
            raise ValueError('Please enter CW or CCW for direction.')
    
        # Start the motor
        # PWM.start(channel, duty, freq=2000, polarity=0)
        if 0 <= speed <= 100:
            PWM.start(self.PWMpin, speed)
        else:
            raise ValueError("Please enter speed between 0 and 100, \
                              representing a percentage of the maximum \
                              motor speed.")

        # set the status attributes
        self.isRunning = True
        self.currentDirection = direction
        self.currentSpeed = speed

    def stop(self):
        """ redirects to a soft stop """
        self.soft_stop()


    def hard_stop(self):
        """ Method to hard stop an individual motor"""
        
        PWM.set_duty_cycle(self.PWMpin, 0.0)
        
        # set the status attributes
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0


    def soft_stop(self):
        """ Method to soft stop (coast to stop) an individual motor"""
        
        # Make both control pins low
        GPIO.output(self.ControlPin1, GPIO.LOW)
        GPIO.output(self.ControlPin2, GPIO.LOW)
        PWM.stop(self.PWMpin)
        GPIO.output(self.STBYpin, GPIO.LOW)
        
        # set the status attributes
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0.0


    def set_speed(self, newSpeed):
        """ Method to change the speed of the motor, direciton is unchanged
        
        Arugments
          newSpeed : the desired new speed 0-100 (as percentage of max)
        """
        
        PWM.set_duty_cycle(self.PWMpin, newSpeed)
        self.currentSpeed = newSpeed


if __name__ == '__main__':
    # Demonstrates the use of this class
    
    # Set up the pins - These are mutable, but *don't* change them
    A01 = 'P8_7'            # A01 pin on board, controls direction along with A02
    A02 = 'P8_8'            # A02 pin on board, controls direction along with A01
    PWMA = 'P8_13'          # PWMA pin on board, controls the speed of Motor A
    B01 = 'P8_9'            # B01 pin on board, controls direction along with B02
    B02 = 'P8_10'           # B01 pin on board, controls direction along with B01
    PWMB = 'P8_19'          # PWMB pin on board, controls the speed of Motor B
    STBY = 'P8_11'          # STBY pin on the breakout, must go low to enable motion
    E_STOP = 'P8_12'        # Pin of the E-Stop
    TOP_LIMIT = 'P8_16'     # Pin of top limit switch
    BOTTOM_LIMIT = 'P8_14'  # Pin of bottom limit switch

    
    # Create the motorA instance of the class
    motorA = motor(A01, A02, PWMA, STBY)
    motorB = motor(B01, B02, PWMB, STBY)
    
    # GPIO P8_12, P8_14, P8_16 switches
    GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(BOTTOM_LIMIT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(E_STOP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  
    # now we'll define the threaded callback function  
    # this will run in another thread when our event is detected  
    def TOPlimit_callback(channel):  
        print 'Top limit reached.'
        motorA.hard_stop()
        motorB.hard_stop() 

    # now we'll define the threaded callback function  
    # this will run in another thread when our event is detected  
    def BOTTOMlimit_callback(channel):  
        print 'Bottom limit reached.'
        motorA.hard_stop()
        motorB.hard_stop()    
        
    # now we'll define the threaded callback function  
    # this will run in another thread when our event is detected  
    def ESTOP_callback(channel):  
        motorA.hard_stop()
        motorB.hard_stop() 
        GPIO.cleanup()           # clean up GPIO
        sys.exit('E-STOP switch is in the emergency stop state. Aborting...')


    # The GPIO.add_event_detect() line below set things up so that  
    # when a rising edge is detected, regardless of whatever   
    # else is happening in the program, the function 'my_callback' will be run  
    GPIO.add_event_detect(TOP_LIMIT, GPIO.RISING, callback=TOPlimit_callback, bouncetime=200)  
    GPIO.add_event_detect(BOTTOM_LIMIT, GPIO.RISING, callback=BOTTOMlimit_callback, bouncetime=200)  
    GPIO.add_event_detect(E_STOP, GPIO.RISING, callback=ESTOP_callback, bouncetime=200)  

    try:
#         while True:
        
        if not GPIO.input(E_STOP):
            GPIO.cleanup()           # clean up GPIO on normal exit  
            sys.exit('\nE-STOP switch is in the emergency stop state. Exiting...\n')

        # Move down
        motorA.start(100, 'CW')
        motorB.start(100, 'CCW')
        time.sleep(0.5)

        while motorA.isRunning:
            # loop here until limit is reached
            print 'Moving down...'
            time.sleep(0.1)

        # Start Moving Motors Up
        motorA.start(100, 'CCW')
        motorB.start(100, 'CW')
        time.sleep(0.5)
    
        while motorA.isRunning:
            # loop here until limit is reached
            print 'Moving up...'
            time.sleep(0.1)


  
    except KeyboardInterrupt:  
        motorA.stop()
        motorB.stop()
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    
    
    GPIO.cleanup()           # clean up GPIO on normal exit  