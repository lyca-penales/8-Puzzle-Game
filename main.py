import pygame, sys
from pygame.locals import *
from queue import PriorityQueue
from copy import deepcopy
from settings import *
import time
import random

#Setup
pygame.init()
clock = pygame.time.Clock()
pygame.display.init()

#Display Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGCOLOUR)
window_title = pygame.display.set_caption(TITLE)

#Checking if Solved
def check(done, starting_loc, ending_loc):
    flag = 0
    for i in starting_loc:
        if i in ending_loc:
            flag += 1
    if flag >= 8:
        done = True

#Moving a Tile by Clicking
def moving_tile(pos,win):
    global starting_loc, empty_tile

    pressed = False
    for i in range(len(starting_loc)):
        if pos[0]>starting_loc[i][0] and pos[0]<starting_loc[i][0]+80 and pos[1]>starting_loc[i][1] and pos[1]<starting_loc[i][1]+80:
            pressed = True
            break
        
    if pressed:
        if starting_loc[i][0]+w == empty_tile[0] and starting_loc[i][1] == empty_tile[1]:
            temp = starting_loc[i]
            empty_tile[2] = starting_loc[i][2]
            starting_loc[i] = empty_tile
            empty_tile = temp
            empty_tile[2] = 0
        elif starting_loc[i][0] == empty_tile[0] and starting_loc[i][1]+w == empty_tile[1]:
            temp = starting_loc[i]
            empty_tile[2] = starting_loc[i][2]
            starting_loc[i] = empty_tile
            empty_tile = temp
            empty_tile[2] = 0
        elif starting_loc[i][0]-w == empty_tile[0] and starting_loc[i][1] == empty_tile[1]:
            temp = starting_loc[i]
            empty_tile[2] = starting_loc[i][2]
            starting_loc[i] = empty_tile
            empty_tile = temp
            empty_tile[2] = 0
        elif starting_loc[i][0] == empty_tile[0] and starting_loc[i][1]-w == empty_tile[1]:
            temp = starting_loc[i]
            empty_tile[2] = starting_loc[i][2]
            starting_loc[i] = empty_tile
            empty_tile = temp
            empty_tile[2] = 0

#Displaying the Board/Tiles
def board(win, state, empty):
    pygame.draw.rect(win, NAVY, ((empty[0]), (empty[1]), 93, 93))
    for l in state:
        pygame.draw.rect(win, DODGEERBLUE, (l[0], l[1], 93, 93))
        text = FONT1.render(str(l[2]), True, WHITE)
        win.blit(text, (l[0]+25, l[1]+7))

#Displaying the Grid
def grid(win):
    for row in range(4):
        pygame.draw.line(win, (255, 255, 255), (x-50, row*95+y-2), (x+330, row*95+y-2), 2)
    for col in range(4):
        pygame.draw.line(win, (255, 255, 255), (col*95+98, y-48), (col*95+98,y+330), 2)
    
#Displaying the Texts
def texts(win):
    title = pygame.image.load('Static/game_title.png').convert_alpha()
    game_title = pygame.transform.scale(title, (x+135, y))
    solve = FONT2.render("SOLVE BY:", True, WHITE)
    solution = FONT2.render("SOLUTION:", True, WHITE)
    win.blit(game_title, (505, 45))
    win.blit(solve, (535, 280))
    win.blit(solution, (50, 471))
    
# To Make buttons
class Button():
    def __init__(self, x,y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()  [0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

#Buttons
shuffle_image = pygame.image.load('Static/shuffle.png').convert_alpha()
shuffle = pygame.transform.scale(shuffle_image, (120, 30))
shuffle_button = Button(533, 190, shuffle, 1.5)

bfs_image = pygame.image.load('Static/bfs.png').convert_alpha()
bfs = pygame.transform.scale(bfs_image, (100, 40))
bfs_button = Button(500, 340, bfs, 1)

astar_image = pygame.image.load('Static/astar.png').convert_alpha()
astar = pygame.transform.scale(astar_image, (100, 40))
astar_button = Button(640, 340, astar, 1)


# shuffle pieces
def shuffle():
    global starting_loc, empty_tile, solved
    solved = False
    #pygame.draw.rect(win, (0,0,0), (0, 493, 480, 31))
    visited = []
    a = modif()

    visited.append(a)

    while len(visited) < 11:
        move = []
        b = move_list(visited[-1])
        i = random.randint(0, len(b)-1)
        move.append(b[i])

        c = move_tile(visited[-1], move)
        c[0].sort()

        if c[0] not in visited:
            for i in c[0]:
                if i[2] == 0:
                    temp = deepcopy(c[0])
                    empty_tile = temp.pop(temp.index(i))
                    starting_loc = temp
                    break
            visited.append(c[0])

#*************************START OF THE BFS SEARCH*************************#    
def move_list(start):
    global starting_loc
    global ending_loc
    global empty_tile
    global x, y, w

    s = deepcopy(start)
    move_list = []
    
    for i in range(len(s)):
        if s[i][2] == 0:
            if s[i][0] < (x+w*2):
                if "R" not in move_list:
                    move_list.append("R")
            if s[i][1] < (y+w*2):
                if "D" not in move_list:
                    move_list.append("D")
            if s[i][1] > y:
                if "U" not in move_list:
                    move_list.append("U")
            if s[i][0] > x:
                if "L" not in move_list:
                    move_list.append("L")
    return move_list
    
def move_tile(current_loc, movlist):
    result = []
    temp = deepcopy(current_loc)
    for i in temp:
        if i[2] == 0:
            empty = temp.index(i)
    for j in movlist:
        if j == 'R':
            temp[empty][2], temp[empty+3][2] = temp[empty+3][2], temp[empty][2]
        elif j == 'D':
            temp[empty][2], temp[empty+1][2] = temp[empty+1][2], temp[empty][2]
        elif j == 'L':
            temp[empty][2], temp[empty-3][2] = temp[empty-3][2], temp[empty][2]
        elif j == 'U':
            temp[empty][2], temp[empty-1][2] = temp[empty-1][2], temp[empty][2]
        result.append(temp) 
        temp = deepcopy(current_loc) 
    return result

def modif():
    global starting_loc
    global empty_tile
    curloc = deepcopy(starting_loc)
    emloc = deepcopy(empty_tile)
    curloc.append(emloc)
    curloc.sort()
    return curloc

def backtrace(start, level, end, count):
    path = [end]
    for i in range(count-1, -1, -1):
        if end in level[i] and level[i][0] != start:
            path.append(level[i][0])
            end = level[i][0]
    path.append(start)
    path.reverse()
    return path

def bfs(start):
    global ending_loc
    print("Currently doing Breadth-First search algorithm... ")

    solved = deepcopy(ending_loc)
    solved.append([x+w*0, y+w*0, 0])
    solved.sort()

    
    visited = []
    level = {0:[start]}
    queue =[]
    count = 1

    
    queue.append(start)

    
    while queue:
        path = queue.pop(0)  
        if path == solved:
            return backtrace(start, level, solved, count)

        elif path not in visited:
            s = move_list(path)
            t = move_tile(path, s)
            level[count] = [path]
            for adjacent in t:
                if adjacent not in visited:
                        
                    level[count].append(adjacent)
                    queue.append(adjacent)
            count+=1
        visited.append(path)

#*************************END OF THE BFS SEARCH*************************# 

#*************************START OF THE A* SEARCH*************************# 
class Astarframework:
    goal_state=[0,1,2,3,4,5,6,7,8]
    heuristic=None
    evaluation_function=None
    needs_hueristic=True
    num_of_instances=0

    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.manhattan_distance()
            self.evaluation_function=self.heuristic+self.path_cost
        Astarframework.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def manhattan_distance(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def ifsolved(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j, prev_action=''):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0 or prev_action == 'D':  # up is disable
            legal_action.remove('U')
        if i == 2 or prev_action == 'U':  # down is disable
            legal_action.remove('D')
        if j == 0 or prev_action == 'R': # left is disable
            legal_action.remove('L')
        if j == 2 or prev_action == 'L': # right is disable
            legal_action.remove('R')
        return legal_action

    @staticmethod
    def find_blank_pos(arr):
        x = arr.index(0)
        i = int(x / 3)
        j = int(x % 3)
        return i,j,x

    def generate_child(self):
        children = []
        i,j,x = Astarframework.find_blank_pos(self.state)
        legal_actions = Astarframework.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Astarframework(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        global sol
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        sol = solution
        return 

def astar_search(initial_state):
    print("Currently doing A * search algorithm...")
    count=0
    explored=[]
    start_node=Astarframework(initial_state,None,None,0,True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function,count,start_node))

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.ifsolved():
            return node.find_solution()

        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                q.put((child.evaluation_function,count,child))
    return

def move_to(current_loc, move):
    temp = deepcopy(current_loc)
    for i in temp:
        if i[2] == 0:
            empty = temp.index(i)
    if move == 'R':
        temp[empty][2], temp[empty+3][2] = temp[empty+3][2], temp[empty][2]
    elif move == 'D':
        temp[empty][2], temp[empty+1][2] = temp[empty+1][2], temp[empty][2]
    elif move == 'L':
        temp[empty][2], temp[empty-3][2] = temp[empty-3][2], temp[empty][2]
    elif move == 'U':
        temp[empty][2], temp[empty-1][2] = temp[empty-1][2], temp[empty][2]
    return temp
    

sol = []

def convert(current_loc):
    place = []
    for i in current_loc:
        place.append(i[2])
    return place

def takeSecond(elem): 
    return elem[1]

def convert2(sol, start):
    global asol2
    temp = deepcopy(start)
    count = 0
    result= [temp]
    for i in sol:
        x = move_to(result[count], i)
        #print("this is the x: "+ str(x))
        s = deepcopy(x)
        result.append(s)
        count +=1
    return result

def a_star(start):
    global sol
    hold = deepcopy(start)
    hold.sort(key=takeSecond)
    x = convert(hold)
    astar_search(x)

    z = convert2(sol, start)

    return z
#*************************END OF A* SEARCH*************************# 

# get solution 
def solution(s):
    sol = []
    for i in range(0,len(s)):
        a = move_list(s[i])
        for j in a:
            b = move_tile(s[i], j)
            b[0].sort()
            s[i].sort()
            try:
                if b[0] == s[i+1]:
                    sol.append(j)
                    break
            except:
                pass
    return sol

# display solution to screen
def dispSol(win, sol):
    pygame.draw.rect(win, BLACK, (50, 525, 700, 60))
    this = ' '.join(sol)

    solution = FONT3.render(this, True, AQUA)
    win.blit(solution, (70, 543))

# main           
def game(animating, value):
    global starting_loc, empty_tile, solved
    
    game = True
    while game:
        clock.tick(60)
        for event in pygame.event.get():
            if bfs_button.draw():
                if solved == False:
                    start = modif()
                    start2 = time.time()
                    s = bfs(start)
                    end = time.time()
                    print("Solution Found in " + str(end - start2) +" seconds!")
                    g = solution(s)
                    dispSol(screen, g)
                    solved = True
                else:
                    if animating == False:
                        animating = True
                        game = False
                        solve(animating, value, s)
                    else:
                        animating = False
            if astar_button.draw():
                if solved == False:
                    start = modif()
                    start2 = time.time()
                    s = a_star(start)
                    end = time.time()
                    print("Solution Found in " + str(end - start2) +" seconds!")
                    g = solution(s)
                    dispSol(screen, g)
                    solved = True
                else:
                    if animating == False:
                        animating = True
                        game = False
                        solve(animating, value, s)
                    else:
                        animating = False
            if shuffle_button.draw():
                shuffle()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #solved = False
                pos1 = pygame.mouse.get_pos()
                moving_tile(pos1, screen)
                if pos1[0] > 75 and pos1[0] < 375 and pos1[1] > 135 and pos1[1] < 405:
                    solved = False
                board(screen, starting_loc, empty_tile)

        pygame.display.flip()
        board(screen, starting_loc, empty_tile)

# solving        
def solve(animating, value, moves):
    global starting_loc, empty_tile, solved
    solve = True
    while solve:
        clock.tick(5)
        if value >= len(moves):
            value = 0
            animating = False
            solve = False
            solved = False
            game(animating, value)
            
        try:
            move = moves[value]
        except:
            pass

        if animating == True:
            for i in move:
                if i[2] == 0:
                    temp = deepcopy(move)
                    empty_tile = temp.pop(temp.index(i))
                    starting_loc = temp
                    break
        pygame.display.flip()
        board(screen, starting_loc, empty_tile)
        #screen.fill((0,0,0))

        if animating == True:
            value += 1
    screen.fill((0,0,0))

#Display the Grids
grid(screen)

#Display the Texts 
texts(screen)

#Run the Game   
game(animating, value)

    