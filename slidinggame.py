import pygame, sys, random, os, subprocess
from pygame.locals import *


class Color:
    BLACK =         (  0,   0,   0)
    WHITE =         (255, 255, 255)
    BRIGHTBLUE =    (  0,  50, 255)
    DARKTURQUOISE = (  3,  54,  73)
    GREEN =         (  0, 204,   0)


class BoardProperty:
    NUMROWS = NUMCOLUMNS = 4
    TILESIZE = (int)(240/NUMROWS)
    WINDOWWIDTH = 1366
    WINDOWHEIGHT = 750
    FPS = 30
    TEXTCOLOR = Color.WHITE
    BASICFONTSIZE = 20
    BGCOLOR = Color.DARKTURQUOISE
    BORDERCOLOR = Color.BRIGHTBLUE
    STARTPUZZLE = 'startpuzzle'
    GOALPUZZLE = 'goalpuzzle'
    ANIMATIONSPEED = TILESIZE/5
    NUMOFMOVES = 60

class TileProperty:
    BLANK = None #Blank Tile
    class Direction:
        UP = "up"
        DOWN = "down"
        RIGHT = "right"
        LEFT = "left"
    TILECOLOR = Color.GREEN


def main():
    # the main loop etc.
    global FPSCLOCK,DISPLAYSURF,BASICFONT,RESET_SURF,RESET_RECT,SOLVE_SURF,SOLVE_RECT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((BoardProperty.WINDOWWIDTH,BoardProperty.WINDOWHEIGHT))
    pygame.display.set_caption('The Slide Puzzle Solver')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BoardProperty.BASICFONTSIZE)
    
    #the buttons
    RESET_SURF, RESET_RECT = returnText('Reset', BoardProperty.TEXTCOLOR, Color.DARKTURQUOISE, BoardProperty.WINDOWWIDTH-120, BoardProperty.WINDOWHEIGHT-90)
    SOLVE_SURF, SOLVE_RECT = returnText('Solve', BoardProperty.TEXTCOLOR, Color.DARKTURQUOISE, BoardProperty.WINDOWWIDTH-120, BoardProperty.WINDOWHEIGHT-60)
    

    #goalBoard = generateNewPuzzle()   #this is the goal board
    #goalBoard = [[0,1,2],[3,4,5],[6,7,8]]
    goalBoard = []
    index = 0
    for i in range(BoardProperty.NUMROWS):
        r = []
        for j in range(BoardProperty.NUMCOLUMNS):
            r.append(index)
            index=index+1
        goalBoard.append(r)
    goalBoard[0][0] = TileProperty.BLANK
    
    startBoard = generateNewPuzzle(goalBoard)  #generate random board from initial states
    #game loop
    while True:
        DISPLAYSURF.fill(BoardProperty.BGCOLOR)
        drawBoard(startBoard, 0, BoardProperty.STARTPUZZLE)
        #drawBoard(goalBoard, (int)(2.5*BoardProperty.TILESIZE*BoardProperty.NUMCOLUMNS), BoardProperty.GOALPUZZLE)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if RESET_RECT.collidepoint(event.pos):
                    startBoard = generateNewPuzzle(goalBoard)
                    #goalBoard = generateNewPuzzle()
                elif SOLVE_RECT.collidepoint(event.pos):
                    sequence = getSolutionSequence(startBoard, goalBoard, BoardProperty.NUMROWS, BoardProperty.NUMCOLUMNS)
                    animation(startBoard, sequence, 0)
        checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick(BoardProperty.FPS)

        

def getLeftTopOfTile(tilex, tiley, offset):
    return (tiley+1)*BoardProperty.TILESIZE+40+offset, (tilex+1)*BoardProperty.TILESIZE+40


def drawTile(tilex, tiley, val, offset, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley, offset)
    left = left+adjy
    top = top+adjx
    pygame.draw.rect(DISPLAYSURF, TileProperty.TILECOLOR, (left, top, BoardProperty.TILESIZE, BoardProperty.TILESIZE))
    textSurf = BASICFONT.render(str(val), True, BoardProperty.TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(BoardProperty.TILESIZE/2), top+int(BoardProperty.TILESIZE/2)
    pygame.draw.rect(DISPLAYSURF, Color.BLACK,(left, top, BoardProperty.TILESIZE, BoardProperty.TILESIZE), 1)
    DISPLAYSURF.blit(textSurf, textRect)
    

def drawBoard(board, offset, message):
    #DISPLAYSURF.fill(BoardProperty.BGCOLOR)
    if message:
        textSurf, textRect = returnText(message, BoardProperty.TEXTCOLOR, BoardProperty.BGCOLOR, offset+5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley], offset,0,0)
    
    left, top = getLeftTopOfTile(0, 0, offset)
    width = BoardProperty.TILESIZE*BoardProperty.NUMCOLUMNS
    height = BoardProperty.TILESIZE*BoardProperty.NUMROWS
    pygame.draw.rect(DISPLAYSURF, BoardProperty.BORDERCOLOR, (left-5
, top-5, width+11, height+11), 4)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    
    
def generateNewPuzzle(startBoard):
    board = startBoard
    vmoves = [TileProperty.Direction.UP, TileProperty.Direction.DOWN]
    hmoves = [TileProperty.Direction.LEFT, TileProperty.Direction.RIGHT]
    for i in range(BoardProperty.NUMOFMOVES):
        desx, desy = getBlankPosition(board)
        if i%2==0:
            move = random.choice(vmoves)
        else:
            move = random.choice(hmoves)
        if isValidMove(board,move):
            #slideAnimation(board, move,0)
            x,y = 0,0
            if move==TileProperty.Direction.UP:
                x = 1
            elif move==TileProperty.Direction.DOWN:
                x = -1
            elif move==TileProperty.Direction.RIGHT:
                y = -1
            elif move==TileProperty.Direction.LEFT:
                y = 1
            board[desx][desy], board[desx-x][desy-y] = board[desx-x][desy-y], board[desx][desy]
        else:
            i=i-1
    return board


def returnText(text,color,bgcolor,top,left):
    #return text surface and rect object
    textSurf = BASICFONT.render(text,True,color,bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getSolutionSequence(startBoard, goalBoard, rows, columns):  #returns the moves the blank tile has to undergo to reach the goal board
    #generate input string
    #must have rows=columns
    DISPLAYSURF.fill(BoardProperty.BGCOLOR)
    drawBoard(startBoard,0,"generating solution....")
    pygame.display.update()
    s=str(rows)+"\n"
    for i in startBoard:
        for j in i:
            if j==TileProperty.BLANK:
                s=s+"0\n"
            else:
                s=s+str(j)+"\n"

    #run the npuzzle code
    subprocess.call(["g++","npuzzle.cpp"])
    p = subprocess.Popen(["./a.out"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(input=s)
    output = output.split('\n')

    if err!=None and err!='':
        print 'some mistake in compilation/run'
        exit(0)
    return output
    
def getBlankPosition(board):
    for i in range(BoardProperty.NUMROWS):
        for j in range(BoardProperty.NUMCOLUMNS):
            #print "board:", i, j, board[i][j]
            if board[i][j]==None:
                return (i,j)

def isValidMove(board, move):
    x, y = getBlankPosition(board)
    #print 'position:',x,y,board[x][y]
    if move==TileProperty.Direction.UP:
        x = x-1
    elif move==TileProperty.Direction.DOWN:
        x = x+1
    elif move==TileProperty.Direction.LEFT:
        y = y-1
    elif move==TileProperty.Direction.RIGHT:
        y=y+1
    if x>=0 and x<BoardProperty.NUMROWS and y>=0 and y<BoardProperty.NUMCOLUMNS:
        return True
    else:
        return False


def slideAnimation(board, move, offset):      #assuming that the move is valid on board
    desx, desy = getBlankPosition(board)
    (x,y)=(0,0)
    if move==TileProperty.Direction.UP:
        x = 1
    elif move==TileProperty.Direction.DOWN:
        x = -1
    elif move==TileProperty.Direction.RIGHT:
        y = -1
    elif move==TileProperty.Direction.LEFT:
        y = 1
    else:
        return 
    
    movex = desx-x
    movey = desy-y
    baseSurf = DISPLAYSURF.copy()
    blanktop, blankleft = getLeftTopOfTile(movex, movey, offset)
    pygame.draw.rect(baseSurf, BoardProperty.BGCOLOR, (blanktop, blankleft, BoardProperty.TILESIZE, BoardProperty.TILESIZE))
    
    for i in range(0,BoardProperty.TILESIZE+1, BoardProperty.ANIMATIONSPEED):
        DISPLAYSURF.blit(baseSurf, (0,0))
        drawTile(movex, movey, board[movex][movey], offset, x*i, y*i)
        pygame.display.update()
        FPSCLOCK.tick(BoardProperty.FPS)
    
    board[desx][desy], board[movex][movey] = board[movex][movey], board[desx][desy]
    

def animation(board, solutionSequence, offset):
    for move in solutionSequence:
        if isValidMove(board, move):
            slideAnimation(board, move, offset)

            


def terminate():
    pygame.quit()
    sys.exit()


if __name__=='__main__':
   main()
