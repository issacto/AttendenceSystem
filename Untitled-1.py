import face_recognition
import cv2
import os.path
from os import path
import tkinter
from tkinter import *  
from tkinter import Button
import time
from PIL import ImageTk, Image
import os
import re
from datetime import date
import csv
from csv import writer


with open('AttendenceRecords/Attendence.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    peopleAttended = []
    for row in csv_reader:
        if(row[0]==date.today()):
            for member in peopleAttended:
                if member != row[1]:
                    peopleAttended.append(row[1])

