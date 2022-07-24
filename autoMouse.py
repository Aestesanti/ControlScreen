from tkinter import Button, Label, Tk
from random import randrange
import pyautogui
from PIL import ImageGrab

root = Tk()
root.title("MoveController v0.0")
root.geometry("200x140")
root.eval("tk::PlaceWindow . center")

moveIntensity = 100
moveTransition = 0.5
isLoopMove = True
pyautogui.FAILSAFE=False

def controlScreen():
    image = ImageGrab.grab(all_screens=True)
    image.save("test.png")

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
            root.after(500, startMove, isLoopMove)
        else:
            print("REPETIMOS")
            root.after(500, startMove, isLoopMove)
    else:
        print ("paramos")        
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
    moveXIntensity = randrange(-250,250)
    moveYIntensity = randrange(-250,250)     

    return moveXIntensity, moveYIntensity

resX, resY = currentResolution()
configResLblText = "Your resolution is: " + str(resX) + "x" + str(resY)

startMoveBtn = Button(root, heigh=4, width=20, text="Start Moving", command=startMove)
controlScreenBtn = Button(root, text="Control Screen", command=controlScreen)
statusLbl = Label(root, text="Etiqueta de estado")
configResLbl = Label(root, text=configResLblText)

startMoveBtn.focus()
startMoveBtn.bind("a", finishMove)

statusLbl.pack()
startMoveBtn.pack()
controlScreenBtn.pack()
configResLbl.pack()

root.mainloop()
