import pygame, random
from datetime import timedelta, datetime
pygame.init()         
 # pygame 초기화

#### 2. pygame에 사용되는 전역변수 선언
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
size = [800, 800]
KEY_DIRECTION = {
    pygame.K_w: [0,-1],
    pygame.K_s: [0,1],
    pygame.K_a: [-1,0],
    pygame.K_d: [1,0],
}
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont('malgungothic', 20)
# pygame.display.set_mode(size, FULLSCREEN) 

clock = pygame.time.Clock()
class Snake:
    def __init__(self):
        self.direction = [1,0]
        self.position = [[3,0],[2,0],[1,0]]
        self.length = 3
        self.had_existed_position = [0,0]
        
    def go(self):
        self.had_existed_position=self.position[-1]
        for i in range(1,self.length):
            front = i + 1
            self.position[-i] = self.position[-front]
        self.position[0] = [self.position[0][0] + self.direction[0], self.position[0][1] + self.direction[1]]
        
    def grow(self):
        self.position.append(self.had_existed_position)
        self.length += 1
    
    def check_collide(self):
        self_collide = False 
        for i in range(1,self.length):
            if self.position[0] == self.position[i]:
                self_collide = True
                break
        wall_collide = self.position[0][0] < 0 or self.position[0][0] > 19 or self.position[0][1] < 0 or self.position[0][1] > 19
        return self_collide or wall_collide
    
    def check_apple(self, apple):
        return apple.position == self.position[0]

    def render(self):
        draw_block(BLUE,self.position[0])
        for i in range(1,self.length):
            draw_block(GREEN, self.position[i])

class Apple:
    def __init__(self,snake_position):
        self.replace(snake_position)
        
    def replace(self,snake_position):
        no_snake = True
        pos = [random.randint(0, 19), random.randint(0, 19)]
        while not no_snake:
            pos = [random.randint(0, 19), random.randint(0, 19)]
            for i in snake_position:
                if i == pos:
                    break
            no_snake = False
        self.position = pos
        print(self.position)
    def render(self):
        draw_block(RED, self.position)

def draw_block(color, position):
    block = pygame.Rect((position[0] * 40, position[1] * 40), (40, 40))
    
    pygame.draw.rect(screen, color, block)

def runGame():
    global pygame,screen
    last_moved_time = datetime.now()
    play = False
    done = False
    old_snake = False
    temp_direction = False
    while not done:
        clock.tick(30)
        screen.fill(WHITE)
        if play == True :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key in KEY_DIRECTION:
                        if KEY_DIRECTION[event.key][0] + snake.direction[0] or KEY_DIRECTION[event.key][1] + snake.direction[1]: 
                            temp_direction = KEY_DIRECTION[event.key]
                            # print(event.key)
                            # break
            if timedelta(seconds=0.05) <= datetime.now() - last_moved_time:
                if temp_direction:
                    snake.direction = temp_direction
                    temp_direction = False
                snake.go()
                last_moved_time = datetime.now()
            if snake.check_collide():
                play = False
                print("COLLIDE!!!")
                old_snake = True
            if snake.check_apple(apple):
                snake.grow()
                apple.replace(snake.position)
            
                # text = myfont.render(SnakeLevel, False, (0, 0, 0))
                # SnakeLevel = str(int(SnakeLevel) + 1)
        else:
            text = myfont.render('Snake 게임', True, (0, 0, 0))
            screen.blit(text, (90, 30))

            # text = myfont.render('   너의 최종 Snake Lv.' + SnakeLevel, True, (255, 255, 255))
            # screen.blit(text, (90, 60))

            text = myfont.render('시작은 스페이스바 ㄱ ㄱ', True, (0, 0, 0))
            screen.blit(text, (90, 330))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE :

                        play = True
                        snake = Snake() 
                        apple = Apple(snake.position) 
                        old_snake = None
                        
        #                 # SnakeLevel = str(int(1)) 
        
        if play:
            snake.render()
            apple.render()
        if old_snake:
            snake.render()
        pygame.display.update()
        

#### 4. pygame 게임 종료
runGame()
pygame.quit()