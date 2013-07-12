#!/usr/bin/python

import time
import datetime
import sys
from random import randrange
sys.path.insert(0, '../')
from Adafruit_8x8 import ColorEightByEight

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = ColorEightByEight(address=0x70)

print "Press CTRL+C to exit"

iter = 0
#Define Color Indexs for Pixels
Pixel_Array = ["Blank","Green","Red","Yellow"]
Passed_Pixel = 0
Blank_Pixel = 0
Green_Pixel = 1
Red_Pixel = 2
Yellow_Pixel = 3

#Define constant periodic intervals
Pixel_Display_Interval = .000001
Page_Display_Interval = 3.0

# Continually update the 8x8 display one pixel at a time
while(True):
  iter += 1

  time.sleep(Page_Display_Interval)

  #This sets the pixel between 0-4 values based on the interator
  #Passed_Pixel = iter % 4
  #print "Displaying %s colored pixels." %Pixel_Array[Passed_Pixel]

  x = randrange(0,8)
  y = randrange(0,8) 
  Passed_Pixel = randrange(0,4)    
  #The function where we update the pixels
  grid.setPixel(x, y, Passed_Pixel )

  #Wait for the duration and then the loop continues
  time.sleep(Pixel_Display_Interval)
