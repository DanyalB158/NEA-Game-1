import pygame as pg
import numpy as np
from numba import njit
import sys
import requests
##from Quiz import Question, QuizBrain

pg.init()
test_font = pg.font.SysFont(None ,75)
##parameters = {
##    "amount" : 10,
##    "type" : "boolean"
##}
##
##response = requests.get(url="https://opentdb.com/api.php?amount=10&type=boolean" , params = parameters)
##question_data = response.json()['results']
##    
##
##question_bank = []
##
##for question in question_data:
##    question_text = question["question"]
##    question_answer = question["correct_answer"]
##    new_question = Question(question_text, question_answer)
##    question_bank.append(new_question)
##    
##quiz = QuizBrain(question_bank)
##
##
##while quiz.still_has_questions():
##    quiz.next_question()
##    

    
    



def main():
    screen = pg.display.set_mode((800,600))
    running = True
    clock = pg.time.Clock()
    #increasing causes lower fps but better graphics, but decreasing does opposite.
    hres = 120 #horizontal res
    halfvres = 100 #half of the vertical res

    mod = hres / 60 # scale factor between 60 degree fov and hres.
    posx , posy, rot = 0, 0, 0 # starting points and starting rotation.
    size = 15
    maph = np.random.choice([0, 0, 0, 1], (size, size))#generate a matrix, 1s represent obstacles/walls. Acts as a map.
    mapc = np.random.uniform(0, 1, (size, size, 3))
    frame = np.random.uniform(0, 1, (hres, halfvres*2, 3))
    sky = pg.image.load('skybox.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres*2)))
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg'))/255
    wall = pg.surfarray.array3d(pg.image.load('wall.jpg'))/255

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        frame = new_frame(posx, posy, rot, frame, hres, halfvres, mod, sky, floor, maph, size, wall, mapc)




                
    ##        if int(x)%2 == int(y)%2:
    ##            frame[i][halfvres*2-j-1] = [0, 0, 0]
    ##        else:
    ##            frame[i][halfvres*2-j-1] = [1, 1, 1]
        
        surf = pg.surfarray.make_surface(frame*255)
        
        surf = pg.transform.scale(surf, (800, 600))
        fps = int(clock.get_fps())
        pg.display.set_caption("FPS: " + str(fps))
 
        
        screen.blit(surf, (0,0))
        pg.display.update()

        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed(),clock.tick(120))#varying the value in the clock.tick()  function varies the maximum frames per second. 
            
def movement(posx , posy , rot , keys , et):
    if keys[pg.K_LEFT] or keys[ord('a')]:
        rot -= 0.001 * et 
    if keys[pg.K_RIGHT] or keys[ord('d')]:
        rot += 0.001 * et 
    if keys[pg.K_UP] or keys[ord('w')]:
        posx, posy = posx + np.cos(rot) * 0.001 * et , posy + np.sin(rot) * 0.001 * et 
    if keys[pg.K_DOWN] or keys[ord('s')]:
        posx, posy = posx -  np.cos(rot) * 0.001 * et , posy - np.sin(rot) * 0.001 * et
        
    return posx, posy, rot

@njit()
def new_frame(posx, posy, rot, frame, hres, halfvres, mod, sky, floor, maph, size, wall, mapc):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i/mod-30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod-30)) ##handles rotations, angles in radians
        frame[i][:] = sky[int(np.rad2deg(rot_i)%359)][:]/255
        x, y = posx, posy
        while maph[int(x)%(size-1)][int(y)%(size-1)] == 0:
            x, y = x+0.02*cos, y+0.02*sin
        n = abs((x-posx)/cos)
        h = int(halfvres/(n*cos2 + 0.001))

        xx = int(x*2%1*99)
        if x % 1 < 0.02 or x%1 > 0.98:
            xx = int(y*2%1*99)
        yy = np.linspace(0 , 198, h*2)%99
        shade = 0.3 + 0.7*(h/halfvres)
        if shade > 1:
            shade = 1#prevent shade bursts.
            
        c = shade* mapc[int(x)%(size-1)][int(y)%(size-1)]           
        for k in range(h*2):
            if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                frame[i][halfvres - h + k] = c*wall[xx][int(yy[k])]
        for j in range(halfvres - h):
            n = (halfvres/(halfvres-j))/cos2#distance from user view to object.
            x, y = posx + cos*n, posy + sin*n #x and y distance of the object
            xx, yy = int(x*2%1*100), int(y*2%1*100)
            shade = 0.2 + 0.8*(1-j/halfvres)
                        
            frame[i][halfvres * 2-j-1] = shade*floor[xx][yy]
            


    return frame
    

if __name__ == '__main__':
    pg.quit()
    main()




