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

class faceRecognition():
    '''class for facial recognition starts here'''
    def takePic(self):
        #take photo for attendee
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        self.image = image
        cv2.imwrite('something.png', image)
        image = Image.open('something.png')
        image1 = image.resize((400,400), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image1)
        del(camera)
        return image2
        
    def realizeWho(self):
        #realize who the person got taken is from file Members_photos
        try:
            directory = "/Users/issac/Documents/python/Attendence_Machine/Members_Photos"
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".jpg"):
                    filenamePath = directory+ "/"+filename
                    known_image =  face_recognition.load_image_file(filenamePath)
                    unknown_image = self.image
                    biden_encoding = face_recognition.face_encodings(known_image)[0]
                    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

                    '''reseults is found in this stage and do the relevant procedures acc to the result'''

                    if results[0] == True:
                        file = open("AttendenceRecords/Attendence.csv")
                        reader = csv.reader(file)
                        nextLines= len(list(reader))
                        name = 'opencv'+str(nextLines)+'.png'
                        memberName = filename.split(".")
                        self.memberName = memberName[0]
                        #wrtie the file into PhotosTaken file
                        path = "/Users/issac/Documents/python/Attendence_Machine/PhotosTaken"
                        cv2.imwrite(os.path.join(path, name), self.image)

                        #record the member into the csv along with the date the pic's taken
                        with open('AttendenceRecords/Attendence.csv', 'a+', newline='') as write_obj:
                            csv_writer = writer(write_obj)
                            csv_writer.writerow([date.today(),self.memberName])
                        return 1
            else:
                return 0
        except:
            return -1 
    
        

class gui():
    ''' class for GUI starts here'''
    signedUp = 0
    def __init__(self):
        #create window
        window = tkinter.Tk()
        window.geometry("600x600")
        window.resizable(0,0)
        window.title("Face Recognition")
        #background Image
        backgroundImage = Image.open("BackgroundPics/Display.jpg")
        backgroundImage = backgroundImage.resize((600, 600), Image.ANTIALIAS)
        backgroundImage = ImageTk.PhotoImage(backgroundImage)
        background_label = Label(window, image=backgroundImage)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #textdisplayed
        self.textDisplayed = tkinter.StringVar()
        self.textDisplayed.set("Press when you are ready for being photo taken")
        #label
        label = tkinter.Label(window, textvariable=self.textDisplayed)
        label.pack()
        #pircturelabel
        image = Image.open("BackgroundPics/kingsCollegeLondon.png")
        image = image.resize((400, 400), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image)
        self.panel = Label(window, image = image1)
        self.panel.pack()
        #press button
        btn_text = tkinter.StringVar()
        btn_text.set("Press when you are ready")
        pressButton = tkinter.Button(window, textvariable= btn_text, command = lambda: self.helloCallBack())
        pressButton.pack()
        pressButton.place(x = 400,y = 470)
        #check button
        checkButton = tkinter.Button(window, text = "Check", command = lambda: self.calculateButton())
        checkButton.pack()
        checkButton.place(x = 500,y = 550)
        #run
        window.mainloop()
    
    def helloCallBack(self):
        '''subsequent action when press button is printed'''
        x = faceRecognition()
        pictureDisplayed = x.takePic()
        self.panel.configure(image=pictureDisplayed)
        self.panel.image = pictureDisplayed
        y=x.realizeWho()
        #change the label on the top of the gui acc to the result of who the guy is
        if y == 1:
            self.signedUp += 1
            self.textDisplayed.set("Hi "+x.memberName+"!"+" You are logged in!")
        elif y == 0:
            self.textDisplayed.set("Can't identify you, Sorry! Have you signed up yet?") 
        else:
            self.textDisplayed.set("Please press again!")

    def calculateButton(self):
        y = guiInsideGui()
   
class guiInsideGui():
    '''class for the pop up gui starts here '''
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("200x200")
        self.window.resizable(0,0)
        self.window.title("Check")
        attendence = self.calculateAttendence()
        #top label
        leftTextDisplayed = "Number of people signed in:"
        leftLabel = tkinter.Label(self.window, text=leftTextDisplayed)
        leftLabel.place(x=0,y=0)
        #bottom label
        rightTextDisplayed = str(len(attendence))
        rightLabel = tkinter.Label(self.window, text=rightTextDisplayed)
        rightLabel.place(x=50,y=0)
        #Names String Label
        leftAttendenceTextDisplayed = "Name:"
        leftAttendenceDisplayed = tkinter.Label(self.window, text=leftAttendenceTextDisplayed)
        leftAttendenceDisplayed.place(x=0,y=20)
        #Names Members Labels
        rightAttendenceTextDisplayed = str(attendence)
        rightAttendenceDisplayed = tkinter.Label(self.window, text=rightAttendenceTextDisplayed)
        rightAttendenceDisplayed.place(x=50,y=20)
        #back button
        button = tkinter.Button(self.window, text = 'Finalize Attendence')
        button.place(x = 150,y = 50)
        #print button
        button = tkinter.Button(self.window, text = 'OK', command=lambda: self.quit())
        button.place(x = 150,y = 100)
        #run
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def calculateAttendence(self):
        '''calculate how many people are signed up for that day'''
        with open('AttendenceRecords/Attendence.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            peopleAttended = []
            for row in csv_reader:
                if(row[0]==date.today().strftime("%Y-%m-%d")):
                    if peopleAttended:
                        for member in peopleAttended:
                            if member != row[1]:
                                peopleAttended.append(row[1])
                    else:
                        peopleAttended.append(row[1])

            print (peopleAttended)
        return peopleAttended

if __name__ == "__main__":
    '''program runs here'''
    x =gui()

        




