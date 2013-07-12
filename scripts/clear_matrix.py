#!/usr/bin/python
import sys
sys.path.insert(0, 'classes/')
from class_LED_Matrix import LED_Matrix

#Code under here
Matrix = LED_Matrix()

print "Clearing Matrix"
Matrix.set_All_Pixels("Blank")