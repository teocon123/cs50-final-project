import pygame
import random

pygame.init()
width = 12
height = 18
cell = 30
screen = pygame.display.set_mode((width * cell, height * cell))
title = pygame.display.set_caption(title = 'Tetrix')
clock = pygame.time.Clock()
running = True
class Grid:
    def __init__(self, width, height, cell):
        self.width = width
        self.height = height
        self.cell = cell
        self.grid = [[0 for i in range(self.width)] for j in range(self.height)]
        self.color = self.get_color()
        
    def get_color(self):
        dark_grey = (26, 31, 40)
        green = (47, 230, 23)
        red = (232, 18, 18)
        orange = (226, 116, 17)
        yellow = (237, 234, 4)
        purple = (166, 0, 247)
        cyan = (21, 204, 209)
        blue = (13, 64, 216)
        chocolate = (210, 105, 30)
        return [dark_grey, green, red, orange, yellow, purple, cyan, blue, chocolate]
    
    def draw(self, screen):
        for j in range(self.height):
            if j == 0:
                for i in range(self.width):
                    gr = pygame.Rect(self.cell*i,self.cell*j, self.cell, self.cell)
                    pygame.draw.rect(screen, self.color[8], gr)
            else:
                for i in range(self.width):
                    gr = pygame.Rect(self.cell*i + 1,self.cell*j + 1, self.cell - 1, self.cell - 1)
                    pygame.draw.rect(screen, self.color[self.grid[j][i]] , gr)
 
def tetromino(current):
    global num, x, y
    x, y = 0 , 0    
    current.clear()
    num = random.randint(1,7)
    if num == 1:
        block = [[-1,4],[-1,5],[-1,6],[-1,7]] # I
    elif num == 2:
        block = [[-1,4],[-2,5],[-1,5],[-2,6]] # S
    elif num == 3:
        block = [[-1,4],[-1,6],[-1,5],[-2,4]] # J
    elif num == 4:
        block = [[-1,5],[-2,4],[-2,5],[-2,6]] # T
    elif num == 5:
        block = [[-2,4],[-2,5],[-1,5],[-1,6]] # Z
    elif num == 6:
        block = [[-1,5],[-1,6],[-2,5],[-2,6]] # O
    elif num == 7:
        block = [[-1,4],[-1,6],[-1,5],[-2,6]] # L
    for i in range(4):
        current.append(block[i])    
            
def rorate():
    denta_x = current[2][1]; denta_y = current[2][0]
    for i in range(4):
        current[i][0] -= denta_y
        current[i][1] -= denta_x
        t = current[i][0]
        current[i][0] = current[i][1] + denta_y
        current[i][1] = -t + denta_x
        
def move_down():
    global y
    y+=1
    
def min_xxx():
    global min_x,x
    min_x = current[0][1]
    for i in current:
        if i[1] < min_x:
            min_x = i[1]
    
def max_xxx():
    global max_x, x
    max_x = current[0][1]
    for i in current:
        if i[1] > max_x:
            max_x = i[1]
   
def max_yyy():
    global max_y, y
    max_y = current[0][0]
    for i in current:
        if i[0] > max_y:
            max_y = i[0] 

def clear_row():
    global score
    row_to_remove = [i for i, row in enumerate(grid.grid) if all(row)] # if all elements in row are non-zero, return True
    for row in row_to_remove:
        del grid.grid[row]
        grid.grid.insert(1 ,[0 for i in range(width)])
        score+=1
                    
def value(y, x):
    for i in current:
        if i[0] + y == 0:
            grid.grid[i[0] + y][i[1] + x] == 8
        else:
            grid.grid[i[0] + y][i[1] + x] = num
             
def check_collision():
    global x, y, running
    if max_y + y == height - 1:
        return True
    if max_y + y >= height:
        y-=1
        return True
    for i in current:
        if max_y + y == 1:
            if grid.grid[1][i[1]+x] in color:
                font = pygame.font.SysFont('Times New Roman', 40, bold=True)
                text = font.render("Game over", 1, (255,255,255))
                screen.blit(text, (3*cell, 6*cell))
                tt_scores(score)
                pygame.display.update()
                pygame.time.delay(1500)
                running = False
                y=-1
        if 0 < i[0] + y < height-1:
            if grid.grid[i[0] + y + 1][i[1]+x] in color:
                return True                
    return False

def tt_scores(score):
    total_score = pygame.font.SysFont('Times New Roman', 20, bold=True).render("Score:" + str(score), 1, (255,255,255))
    screen.blit(total_score, (5*cell,0))
    
game_update = pygame.USEREVENT
pygame.time.set_timer(game_update, 500)
grid = Grid(width, height, cell)
current, color = [], [1,2,3,4,5,6,7]
num, x, y, score = 0,0,0,0
tetromino(current)
min_x, max_x, max_y = 0, 0, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                min_xxx()
                if min_x + x > 0:
                    x-=1
            if event.key == pygame.K_RIGHT:
                max_xxx()
                if max_x + x < width - 1:                
                    x+=1
            if event.key == pygame.K_DOWN:
                max_yyy()
                if max_y + y < height - 1:
                    y+=1
            if event.key == pygame.K_UP:              
                rorate()
                min_xxx()
                #Limit the left boundary when rotating
                if min_x + x == -1:
                    x+=1
                if min_x + x == -2:
                    x+=2
                #limit the right boundary when rotating
                max_xxx()
                if max_x + x == width:
                    x-=1
                if max_x + x == width + 1:
                    x-=2
                max_yyy()
        if event.type == game_update:
            move_down()
    screen.fill((0,0,0))
    grid.draw(screen)
    collision = check_collision()
    if collision:
        for i in current:
            if i[0] + y == 0:               
                pygame.draw.rect(screen, grid.color[8], pygame.Rect((i[1]+x)*cell + 1, (i[0]+y)*cell + 1, cell - 1, cell - 1))
            else:        
                pygame.draw.rect(screen, grid.color[num], pygame.Rect((i[1]+x)*cell + 1, (i[0]+y)*cell + 1, cell - 1, cell - 1))
        value(y, x)
        x, y = 0,0
        clear_row()
        tetromino(current)
    else:
        for i in current:
            if i[0] + y == 0:
                pygame.draw.rect(screen, grid.color[8], pygame.Rect((i[1]+x)*cell + 1, (i[0]+y)*cell + 1, cell - 1, cell - 1))
            else:            
                pygame.draw.rect(screen, grid.color[num], pygame.Rect((i[1]+x)*cell + 1, (i[0]+y)*cell + 1, cell - 1, cell - 1)) 
    tt_scores(score)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()