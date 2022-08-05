from tkinter import Button, Checkbutton, Entry, IntVar, Label, StringVar, Tk, Toplevel, messagebox
from random import randrange
import pyautogui
import pygetwindow
from PIL import ImageGrab
import simpleaudio
import pywhatkit

root = Tk()
root.title("MoveController v0.1")
root.geometry("275x175")
root.eval("tk::PlaceWindow . center")

#Variables list:
phoneToAlert_Var = StringVar()
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

def configMenuAler():
    if checkAlertMssg_Var.get() == 1:
        menuAlertRoot = Toplevel(root)  
        menuAlertRoot.title("Config Message Alert")
        menuAlertRoot.geometry("200x50")
        menuAlertRoot.grab_set()

        phoneToAlert_Lbl = Label(menuAlertRoot, text="Phone to alert:")
        phoneToAlert = Entry(menuAlertRoot, textvariable=phoneToAlert_Var)        

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
                pywhatkit.sendwhatmsg_instantly(phoneToAlert_Var.get(), "Test", tab_close=True)            
        
        phoneToAlert_TestBtn = Button(menuAlertRoot, text="TestPhone", command=testWhats)

        phoneToAlert.focus()
        phoneToAlert.bind('<Return>', setPhoneNumber)        

        phoneToAlert_Lbl.pack()
        phoneToAlert.pack()
        phoneToAlert_TestBtn.pack()

        menuAlertRoot.mainloop()

def cUEntry():
    if checkSCType_Var.get() == 1:
        appTitleToFind.config(state="disabled")
        print("NO ACTIVO ENTRY")
    elif checkSCType_Var.get() == 0:
        appTitleToFind.config(state="normal")
        print("Activo entry")

def configControlScreen():
    global listApssAtStart
    controlScreenBtn.config(background="green", relief="sunken")
    root.update()
    listApssAtStart = pygetwindow.getAllTitles()
    print("Hay "+ str(len(listApssAtStart)) + " ventanas ejecutandose")
    startControlScreen()

def startControlScreen():
    global isLoopControl, listApssAtStart
    if isLoopControl:
        listApssAtNow = pygetwindow.getAllTitles()

        if checkSCType_Var.get() == 0:
            print("DEBERIA BUSCAR EL PROGRAMA ESCRITO EN EL CAMPO")

        elif checkSCType_Var.get() == 1:        

            if len(listApssAtNow) > len(listApssAtStart): #Salta la alarma si se cumple
                image = ImageGrab.grab(all_screens=True)
                image.save("test.png")
                listTitles = pygetwindow.getActiveWindow().title
                playSoundAlert()  
                sendPhoneAlert()              
                print("Salta la alarma con: " + listTitles)
                autoStopControlScreen()
            
        root.after(3000, startControlScreen)            
    else:
        isLoopControl = True
        listApssAtStart.clear()
        print("Paramos el control de screen")
        #Paramos tb el automove
        finishMove()
        startMove()

def sendPhoneAlert():
    if checkAlertMssg_Var.get() == 1:
        pywhatkit.sendwhatmsg_instantly(phoneToAlert_Var.get(), "Ha saltado alarma, mando Imagen", tab_close=True)
    

def playSoundAlert():
    if checkAlertSound_Var.get() == 1:
        sound.play()


def autoStopControlScreen(*args):
    global isLoopControl
    isLoopControl = False

def stopControlScreen(*args):
    global isLoopControl
    isLoopControl = False
    controlScreenBtn.config(background="SystemButtonFace", relief="raised")
    root.update()
    simpleaudio.stop_all()


def startMove(*args):
    global isLoopMove
    if isLoopMove:
        startMoveBtn.config(background="red", relief="sunken")
        statusLbl.config(text="Pulsa tecla 'a' para salir")
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
    startMoveBtn.config(background="SystemButtonFace", relief="raised")
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

startMoveBtn = Button(root, heigh=4, width=20, text="Start Moving", command=startMove)
controlScreenBtn = Button(root, text="Screen Control", command=configControlScreen)
checkSCType = Checkbutton(root, text="Any", variable=checkSCType_Var, command=cUEntry)
checkAlertSound = Checkbutton(root, text="AlertSound", variable=checkAlertSound_Var)
checkAlertMssg = Checkbutton(root, text="WhatsappAlert", variable=checkAlertMssg_Var, command=configMenuAler)
appTitleToFind = Entry(root, state="disabled")
statusLbl = Label(root, text="Etiqueta de estado")
configResLbl = Label(root, text=configResLblText)

root.focus()
root.bind("a", finishMove)
root.bind("A", finishMove)
root.bind("s", stopControlScreen)
root.bind("S", stopControlScreen)

statusLbl.pack()
startMoveBtn.pack()
checkSCType.pack()
appTitleToFind.pack()
checkAlertSound.pack()
checkAlertMssg.pack()
controlScreenBtn.pack()
configResLbl.pack()

root.mainloop()
