#importing libraries
import cv2
import numpy as np
import imutils
from pyfirmata import Arduino,SERVO,util
from sympy import *
from time import sleep
import math
port='/dev/cu.usbserial-10'             #selecting port in which arduino is connected to 
Board=Arduino(port)                     #creating object to handle I/O pins of arduino board
Board.digital[2].mode=SERVO             #declaring the mode of the digital pins to servo
Board.digital[3].mode=SERVO
Board.digital[4].mode=SERVO
Board.digital[6].mode=SERVO
Board.digital[2].write(180)             #initial angle of all the servos 
Board.digital[3].write(150)
Board.digital[4].write(30)
Board.digital[6].write(90)
board = [' ' for x in range(10)]        #board variable to store the value of all the boxes in the game
vid = cv2.VideoCapture(1)               #object to capture video of the game board
lower_white = np.array([200,200,200])   #hsv values to detect location of the boxes
upper_white = np.array([255,255,255])
p=0
q=0
X=0
Y=0
betai=150                               #current position of servos
alphai=30
thetai=180
handi=90
temp2=[]
temp3=[]
temp4=[]
while True:
    ret, frame = vid.read()
    cv2.waitKey(2000)
    arenacentres=[]
    mask=cv2.inRange(frame,lower_white,upper_white)
    contours=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=imutils.grab_contours(contours)
    a=0
    for c in contours:                          #determining the centres of all the boxes in the grid
        if cv2.contourArea(c)>10000:
            M=cv2.moments(c)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
            arenacentres.append([cx,cy])
            cv2.circle(frame,(cx,cy),10,255,-1)
            cv2.circle(mask,(cx,cy),10,255,-1)
    if not (len(arenacentres)==9):
        arenacentres=[]
        continue
    arenacentres.sort(key=lambda row: (row[1])) #sorting the coordinates from top-left corner to bottom right corner
    for k in range(0,3):
        temp2.append(arenacentres[k])
        temp2.sort(key=lambda row: (row[0]))
    for k in range(3,6):
        temp3.append(arenacentres[k])
        temp3.sort(key=lambda row: (row[0]))
    for k in range(6,9):
        temp4.append(arenacentres[k])
        temp4.sort(key=lambda row: (row[0]))
    arenacentres=temp2+temp3+temp4  
    print(arenacentres)
    break
def move_to_coordinate(X,Y,theta,hand,betai,alphai,thetai,handi):#function to move the robot head to a particular coordinate in cylindrical system
    X=float(X)
    Y=float(Y)
    theta=int(theta)
    a=57.29578*2*asin(pow(X*X+Y*Y,0.5)/18)
    b=((atan(-X/Y)+3.14)*57.29578-a/2)
    Alpha=180-b
    Beta=(a+b)
    print(a,b)
    
    rotateServo(3,Beta,betai)
    rotateServo(4,Alpha,alphai)
    rotateServo(2,theta,thetai)

    rotateServo(6,hand,handi)
    betai=Beta
    alphai=Alpha
    thetai=theta
    handi=hand
    return(betai,alphai,thetai,handi)
def rotateServo(pin,angle,initial):#function to rotate the servos to the angles returned by move_to_coordinate function
    initial=int(initial)
    angle=int(angle)
    if(initial>angle):
        for i in range(initial,angle,-1):
            Board.digital[pin].write(i)
            sleep(0.02)
    else:
        for i in range(initial,angle):
            Board.digital[pin].write(i)
            sleep(0.02)
def camInput():#function to detect the input from the player i.e the move made by the human
    while True:
        lower_green=np.array([40,100,20])
        upper_green=np.array([70,255,150])

        ret, frame = vid.read()
        
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
        green_mask=cv2.inRange(hsv,lower_green,upper_green)
        for Q in range(0,9):
            if(spaceIsFree(Q+1)):
                if(  green_mask[arenacentres[Q][1]][arenacentres[Q][0]]==255): 
                    cv2.waitKey(200)
                    if(  green_mask[arenacentres[Q][1]][arenacentres[Q][0]]==255):     
                        print(Q)
                        return Q+1
def insertLetter(letter, pos):#function to update the board variable
    board[pos] = letter
def spaceIsFree(pos):#function to find whether that given position is unoccupied
    return board[pos] == ' '
def printBoard(board):#function to print the current board situation
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
def isWinner(bo, le):#condition if there is winner
    return (bo[7] == le and bo[8] == le and bo[9] == le) or (bo[4] == le and bo[5] == le and bo[6] == le) or(bo[1] == le and bo[2] == le and bo[3] == le) or(bo[1] == le and bo[4] == le and bo[7] == le) or(bo[2] == le and bo[5] == le and bo[8] == le) or(bo[3] == le and bo[6] == le and bo[9] == le) or(bo[1] == le and bo[5] == le and bo[9] == le) or(bo[3] == le and bo[5] == le and bo[7] == le)
def playerMove():#update the variables if the players move is valid else return error
    run = True
    while run:

        move = camInput()
        try:
            move = int(move)
            if move > 0 and move < 10:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print('Sorry, this space is occupied!')
            else:
                print('Please type a number within the range!')
        except:
            print('Please type a number!')
def compMove():#determine the next best possible move for the bot
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0

    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move

    cornersOpen = []
    for i in possibleMoves:
        if i in [1,3,7,9]:
            cornersOpen.append(i)
            
    if len(cornersOpen) > 0:
        move = selectRandom(cornersOpen)
        return move

    if 5 in possibleMoves:
        move = 5
        return move

    edgesOpen = []
    for i in possibleMoves:
        if i in [2,4,6,8]:
            edgesOpen.append(i)
            
    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)
        
    return move
def selectRandom(li):#selecting any random move from all the best moves possible
    import random
    ln = len(li)
    r = random.randrange(0,ln)
    return li[r]
def isBoardFull(board):#function to find if the board is full
    if board.count(' ') > 1:
        return False
    else:
        return True
def main():
    print('Welcome to Tic Tac Toe!')
    printBoard(board)
    height=7.8
    betai=150
    alphai=30
    thetai=180
    handi=90
    while not(isBoardFull(board)):
        
        if not(isWinner(board, 'O')):
            playerMove()
            printBoard(board)
        else:
            print('Sorry, O\'s won this time!')
            break



        if not(isWinner(board, 'X')):
            move = compMove()
            if move == 0:
                print('Tie Game!')
            else:
                insertLetter('O', move)
                betai,alphai,thetai,handi=move_to_coordinate(1,height,180,90,betai,alphai,thetai,handi)
                betai,alphai,thetai,handi=move_to_coordinate(6,height,180,90,betai,alphai,thetai,handi)
                betai,alphai,thetai,handi=move_to_coordinate(6,height,180,140,betai,alphai,thetai,handi)
                betai,alphai,thetai,handi=move_to_coordinate(6,height+3,180,140,betai,alphai,thetai,handi)
                betai,alphai,thetai,handi=move_to_coordinate(2,height+3,180,140,betai,alphai,thetai,handi)
                betai,alphai,thetai,handi=move_to_coordinate(2,height+3,90,140,betai,alphai,thetai,handi)
                height=height-2
                if(move==1):
                    betai,alphai,thetai,handi=move_to_coordinate(6,3,60,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(6,5,60,90,betai,alphai,thetai,handi)
                    
                if(move==2):
                    betai,alphai,thetai,handi=move_to_coordinate(6,3,90,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(6,5,90,90,betai,alphai,thetai,handi)
                if(move==3):
                    betai,alphai,thetai,handi=move_to_coordinate(6,3,120,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(6,6,120,90,betai,alphai,thetai,handi)
                if(move==4):
                    betai,alphai,thetai,handi=move_to_coordinate(11,5,70,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(6,8,120,90,betai,alphai,thetai,handi)
                if(move==5):
                    betai,alphai,thetai,handi=move_to_coordinate(11,5,90,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(11,8,90,90,betai,alphai,thetai,handi)
                if(move==6):
                    betai,alphai,thetai,handi=move_to_coordinate(11,5,100,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(11,8,100,90,betai,alphai,thetai,handi)
                if(move==7):
                    betai,alphai,thetai,handi=move_to_coordinate(16,5,75,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(16,8,75,90,betai,alphai,thetai,handi)
                if(move==8):
                    betai,alphai,thetai,handi=move_to_coordinate(16,5,90,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(16,8,90,90,betai,alphai,thetai,handi)
                if(move==9):
                    betai,alphai,thetai,handi=move_to_coordinate(16,5,105,90,betai,alphai,thetai,handi)
                    betai,alphai,thetai,handi=move_to_coordinate(16,8,105,90,betai,alphai,thetai,handi)
                
                betai,alphai,thetai,handi=move_to_coordinate(3,7,90,90,betai,alphai,thetai,handi)
                print('Computer placed an \'O\' in position', move , ':')

                printBoard(board)
        else:
            print('X\'s won this time! Good Job!')
            break




    if isBoardFull(board):
        print('Tie Game!')
while True:
    answer = input('Do you want to play again? (Y/N)')
    if answer.lower() == 'y' or answer.lower == 'yes':
        board = [' ' for x in range(10)]
        print('-----------------------------------')
        main()
    else:
        break