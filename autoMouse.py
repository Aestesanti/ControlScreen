from tkinter import Button, Checkbutton, Entry, IntVar, Label, PhotoImage, StringVar, Tk, Toplevel, messagebox
from random import randrange
from tkinter.ttk import Separator
import pyautogui
import pygetwindow
from PIL import ImageGrab
import simpleaudio
import pywhatkit
import os

root = Tk()
icon = PhotoImage(file="./winicon.png")
root.title("ControlScreen v1.0.0")
root.eval("tk::PlaceWindow . center")
root.configure(background="#212F3C")
root.resizable(False, False)
root.iconphoto(True, icon)

#Variables list:
changeNameApp_Var = StringVar()
phoneToAlert_Var = StringVar()
appTitleToFind_Var = StringVar()
soundRoute = "sounds/submarine-submersion-alarm.wav"
sound = simpleaudio.WaveObject.from_wave_file(soundRoute)
moveIntensity = 100
moveTransition = 0.5
isLoopMove = True
isLoopControl = True
checkSCType_Var = IntVar(value=1)
checkAlertSound_Var = IntVar(value=1)
checkAlertMssg_Var = IntVar(value=0)
listApssAtStart = []
pyautogui.FAILSAFE = False    

def setNameApp(*args):
    if changeNameApp_Var.get() != "":
        root.title(changeNameApp_Var.get())
        root.update()
        root.focus()
    else:
        root.title("MoveController v0.1")
        root.focus()

def configMenuAler():
    if checkAlertMssg_Var.get() == 1:
        root_x = root.winfo_x()
        root_y = root.winfo_y()

        menuAlertRoot = Toplevel(root)  
        menuAlertRoot.title("Config Message Alert")
        menuAlertRoot.geometry(f'+{root_x+50}+{root_y+100}')
        menuAlertRoot.grab_set()
        menuAlertRoot.config(background="#212F3C")
        menuAlertRoot.resizable(False, False)

        phoneToAlert_Lbl = Label(menuAlertRoot, text="Phone to alert:", background="#212F3C", foreground="#CACFD2")
        phoneToAlert = Entry(menuAlertRoot, textvariable=phoneToAlert_Var, background="#808B96", foreground="#CACFD2")        

        def setPhoneNumber(*args):
            if phoneToAlert_Var.get() != "" and "+" == phoneToAlert_Var.get()[0] and phoneToAlert_Var.get().replace("+","").isnumeric():
                print (phoneToAlert_Var.get())
                menuAlertRoot.destroy()
                return True
            else:
                phoneToAlert_Var.set("")
                messagebox.showerror("Phone number error:","Incorrect phone number, please ensure you have entered country code (+34..) and only numbers.")
                return False
        
        def testWhats():
            if setPhoneNumber():
                pywhatkit.sendwhatmsg_instantly(phoneToAlert_Var.get(), "Test", tab_close=True, close_time=1)  

        def closeMenuAlert():
            checkAlertMssg_Var.set(0)
            phoneToAlert_Var.set("")        
            menuAlertRoot.destroy()
        
        phoneToAlert_TestBtn = Button(menuAlertRoot, text="TestPhone", command=testWhats, background="#566573", foreground="#CACFD2")

        phoneToAlert.focus()
        phoneToAlert.bind('<Return>', setPhoneNumber)        

        phoneToAlert_Lbl.grid(row=0, column=0)
        phoneToAlert.grid(row=0, column=1)
        phoneToAlert_TestBtn.grid(row=1, column=0, columnspan=2)

        phoneToAlert.grid_columnconfigure(0, weight=1)
        phoneToAlert.grid_columnconfigure(1, weight=1)

        menuAlertRoot.config(padx=5, pady=5)

        menuAlertRoot.protocol("WM_DELETE_WINDOW", closeMenuAlert)
        menuAlertRoot.mainloop()

def cUEntry():
    if checkSCType_Var.get() == 1:
        appTitleToFind.config(state="disabled")
        print("NO ACTIVO ENTRY")
    elif checkSCType_Var.get() == 0:
        appTitleToFind.config(state="normal")
        print("Activo entry")

def configControlScreen():
    global listApssAtStart, isLoopControl
    controlScreenBtn.config(background="green", relief="sunken")
    appTitleToFind.config(state="disabled")
    root.focus()
    root.update()
    listApssAtStart = pygetwindow.getAllTitles()
    isLoopControl =True
    statusLbl.config(text="Press 'Alt + s' to cancel all systems")
    print("Hay "+ str(len(listApssAtStart)) + " ventanas ejecutandose")
    startControlScreen()

def startControlScreen():
    global isLoopControl, listApssAtStart
    if isLoopControl:
        listApssAtNow = pygetwindow.getAllTitles()

        if checkSCType_Var.get() == 0:
            print ("BUSCANDO APP CONCRETA")
            findApp = appTitleToFind_Var.get()
            
            for app in listApssAtNow:
                if findApp in str(app):
                    activateAlarm()

        elif checkSCType_Var.get() == 1:        

            if len(listApssAtNow) > len(listApssAtStart): #Salta la alarma si se cumple
                activateAlarm()

        root.after(2000, startControlScreen)            
    else:
        isLoopControl = True
        listApssAtStart.clear()
        print("Paramos el control de screen")
        #Paramos tb el automove
        finishMove()
        startMove()

def sendPhoneAlert(nameApp):
    if checkAlertMssg_Var.get() == 1:
        pywhatkit.sendwhats_image(phoneToAlert_Var.get(), "./Screenshot.png", "Ha saltado alarma, con: " + nameApp, tab_close=True)
    

def playSoundAlert():
    if checkAlertSound_Var.get() == 1:
        sound.play()

def activateAlarm(*args):
    global isLoopControl
    image = ImageGrab.grab(all_screens=True)
    image.save("Screenshot.png")    
    nameApp = pygetwindow.getActiveWindow().title
    playSoundAlert()
    sendPhoneAlert(nameApp)
    os.remove("./Screenshot.png")
    isLoopControl = False

def stopControlScreen(*args):
    global isLoopControl
    isLoopControl = False
    controlScreenBtn.config(relief="raised", background="#566573", foreground="#CACFD2")
    cUEntry()
    root.update()
    simpleaudio.stop_all()

def startMove(*args):
    global isLoopMove
    if isLoopMove:
        startMoveBtn.config(background="red", relief="sunken")
        statusLbl.config(text="Press 'Alt + a' to cancel movement")
        root.update()

        x, y = globalSituation()
        moveX, moveY = randomiceIntensity()
        if pyautogui.onScreen(x+moveX, y+moveY):
            pyautogui.moveTo(x+moveX, y+moveY, moveTransition)
            root.after(500, startMove)
        else:
            print("REPETIMOS")
            root.after(500, startMove)
    else:
        print("paramos")
        isLoopMove = True


def finishMove(*args):
    global isLoopMove
    isLoopMove = False
    startMoveBtn.config(background="#566573", relief="raised", foreground="#CACFD2")
    statusLbl.config(text="Etiqueta de estado")
    root.update()

def currentResolution():
    return pyautogui.size()

def globalSituation():
    positionX, positionY = pyautogui.position()
    print("Mouse position: X=", positionX, "Y=", positionY)

    return positionX, positionY

def randomiceIntensity():
    moveXIntensity = randrange(-250, 250)
    moveYIntensity = randrange(-250, 250)

    return moveXIntensity, moveYIntensity


resX, resY = currentResolution()
configResLblText = "Your resolution is: " + str(resX) + "x" + str(resY)

changeNameAppLbl = Label(root, text="Name to set:", background="#212F3C", foreground="#CACFD2")
changeNameApp = Entry(root, textvariable=changeNameApp_Var, background="#808B96", foreground="#CACFD2")
separator_1 = Separator(root, orient="horizontal")
startMoveBtn = Button(root, heigh=4, width=20, text="Start Moving", command=startMove, background="#566573", foreground="#CACFD2")
separator_2 = Separator(root, orient="horizontal")
controlScreenBtn = Button(root, text="Screen Control", command=configControlScreen, background="#566573", foreground="#CACFD2")
checkSCType = Checkbutton(root, text="Any", variable=checkSCType_Var, command=cUEntry, background="#212F3C", 
foreground="#CACFD2", activebackground="#212F3C", activeforeground="#CACFD2", selectcolor="#808B96")
checkAlertSound = Checkbutton(root, text="AlertSound", variable=checkAlertSound_Var, foreground="#CACFD2", background="#212F3C", 
activebackground="#212F3C", activeforeground="#CACFD2", selectcolor="#808B96")
checkAlertMssg = Checkbutton(root, text="WhatsappAlert", variable=checkAlertMssg_Var, command=configMenuAler, foreground="#CACFD2", background="#212F3C",
activebackground="#212F3C", activeforeground="#CACFD2", selectcolor="#808B96")
appTitleToFind = Entry(root, state="disabled", textvariable=appTitleToFind_Var, background="#808B96", foreground="#CACFD2", disabledbackground="#131313", disabledforeground="#DBDBDB")
statusLbl = Label(root, text="Etiqueta de estado", background="#212F3C", foreground="#CACFD2")
configResLbl = Label(root, text=configResLblText, background="#212F3C", foreground="#CACFD2")

root.focus()
root.bind("<Alt-KeyPress-a>", finishMove)
root.bind("<Alt-KeyPress-A>", finishMove)
root.bind("<Alt-KeyPress-s>", stopControlScreen)
root.bind("<Alt-KeyPress-S>", stopControlScreen)
changeNameApp.bind("<Return>", setNameApp)

changeNameAppLbl.grid(row=0, column=0)
changeNameApp.grid(row=0, column=1)
separator_1.grid(row=1, column=0, sticky="ew", columnspan=2, pady=10)
configResLbl.grid(row=2, column=0, columnspan=2)
startMoveBtn.grid(row=3, column=0, columnspan=2)
separator_2.grid(row=4, column=0, sticky="ew", columnspan=2, pady=10)
checkSCType.grid(row=5, column=0)
appTitleToFind.grid(row=5, column=1)
checkAlertSound.grid(row=6, column=0)
checkAlertMssg.grid(row=6, column=1)
controlScreenBtn.grid(row=7, column=0, columnspan=2)
statusLbl.grid(row=8, column=0, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.grid_columnconfigure(8, weight=1)

root.config(padx=5, pady=5)

root.mainloop()
