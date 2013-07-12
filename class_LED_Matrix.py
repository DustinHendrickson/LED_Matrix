#!/usr/bin/python

import time
import ConfigParser
import thread
#import datetime
#import settings
import MySQLdb as Database
from random import randrange
import sys
from Adafruit_8x8 import ColorEightByEight
import MySQLdb as Database


class LED_Matrix:
    #Variables for converting Pixel Colors
    ColorInt_To_String = ["Blank", "Green", "Red", "Yellow"]
    ColorString_To_Int = {"Blank": 0, "Green": 1, "Red": 2, "Yellow": 3}
    #These are used for easy use throughout the code for specific colors
    Blank_Pixel = 0
    Green_Pixel = 1
    Red_Pixel = 2
    Yellow_Pixel = 3
    #We need to track the state of each Grid LED.
    Grid_State = [[0 for Column in range(8)] for Row in range(8)]
    Pixel_Refresh_Rate = 0.0001
    #Reference locations
    # x,y | References for Grid
    #----------------
    # 0,0 = TOP RIGHT
    # 7,0 = TOP LEFT
    # 0,7 = BOTTOM RIGHT
    # 7,7 = BOTTOM LEFT

    #Construction function that is ran when class is initiated.
    #Here we initiate the Adafruit8x8 API
    def __init__(self):
        self.Grid = ColorEightByEight(address=0x70)
        self.Connection = Database.connect('localhost', 'root', 'cool', 'gamedb')

    #===========================================
    #General Use Functions that return a value==
    #===========================================
    def get_Random_ColorString(self, boolean_Inc_Blank=True):
        if boolean_Inc_Blank is True:
            return LED_Matrix.ColorInt_To_String[randrange(0, 4)]
        else:
            return LED_Matrix.ColorInt_To_String[randrange(1, 3)]

    def get_Buffer_Value(self, i):
        return self.Grid.getBufferValue(i)

    def get_Random_ColorInt(self, boolean_Inc_Blank=True):
        if boolean_Inc_Blank is True:
            return randrange(0, 4)
        else:
            return randrange(1, 3)

    def get_Current_XY_Color(self, x, y):
        return LED_Matrix.ColorInt_To_String[LED_Matrix.Grid_State[x][y]]

    #===========================================
    #End of General Use Functions===============
    #===========================================

    #===========================================
    #Drawing Functions
    #===========================================
    def draw_4px_Square(self, Bottom_Left_X, Bottom_Left_Y, string_Pixel_Color="Blank"):
        self.set_Pixel(Bottom_Left_X, Bottom_Left_Y, string_Pixel_Color)
        self.set_Pixel(Bottom_Left_X, Bottom_Left_Y-1, string_Pixel_Color)
        self.set_Pixel(Bottom_Left_X-1, Bottom_Left_Y-1, string_Pixel_Color)
        self.set_Pixel(Bottom_Left_X-1, Bottom_Left_Y, string_Pixel_Color)

    def draw_Row_Line(self, row_number, string_Row_Color="Blank"):
        y = 0
        Random = False
        if(string_Row_Color=="Rainbow"):
            Random = True
        while(y < 8):
            if(Random==True):
                string_Row_Color = self.get_Random_ColorString(False)
            self.set_Pixel(row_number, y, string_Row_Color)
            y = y + 1
            time.sleep(LED_Matrix.Pixel_Refresh_Rate)

    def draw_Column_Line(self, column_number, string_Column_Color="Blank"):
        x = 0
        Random = False
        if(string_Column_Color=="Rainbow"):
            Random = True
        while(x < 8):
            if(Random==True):
                string_Column_Color = self.get_Random_ColorString(False)
            self.set_Pixel(x, column_number, string_Column_Color)
            x = x + 1
            time.sleep(LED_Matrix.Pixel_Refresh_Rate)
    #===========================================
    #End of Drawning Functions==================
    #===========================================


    #===========================================
    #I/O Functions
    #===========================================
    def write_FlatFile(self):
        Config = ConfigParser.ConfigParser()

        with open ('Grid_Status.ini', 'w') as FlatFile:
            Config.read('Grid_Status')
            Config.add_section('Grid_Status')
            for x in range(0, 8):
                    for y in range(0, 8):
                        Config.set("Grid_Status", str(x) + "," + str(y), self.get_Current_XY_Color(x, y) )
            Config.write(FlatFile)

    #===========================================
    #End of I/O Functions=======================
    #===========================================


    #===========================================
    #Set Functions
    #===========================================
    #Instant grid clear for prettier transitions.
    #We do it this way to bypass the pixel refresh interval.
    def set_Clear_Grid(self):
        self.Grid.clear()
        for x in range(0, 8):
            for y in range(0, 8):
                LED_Matrix.Grid_State[x][y] = 0

    #Wrapper for setting a pixel so we can track it in our code and not need to reference the hardware.
    def set_Pixel(self, x, y, string_Pixel_Color="Blank"):
        int_Pixel_Color = LED_Matrix.ColorString_To_Int[string_Pixel_Color]
        #Here we update our instances's record of the grid screen
        LED_Matrix.Grid_State[x][y] = int_Pixel_Color
        #This is the function from our AdaFruit_8x8.py API
        self.Grid.setPixel(x, y, int_Pixel_Color)
        #If x and y are valid, update the database
        #//if (x >= 0 and y >= 0):
            #//self.write_FlatFile()
            #//self.set_Database_GridStatus_Update(x, y, int_Pixel_Color)
            #//thread.start_new_thread(self.set_Database_GridStatus_Update, (x, y, int_Pixel_Color))

    #This function will display a color to every pixel of the matrix based on input string.
    #See Class Variables for acceptable input. Defaults to BLANK.
    def set_All_Pixels(self, string_Pixel_Color="Blank"):
        for x in range(0, 8):
            for y in range(0, 8):
                self.set_Pixel(x, y, string_Pixel_Color)
                time.sleep(LED_Matrix.Pixel_Refresh_Rate)

    def set_Random_Pixel(self, string_Pixel_Color="Blank"):
        x = randrange(0, 8)
        y = randrange(0, 8)
        self.set_Pixel(x, y, string_Pixel_Color)

    #Brightness is messured 0-15
    def set_Matrix_Brightness(self, brightness):
        self.Grid.setBrightness(brightness)

    # Sets the displays Blink Rate, 0 = OFF , 1 = 2HZ , 2 = 1HZ , 3 = Half HZ
    def set_Matrix_BlinkRate(self, blinkRate):
        self.Grid.setBlinkRate(blinkRate)

    def set_Database_GridStatus_Update(self, x, y, int_Color):
        with self.Connection:
            Cursor = self.Connection.cursor()
            #SQL = "INSERT INTO Grid_Status(ID, Value) VALUES(%s, %s) ON DUPLICATE KEY UPDATE Value = %s"
            SQL = "UPDATE Grid_Status SET Value = %s WHERE ID = %s"
            DATA = ( str(int_Color), str(x) + "," + str(y), )
            Cursor.execute(SQL, DATA)
            time.sleep(LED_Matrix.Pixel_Refresh_Rate)

    #===========================================
    #End of Set Functions=======================
    #===========================================
