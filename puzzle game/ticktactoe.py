__author__ = 'uSER'

import pygame
import time

WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )
RED   = (255,0  ,0  )
BLUE  = (0  ,0  ,255)
GREEN = (0  ,255,0  )
YELLOW= (255,255,0  )

COLOR1 = GREEN
COLOR2 = RED
SCREENWIDTH = 600
SCREENHEIGHT= 400
SCREENSIZE  = (SCREENWIDTH,SCREENHEIGHT)
BOARDROW    = 3
BOARDCOLUMN = 3
TILESIZE    = 80
BUTTONSIZE  = 50
NUMBERTOWIN = 3


BLANK='.'
X ='x'
O ='o'
GAP = 10
FPS = 30
clock = pygame.time.Clock()

XMARGIN = int((SCREENWIDTH - BOARDCOLUMN*(TILESIZE+GAP))/2)
YMARGIN = int((SCREENHEIGHT- BOARDROW*   (TILESIZE+GAP))/2)

assert (SCREENHEIGHT > BOARDROW*(TILESIZE+GAP)  and SCREENWIDTH > BOARDCOLUMN*(TILESIZE+GAP)+BUTTONSIZE ),'screen is not big enough'
assert (XMARGIN > 0 and YMARGIN > 0),'screen too small'

def main():
    pygame.init()
    # try:
    #     music = pygame.mixer.music
    #     music.load('TobuCloudNCS.mp3')
    #     music.play(-1,20.0)
    # except:
    #     print("could not find TobuCloudNCS.mp3")

    Run_Game()
    music.stop()
    terminate()


def Run_Game():

    screen    = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Tick tac toe')
    background= pygame.Surface(SCREENSIZE)
    background.fill(BLACK)
    board = Generate_New_Board()

    screen.blit(background,(0,0))
    Draw_Board(screen,board)


    game_exit = False
    player1=True
    player2=False
    game_over=False
    Show_Status(screen,player1)
    moves=[]
    while not game_exit:
        # mousex,mousey,click = Get_Mouse_Pos()
        click=False
        clock.tick(FPS)
        screen.blit(background,(0,0))
        Draw_Board(screen,board)

       # Check_Win(screen,board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                click= True
                mousex,mousey = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Move_Back(board,moves)
                if event.key == pygame.K_ESCAPE:
                    return

        tile_row,tile_column= Convert_To_Tile(mousex,mousey)
        if tile_row!= None and tile_column!= None:

            if player1==True:
                if not click:
                    Draw_Hightlight(screen,tile_row,tile_column,COLOR1)
                if click:
                    #check: if the  move is already there.
                    check= [tile_row,tile_column] in moves
                    if not check:
                        board[tile_row][tile_column]='x'
                        moves.append([tile_row,tile_column])
                        player1=False
                        player2=True


            if player2==True:
                 if not click:
                    Draw_Hightlight(screen,tile_row,tile_column,COLOR2)
                 if click:
                    check= [tile_row,tile_column] in moves
                    if not check:
                        board[tile_row][tile_column]='o'
                        moves.append([tile_row,tile_column])
                        player1=True
                        player2=False
        game_over = Check_Win(screen,board)
        if game_over:
            Show_Message(screen,'Congratulation')

        Show_Status(screen,player1)

        pygame.display.update()

def Check_Win(screen,board):
    win = False
    for row in range(BOARDROW):
        for column in range(BOARDCOLUMN):
            if board[row][column]==BLANK:
                continue
            elif board[row][column]=='x' or board[row][column]=='o':
                #check row
                if board[row][column:column+NUMBERTOWIN]==NUMBERTOWIN*[board[row][column]]:
                    win=True
                    left,top= Convert_To_Pixel(row,column)
                    pygame.draw.rect(screen,YELLOW,(left,top+TILESIZE/2,NUMBERTOWIN*(TILESIZE+GAP),GAP))
                #check column
                check_column=False
                first_row = board[row][column]
                for i in range(NUMBERTOWIN):
                    if BOARDROW - row < NUMBERTOWIN:
                        break
                    if first_row==board[row+i][column]:
                        check_column=True
                    else:
                        check_column=False
                        break
                if check_column:
                    win=True
                    left,top=Convert_To_Pixel(row,column)
                    pygame.draw.rect(screen,YELLOW,(left+TILESIZE/2,top,GAP,NUMBERTOWIN*(TILESIZE+GAP)))
                #check diagonal
                check_diagonal_left=False
                first_diagonal = board[row][column]
                for i in range(NUMBERTOWIN):
                    if BOARDROW - row < NUMBERTOWIN or BOARDCOLUMN - column < NUMBERTOWIN:
                        break
                    if first_diagonal == board[row+i][column+i]:
                        check_diagonal_left= True
                    else:
                        check_diagonal_left=False
                        break
                if check_diagonal_left:
                    win=True
                    left,top=Convert_To_Pixel(row,column)
                    width = NUMBERTOWIN*(TILESIZE+GAP)
                    pygame.draw.line(screen,YELLOW,(left,top),(left+width,top+width),GAP)
                #check diagonal right:
                check_diagonal_right=False
                first_diagonal=board[row][column]
                for i in range(NUMBERTOWIN):
                    if row + 1< NUMBERTOWIN or BOARDCOLUMN-column< NUMBERTOWIN:
                        break
                    if first_diagonal == board[row-i][column+i]:
                        check_diagonal_right=True
                    else:
                        check_diagonal_right=False
                        break
                if check_diagonal_right:
                    win=True
                    left,top=Convert_To_Pixel(row+1,column)
                    width = NUMBERTOWIN*(TILESIZE+GAP)
                    pygame.draw.line(screen,YELLOW,(left,top),(left+width,top-width),GAP)
    return win







def terminate():
    pygame.quit()
    quit()

def Generate_New_Board():
    board = []
    for row in range(BOARDROW):
        column = []
        for columns in range(BOARDCOLUMN):
            column.append('.')
        board.append(column)

    return board


def Convert_To_Pixel(row,column):
    pixelx= XMARGIN + column*(TILESIZE+GAP)
    pixely= YMARGIN + row*(TILESIZE+GAP)
    return pixelx,pixely

def Convert_To_Tile(x,y):
    for row in range(BOARDROW):
        for column in range(BOARDCOLUMN):
            top,left = Convert_To_Pixel(row,column)
            tile = pygame.Rect(top,left,TILESIZE,TILESIZE)
            if tile.collidepoint(x,y):
                return row,column
    return None,None

def Draw_Board(screen,board):
    #draw grid
    row = 0
    for column in range(BOARDCOLUMN):
        if column == 0:
            continue
        left,top = Convert_To_Pixel(row,column)
        pygame.draw.rect(screen,BLUE,(left-GAP,top,GAP,BOARDROW*(TILESIZE+GAP)))

    column = 0
    for row in range(BOARDROW):
        if row == 0:
            continue
        left,top = Convert_To_Pixel(row,column)
        pygame.draw.rect(screen,BLUE,(left,top-GAP,BOARDCOLUMN*(TILESIZE+GAP),GAP))

    for row in range(BOARDROW):
        for column in range(BOARDCOLUMN):
            if board[row][column]==BLANK:
                continue
            if board[row][column]=='x':
                Draw_x(screen,row,column)
            if board[row][column]=='o':
                Draw_o(screen,row,column)

def Draw_Hightlight(screen,row,column,color):
    left,top= Convert_To_Pixel(row,column)
    pygame.draw.rect(screen,color,(left,top,TILESIZE,TILESIZE),GAP)

def Draw_x(screen,row,column):
    left,top = Convert_To_Pixel(row,column)
    pygame.draw.line(screen,GREEN,(left,top),(left+TILESIZE,top+TILESIZE),GAP)
    pygame.draw.line(screen,GREEN,(left+TILESIZE,top),(left,top+TILESIZE),GAP)

def Draw_o(screen,row,column):
    left,top= Convert_To_Pixel(row,column)
    center = int(left+TILESIZE/2),int(top+TILESIZE/2)
    radius = int(TILESIZE/2)
    pygame.draw.circle(screen,GREEN,center,radius,GAP)


def Move_Back(board,moves):
    if len(moves) >= 1:
        last_row = moves[-1][0]
        last_column = moves[-1][1]
        del moves[-1]
        board[last_row][last_column]='.'


def Make_Text(msg,color,size='small'):

    smallfont = pygame.font.SysFont(None,20)
    medfont   = pygame.font.SysFont(None,40)
    bigfont   = pygame.font.SysFont(None,60)
    if size == 'small':
        font = smallfont
    elif size=='medium':
        font = medfont
    elif size == 'big':
        font = bigfont

    text =font.render(msg,True,color)
    text_rect= text.get_rect()
    return text,text_rect

def Show_Status(screen,player):
    if player:
        p = '1'
    else:
        p = '2'
    text,text_rect= Make_Text('Player:'+p,YELLOW,size='medium')
    text_rect.center= int(SCREENWIDTH-XMARGIN/2),int(YMARGIN)
    screen.blit(text,text_rect)

def Show_Message(screen,msg,color=RED,size='big'):
    text,text_rect=Make_Text(msg,color,size)
    text_rect.center=int(SCREENWIDTH/2),int(SCREENHEIGHT/2)
    screen.blit(text,text_rect)
    #take input from player
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            terminate()






if __name__=='__main__':
    main()








