#!/usr/bin/python
import time
import sys
import math
from random import randrange
sys.path.insert(0, '../')
from class_LED_Matrix import LED_Matrix

#Variables
REFRESH_RATE = 1.0
SUB_REFRESH_RATE = 0.1

#Code under here
Matrix = LED_Matrix()

print "Displaying Red Pixels"
Matrix.set_All_Pixels("Red")
time.sleep(REFRESH_RATE)

#print "Red Grid Buffer Row Value 1 = " + str(Matrix.get_Buffer_Value(1))
#time.sleep(2.0)

print "Displaying Green Pixels"
Matrix.set_All_Pixels("Green")
time.sleep(REFRESH_RATE)

#print "Green Grid Buffer Row Value 1 = " + str(Matrix.get_Buffer_Value(1))
#time.sleep(2.0)

print "Displaying Yellow Pixels"
Matrix.set_All_Pixels("Yellow")
time.sleep(REFRESH_RATE)

#print "Yellow Grid Buffer Row Value 1 = " + str(Matrix.get_Buffer_Value(1))
#time.sleep(2.0)

print "Clearing display."
Matrix.set_Clear_Grid()
time.sleep(REFRESH_RATE)

print "Displaying Rows."
#This displays an entire row based on the input row Number 0-7
for i in range(0, 8):
    Matrix.draw_Row_Line(i, "Rainbow")
    #print "Row Buffer Row Value " + str(i) + " = " + str(Matrix.get_Buffer_Value(i))
    time.sleep(SUB_REFRESH_RATE)
    Matrix.set_Clear_Grid()

print "Displaying Columns."
#This displays an entire column based on the input row Number 0-7
for i in range(0, 8):
    Matrix.draw_Column_Line(i, "Rainbow")
    time.sleep(SUB_REFRESH_RATE)
    Matrix.set_Clear_Grid()

print "Displaying Random Pixels"
i = 0
ilimit = 500
while(i < ilimit):
    i += 1
    print "Displaying [%d / %d]" % (i, ilimit)
    Matrix.set_Random_Pixel(Matrix.get_Random_ColorString())

Matrix.set_Clear_Grid()

#This snippit displays a 4x4 square along the center of the grid, doesn't touch edges
Matrix.draw_Row_Line(0, "Red")
Matrix.draw_Row_Line(7, "Red")
Matrix.draw_Column_Line(0, "Red")
Matrix.draw_Column_Line(7, "Red")

for x in range(2, 7):
    for y in range(2, 7):
        print "Bottom Left %d,%d" % (x, y)

        Matrix.draw_4px_Square(x, y, "Green")
        time.sleep(SUB_REFRESH_RATE)
        Matrix.draw_4px_Square(x, y, "Blank")

time.sleep(REFRESH_RATE)

#This snippey runs through the entire brightness scale
Matrix.set_All_Pixels("Red")
i = 0
x = 0
y = 0
#Here we fill up 2 rows of pixels 0-15, displaying yellow everytime we increase the brightness.
while(i <= 15):
    if y >= 8:
        y = 0
    x = int(math.floor(i / 8))
    Matrix.set_Matrix_Brightness(i)
    Matrix.set_Pixel(x, y, "Yellow")
    print "Setting Brightness To %d" %i
    i = i + 1
    y = y + 1
    time.sleep(0.1)

time.sleep(REFRESH_RATE)
print "Finished all sub routines...Preparing for Simulation..."
Matrix.set_Clear_Grid()
time.sleep(REFRESH_RATE)

print "Starting Simulation..."

#FUNCTION DEFINITION
def move_Unit_A_Random_Direction(unit_x, unit_y):
    #Colorization Themes
    Unit_Color = "Green"
    Obsticle_Color = "Red"
    Exit_Color = "Yellow"
    Tile_Color = "Blank"

    #Set the next checked pixel.
    left_x = unit_x + 1
    if(left_x > 7 or left_x < 0):
        left_x = unit_x 
    right_x = unit_x - 1
    if(right_x > 7 or right_x < 0):
        right_x =  unit_x
    down_y = unit_y + 1
    if(down_y > 7 or down_y < 0):
        down_y = unit_y
    up_y = unit_y - 1
    if(up_y > 7 or up_y < 0):
        up_y = unit_y

    x_check_if_stay_left_right = 0
    y_check_if_stay_up_down = 0
    next_pixel_x = 0
    next_pixel_y = 0

    #This is to prevent the unit from standing still this frame.
    while(x_check_if_stay_left_right == 0 and y_check_if_stay_up_down == 0):
        x_check_if_stay_left_right = randrange(0, 3)
        y_check_if_stay_up_down = randrange(0, 3)

    if y_check_if_stay_up_down == 0:
        next_pixel_y = unit_y
    elif y_check_if_stay_up_down == 1:
        next_pixel_y = up_y
    elif y_check_if_stay_up_down == 2:
        next_pixel_y = down_y

    if x_check_if_stay_left_right == 0:
        next_pixel_x = unit_x
    elif x_check_if_stay_left_right == 1:
        next_pixel_x = left_x
    elif x_check_if_stay_left_right == 2:
        next_pixel_x = right_x

    if (Matrix.get_Current_XY_Color(next_pixel_x, next_pixel_y) == Tile_Color or Matrix.get_Current_XY_Color(next_pixel_x, next_pixel_y) == Exit_Color ):

        if Matrix.get_Current_XY_Color(next_pixel_x, next_pixel_y) == Exit_Color:
            print "Changing rooms"

            Exit_X = randrange(0, 8)
            Exit_Y = randrange(0, 8)
        
            Matrix.set_All_Pixels(Tile_Color)

            for i in range(randrange(5,10)):
                Obsticle_X = randrange(0, 8)
                Obsticle_Y = randrange(0, 8)
                Matrix.set_Pixel(Obsticle_X, Obsticle_Y, Obsticle_Color)
                print "Making Obsticle #" + str(i) + " @ " + str(Obsticle_X) + "," + str(Obsticle_Y)

            Matrix.set_Pixel(Exit_X, Exit_Y, Exit_Color)
            time.sleep(1)

        print "Moving " + str(next_pixel_x) + "," + str(next_pixel_y)
        #Everything is good so we change the new square to our current spot
        Matrix.set_Pixel(unit_x, unit_y, Tile_Color)
        Matrix.set_Pixel(next_pixel_x, next_pixel_y, Unit_Color)

        unit_x = next_pixel_x
        unit_y = next_pixel_y

    return (unit_x, unit_y)
#END FUNCTION DEFINITION

#Colorization Themes
Unit_Color = "Green"
Obsticle_Color = "Red"
Exit_Color = "Yellow"
Tile_Color = "Blank"

#Setup Variables used in simulation.
unit_x = 0
unit_y = 0
Matrix.set_Pixel(unit_x, unit_y, Unit_Color)

Bottom_Left_X = randrange(2, 7)
Bottom_Left_Y = randrange(2, 7)
Matrix.set_All_Pixels(Tile_Color)
Matrix.draw_4px_Square(Bottom_Left_X, Bottom_Left_Y, Obsticle_Color)
Matrix.set_Pixel(7, 7, Exit_Color)

while(True):
    unit_x, unit_y = move_Unit_A_Random_Direction(unit_x, unit_y)
    time.sleep(.2)
