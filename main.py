from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox
import pygame as pg
import numpy as np
from numba import njit
import sys, requests
from quiz import Question, QuizBrain, QuizInterface
from random import shuffle
from buttons import Buttons
import html, math
import pygame_menu



#url_list = ["https://opentdb.com/api.php?amount=10&type=multiple", "https://opentdb.com/api.php?amount=10&category=21","https://opentdb.com/api.php?amount=10&category=9&difficulty=hard"]

pg.init()
pg.font.init()
total_time = pg.time.get_ticks()

bg = pg.image.load('star_bg.png')

parameters = {
"amount" : 10,
"type" : "multiple"
}

response = requests.get(url="https://opentdb.com/api.php?amount=10&category=9&difficulty=hard" , params = parameters)
question_data = response.json()['results']

def quiz_make():
    question_bank = []
    for question in question_data:
        choices = []

        

        question_text = html.unescape(question["question"])
        question_answer = html.unescape(question["correct_answer"])
        wrong_answers = question["incorrect_answers"]
        for ans in wrong_answers:
            choices.append(html.unescape(ans))
        choices.append(question_answer)    
        shuffle(choices)
        new_question = Question(question_text, question_answer, choices)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz)


    while quiz.still_has_questions():
        quiz.next_question()
    global score
    score = quiz.score
    main(screen)
    
screen = pg.display.set_mode((800,600))

def main(screen):
    running = True
    clock = pg.time.Clock()
    #increasing causes lower fps but better graphics, but decreasing does opposite.
    hres = 60 #horizontal res
    halfvres = 50 #half of the vertical res

    mod = hres / 60 # scale factor between 60 degree fov and hres.
    size = 25
    posx, posy, rot, maph, mapc, exitx, exity = gen_map(size)#starting points, rotations, and map generator
    frame = np.random.uniform(0, 1, (hres, halfvres*2, 3))
    sky = pg.image.load('skybox.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres*2)))
    floor = pg.surfarray.array3d(pg.image.load('snow.jpg'))/255
    wall = pg.surfarray.array3d(pg.image.load('wall.jpg'))/255
    # sprites,spsize = get_sprites(hres)
    # enemy_no = size*2
    # enemies = spawn_enemies(enemy_no, maph, size)

    while running:
        
        ticks = pg.time.get_ticks()
        seconds = math.trunc((60000-(ticks - total_time))/1000) + 10*score
        if seconds <= 0:
            running = False

        if int(posx) == exitx and int(posy) == exity:
            running = False
        screen.fill('white')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        frame = new_frame(posx, posy, rot, frame, hres, halfvres, mod, sky, floor, maph, size, wall, mapc, exitx, exity)





                
    ##        if int(x)%2 == int(y)%2:
    ##            frame[i][halfvres*2-j-1] = [0, 0, 0]
    ##        else:
    ##            frame[i][halfvres*2-j-1] = [1, 1, 1]
        
        surf = pg.surfarray.make_surface(frame*255)
        # enemies = sort_sprites(posx, posy, rot, enemies, maph, size)
        # surf = draw_sprites(surf, sprites, enemies, spsize, hres, halfvres, ticks)
        surf = pg.transform.scale(surf, (800, 600))
        
        

        fps = int(clock.get_fps())
        pg.display.set_caption("FPS: " + str(fps) + " Time remaining: " + str(seconds))
        
        screen.blit(surf, (0,0))
        pg.display.update()

        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed(),clock.tick(), maph, score)
        
            
def movement(posx , posy , rot , keys , et, maph, multiplier):
    x,y = posx, posy
    if keys[pg.K_LEFT] or keys[ord('a')]:
        rot -= 0.001 * et * (multiplier+1) /2
    if keys[pg.K_RIGHT] or keys[ord('d')]:
        rot += 0.001 * et * (multiplier+1) / 2
    if keys[pg.K_UP] or keys[ord('w')]:
        x, y = x + np.cos(rot) * 0.001 * et * (multiplier+1)/2 , y + np.sin(rot) * 0.001 * et * (multiplier+1)/2 
    if keys[pg.K_DOWN] or keys[ord('s')]:
        x, y = x -  np.cos(rot) * 0.001 * et * (multiplier+1)/2 , y - np.sin(rot) * 0.001 * et * (multiplier+1)/2
    
    if not(maph[int(x-0.2)][int(y)] or maph[int(x+0.2)][int(y)] or maph[int(x)][int(y-0.2)] or maph[int(x)][int(y+0.2)]):
        posx, posy = x, y
    elif not(maph[int(posx-0.2)][int(y)] or maph[int(posx+0.2)][int(y)] or maph[int(posx)][int(y-0.2)] or maph[int(posx)][int(y+0.2)]):
        posy = y
    elif not(maph[int(x-0.2)][int(posy)] or maph[int(x+0.2)][int(posy)] or maph[int(x)][int(posy-0.2)] or maph[int(x)][int(posy+0.2)]):
        posx = x

    return posx, posy, rot
#the function movement checks the user input and moves the character with correspondence to the button pressed, with reference to the controls of the game.


@njit()
def new_frame(posx, posy, rot, frame, hres, halfvres, mod, sky, floor, maph, size, wall, mapc, exitx, exity):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i/mod-30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod-30)) ##handles rotations, angles in radians
        frame[i][:] = sky[int(np.rad2deg(rot_i)%359)][:]/255
        x, y = posx, posy
        while maph[int(x)%(size-1)][int(y)%(size-1)] == 0:
            x, y = x+0.02*cos, y+0.02*sin
        n = abs((x-posx)/cos)
        h = int(halfvres/(n*cos2 + 0.001))

        xx = int(x*3%1*99)
        if x % 1 < 0.02 or x%1 > 0.98:
            xx = int(y*3%1*99)
        yy = np.linspace(0 , 3, h*2)*99%99
        shade = 0.3 + 0.7*(h/halfvres)
        if shade > 1:
            shade = 1
        ash = 0
        if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
            ash = 1
        if maph[int(x-0.01)%(size-1)][int(y-0.01)%(size-1)]:
            shade, ash = shade*0.5, 0

            
        c = shade* mapc[int(x)%(size-1)][int(y)%(size-1)]           
        for k in range(h*2):
            if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                if ash and 1-k/(2*h) < 1- xx/99:
                    c, ash = 0.5*c, 0
                frame[i][halfvres - h + k] = c*wall[xx][int(yy[k])]
                if halfvres+3*h-k < halfvres*2:
                    frame[i][halfvres+3*h-k] = c*wall[xx][int(yy[k])]
        for j in range(halfvres - h):
            n = (halfvres/(halfvres-j))/cos2#distance from user view to object.
            x, y = posx + cos*n, posy + sin*n #x and y distance of the object
            xx, yy = int(x*2%1*100), int(y*2%1*100)
            shade = 0.2 + 0.8*(1-j/halfvres)
            if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
                shade = shade*0.5
            elif ((maph[int(x-0.33)%(size-1)][int(y)%(size-1)] and y%1>x%1) or  (maph[int(x)%(size-1)][int(y-0.33)%(size-1)] and x%1>y%1)):
                shade = shade*0.5
                        
            frame[i][halfvres * 2-j-1] = shade*(floor[xx][yy] + frame[i][halfvres*2-j-1])/2
            if int(x) == exitx and int(y) ==  exity and (x%1-0.5)**2 + (y%1-0.5)**2 < 0.2:
                ee = j/(10* halfvres)
                frame[i][j:2*halfvres-j] = (ee*np.ones(3) * frame[i][j:2*halfvres-j])/1+ee

    return frame
# @njit()   
# def sort_sprites(posx, posy, rot, enemies, maph, size):
#     for en in range(len(enemies)):
#         enx , eny = enemies[en][0], enemies[en][1]
#         angle = np.arctan((eny-posy)/(enx-posx))
#         if abs(posx+np.cos(angle)-enx) > abs(posx-enx):
#             angle = (angle - np.pi)%(2*np.pi)
#         angle2 = (rot-angle)%(2*np.pi)
#         if angle2 < 10.5*np.pi/6 or angle2 < 1.5*np.pi/6:
#             dir2p = ((enemies[en][6] - angle - 3*np.pi/4)%(2*np.pi))/(np.pi/2)
#             enemies[en][2] = angle2
#             enemies[en][7] = dir2p
#             enemies[en][3] = 1/np.sqrt((enx-posx)**2 + (eny-posy)**2+1e-16)
#             cos, sin = (posx-enx) * enemies[en][3], (posy-eny) *enemies[en][3]
#             x,y = enx, eny
#             for i in range(int((1/enemies[en][3])/0.05)):
#                 x, y = x+0.05*cos, y+0.05*sin
#                 if (maph[int(x-0.02*cos)%(size-1)][int(y)%(size-1)] or maph[int(x)%(size-1)][int(y-0.02*sin)%(size-1)]):
#                     enemies[en][3] = 9999
#                     break
#         else:
#             enemies[en][3] = 9999
#     enemies = enemies[enemies[:,3].argsort()]
#     return enemies
 
# def draw_sprites(surf, sprites,enemies, spsize, hres, halfvres, ticks):
#     cycle = int(ticks)%3 # animation cycle for monsters
#     for en in range(len(enemies)):
#         if enemies[en][3] > 10:
#             break
#         types, dir2p = int(enemies[en][4]), int(enemies[en][7])
#         cos2 = np.cos(enemies[en][2])
#         scale = abs(min(enemies[en][3], 2)*spsize*enemies[en][5]/cos2)
#         vert = halfvres + halfvres*min(enemies[en][3], 2)/cos2
#         hor = hres/2 - hres*np.sin(enemies[en][2])
#         spsurf = pg.transform.scale(sprites[types][cycle][dir2p], scale)
#         surf.blit(spsurf, (hor,vert)-scale/2)

#     return surf
def gen_map(size):
    mapc = np.random.uniform(0, 1, (size, size, 3))
    maph = np.random.choice([0,0,0,0,1,1], (size,size))
    maph[0,:], maph[size-1,:], maph[:,0], maph[:,size-1] = [1,1,1,1]

    posx, posy, rot = 1.5, np.random.randint(1, size-1) +.5, np.pi/4
    x,y = int(posx), int(posy)
    maph[x][y] = 0
    count = 0
    while True:
        testx, testy = (x,y)
        if np.random.uniform() > 0.5:
            testx += np.random.choice([-1,1])
        else:
            testy += np.random.choice([-1,1])
        if testx > 0 and testx < size-1 and testy > 0 and testy < size-1:
            if maph[testx][testy] == 0 and count > 5:
                count = 0
                x,y = (testx, testy)
                maph[x][y] = 0
                if x == size-2:
                    exitx, exity = (x,y)
                    break
            else:
                count += 1
    return posx, posy, rot, maph, mapc, exitx, exity


# def spawn_enemies(number, maph, msize):
#     enemies = []
#     for i in range(number):
#         x,y = np.random.uniform(1,msize-2), np.random.uniform(1,msize-2)
#         while (maph[int(x-0.1)%(msize-1)][int(y-0.1)%(msize-1)] or maph[int(x-0.1)%(msize-1)][int(y+0.1)%(msize-1)] or maph[int(x+0.1)%(msize-1)][int(y-0.1)%(msize-1)] or maph[int(x+0.1)%(msize-1)][int(y+0.1)%(msize-1)]):

#             x,y = np.random.uniform(1, msize-1), np.random.uniform(1,msize-1)
#         angle2p, invdist2p,dir2p = 0,0,0
#         entype = np.random.choice([0,1])
#         direction = np.random.uniform(0, 2*np.pi)
#         size = np.random.uniform(7,10)
#         enemies.append([x,y,angle2p,invdist2p,entype,size,direction,dir2p])

#     return np.asarray(enemies)


# def get_sprites(hres):
#     sheet = pg.image.load("sprites2.png")
#     sprites = [[],[]]
#     for i in range(3):
#         xx = i*32
#         sprites[0].append([])
#         sprites[1].append([])
#         for j in range(4):
#             yy = j*100
#             sprites[0][i].append(pg.Surface.subsurface(sheet, (xx,yy,32,100)))  # type: ignore
#             sprites[1][i].append(pg.Surface.subsurface(sheet, (xx+96,yy,32,100)))  # type: ignore
#     sprite = sprites[0][1][0]
#     spsize = np.asarray(sprite.get_size())*hres/800

#     return sprites, spsize
font = pg.font.SysFont('Arial',100,False)
font2 = pg.font.SysFont('Arial',75,False)

menu = pygame_menu.Menu("Danyal's Dead maze", 600, 400, theme=pygame_menu.themes.THEME_SOLARIZED )

menu.add.button('Play',quiz_make)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
      




#this is a test.

