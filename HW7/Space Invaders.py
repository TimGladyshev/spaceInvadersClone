'''
    Space Invaders Project
    CS 5001 Spring 2019
    Tim Gladyshev
    04.11.19
'''
import turtle
import random
import math
import time
import winsound

num_enemies = 10

enemies = []

BULLETSTATE = 'charged'

class Enemy(turtle.Turtle):
    enemy_speed = 3
    def __init__(self, x, y, shape = 'alien3.gif', *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.speed(0)
        self.shape(shape)
        self.penup()
        self.setpos(x,y)
        self.health = 3
        self.alive = True

    def is_collision(self, object_2):
        dist = math.sqrt(abs((self.xcor() - object_2.xcor())**2 + ((self.ycor() - object_2.ycor())**2)))
        if dist < 35:
            return True
        else:
            return False

    def __str__(self):
        if self.alive == True:
            print_output = 'This invader has' + self.health + 'health'
        else:
            print_output = 'This enemy is dead'
        return print_output
        

    def __eg__(self, other):
        return self.xcor() == other.xcor() and self.ycor() == other.ycor()
    
class Player(turtle.Turtle):
    is_on_right = False
    is_on_left = False
    def __init__(self, shape = 'player.gif', x = 0, y = -270, player_speed = 15, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.speed(0)   
        self.penup()
        self.shape(shape)
        self.setpos(x,y)
        self.player_speed = player_speed
        self.health = 12
        
    def move_left(self, *args, **kwargs):
        if self.xcor() > -280:
            self.setpos(self.xcor() - self.player_speed, self.ycor())
        else:
            self.setpos(self.xcor(), self.ycor())
        
    def move_right(self):
        if self.xcor() < 280:
            self.setpos(self.xcor() + self.player_speed, self.ycor())
        else:
            self.setpos(self.xcor(), self.ycor())

    def is_collision(self, object_2):
        dist = math.sqrt(abs((self.xcor() - object_2.xcor())**2 + ((self.ycor() - object_2.ycor())**2)))
        if dist < 30:
            return True
        else:
            return False

class Bullet(turtle.Turtle):
    def __init__(self, x = 0, y = -400, shape = 'bullet.gif', color = 'black', *args, **kwargs):
        super(Bullet, self).__init__(*args, **kwargs)
        self.setheading(90)
        self.shape(shape)
        self.speed(0)
        self.bullet_speed = 30
        self.penup()
        self.setpos(x,y)
        self.hideturtle()
        self.state_a = 'waiting'

    def is_collision(self, object_2):
        dist = math.sqrt(abs((self.xcor() - object_2.xcor())**2 + ((self.ycor() - object_2.ycor())**2)))
        if dist < 35:
            return True
        else:
            return False

#functions ----------------------------------------------------------------------------

#def fire_bullet():
def fire_bullet():
    global BULLETSTATE
    if BULLETSTATE == 'charged':
        winsound.PlaySound('playerlaser.wav', winsound.SND_ASYNC)
        BULLETSTATE = 'charging'
        x = player.xcor()
        y = player.ycor() + 5
        bullet.setpos(x, y + 20)
        bullet.showturtle()

#set up the screen --------------------------------------------------------------------
    
#draw screen    
window = turtle.Screen()
window.bgpic('redcity.gif')
window.title('Space Invaders Clone - Tim Gladyshev')

#Draw border
border = turtle.Turtle()
border.speed(0)
border.hideturtle()
border.pencolor('red3')
border.penup()
border.setpos(int(-300), -300)
border.pensize(3)
border.pendown()
border.setpos(-300, 300)
border.setpos(300, 300)
border.setpos(300, -300)
border.setpos(-300, -300)
border.hideturtle()

#register shapes
turtle.register_shape('alien2.gif')
turtle.register_shape('bullet.gif')
turtle.register_shape('player.gif')
turtle.register_shape('alienbullet.gif')
turtle.register_shape('alienbullet2.gif')
turtle.register_shape('alien3.gif')
turtle.register_shape('barrier.gif')

#Draw score
score = turtle.Turtle()
score.speed(0)
score.color('red3')
score.penup()
score.setpos(-290, 301)
score_str = 'Score: ' + '0' + '  Lives: ' + '3' + '  Wave:' + '1'
score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
score.hideturtle()

#make enemies
poss_x = []
poss_y = []
for i in range(-250, 250, 50):
    poss_x.append(i)
for i in range(50, 200, 50):
    poss_y.append(i)
for i in range(num_enemies):
    x_cor = random.choice(poss_x)
    y_cor = random.choice(poss_y)
    enemies.append(Enemy(x = x_cor, y = y_cor))

#make alpha enemy
alpha_enemy = Enemy(x = 0, y = 250, shape = 'alien2.gif')

#make player
player = Player()

#make bullet
bullet = Bullet(x = player.xcor(), y = player.ycor() + 5)

#make alien weapon
a_bullet = Bullet(shape = 'alienbullet.gif')

#make alpha alien weapon
alpha_bullet = Bullet(shape = 'alienbullet2.gif')

#make barriers
barriers = []
for i in range(3):
    b_x_cor = -250 + i * 250
    barriers.append(Player(x = b_x_cor, y = -230, shape = 'barrier.gif'))

#make keyboard bindings
window.listen()
window.onkey(player.move_left, 'Left')
window.onkey(player.move_right, 'Right')
window.onkey(fire_bullet, 'space')

#main loop----------------------------------------------------------------------------    

def main():
    global BULLETSTATE
    game_score = 0
    start_time = time.time()
    start_time2 = time.time()
    lives = 3
    dead = []
    level = 1

    #open file for reading
    try:
        infile = open('highscore.txt', 'r')
        lines = infile.read()
        winner = lines.splitlines()
        infile.close()
    except OSError:
        print('whoops')

    highscore = int(winner[0])
    name = winner[1]

    high_score = turtle.Turtle()
    high_score.speed(0)
    high_score.color('red3')
    high_score.penup()
    high_score.setpos(50, 301)
    high_score_str = 'High Score:  ' + str(highscore) + '---' + str(name)
    high_score.write(high_score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
    high_score.hideturtle()
    
    #main game loop
    while True:

        #move enemies
        for i in range(len(enemies)):
            if enemies[i].alive == True:
                x = enemies[i].xcor()
                x += enemies[i].enemy_speed
                y = enemies[i].ycor()
                enemies[i].setpos(x, y)

            #bounce back if at right wall
            if enemies[i].xcor() > 280:
                Enemy.enemy_speed *= -1
                for j in range(len(enemies)):
                    y = enemies[j].ycor()
                    y -= 25
                    enemies[j].sety(y)
                
            #bounce back if at left wall
            if enemies[i].xcor() < -280:
                y = enemies[i].ycor()
                y -= 25
                Enemy.enemy_speed *= -1
                enemies[i].sety(y)
                
            #check collision of player's bullet and enemy
            if bullet.is_collision(enemies[i]):
                winsound.PlaySound('explosion.wav', winsound.SND_ASYNC)
                bullet.hideturtle()
                BULLETSTATE = 'charged'
                bullet.setposition(0, -400)
                game_score += 10
                score.clear()
                score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) + '  Wave: ' + str(level) 
                score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
                clone = enemies[i].clone()
                enemies[i].hideturtle()
                clone.speed(30)
                color = ['red1', 'red2', 'red3', 'red4', 'yellow1', 'yellow2', 'yellow3']
                for j in range(30,120,10):
                    clone.clear()
                    window.ontimer(clone.dot(j ,color[random.randint(0,6)]), 50)
                    clone.clear()
                clone.hideturtle()
                del clone
                enemies[i].alive = False
                enemies[i].setpos(0, 400)
                # for continuous mode
                '''
                x = random.randrange(-250, 250, 50)
                y = random.randrange(100, 250, 50)
                enemies[i].setpos(x,y)
                enemies[i].showturtle()
                '''
            #check collition of enemy and player
            if player.is_collision(enemies[i]):
                window.clear()
                score.setpos(0,10)
                score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) + '  Wave: ' + str(level)
                score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
                score.setpos(0, -10)
                score.write('GAME OVER', False, align = 'left', font = ('Arial', 14, 'normal'))
                break

            #check collision of enemy and barrier
            for j in range(len(barriers)):
                if barriers[j].is_collision(enemies[i]):
                    winsound.PlaySound('barrierimpact.wav', winsound.SND_ASYNC)
                    barriers[j].health -= 3
                    clone = enemies[i].clone()
                    clone.speed(30)
                    color = ['red1', 'red2', 'red3', 'red4', 'yellow1', 'yellow2', 'yellow3']
                    for q in range(30,120,10):
                        clone.clear()
                        window.ontimer(clone.dot(q ,color[random.randint(0,6)]), 50)
                        clone.clear()
                    clone.hideturtle()
                    del clone
                    enemies[i].hideturtle()
                    enemies[i].alive = False
                    enemies[i].setpos(0, 400)

                    #for continuous mode
                    '''
                    x = random.randrange(-250, 250, 50)
                    y = random.randrange(100, 250, 50)
                    enemies[i].setpos(x,y)
                    enemies[i].showturtle()
                    '''

            #check if enemy made it to the end
            if enemies[i].ycor() < -275:
                window.clear()
                score.setpos(-300, 250)
                score_str = 'Score: ' + str(game_score) + '  Waves: ' + str(level)
                score.write('GAME OVER', False, align = 'left', font = ('Arial', 20, 'normal'))
                score.setpos(-300, 200)
                score.write(score_str, False, align = 'left', font = ('Arial', 20, 'normal'))
                break

        #move alpha enemy
        x_alpha = alpha_enemy.xcor()
        x_alpha += alpha_enemy.enemy_speed * .5 
        y_alpha = alpha_enemy.ycor()
        alpha_enemy.setpos(x_alpha, y_alpha)
        
        #bounce alpha back from right or left
        if alpha_enemy.xcor() > 200:
            alpha_enemy.enemy_speed *= -1
        if alpha_enemy.xcor() < -200:
            alpha_enemy.enemy_speed *= -1

        #check for collisions .......................................................
        #check for collision of alien bullet and player
        if a_bullet.is_collision(player):
            winsound.PlaySound('playerimpact.wav', winsound.SND_ASYNC)
            a_bullet.hideturtle()
            a_bullet.state_a = 'waiting'
            a_bullet.setposition(0, -400)
            lives -= 1
            score.clear()
            score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) + '  Wave: ' + str(level) 
            score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))

        #check for collision of alien bullets, alpha and barrier
        for i in range(len(barriers)):
            if barriers[i].is_collision(a_bullet):
                winsound.PlaySound('barrierimpact.wav', winsound.SND_ASYNC)
                barriers[i].health -= 1
                a_bullet.state_a = 'waiting'
                a_bullet.hideturtle()
                a_bullet.setpos(0, -400)
            if barriers[i].is_collision(alpha_bullet):
                winsound.PlaySound('barrierimpact.wav', winsound.SND_ASYNC)
                barriers[i].health -= 3
                alpha_bullet.state_a = 'waiting'
                alpha_bullet.hideturtle()
                alpha_bullet.setpos(0, -400)
            if barriers[i].is_collision(alpha_enemy):
                winsound.PlaySound('barrierimpact.wav', winsound.SND_ASYNC)
                barriers[i].health -= 3
            if barriers[i].health < 1:
                if barriers[i].xcor() > -400:
                    winsound.PlaySound('explosionlarge2.wav', winsound.SND_ASYNC)
                    barriers[i].speed(2)
                    bar_x_cor = barriers[i].xcor() - 30
                    bar_y_cor = barriers[i].ycor()
                    barriers[i].setpos(bar_x_cor, bar_y_cor)

        #check for collition of alpha alien bullet and player
        if alpha_bullet.is_collision(player):
            winsound.PlaySound('playerimpact.wav', winsound.SND_ASYNC)
            alpha_bullet.hideturtle()
            alpha_bullet.state_a = 'waiting'
            alpha_bullet.setposition(0, -400)
            lives -= 1
            score.clear()
            score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) 
            score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))

        #check for collitions of alpha alien and player
        if player.is_collision(alpha_enemy):
            window.clear()
            score.setpos(0,10)
            score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) + '  Wave: ' + str(level)
            score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
            score.setpos(0, -10)
            score.write('GAME OVER', False, align = 'left', font = ('Arial', 14, 'normal'))
            break
            
        #check if alpha made it to the end
        if alpha_enemy.ycor() < -275:
            window.clear()
            score.setpos(-300, 250)
            score_str = 'Score: ' + str(game_score) + '  Waves: ' + str(level)
            score.write('GAME OVER', False, align = 'left', font = ('Arial', 20, 'normal'))
            score.setpos(-300, 200)
            score.write(score_str, False, align = 'left', font = ('Arial', 20, 'normal'))
            break
       
        #check for collision of player bullet and alpha alien 
        if alpha_enemy.is_collision(bullet):
            winsound.PlaySound('alphamoan.wav', winsound.SND_ASYNC)
            bullet.hideturtle()
            BULLETSTATE = 'charged'
            bullet.setposition(0, -400)
            game_score += 10
            score.clear()
            score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) 
            score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
            alpha_enemy.sety(alpha_enemy.ycor() - 50)
            #winsound.PlaySound('playerimpact.wav', winsound.SND_ASYNC)
        
        #fire enemy bullets .........................................................
        #little enemies fire 
        total_time = int((time.time() - start_time) + 1)
        x_t = total_time % 5
        if x_t == 0:
            winsound.PlaySound('enemylasersmall.wav', winsound.SND_ASYNC)
            count = 0
            alive = []
            for i in range(len(enemies)):
                if enemies[i].alive == True:
                    alive.append(i)
            if len(alive) > 0:
                x_e = random.choice(alive)
                a_bullet.setpos(enemies[x_e].xcor(), enemies[x_e].ycor())
                a_bullet.showturtle()
                a_bullet.state_a = 'fire'
                start_time = time.time()

        #fire alpha's bullet
        total_time2 = int((time.time() - start_time2) + 1)
        x_t2 = total_time2 % 7
        if x_t2 == 0:
            winsound.PlaySound('enemylaserlarge.wav', winsound.SND_ASYNC)
            alpha_bullet.setpos(alpha_enemy.xcor(), alpha_enemy.ycor())
            alpha_bullet.showturtle()
            alpha_bullet.state_a = 'fire'
            start_time2 = time.time()    

        #move bullets ...................................................................
        #move player bullet if fired
        if BULLETSTATE == 'charging':
            y = bullet.ycor()
            y += bullet.bullet_speed
            bullet.sety(y)
            
        #stop moving bullet at top of screen   
        if bullet.ycor() > 285:
            BULLETSTATE = 'charged'
            bullet.hideturtle()
            bullet.setpos(0, -400)

        #move enemy bullet if fired
        if a_bullet.state_a == 'fire':
            a_y = a_bullet.ycor()
            a_y -= a_bullet.bullet_speed * 1.5
            a_bullet.sety(a_y)

        #stop enemy bullet if at the end of screen
        if a_bullet.ycor() < -320:
            a_bullet.state_a = 'waiting'
            a_bullet.hideturtle()
            a_bullet.setpos(0, -400)

        #move alpha enemy bullet if fired
        if alpha_bullet.state_a == 'fire':
            alpha_y = alpha_bullet.ycor()
            alpha_y -= alpha_bullet.bullet_speed * 1.5
            alpha_bullet.sety(alpha_y)

        #stop alpha bullet if at the end of screen 
        if alpha_bullet.ycor() < -320:
            alpha_bullet.state_a = 'waiting'
            alpha_bullet.hideturtle()
            alpha_bullet.setpos(0, -400)
        
        #check lives
        if lives == 0:
            window.clear()
            score.setpos(-300, 250)
            score_str = 'Score: ' + str(game_score) + '  Waves: ' + str(level)
            score.write('GAME OVER', False, align = 'left', font = ('Arial', 20, 'normal'))
            score.setpos(-300, 200)
            score.write(score_str, False, align = 'left', font = ('Arial', 20, 'normal'))
            break

        alive = []
        for i in range(len(enemies)):
            if enemies[i].alive == True:
                    alive.append(i)
        if len(alive) == 0:
            level += 1
            score_str = 'Score: ' + str(game_score) + '  Lives: ' + str(lives) + '  Wave: ' + str(level)
            score.write(score_str, False, align = 'left', font = ('Arial', 14, 'normal'))
            for i in range(-250, 250, 50):
                poss_x.append(i)
            for i in range(50, 200, 50):
                poss_y.append(i)
            for i in range(len(enemies)):
                x_cor = random.choice(poss_x)
                y_cor = random.choice(poss_y)
                enemies[i].showturtle()
                enemies[i].setpos(x_cor, y_cor)
                enemies[i].alive = True
            Enemy.enemy_speed *= 1.25

    #ask for highscore
    if game_score > highscore:
        name = input('Please enter your name\n')
        outfile = open('highscore.txt', 'w')
        outfile.write(str(game_score) + '\n' + str(name))
        outfile.close()
          
main()
