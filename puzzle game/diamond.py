__author__ = 'uSER'
import pygame,random,sys

SCREENWIDTH  = 700
SCREENHEIGHT = 500
SCREENSIZE   = (700,500)
BOXSIZE      = 50
BOARDCOLUMNS= 7
BOARDROWS    = 8
GAP          = 10
REVEALSPEED  = 2
FPS          = 30

WHITE     = (255,255,255)
BLACK     = (0  ,0  ,  0)
BLUE      = (12 ,2  ,180)
RED       = (200,0  ,0  )
GREEN     = (0  ,220,0  )
YELLOW    = (180,180,0  )
ORANGE    = (255,128,9  )
LIGHTBLUE = (0  ,255,255)
GREEN2    = (128,128,0  )
PINK      = (255,0  ,255)

BGCOLOR   = BLACK
BOXCOVER = WHITE
HIGHTLIGHT= LIGHTBLUE
clock = pygame.time.Clock()

DONUT   = 'donut'
DIAMOND = 'diamond'
LINES   = 'lines'
CIRCLE  = 'cirle'
PYRAMID = 'pyramid'

ALLCOLOR = (BLUE,RED,GREEN,YELLOW,ORANGE,PINK,WHITE)
ALLSHAPE= (DONUT,DIAMOND,LINES,CIRCLE,PYRAMID)

XMARGIN = (SCREENWIDTH -  (BOARDCOLUMNS*(BOXSIZE+GAP))) /2
YMARGIN = (SCREENHEIGHT - (BOARDROWS*   (BOXSIZE+GAP))) /2

assert (((BOARDCOLUMNS*BOARDROWS)%2) == 0),'number of box has to be even'
assert (XMARGIN > 0 and YMARGIN > 0),'screen is not big enough'
assert (len(ALLCOLOR)*len(ALLSHAPE)*2 <= SCREENHEIGHT*SCREENWIDTH),'the screen is not big enough'
assert (len(ALLCOLOR)*len(ALLSHAPE)*2 >= BOARDROWS * BOARDCOLUMNS),'there is not enough color or shapes'

def main():
    #start animation
    #main_game
        #player: move mouse
               #if he not click: highlight the box
               #if he click:
                    #check if that is 1st selection
                       #if yes, open that box
                       #if no, check if no1 and no2 match
                            #if no, wait 1 second, close both
                            #if yes, check if game is over
                                #if no, continue
                                #if yes, change map, set everything box convered
                       #set no1 selection: None


    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Diamond')

    background = pygame.Surface(SCREENSIZE)
    background.fill(BGCOLOR)
    screen.blit(background,(0,0))

    reveal_box = Generate_Reveal_Box(False) #set all box unrevealed, this will return the list,
                                            #comprised of state of all box: whether False or True
    board = Generate_New_Board()#this function returns shape,color,x,y of the box
    Draw_Board(screen,board,reveal_box)

    first_selection = None

    BACKMUSIC    = pygame.mixer.music
    BACKMUSIC.load('Different.HeavenNCS.mp3')
    BACKMUSIC.set_volume(0.5)
    BACKMUSIC.play(-1,5.0)
    Animation_Start(screen,board)
    game_exit = False
    while not game_exit:
        mouse_clicked = False
        box_x,box_y = None,None
        clock.tick(FPS)
        screen.blit(background,(0,0))
        Draw_Board(screen,board,reveal_box)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.MOUSEMOTION:
                mouse_x,mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked   = True
                mouse_x,mouse_y = event.pos

        box_x,box_y = Get_Box(mouse_x,mouse_y)
        if box_x != None and box_y != None:
            if not mouse_clicked:
                Highlight_Box(screen,box_x,box_y)
            if not reveal_box[box_x][box_y] and mouse_clicked:
                Animation_Reveal(screen,board,[(box_x,box_y)])
                reveal_box[box_x][box_y] = True #mean that: after the while
                                        #loop, that box will be True
                if first_selection == None:
                    first_selection = (box_x,box_y)
                else:
                    icon1shape,icon1color = Get_Shapecolor(board,first_selection[0],first_selection[1])
                    icon2shape,icon2color = Get_Shapecolor(board,box_x,box_y)
                    if icon1color != icon2color or icon1shape != icon2shape:
                        pygame.time.wait(1*1000)
                        Animation_Cover(screen,board,[(first_selection[0],first_selection[1]),(box_x,box_y)])
                        reveal_box[first_selection[0]][first_selection[1]] = False
                        reveal_box[box_x][box_y] = False
                    #check if game is over
                    else:
                        if Level_Over(board,reveal_box):
                            pygame.time.wait(5*1000)
                            board = Generate_New_Board()
                            reveal_box = Generate_Reveal_Box(False)
                            Draw_Board(screen,board,reveal_box)
                            Animation_Start(screen,board)

                    first_selection = None





        pygame.display.update()



def Generate_Reveal_Box(val):
    reveal_boxs = []
    for i in range(BOARDROWS):
        column =  [val]*BOARDCOLUMNS
        reveal_boxs.append(column)
    return reveal_boxs

def Generate_New_Board():

    icons = []
    for shape in ALLSHAPE:
        for color in ALLCOLOR:
            icons.append((shape,color))

    random.shuffle(icons)
    no_icons_use = int(BOARDCOLUMNS*BOARDROWS/2)
    icons_use = icons[:no_icons_use] * 2 #to get pair of every color
    random.shuffle(icons_use)

    board = []
    for row in range(BOARDROWS):
        column= []
        for item in range(BOARDCOLUMNS):
            column.append(icons_use[0])
            del icons_use[0]
        board.append(column)
    return board

def Draw_Board(screen,board,reveal_box):
    for row in range(BOARDROWS):
        for column in range(BOARDCOLUMNS):
            x,y = Get_Topleft(row,column)
            shape,color = Get_Shapecolor(board,row,column)
            if not reveal_box[row][column]:#check if the box is covered or not
                pygame.draw.rect(screen,BOXCOVER,(x,y,BOXSIZE,BOXSIZE))
            else:
                surface = pygame.Surface((BOXSIZE,BOXSIZE))
                Draw_Icon(surface,shape,color)
                screen.blit(surface,(x,y))


def Get_Topleft(row,column):
    x = XMARGIN + (BOXSIZE+GAP)*column
    y = YMARGIN + (BOXSIZE+GAP)*row
    return x,y
def Get_Shapecolor(board,row,column):
    shape = board[row][column][0]
    color = board[row][column][1]
    return shape,color
def Draw_Icon(surface,shape,color):
    #draw icon on surface 50x50
    center = (int(BOXSIZE/2),int(BOXSIZE/2))
    quarter      = int(BOXSIZE/4)
    mid          = int(BOXSIZE/2)
    topleft      = (0,0)
    downright    = (BOXSIZE,BOXSIZE)
    downleft     = (0,BOXSIZE)
    diamond_point=[(0,mid),
                   (BOXSIZE,mid),
                   (mid,0),
                   (mid,BOXSIZE)
                   ]
    pyramid_point=[(mid,0),
                   downleft,
                   downright
                  ]


    if shape == DONUT:
        pygame.draw.circle(surface,BGCOLOR,center,int(BOXSIZE/5))
        pygame.draw.circle(surface,color  ,center,int(2*BOXSIZE/5),int(BOXSIZE/5))
    elif shape == DIAMOND:
        pygame.draw.polygon(surface,color,diamond_point)
    elif shape == LINES:
        pygame.draw.rect(surface,color,(0,0,BOXSIZE,BOXSIZE),2)
        for i in range(0,BOXSIZE,4):
            pygame.draw.aaline(surface,color,(i,0),(BOXSIZE,i))
            pygame.draw.aaline(surface,color,(0,i),(i,BOXSIZE))
    elif shape == CIRCLE:
        pygame.draw.circle(surface,color,center,int(BOXSIZE/5))
    elif shape == PYRAMID:
        pygame.draw.polygon(surface,color,pyramid_point)

def Get_Box(x,y):
    for row in range(BOARDROWS):
        for column in range(BOARDCOLUMNS):
            left,top = Get_Topleft(row,column)
            boxrect= pygame.Rect(left,top,BOXSIZE,BOXSIZE)

            if boxrect.collidepoint(x,y):
                return (row,column)
    return (None,None)

def Highlight_Box(screen,row,column):
    left,top = Get_Topleft(row,column)
    halfgap = int(GAP/2)
    pygame.draw.rect(screen,HIGHTLIGHT,(left-halfgap,top-halfgap,BOXSIZE+halfgap,BOXSIZE+halfgap),GAP)

def Animation_Reveal(screen,board,boxes):
    for coverage in range(BOXSIZE,(-REVEALSPEED)-1,-REVEALSPEED):
        Draw_Box_Cover(screen,board,boxes,coverage)

def Animation_Cover(screen,board,boxes):
    for coverage in range(-REVEALSPEED-1,BOXSIZE,REVEALSPEED):
        Draw_Box_Cover(screen,board,boxes,coverage)

def Draw_Box_Cover(screen,board,boxes,coverage):
    #draw Rect ==> Icon ==> Coverage
    #keep everything else still, go to pos of the box, draw the box again many times
    for box in boxes:
        left,top= Get_Topleft(box[0],box[1])
        pygame.draw.rect(screen,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        shape,color= Get_Shapecolor(board,box[0],box[1])
        surf = pygame.Surface((BOXSIZE,BOXSIZE))
        Draw_Icon(surf,shape,color)
        screen.blit(surf,(left,top))
        if coverage > 0:
            pygame.draw.rect(screen,BOXCOVER,(left,top,coverage,BOXSIZE))
    pygame.display.update()
    clock.tick(FPS)

def Animation_Start(screen,board):
    #reveal all boxes in short time at the game begin
    reveal_box = Generate_Reveal_Box(False)
    boxes = []
    for row in range(BOARDROWS):
        for column in range(BOARDCOLUMNS):
            boxes.append((row,column))
    random.shuffle(boxes)
    boxgroup = Split_Into_Group(boxes,8)
    Draw_Board(screen,board,reveal_box)
    for group in boxgroup:
        Animation_Reveal(screen,board,group)
        Animation_Cover(screen,board,group)

def Split_Into_Group(boxes,size):
    old_group = boxes
    new_group = []
    number_of_group = int((len(boxes))/size)
    for j in range(number_of_group):
        small_group = []
        for i in range(size):
            small_group.append(old_group[0])
            del old_group[0]
        new_group.append(small_group)
    return new_group

def Level_Over(board,reveal_box):
    for i in reveal_box:
        if False in i:
            return False # return False if any boxes are covered.
    return True














if __name__ == '__main__':
    main()





