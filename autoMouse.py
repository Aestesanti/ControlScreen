from tkinter import Button, Label, Tk
from random import randrange
import pyautogui

root = Tk()
root.title("MoveController v0.0")
root.geometry("200x100")

moveIntensity = 100
moveTransition = 0.5
isLoopMove = True

def startMove(*args):
    global isLoopMove
    if isLoopMove:
        startMoveBtn.config(background="red", relief="sunken")        
        statusLbl.config(text="Pulsa tecla 'a' para salir")
        root.update()

        x, y = globalSituation()
        moveX, moveY = randomiceIntensity()
        pyautogui.moveTo(x+moveX, y+moveY, moveTransition)
        root.after(500, startMove, isLoopMove)
    else:
        print ("paramos")        
        isLoopMove = True


def finishMove(*args):
    global isLoopMove
    isLoopMove = False
    startMoveBtn.config(background="SystemButtonFace", relief="raised")
    statusLbl.config(text="Etiqueta de estado")

def globalSituation():
    ressX, ressY = pyautogui.size()
    print("Current screen res: X=", ressX, "Y=", ressY)

    positionX, positionY = pyautogui.position()
    print("Mouse position: X=", positionX, "Y=", positionY)

    return positionX, positionY

def randomiceIntensity():
    moveXIntensity = randrange(-500,500)
    moveYIntensity = randrange(-500,500)     

    return moveXIntensity, moveYIntensity

startMoveBtn = Button(root, heigh=4, width=20, text="Start Moving", command=startMove)
statusLbl = Label(root, text="Etiqueta de estado")

startMoveBtn.focus()
startMoveBtn.bind("a", finishMove)

statusLbl.pack()
startMoveBtn.pack()

root.mainloop()
